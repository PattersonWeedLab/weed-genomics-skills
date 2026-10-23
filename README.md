# Weed Genomics Skills

A source-linked knowledge layer for weed genomics research by scientists and AI
agents. It captures the biological context, reference identities, exceptions
and failure modes that can change an analysis or its interpretation.

This v0.1 foundation supplies one portable **weed-genomics** Agent Skill,
focused Markdown references, small YAML/TSV registries, contributor templates,
and offline validation. It supports selecting and interpreting data; it does
not run genomics pipelines or replace genome databases.

**Scientific status:** all starter records are AI-assisted **drafts**. Their
sources were checked, but no human scientific approval or model-performance
improvement is claimed. This is a PattersonWeedLab repository and a potential
foundation for future IWGC resources, not an officially adopted consortium
standard.

## Try it

Clone the repository and install the single canonical skill:

```bash
git clone https://github.com/PattersonWeedLab/weed-genomics-skills.git
cd weed-genomics-skills
# Codex, user-level installation:
python3 scripts/install_skill.py --client codex
# OR Claude Code, user-level installation:
python3 scripts/install_skill.py --client claude
```

The installer uses only the Python standard library, refuses to overwrite an
existing destination, includes the Apache license and records the source commit,
dirty state and file hashes. It copies from `skills/weed-genomics/`; installed
copies are deployment artifacts, never independent editable sources. For an
update, review the changes and explicitly archive/move your previous install
before reinstalling. Do not contribute edits from an installed copy.

The documented user directories are `~/.agents/skills/weed-genomics` for
[Codex](https://learn.chatgpt.com/docs/build-skills) and
`~/.claude/skills/weed-genomics` for
[Claude Code](https://code.claude.com/docs/en/skills) (checked 2026-10-23).
Start a fresh local client session and invoke `$weed-genomics` in Codex or
`/weed-genomics` in Claude Code. Client discovery and hosted environments vary;
these are local installation instructions, not a hosted integration guarantee.

For another [Agent Skills](https://agentskills.io/specification) client, copy
the complete `skills/weed-genomics` directory to its documented skill location
and include the root LICENSE. Or point the agent directly at
[SKILL.md](skills/weed-genomics/SKILL.md) and allow it to read nearby files.
No runtime Python dependency, API key or network connection is required to read
the bundled knowledge.

Example prompts:

- “Use weed-genomics to explain what I must establish before comparing gene
  counts from a polyploid weed and a diploid relative.”
- “For Chenopodium album dcCheAlbu1, do chromosome labels 1–27 identify
  subgenomes? State the source and the limits of that interpretation.”
- “I have primary and alternate annotation files with matching gene-number
  suffixes. What evidence would establish gene correspondence?”
- “Help me choose a reference for herbicide-resistance genomics. Identify
  missing sample and annotation context, and gaps in this knowledge base.”

## Browse without an agent

Start with the [index](skills/weed-genomics/index.yaml). It routes directly to
three topics: [reference identity](skills/weed-genomics/references/workflows/reference-identity.md),
[polyploid copy relationships](skills/weed-genomics/references/shared/polyploid-copy-relationships.md),
and [Chenopodium album dcCheAlbu1](skills/weed-genomics/references/species/chenopodium-album.md).
Source and assembly IDs resolve in the skill's
[data directory](skills/weed-genomics/data/README.md).

The skill uses progressive disclosure: discovery metadata, a short routing
entrypoint, then only relevant references and registry rows. Family and tool
categories are ready for contributions but have no curated entries yet.

## Contribute and validate

Read [CONTRIBUTING.md](CONTRIBUTING.md), choose a [template](templates/README.md),
and submit a small source-supported change with a reasoning case.
Coding agents must first read [AGENTS.md](AGENTS.md).
[Source policy](SOURCE_POLICY.md) separates evidence from
[human review](GOVERNANCE.md); passing CI never constitutes scientific approval.

Python 3.10+ is required for maintenance:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

After dependencies are installed, checks make no network calls and do not edit
records. They validate schemas, scopes, IDs, provenance links, packaging and
evaluation structure. [Biological evaluations](tests/README.md) specify expected
behavior; they are not executed model benchmarks.
The [implementation validation report](docs/validation-report.md) records the
local checks and their limits.

## Scope, sources and next steps

Coverage is deliberately small. The public dcCheAlbu1 assembly example is not
an unpublished IWGC assembly. Its annotation release is unresolved.
A Cyperus haplotype-ID mapping has not been verified. The assembly registry
is not a current genome catalog. See the [research audit](docs/research-audit.md)
for consulted precedents, access failures and exclusions.

WeedPedia's role is documented historically in a 2024
[IWGC resource paper](https://doi.org/10.1186/s13059-024-03274-y).
Its historical endpoint could not be verified operational during this task;
the species page also could not be retrieved. Neither is a runtime dependency.
We do not ingest International Herbicide-Resistant Weed Database records;
its [AI/data-use policy](https://weedscience.org/UC/AIPolicy.html) requires
permission for those uses.

The [roadmap](ROADMAP.md) proposes expert curation, more species and assemblies,
richer evaluations and future tool interoperability. There is no MCP server,
live API, UI or analysis pipeline in v0.1.

## Citation and license

Use [CITATION.cff](CITATION.cff), adding the commit/release used in your analysis.
No project DOI or tagged release is claimed. Maintainers can follow the
[release procedure](docs/releases.md) for tags and optional Zenodo archiving.
The original [Apache-2.0 license](LICENSE) is preserved; third-party sources
retain their own terms. Design precedents are attributed in the
[research audit](docs/research-audit.md).
