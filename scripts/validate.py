#!/usr/bin/env python3
"""Offline, read-only structural validation. Does not certify biological truth."""
from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

try:
    import yaml
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError
except ImportError:
    raise SystemExit("Install maintenance dependencies: python -m pip install -r requirements-dev.txt")

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("skills/weed-genomics")
CATEGORIES = {"shared": "shared", "family": "families", "species": "species",
              "workflow": "workflows", "tool": "tools"}
LIST_COLUMNS = {"source_ids", "related_assemblies", "reviewed_by", "review_evidence", "superseded_by"}
SOURCE_TAG = re.compile(r"\[(src\.[a-z0-9.-]+)(?::[^\]]*)?\]")


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently changing provenance."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, (str, int, float, bool, type(None))):
            raise ValueError("YAML keys must be scalar")
        if key in result:
            raise ValueError(f"duplicate YAML key: {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def read_yaml(text):
    return yaml.load(text, Loader=UniqueLoader)


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)\Z", text, re.S)
    if not match:
        raise ValueError("missing or unclosed YAML frontmatter")
    meta = read_yaml(match[1])
    if not isinstance(meta, dict):
        raise ValueError("frontmatter must be a mapping")
    return meta, match[2]


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.counts = {}

    def error(self, where, message):
        self.errors.append(f"{where}: {message}")

    def warn(self, where, message):
        self.warnings.append(f"{where}: {message}")


def safe_path(base, value):
    """Contain runtime paths even through symlinks, absolute paths or traversal."""
    if not isinstance(value, str) or not value or Path(value).is_absolute() or "\\" in value:
        raise ValueError("expected a relative POSIX path")
    target = (base / value).resolve()
    if not target.is_relative_to(base.resolve()):
        raise ValueError("path escapes its distribution boundary")
    if not target.exists():
        raise ValueError(f"missing path: {value}")
    return target


def validate_skill(path, report):
    try:
        meta, body = frontmatter(path / "SKILL.md")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        report.error("SKILL.md", str(exc))
        return
    allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    if set(meta) - allowed:
        report.error("SKILL.md", f"unsupported metadata: {set(meta) - allowed}")
    name = meta.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64 or name != path.name:
        report.error("SKILL.md", "invalid name or directory/name mismatch")
    for key, limit in [("description", 1024), ("compatibility", 500)]:
        if key == "description" or key in meta:
            value = meta.get(key)
            if not isinstance(value, str) or not value.strip() or len(value) > limit:
                report.error("SKILL.md", f"{key} must be a nonempty string <= {limit} characters")
    for key in ("license", "allowed-tools"):
        if key in meta and (not isinstance(meta[key], str) or not meta[key].strip()):
            report.error("SKILL.md", f"{key} must be nonempty text")
    metadata = meta.get("metadata", {})
    if not isinstance(metadata, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in metadata.items()):
        report.error("SKILL.md", "metadata must map strings to strings")
    if not body.strip():
        report.error("SKILL.md", "empty instructions")
    if len((path / "SKILL.md").read_text().splitlines()) > 250:
        report.warn("SKILL.md", "exceeds the project's 250-line entrypoint target")


