# Design and source audit

Inspected 2026-10-23 during the v0.1 implementation. This is an audit of design
inputs and access, not a claim of independent scientific review. No upstream
implementation, document, database or skill bundle was copied into this project.
Local templates and validation code were written for this repository.

## Precedents inspected

| Resource | What was inspected and influence |
| --- | --- |
| [Agent Skills specification](https://agentskills.io/specification) | Current frontmatter rules, directory/name agreement, optional metadata and progressive disclosure. The validator implements these entrypoint checks; no vendor extensions are required. |
| [Biology Skills](https://github.com/biologyskills/biology-skills) and [website](https://biologyskills.com/) | README, SOURCE_POLICY.md, TOPIC_TEMPLATE.md, GOVERNANCE.md, scripts/validate.py and evals/README.md. Influenced broad domain routing, concise behavioral rules, source-led interpretation, separate human review and vendor-neutral behavior cases. The local schema additionally checks assembly/sample scope and registry relationships. |
| [Science Skills](https://github.com/google-deepmind/science-skills) | README's portable instruction/script/reference pattern and distinction between project licensing and third-party source terms. No scripts or dependencies adopted. |
| [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) | README's tool discovery, composition and MCP separation. Suggests future adapters; no tool runtime or server added. |
| [plant-genomics-mcp](https://github.com/musharna/plant-genomics-mcp) | README's public-database lookup interface, evaluation controls and explicit benchmark limits. Live lookups complement biological knowledge; neither proves source correctness. No performance claims transferred to this project. |
| [OpenAI4S](https://github.com/PKU-YuanGroup/OpenAI4S) | README's separation of orchestration, computation and artifact provenance. Its execution platform is outside this knowledge framework's scope. |
| [bioSkills](https://github.com/GPTomics/bioSkills) | README's workflow-oriented skills, installations and benchmark pointer. README states the repository is archived; this remains an architectural precedent, not a maintenance dependency. No benchmark report was independently evaluated. |
| [IWGC website](https://www.weedgenomics.org/) | Public home page's consortium and resource descriptions. No official adoption of this repository was established. |
| [IWGC annotation pipeline](https://github.com/PattersonWeedLab/IWGC_annotation_pipeline) | README's structural/functional annotation stages, dependency versions and MetaCyc license requirement. It is a method reference, not a verified turnkey interface or a source for unpublished assemblies. |
| [WeedScience.org policy](https://weedscience.org/UC/AIPolicy.html) | Policy page read. Database scraping and AI reuse require permission; no database records were retrieved or ingested. |

Biology Skills declares Apache-2.0; Science Skills distinguishes Apache software,
CC-BY other materials and separate data terms. These projects are credited for
ideas, not represented as contributors or endorsers. No adapted text/code is
vendored, so no upstream notice is incorporated as though code were reused.
If later contributions adapt material, review licenses and retain notices.

For reproducible precedent identification, inspected GitHub file blobs include:

- Biology Skills source policy: f79a89a976749fde9b57d18137e73f08400600d2;
  topic template: b4d224fc3659602096afc109cca2b9d146b64f60;
  governance: 107b9ad1699e99ad3f2c70a2d4af404c070d7d59;
  validator: 00afa72f40eff027a04a3ae16d64d498194a0d8e;
  evaluation format: e38a5b2a14acf0a0c854d08a2a73e117c07f822d.
- Science Skills README: a2788c2e6c07c4d7a0cce136e55504acffd8a8b5.
- ToolUniverse README: bfc709d078a68c092cc7f506a97b50b7c44dfc18.
- plant-genomics-mcp: current README inspected; no pinned code integration.
- OpenAI4S README: d19d03690ce2b85a8d4dad9143269fbc648efd4d.
- bioSkills README: 4121538f3300441b85dcc42a5739d3adcacb3c60.
- IWGC annotation pipeline README: 8819d0dbc89374442e47dafaddaa846659286679.

## Science verification and exclusions

The source registry records exact locators and verification scope. NCBI's
versioning policy and the Sequence Ontology GFF3 specification support reference
identity rules. Glover et al. (2016) support the relationship among homeology,
orthology and subgenome inference. Guan et al. (2020) support the possibility
of haplotypic duplication in primary assemblies. Recommendations derived from
these are explicitly identified as interpretation.

The Chenopodium example comes from the public genome note, inspected via
Europe PMC XML (PMC11452771), particularly Tables 2–3 and methods. The XML
identifies DOI 10.12688/wellcomeopenres.23015.2 and PMC11452771.2; its revision
prose mentions Version 3. That labeling ambiguity is retained in provenance;
no claim that this is the latest publisher version is made. Annotation release,
phasing completeness and an alternate gene crosswalk remain unresolved.
No unpublished Chenopodium data or lab directories were consulted.

The public Cyperus esculentus genome article
[10.1093/gbe/evad027](https://academic.oup.com/gbe/article/15/3/evad027/7049323)
was located through its publisher abstract/data-availability information.
This did not establish the proposed primary/alternate annotation crosswalk.
No species record or accession mapping was invented. The generic gene-number
evaluation uses explicitly synthetic identifiers and the GFF3 source.

## Access limitations and historical resources

- The IWGC species page at [the supplied URL](https://www.weedgenomics.org/species/)
  failed in browsing; a direct request returned HTTP 403. Its species content
  was not inspected.
- The 2024 [IWGC resource paper](https://doi.org/10.1186/s13059-024-03274-y),
  inspected through Europe PMC XML, describes WeedPedia's historical role.
  Reference 168 gives https://weedpedia.weedgenomics.org/ . The endpoint failed
  with a browsing 502 and a direct TLS EOF error. Current availability is
  unverified; these failures do not prove permanent discontinuation.
- PMC browser pages presented a challenge; Europe PMC full-text XML worked for
  the Chenopodium, IWGC and Guan papers. The Wellcome publisher page returned no
  readable text in the browser. The original NCBI documentation URL redirected;
  the working version is recorded in the source registry.
- Installation directories were checked against official
  [Codex](https://learn.chatgpt.com/docs/build-skills) and
  [Claude Code](https://code.claude.com/docs/en/skills) documentation. Local
  filesystem installation is tested; end-to-end client invocation is not.
- No source access restriction was bypassed, and no confidential consortium
  material or restricted weed-resistance records were acquired.

Runtime references, registries and schema all live inside the canonical skill.
Repository tooling, templates and this audit are maintenance-only. Third-party
source availability is not required by deterministic validation.
