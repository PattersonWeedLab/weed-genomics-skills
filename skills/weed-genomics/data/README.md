# Data contract (schema version 1)

[schema.yaml](schema.yaml) is JSON Schema Draft 2020-12 written in YAML.
The root validator applies its definitions to Markdown frontmatter, the
index, TSV rows and evaluation cases, then checks relational constraints.
YAML duplicate keys are errors. Quote ISO dates; use true/false for booleans.
Extra fields are errors, so schema changes are explicit.

## Records and discovery

Every scientific Markdown file in references has required frontmatter:
id, title, category, scope, evidence_types, review_status, reviewed_by,
reviewed_on, review_evidence, review_note, sources, last_verified, deprecated,
superseded_by, deprecation_reason, related_records and uncertainty.

Use stable IDs such as `wg.reference-identity`, `src.ncbi-assembly-version`
and `asm.gca-948465745-1`. They are local identifiers, not database accessions.
Categories map to shared, families, species, workflows and tools folders;
exception and annotation records use species for specific scope or shared
for general guidance. Annotation records require annotation metadata.
Tool records require tool name, upstream URL, version scope, inputs, outputs
and a citation ID; prose explains use/avoid cases and failure modes.

Scope is mandatory:
- general: empty taxa and assemblies; biological_material is not_applicable.
- taxon: one or more declared taxon IDs, no assemblies; material may be unknown.
- assembly: one or more exact registry IDs, matching taxa, and explicit material.
  If multiple materials apply, state each in the string and qualify each
  assertion in prose. Inclusion in a scope does not make every sentence true
  of every listed assembly; label assembly-specific statements explicitly.

Taxon IDs and names are declared once in the index, with supporting sources.
Use NCBI IDs when verified, otherwise a documented local ID; never guess.
The index holds discovery metadata, not scientific claims. Its category and
taxa must agree with the record. Aliases aid retrieval; they do not establish
taxonomic synonymy. Taxonomic rank does not imply chromosome architecture.

## Registries

[source_registry.tsv](source_registry.tsv) has one row per identifiable source
version. Required columns are specified by the schema's source definition.
DOI and accession may be empty when unavailable. verification_status describes
access/source checking, not human scientific review; verification_notes records
exactly what was inspected. Unverified/inaccessible entries may remain, with
warnings for their users. Never fabricate a verification date.

[assembly_registry.tsv](assembly_registry.tsv) has one row per assembly
accession + version, independent of annotation releases. Store the accession
base and version separately; report both together. For a non-INSDC reference,
use its actual upstream identifier and version, plus a stable locator in its
source. A file with no declared release needs a reproducible checksum-based
version and a public provenance source before registration.

Keep sample/accession/genotype identity in biological_material; representation
is primary, alternate or phased only when supported. phasing describes the
verified extent or an uncertainty state. Related assemblies are relationships,
not replacements. All rows have independent human review and deprecation fields.

An annotation can be described by a record's optional annotation object:
assembly_id, provider, release, and optional locator. This is the canonical
place for that annotation reference; adding a second annotation requires its
own record, not a duplicate assembly row. Use unknown/unverified for unresolved
releases; such entries cannot establish reproducible gene coordinates.
The validator rejects duplicate known (assembly_id, provider, release) keys.

TSV uses UTF-8, a header and literal tabs. List columns (source_ids,
related_assemblies, reviewed_by, review_evidence, superseded_by) use semicolons.
Empty lists are empty cells. reviewed_on is empty for drafts; deprecated is
true or false. Other required text cells must be nonempty. No multiline cells.

## Evidence, uncertainty and review

See the evidence enum in schema.yaml. Source types describe provenance; a
record can also declare expert_interpretation for a recommendation derived
from sources. Declared evidence types must be supported by the listed sources
or explicitly represent interpretation/unverified assertions.

Review status is independent. Drafts have no reviewers, date, evidence or note.
Promotions require actual human approval: one reviewer for reviewed; two for
verified/consensus; date, public review evidence and rationale for all.
Consensus also needs a formal standard or review synthesis in its evidence.
Presence checks cannot authenticate humans or establish scientific consensus.

unknown = not established here; not_applicable = no meaning in this scope;
conflicting = disagreeing evidence; unverified = candidate information not
checked. Use these words in prose/metadata instead of ambiguous blank facts.
uncertainty lists applicable states but does not replace explaining them.

Keep deprecated records and IDs; explain the reason and link superseded_by
when a replacement exists. Cross-links must resolve without self-links or
supersession cycles. Dates reflect actual checking, not automated approval.
