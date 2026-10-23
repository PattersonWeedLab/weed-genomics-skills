# v0.1 implementation validation

Checked 2026-10-23 on Python 3.11.3 before the implementation commit on main.
The initial repository had only README.md and LICENSE, with no unrelated
working-tree changes. No tag, release or organizational approval is implied
by this report.

## Results

| Check | Result |
| --- | --- |
| `python scripts/validate.py` | PASS: 3 topics, 7 sources, 2 assembly rows, 10 evaluation cases; 0 errors, 2 expected warnings. |
| `python -m unittest discover -s tests -v` | PASS: 42 tests, including malformed metadata, provenance, scopes, review promotion, paths, offline validation and installation. |
| Bundled skill-creator `quick_validate.py` | PASS. Local validator also checks current Agent Skills optional fields and directory/name agreement. |
| Official CFF 1.2.0 JSON Schema | PASS for CITATION.cff; schema fetched for this audit, not a network dependency of CI. |
| Standard-library installer CLI | PASS in a temporary destination, without maintenance dependencies or changes to client installations. |
| Standalone skill | PASS: internal Markdown links and index targets resolve; license and hashed provenance included. |
| `git diff --check` | PASS. |
| Original LICENSE | Byte-identical to HEAD. SHA-256: c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4. |

The two expected warnings report the unknown annotation release and the five
draft topic/assembly records. Source verification_status describes source
inspection, not human scientific approval. All AI-authored scientific records
and biological evaluation cases remain draft.

The canonical SKILL.md is 81 lines. Reading the skill requires no Python
dependencies; maintenance uses PyYAML 6.0.2 and jsonschema 4.23.0 plus their
dependencies. Dependency installation uses the network; validation does not.
Tests disable network socket creation for an offline check, and the validator
rejects remote schema references.

## Implementation inventory

- Modified: README.md.
- Preserved: LICENSE and all Git history.
- Added root policies/metadata: AGENTS.md, CONTRIBUTING.md, GOVERNANCE.md,
  SOURCE_POLICY.md, CITATION.cff, CHANGELOG.md, ROADMAP.md, requirements-dev.txt
  .gitignore and .gitattributes.
- Added one canonical skill: skills/weed-genomics/SKILL.md, index.yaml,
  data/schema.yaml, data/README.md, data/source_registry.tsv,
  data/assembly_registry.tsv; references/shared/polyploid-copy-relationships.md,
  references/workflows/reference-identity.md, references/species/chenopodium-album.md,
  and contribution placeholders in references/families/README.md and
  references/tools/README.md.
- Added templates: README.md, species.md, assembly.tsv, annotation.md,
  pitfall.md, shared-concept.md, family.md, workflow.md, tool.md, source.tsv,
  evaluation.yaml and evaluation-run.yaml under templates/.
- Added tooling/tests: scripts/validate.py, scripts/install_skill.py,
  tests/test_validation.py, tests/biological_edge_cases.yaml and tests/README.md.
- Added CI/review: .github/workflows/validate.yml and
  .github/PULL_REQUEST_TEMPLATE.md.
- Added documentation: docs/research-audit.md, docs/releases.md and this report.

## Limits and human decisions

No model-based benchmark or end-to-end Codex/Claude invocation was run.
GitHub Actions is configured for Python 3.10 and 3.12 but has not run remotely.
Citation schema validation was performed separately; the default validator
checks basic CFF metadata and YAML syntax without vendoring that external schema.

Structural tests cannot establish source entailment, actual reviewer identity,
scientific consensus, reference-file correctness or current source availability.
The Chenopodium source has a retained version-label ambiguity, its annotation
release is unknown, and no Cyperus haplotype gene crosswalk was established.
IWGC species-page and historical WeedPedia endpoint access failed as documented
in the [research audit](research-audit.md). No confidential or restricted
database records were ingested.

Maintainers should confirm governance and reviewer roles, obtain expert review
of the three starter topics and their cases, resolve provenance gaps, and then
consider a tagged foundation release. Expand via small sourced contributions
using the templates. These steps do not require a new architecture.
