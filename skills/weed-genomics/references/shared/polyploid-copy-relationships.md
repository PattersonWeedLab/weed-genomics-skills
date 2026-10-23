---
id: wg.polyploid-copy-relationships
title: Interpret copies in polyploid comparisons
category: shared
scope:
  level: general
  taxa: []
  assemblies: []
  biological_material: not_applicable
evidence_types: [peer_reviewed_review, peer_reviewed_primary, expert_interpretation]
review_status: draft
reviewed_by: []
reviewed_on: null
review_evidence: []
review_note: ""
sources: [src.glover-2016, src.guan-2020, src.iwgc-2024]
last_verified: "2026-10-23"
deprecated: false
superseded_by: []
deprecation_reason: ""
related_records: [wg.reference-identity]
uncertainty: [unknown]
---

# Interpret copies in polyploid comparisons

## When this matters and required context

Use for orthology, gene-family counts, subgenome inference and assembly
duplication. Establish specimen ploidy evidence, assembly representation,
annotation scope, gene-family definition and intended evolutionary comparison.
Weeds span different evolutionary lineages and genome architectures; their
agricultural status is not a genomic grouping. [src.iwgc-2024]

## Evidence and mistake

Glover and colleagues define homoeologs through speciation followed by reunion
in an allopolyploid genome. Their relationship can be described as orthology
between subgenomes; it does not establish a single species-level one-to-one
copy. Terminology varies, so specify the evolutionary definition being used.
[src.glover-2016: definition and inference sections]

Allelic representation can produce duplicate assembly regions. Guan and
colleagues demonstrate haplotypic duplication and effects on downstream
annotation in primary assemblies. [src.guan-2020: introduction and results]

## Consequence and recommended action

**Interpretation:** counting every assembled gene model as a distinct biological
duplication can inflate family size. Conversely, removing every similar copy
can erase genuine polyploid content. Retain candidate relationships; distinguish
alleles, homeologs and paralogs using appropriate sequence, phylogenetic,
syntenic and read-support evidence. Similarity or copy count alone is insufficient.

Do not equate alternate haplotypes with subgenomes. Evaluate the study's
representation before applying diploid purging logic to a polyploid assembly.
Do not remove sequences on this guidance alone.

## Example and boundaries

A synthetic comparison yields three similar weed gene models for one relative's
gene. Keep the relationship potentially many-to-one until ancestry and assembly
representation are assessed. Verified single-copy orthologs with suitable
sampling can still support a comparison; polyploid ancestry is not a blanket
reason to refuse analysis.

These recommendations are scoped methodological interpretations, not a
validated classification of any particular weed's genes.

## Sources

- [src.glover-2016] Glover, Redestig and Dessimoz (2016), homoeolog definitions.
- [src.guan-2020] Guan and colleagues (2020), haplotypic assembly duplication.
- [src.iwgc-2024] IWGC resource review (2024), weed diversity and genomic resources.
