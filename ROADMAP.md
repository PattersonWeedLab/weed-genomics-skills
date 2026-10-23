# Roadmap

Proposed milestones; scientific coverage depends on expert contributors.

- **v0.1:** portable skill, small draft collection, provenance, templates,
  governance, offline validation and evaluation specifications.
- **v0.2:** human review of starter claims, taxonomic naming review, curated
  species and assembly additions, verified annotation release references,
  family-specific guidance and source-maintenance ownership.
- **v0.3:** blinded cross-agent evaluations with positive controls, documented
  comparison baselines, and verified analysis-tool references.
- **Later:** optional MCP/database adapters and IWGC resource integration.

Priorities include repeats, structural variation, synteny, genome evolution,
gene families, population genetics and herbicide-resistance evidence. These
fit existing shared/species/workflow categories; create a new skill only for
a genuinely separate responsibility.

Future adapters can expose index queries and return canonical record IDs,
content, scope, review state and commit. Read existing Markdown/YAML/TSV
directly or build disposable derived caches keyed by commit; never create an
independent editable biological registry. Tool results must retain provenance.

dndsR, iwgc-circos, pangenome, annotation and assembly-validation tools are
candidates for future references. Their interfaces have not been verified
here; no integration or functionality is claimed. Review their public
repositories, versions, citations and input/output assumptions before adding
entries. An MCP server or live database API is outside v0.1.
