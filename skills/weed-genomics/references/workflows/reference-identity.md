---
id: wg.reference-identity
title: Establish reference identity before comparison
category: workflow
scope:
  level: general
  taxa: []
  assemblies: []
  biological_material: not_applicable
evidence_types: [authoritative_database, formal_specification, expert_interpretation]
review_status: draft
reviewed_by: []
reviewed_on: null
review_evidence: []
review_note: ""
sources: [src.ncbi-assembly-version, src.gff3]
last_verified: "2026-10-23"
deprecated: false
superseded_by: []
deprecation_reason: ""
related_records: [wg.polyploid-copy-relationships]
uncertainty: [unknown, unverified]
---

# Establish reference identity before comparison

## When this matters and required context

Use before joining gene tables, comparing coordinates or selecting reference
files. Establish sample, assembly accession/version, annotation provider/release,
sequence identifiers, and primary/alternate/phased representation.

## Evidence and mistake

NCBI versions identify sequence collections; GenBank and RefSeq are versioned
independently. Removing the version suffix can silently change the reference.
[src.ncbi-assembly-version: assembly accessions and versions]

GFF3 feature IDs are unique within a file's scope. A matching numeric suffix
in two independently annotated files is not a specified cross-file mapping.
[src.gff3: ID attribute]

## Consequence and recommended action

**Interpretation:** a join based only on suffixes may attach evidence to the
wrong locus. Preserve original IDs and releases. Require a documented mapping
or evaluate sequence/coordinate correspondence, retaining ambiguous and
unmapped cases. A shared name or equal chromosome count does not establish
coordinate compatibility. Record the methods used if correspondence is tested.

For primary/alternate annotations, request the assembly records and actual
annotation files before deciding whether gene IDs correspond. This rule is
general; no Cyperus esculentus crosswalk is established in this collection.

## Example and boundaries

Synthetic example: independently generated `primary_gene_0042` and
`alternate_gene_0042` do not establish biological identity. These are invented
teaching labels, not real deposited gene IDs. If a versioned, documented
crosswalk is supplied, use it within scope after checking mapping cardinality.

Missing annotation provenance is unknown, not evidence that the assembly has
no annotation. This topic provides checks; it does not perform mapping.

## Sources

- [src.ncbi-assembly-version] NCBI, Genome assembly versioning and status.
- [src.gff3] Sequence Ontology, GFF3 specification, ID attribute.
Resolve source IDs and URLs in the source registry.
