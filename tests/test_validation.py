"""Mutation tests: failures must be rejected without altering canonical files."""
import copy
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


validator = module("validate")
installer = module("install_skill")


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(
            ".git", ".venv", "__pycache__", "build", ".agents", ".codex", ".aws"))
        self.skill = self.root / "skills/weed-genomics"

    def check_error(self, phrase):
        errors = validator.validate(self.root).errors
        self.assertTrue(any(phrase in e for e in errors), errors)

    def topic(self, modify, filename="references/species/chenopodium-album.md"):
        path = self.skill / filename
        meta, body = validator.frontmatter(path)
        modify(meta)
        path.write_text("---\n" + yaml.safe_dump(meta, sort_keys=False) + "---\n" + body)

    def index(self, modify):
        path = self.skill / "index.yaml"
        data = yaml.safe_load(path.read_text())
        modify(data)
        path.write_text(yaml.safe_dump(data, sort_keys=False))

    def registry(self, filename, modify):
        path = self.skill / "data" / filename
        with path.open(newline="") as f:
            reader = csv.DictReader(f, delimiter="\t")
            fields = reader.fieldnames
            rows = list(reader)
        modify(rows)
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)

    def test_repository_valid_and_read_only(self):
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        report = validator.validate(self.root)
        self.assertEqual(report.errors, [])
        self.assertTrue(any("draft" in w for w in report.warnings))
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_validation_is_offline(self):
        with patch("socket.socket", side_effect=AssertionError("network forbidden")):
            self.assertEqual(validator.validate(self.root).errors, [])

    def test_remote_schema_reference_rejected(self):
        path = self.skill / "data/schema.yaml"
        path.write_text(path.read_text().replace("$ref: '#/$defs/text'", "$ref: 'https://example.org/remote-schema'", 1))
        self.check_error("network resolution is disabled")

    def test_missing_required_metadata(self):
        self.topic(lambda m: m.pop("scope"))
        self.check_error("required property")

    def test_unknown_metadata_is_error(self):
        self.topic(lambda m: m.update(approval="looks good"))
        self.check_error("Additional properties")

    def test_yaml_duplicate_keys_rejected(self):
        path = self.skill / "index.yaml"
        path.write_text(path.read_text() + "\nschema_version: 1\n")
        self.check_error("duplicate YAML key")

    def test_bad_yaml_rejected(self):
        (self.skill / "index.yaml").write_text("records: [broken\n")
        self.check_error("index.yaml")

    def test_tsv_ragged_row_rejected(self):
        path = self.skill / "data/source_registry.tsv"
        path.write_text(path.read_text() + "src.bad\ttoo-few-fields\n")
        self.check_error("ragged TSV row")

    def test_duplicate_source_id(self):
        self.registry("source_registry.tsv", lambda rows: rows.append(copy.deepcopy(rows[0])))
        self.check_error("duplicate identifier")

    def test_bad_source_reference(self):
        self.topic(lambda m: m["sources"].append("src.missing"))
        self.check_error("unknown source")

    def test_body_source_mismatch(self):
        path = self.skill / "references/species/chenopodium-album.md"
        path.write_text(path.read_text() + "\nUnsupported [src.fake].\n")
        self.check_error("body source citations")

    def test_evidence_is_independent_of_review(self):
        self.topic(lambda m: m.update(evidence_types=["formal_specification"]))
        self.check_error("evidence types lack")

    def test_bad_review_state(self):
        self.topic(lambda m: m.update(review_status="approved-by-ai"))
        self.check_error("not one of")

    def test_self_promotion_without_humans(self):
        self.topic(lambda m: m.update(review_status="reviewed"))
        self.check_error("human review requires")

    def test_ai_reviewer_rejected(self):
        self.topic(lambda m: m.update(review_status="reviewed", reviewed_by=["Codex"],
                   reviewed_on="2026-10-23", review_evidence=["https://example.org/synthetic-review"], review_note="synthetic fixture"))
        self.check_error("AI cannot be a human reviewer")

    def test_verified_requires_two_humans(self):
        self.topic(lambda m: m.update(review_status="verified", reviewed_by=["synthetic-reviewer"],
                   reviewed_on="2026-10-23", review_evidence=["https://example.org/synthetic-review"], review_note="synthetic fixture"))
        self.check_error("human review requires")

    def test_draft_cannot_keep_approval(self):
        self.topic(lambda m: m.update(reviewed_by=["synthetic-reviewer"]))
        self.check_error("draft must not carry")

    def test_duplicate_index_id(self):
        self.index(lambda d: d["records"].append(copy.deepcopy(d["records"][0])))
        self.check_error("duplicate record identifier")

    def test_missing_index_target(self):
        self.index(lambda d: d["records"][0].update(path="references/shared/missing.md"))
        self.check_error("missing path")

    def test_outside_skill_link_rejected(self):
        path = self.skill / "SKILL.md"
        path.write_text(path.read_text() + "\n[Root policy](../../AGENTS.md)\n")
        self.check_error("distribution boundary")

    def test_path_traversal_rejected(self):
        with self.assertRaises(ValueError):
            validator.safe_path(self.skill, "../../README.md")

    def test_symlink_rejected(self):
        (self.skill / "outside.md").symlink_to(self.root / "README.md")
        self.check_error("symlinks")

    def test_orphan_record_rejected(self):
        shutil.copy2(self.skill / "references/species/chenopodium-album.md", self.skill / "references/species/orphan.md")
        self.check_error("missing from index")

    def test_duplicate_assembly_id(self):
        self.registry("assembly_registry.tsv", lambda rows: rows.append(copy.deepcopy(rows[0])))
        self.check_error("duplicate identifier")

    def test_duplicate_assembly_key(self):
        def mutate(rows):
            new = copy.deepcopy(rows[0])
            new["assembly_id"] = "asm.distinct-but-conflicting"
            rows.append(new)
        self.registry("assembly_registry.tsv", mutate)
        self.check_error("duplicate assembly accession/version")

    def test_assembly_version_separate(self):
        self.registry("assembly_registry.tsv", lambda rows: rows[0].update(accession="GCA_948465745.1"))
        self.check_error("base and positive version")

    def test_taxon_scope_mismatch(self):
        self.registry("assembly_registry.tsv", lambda rows: rows[0].update(taxon_id="local:other-species"))
        self.check_error("taxon/assembly scope mismatch")

    def test_material_scope_mismatch(self):
        self.topic(lambda m: m["scope"].update(biological_material="different individual"))
        self.check_error("biological material")

    def test_annotation_assembly_scope(self):
        self.topic(lambda m: m["annotation"].update(assembly_id="asm.missing"))
        self.check_error("annotation assembly")

    def test_general_scope_cannot_list_taxon(self):
        self.topic(lambda m: m["scope"].update(taxa=["ncbi:3559"]), "references/workflows/reference-identity.md")
        self.check_error("general scope requires")

    def test_supersession_target_and_reason(self):
        self.topic(lambda m: m.update(deprecated=True, superseded_by=["wg.missing"]))
        self.check_error("unknown superseding ID")
        self.check_error("deprecated record requires a reason")

    def test_supersession_cycle(self):
        self.topic(lambda m: m.update(deprecated=True, superseded_by=[m["id"]], deprecation_reason="synthetic cycle"))
        self.check_error("supersession cycle")

    def test_bad_date_rejected(self):
        self.topic(lambda m: m.update(last_verified="2026-02-30"))
        self.check_error("not a 'date'")

    def test_bad_skill_frontmatter(self):
        path = self.skill / "SKILL.md"
        text = path.read_text().replace("name: weed-genomics", "name: Weed--Genomics")
        path.write_text(text)
        self.check_error("invalid name")

    def test_skill_metadata_must_be_strings(self):
        path = self.skill / "SKILL.md"
        path.write_text(path.read_text().replace('version: "0.1.0-dev"', "version: 1"))
        self.check_error("map strings to strings")

    def test_case_sources_must_exist(self):
        path = self.root / "tests/biological_edge_cases.yaml"
        data = yaml.safe_load(path.read_text())
        data["cases"][0]["source_ids"] = ["src.missing"]
        path.write_text(yaml.safe_dump(data))
        self.check_error("unknown evaluation source")

    def test_unverified_source_is_warning(self):
        self.registry("source_registry.tsv", lambda rows: rows[0].update(verification_status="inaccessible"))
        report = validator.validate(self.root)
        self.assertEqual(report.errors, [])
        self.assertTrue(any("source is inaccessible" in w for w in report.warnings))

    def test_cli_independent_of_current_directory(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate.py"), "--root", str(self.root)],
                                cwd=self.temp.name, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.destination = Path(self.temp.name) / "weed-genomics"

    def test_complete_portable_install_and_provenance(self):
        manifest = installer.install(ROOT, self.destination)
        self.assertEqual((self.destination / "LICENSE").read_bytes(), (ROOT / "LICENSE").read_bytes())
        for path, digest in manifest["sha256"].items():
            self.assertEqual(hashlib.sha256((self.destination / path).read_bytes()).hexdigest(), digest)
        data = yaml.safe_load((self.destination / "index.yaml").read_text())
        for entry in data["records"]:
            self.assertTrue((self.destination / entry["path"]).is_file())
        report = validator.Report()
        validator.validate_skill(self.destination, report)
        for path in self.destination.rglob("*.md"):
            validator.check_links(self.destination, path, report, self.destination)
        self.assertEqual(report.errors, [])
        self.assertEqual(json.loads((self.destination / "INSTALLATION.json").read_text()), manifest)
        self.assertNotIn("/mnt/", json.dumps(manifest))

    def test_refuses_existing_install_without_modifying_it(self):
        self.destination.mkdir()
        marker = self.destination / "user-content.txt"
        marker.write_text("preserve")
        with self.assertRaises(ValueError):
            installer.install(ROOT, self.destination)
        self.assertEqual(marker.read_text(), "preserve")
        self.assertEqual(list(self.destination.iterdir()), [marker])

    def test_refuses_repository_mirror(self):
        with self.assertRaises(ValueError):
            installer.install(ROOT, ROOT / "duplicate-skill")

    def test_source_archive_records_unknown_commit(self):
        source = Path(self.temp.name) / "archive"
        (source / "skills").mkdir(parents=True)
        shutil.copytree(ROOT / "skills/weed-genomics", source / "skills/weed-genomics")
        shutil.copy2(ROOT / "LICENSE", source / "LICENSE")
        manifest = installer.install(source, self.destination)
        self.assertIsNone(manifest["commit"])
        self.assertIsNone(manifest["dirty"])


if __name__ == "__main__":
    unittest.main()