def check_links(root, path, report, boundary=None):
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    # Project Markdown uses inline links; anchors are checked for local files.
    for raw in re.findall(r"\[[^\]\n]*\]\(([^\s)]+)\)", text):
        raw = raw.strip("<>")
        parsed = urlsplit(raw)
        if parsed.scheme in {"http", "https", "mailto"}:
            continue
        if parsed.scheme or parsed.netloc:
            report.error(path.relative_to(root), f"unsupported link: {raw}")
            continue
        try:
            base = boundary or root
            candidate = path.parent / unquote(parsed.path) if parsed.path else path
            relative = candidate.relative_to(base).as_posix()
            target = safe_path(base, relative)
            if parsed.fragment and target.suffix == ".md":
                headings = re.findall(r"^#{1,6}\s+(.+)$", target.read_text(), re.M)
                slugs = {re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-") for h in headings}
                if unquote(parsed.fragment) not in slugs:
                    raise ValueError(f"missing heading anchor: {raw}")
        except (ValueError, OSError) as exc:
            report.error(path.relative_to(root), str(exc))


def validate(root=ROOT):
    root = Path(root).resolve()
    skill = root / SKILL
    report = Report()
    validate_skill(skill, report)
    try:
        schema = read_yaml((skill / "data/schema.yaml").read_text())
        Draft202012Validator.check_schema(schema)
        pending = [schema]
        while pending:
            node = pending.pop()
            if isinstance(node, dict):
                for key in ("$ref", "$dynamicRef"):
                    if key in node and not node[key].startswith("#/"):
                        raise ValueError("schema references must be local fragments; network resolution is disabled")
                pending.extend(node.values())
            elif isinstance(node, list):
                pending.extend(node)
    except (OSError, ValueError, yaml.YAMLError, SchemaError) as exc:
        # Bad schemas must be reported rather than allowing incomplete checks.
        report.error("schema.yaml", str(exc))
        return report

    def conforms(item, definition, where):
        validator = Draft202012Validator({"$ref": f"#/$defs/{definition}", "$defs": schema["$defs"]}, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(item), key=lambda e: str(list(e.path)))
        for err in errors:
            report.error(where, f"{'.'.join(map(str, err.path)) or '<root>'}: {err.message}")
        return not errors

    def yaml_file(path):
        try:
            return read_yaml(path.read_text(encoding="utf-8"))
        except (OSError, ValueError, yaml.YAMLError) as exc:
            report.error(path.relative_to(root), str(exc))
            return None

    def table(filename, definition, key):
        path = skill / "data" / filename
        rows = {}
        try:
            with path.open(encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle, delimiter="\t", strict=True)
                headers = reader.fieldnames or []
                expected = set(schema["$defs"][definition]["properties"])
                if len(headers) != len(set(headers)) or set(headers) != expected:
                    report.error(filename, f"headers must be unique and exactly {sorted(expected)}")
                    return rows
                for line, row in enumerate(reader, 2):
                    where = f"{filename}:{line}"
                    if None in row or None in row.values():
                        report.error(where, "ragged TSV row")
                        continue
                    if any("\n" in value or "\r" in value for value in row.values()):
                        report.error(where, "multiline TSV cells are unsupported")
                        continue
                    for col in LIST_COLUMNS & row.keys():
                        row[col] = row[col].split(";") if row[col] else []
                    if "reviewed_on" in row:
                        row["reviewed_on"] = row["reviewed_on"] or None
                    if "deprecated" in row:
                        row["deprecated"] = {"true": True, "false": False}.get(row["deprecated"], row["deprecated"])
                    if not conforms(row, definition, where):
                        continue
                    if row[key] in rows:
                        report.error(where, f"duplicate identifier: {row[key]}")
                    else:
                        rows[row[key]] = row
        except (OSError, csv.Error, UnicodeError) as exc:
            report.error(filename, str(exc))
        return rows

    sources = table("source_registry.tsv", "source", "source_id")
    assemblies = table("assembly_registry.tsv", "assembly", "assembly_id")
    index = yaml_file(skill / "index.yaml")
    if not conforms(index, "index", "index.yaml"):
        return report
    taxa = {}
    for taxon in index["taxa"]:
        if taxon["id"] in taxa:
            report.error("index.yaml", f"duplicate taxon: {taxon['id']}")
        taxa[taxon["id"]] = taxon

    def references(values, registry, where, label):
        for value in values:
            if value not in registry:
                report.error(where, f"unknown {label}: {value}")

    def review(item, where):
        state = item["review_status"]
        if state == "draft":
            if any(item[k] for k in ("reviewed_by", "reviewed_on", "review_evidence", "review_note")):
                report.error(where, "draft must not carry completed human approval")
        else:
            minimum = 1 if state == "reviewed" else 2
            if len(set(item["reviewed_by"])) < minimum or not all(item[k] for k in ("reviewed_on", "review_evidence", "review_note")):
                report.error(where, "human review requires qualified reviewer identities, date, evidence and rationale")
            if any(re.search(r"\b(ai|chatgpt|codex|claude|llm|bot)\b", r, re.I) for r in item["reviewed_by"]):
                report.error(where, "AI cannot be a human reviewer")
            report.warn(where, "human review metadata needs independent identity/expertise confirmation")
        for url in item["review_evidence"]:
            check_url(url, where)

    def lifecycle(registry, where_label):
        for identifier, item in registry.items():
            if item["deprecated"] and not item["deprecation_reason"].strip():
                report.error(identifier, "deprecated record requires a reason")
            if not item["deprecated"] and (item["superseded_by"] or item["deprecation_reason"]):
                report.error(identifier, "supersession/reason requires deprecated: true")
            references(item["superseded_by"], registry, identifier, "superseding ID")
        # Iterative walk keeps long historical chains safe from recursion limits.
        for start in registry:
            pending = [(start, frozenset())]
            while pending:
                node, ancestors = pending.pop()
                if node in ancestors:
                    report.error(where_label, f"supersession cycle containing {node}")
                    break
                if node in registry:
                    pending.extend((n, ancestors | {node}) for n in registry[node]["superseded_by"])

    def check_url(url, where):
        parsed = urlsplit(url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
            report.error(where, "expected an HTTP(S) public locator without credentials")

    for identifier, source in sources.items():
        check_url(source["url"], identifier)
        if source["doi"] and not re.fullmatch(r"10\.\d{4,9}/\S+", source["doi"]):
            report.error(identifier, "malformed DOI")
        if source["verification_status"] != "verified":
            report.warn(identifier, f"source is {source['verification_status']}; do not treat as reverified")
        elif source["last_verified"] in {"unknown", "unverified"}:
            report.error(identifier, "verified source requires a verification date")
    for identifier, taxon in taxa.items():
        references(taxon["sources"], sources, identifier, "source")

    assembly_keys = set()
    for identifier, row in assemblies.items():
        references([row["taxon_id"]], taxa, identifier, "taxon")
        references(row["source_ids"], sources, identifier, "source")
        references(row["related_assemblies"], assemblies, identifier, "related assembly")
        key = (row["accession"], row["version"])
        if key in assembly_keys:
            report.error(identifier, "duplicate assembly accession/version key")
        assembly_keys.add(key)
        if row["accession"].startswith(("GCA", "GCF")):
            if not re.fullmatch(r"GC[AF]_\d{9}", row["accession"]) or not re.fullmatch(r"[1-9]\d*", row["version"]):
                report.error(identifier, "INSDC accession base and positive version must be separate")
        if row["accession"] in {"unknown", "unverified", "not_applicable"} or row["version"] in {"unknown", "unverified", "not_applicable"}:
            report.error(identifier, "assembly identity must be established before registration")
        for other in row["related_assemblies"]:
            if other == identifier or (other in assemblies and assemblies[other]["taxon_id"] != row["taxon_id"]):
                report.error(identifier, "related assemblies must be distinct and have matching taxon scope")
        review(row, identifier)
    lifecycle(assemblies, "assembly_registry.tsv")

    records, paths, annotation_keys = {}, set(), set()
    for entry in index["records"]:
        identifier = entry["id"]
        if identifier in records:
            report.error("index.yaml", f"duplicate record identifier: {identifier}")
        if entry["path"] in paths:
            report.error("index.yaml", f"duplicate record path: {entry['path']}")
        paths.add(entry["path"])
        try:
            path = safe_path(skill, entry["path"])
            meta, body = frontmatter(path)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            report.error(identifier, str(exc))
            continue
        if not conforms(meta, "record", identifier):
            continue
        records[identifier] = meta
        if meta["id"] != identifier or meta["category"] != entry["category"] or set(meta["scope"]["taxa"]) != set(entry["taxa"]):
            report.error(identifier, "index/record ID, category or taxon scope mismatch")
        folder = Path(entry["path"]).parts[1]
        allowed = {CATEGORIES[meta["category"]]} if meta["category"] in CATEGORIES else {"shared", "species"}
        if folder not in allowed:
            report.error(identifier, "record category does not match directory")
        if not body.strip() or not re.search(r"^# " + re.escape(meta["title"]) + r"\s*$", body, re.M):
            report.error(identifier, "body must contain matching H1 title")
        references(meta["sources"], sources, identifier, "source")
        cited = set(SOURCE_TAG.findall(body))
        if cited != set(meta["sources"]):
            report.error(identifier, "body source citations must match metadata sources")
        source_types = {sources[s]["source_type"] for s in meta["sources"] if s in sources}
        if set(meta["evidence_types"]) - source_types - {"expert_interpretation", "unverified_assertion"}:
            report.error(identifier, "declared evidence types lack matching sources")
        if meta["review_status"] == "consensus" and not source_types & {"formal_specification", "peer_reviewed_review"}:
            report.error(identifier, "consensus requires an external standard or documented synthesis")
        review(meta, identifier)
        scope = meta["scope"]
        references(scope["taxa"], taxa, identifier, "taxon")
        references(scope["assemblies"], assemblies, identifier, "assembly")
        if scope["level"] == "general":
            if scope["taxa"] or scope["assemblies"] or scope["biological_material"] != "not_applicable":
                report.error(identifier, "general scope requires empty taxa/assemblies and not_applicable material")
        elif scope["level"] == "taxon":
            if not scope["taxa"] or scope["assemblies"]:
                report.error(identifier, "taxon scope requires taxa and no assemblies")
        else:
            if not scope["assemblies"] or not scope["taxa"]:
                report.error(identifier, "assembly scope requires taxa and assemblies")
            declared_taxa = {assemblies[a]["taxon_id"] for a in scope["assemblies"] if a in assemblies}
            if declared_taxa != set(scope["taxa"]):
                report.error(identifier, "taxon/assembly scope mismatch")
            for a in scope["assemblies"]:
                if a in assemblies and assemblies[a]["biological_material"] not in scope["biological_material"]:
                    report.error(identifier, "assembly biological material is missing from scope")
        if "annotation" in meta:
            ann = meta["annotation"]
            if ann["assembly_id"] not in scope["assemblies"]:
                report.error(identifier, "annotation assembly must be in record scope")
            if ann["release"] in {"unknown", "unverified", "conflicting"}:
                report.warn(identifier, f"annotation release is {ann['release']}")
            else:
                key = (ann["assembly_id"], ann["provider"], ann["release"])
                if key in annotation_keys:
                    report.error(identifier, "duplicate annotation reference key")
                annotation_keys.add(key)
            if "locator" in ann:
                check_url(ann["locator"], identifier)
        if "tool" in meta:
            references([meta["tool"]["citation"]], sources, identifier, "tool citation")
            if meta["tool"]["citation"] not in meta["sources"]:
                report.error(identifier, "tool citation must appear in record sources")
            check_url(meta["tool"]["upstream_repository"], identifier)
    for identifier, meta in records.items():
        references(meta["related_records"], records, identifier, "related record")
        if identifier in meta["related_records"]:
            report.error(identifier, "record cannot link to itself")
    lifecycle(records, "index.yaml")
    for path in sorted((skill / "references").rglob("*.md")):
        if path.name != "README.md" and path.relative_to(skill).as_posix() not in paths:
            report.error(path.relative_to(root), "scientific record missing from index")

    cases = yaml_file(root / "tests/biological_edge_cases.yaml")
    case_ids = set()
    if conforms(cases, "cases", "biological_edge_cases.yaml"):
        kinds = set()
        for case in cases["cases"]:
            identifier = case["id"]
            if identifier in case_ids:
                report.error(identifier, "duplicate evaluation ID")
            case_ids.add(identifier)
            kinds.add(case["kind"])
            references(case["record_ids"], records, identifier, "evaluation record")
            references(case["source_ids"], sources, identifier, "evaluation source")
            supported = {s for r in case["record_ids"] if r in records for s in records[r]["sources"]}
            if set(case["source_ids"]) - supported:
                report.error(identifier, "evaluation sources must be supported by referenced records")
        if not {"positive_control", "negative_control"} <= kinds:
            report.error("biological_edge_cases.yaml", "include positive and negative controls")

    groups = [set(sources), set(assemblies), set(records), set(taxa), case_ids]
    for i, group in enumerate(groups):
        for other in groups[i + 1:]:
            if group & other:
                report.error("identifiers", f"global ID collision: {sorted(group & other)}")
    scientific = list(records.values()) + list(assemblies.values())
    drafts = sum(x["review_status"] == "draft" for x in scientific)
    if drafts:
        report.warn("review", f"{drafts} scientific records/assembly rows are draft; structural checks are not expert curation")
    dates = [date.fromisoformat(s["last_verified"]) for s in sources.values() if s["last_verified"] not in {"unknown", "unverified"}]
    if dates:
        for identifier, source in sources.items():
            if source["last_verified"] not in {"unknown", "unverified"} and (max(dates) - date.fromisoformat(source["last_verified"])).days > 365:
                report.warn(identifier, "verification predates the newest registry check by over a year")

    # Parse other maintained YAML; ignore environments, build output and .git.
    maintained = [root / p for p in ("skills", "templates", "tests", ".github", "docs")]
    for directory in maintained:
        for path in sorted(directory.rglob("*")):
            if path.is_symlink():
                report.error(path.relative_to(root), "symlinks are not supported")
                continue
            if path.is_file() and path.suffix in {".yaml", ".yml"} and path not in {skill / "index.yaml", skill / "data/schema.yaml", root / "tests/biological_edge_cases.yaml"}:
                yaml_file(path)
    markdown = list(root.glob("*.md"))
    for directory in maintained:
        markdown.extend(directory.rglob("*.md"))
    for path in sorted(markdown):
        if path.is_file() and not path.is_symlink():
            check_links(root, path, report, skill if path.is_relative_to(skill) else None)
    citation = yaml_file(root / "CITATION.cff")
    if not isinstance(citation, dict) or citation.get("cff-version") != "1.2.0" or not all(citation.get(k) for k in ("title", "message", "authors", "repository-code")):
        report.error("CITATION.cff", "missing citation metadata or wrong CFF version")
    if not (root / "LICENSE").is_file():
        report.error("LICENSE", "missing distribution license")
    report.counts = {"topics": len(records), "sources": len(sources), "assemblies": len(assemblies), "evaluations": len(case_ids)}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (defaults to script location)")
    args = parser.parse_args()
    report = validate(args.root)
    for item in report.errors:
        print(f"ERROR {item}")
    for item in report.warnings:
        print(f"WARNING {item}")
    print(f"{'FAIL' if report.errors else 'PASS'}: {report.counts}; {len(report.errors)} errors, {len(report.warnings)} warnings")
    return bool(report.errors)


if __name__ == "__main__":
    sys.exit(main())
