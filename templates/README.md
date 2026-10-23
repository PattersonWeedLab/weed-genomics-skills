# Contribution templates

Copy a template, replace every REPLACE/placeholder value, and use the
[schema guide](../skills/weed-genomics/data/README.md) for field semantics.
Templates are scaffolds, not scientific records; they are not indexed.
The record frontmatter fields shown in each Markdown template are mandatory
unless noted. Body prompts may be shortened; retain the six pitfall questions.

| Addition | Template | Destination |
| --- | --- | --- |
| Species | [species.md](species.md) | references/species |
| Assembly | [assembly.tsv](assembly.tsv) | append a verified row to data/assembly_registry.tsv |
| Annotation release | [annotation.md](annotation.md) | references/species |
| Exception/pitfall | [pitfall.md](pitfall.md) | references/species or shared |
| Shared concept | [shared-concept.md](shared-concept.md) | references/shared |
| Family | [family.md](family.md) | references/families |
| Method | [workflow.md](workflow.md) | references/workflows |
| Software | [tool.md](tool.md) | references/tools |
| Source | [source.tsv](source.tsv) | append to data/source_registry.tsv |
| Behavior case | [evaluation.yaml](evaluation.yaml) | append under cases in tests/biological_edge_cases.yaml |

Paths in the destination column are relative to skills/weed-genomics except
tests. Add an index row with id, category, topics, taxa, aliases, path, keywords;
use the existing index entries as examples. Add a taxon declaration only if its
verified ID is absent; aliases assist search and are not assertions of synonymy.

For TSV, keep the exact header from the canonical registry and append only the
filled row. Required text cannot be blank; DOI/accession in a source may be
blank. Empty review fields mean draft; list fields use semicolons.
Assembly accessions/versions must be verified before registration. Do not add
placeholder rows. Annotation metadata is separate from assembly identity.

Good uncertainty: “Table 2 identifies this specimen's alternate accession;
annotation release unknown; no crosswalk verified.” Bad uncertainty: inserting
a plausible-looking release number. Good scope: “primary GCA_948465745.1,
dcCheAlbu1.” Bad scope: “all Chenopodium genomes.”

Sources should be cited inline as `[src.identifier: section/table]`.
Examples in the starter records demonstrate source attribution and explicit
interpretation. Scientific review fields remain empty until real human review.
