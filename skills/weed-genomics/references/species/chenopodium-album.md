---
id: wg.chenopodium-album-dcchealbu1
title: Chenopodium album dcCheAlbu1 reference interpretation
category: species
scope:
  level: assembly
  taxa: [ncbi:3559]
  assemblies: [asm.gca-948465745-1, asm.gca-948466375-1]
  biological_material: "dcCheAlbu1; specimen KDTOL10275"
evidence_types: [peer_reviewed_primary, expert_interpretation]
review_status: draft
reviewed_by: []
reviewed_on: null
review_evidence: []
review_note: ""
sources: [src.chenopodium-genome]
last_verified: "2026-10-23"
deprecated: false
superseded_by: []
deprecation_reason: ""
related_records: [wg.reference-identity, wg.polyploid-copy-relationships]
uncertainty: [unknown, unverified]
annotation:
  assembly_id: asm.gca-948465745-1
  provider: Ensembl Rapid Release
  release: unknown
---

# Chenopodium album dcCheAlbu1 reference interpretation

## When this matters and required context

Use when interpreting the public dcCheAlbu1 reference. Confirm that the user's
files are the listed assembly version and that their sample is the same
biological material before transferring specimen-specific conclusions.

## Source-backed scope

The genome note identifies Chenopodium album (NCBI taxon 3559), specimen
KDTOL10275 / dcCheAlbu1, collected in Kingston, Surrey, UK. Table 2 identifies
primary assembly dcCheAlbu1.1, GCA_948465745.1, and alternate accession
GCA_948466375.1. [src.chenopodium-genome: taxonomy, methods, Table 2]

For the **primary assembly**, the authors report 27 chromosome-scale scaffolds,
named by size, and interpret the sequenced individual as allohexaploid
(2n = 6x = 54). This is their reported inference, not a chromosome count
performed by this project. [src.chenopodium-genome: genome report, Table 3]

## Mistake, consequence and action

**Interpretation:** assigning subgenomes from consecutive chromosome numbers
would turn size labels into unsupported ancestry labels. Consult an explicit
subgenome analysis before doing so. The alternate accession is not itself a
subgenome designation. Do not generalize this specimen's inferred ploidy to
an unidentified sample or all uses of the species name.

## Unknowns and limits

The paper reports Ensembl Rapid Release annotation of the primary assembly;
an exact annotation release has not been established here.
[src.chenopodium-genome: genome annotation]
Phasing completeness and an alternate-annotation gene crosswalk remain
unverified. No current download availability or annotation equivalence is
asserted. Reproductive biology, taxonomic synonyms and population variation
are outside this starter entry.

This public Darwin Tree of Life specimen is not evidence for an unpublished
lab or IWGC assembly. The citation uses the DOI exposed by Europe PMC's
retrieved version; the source registry records a version-label ambiguity that
should be resolved before upgrading review status.

## Sources

- [src.chenopodium-genome] Mian and colleagues, The genome sequence of fat-hen,
  Chenopodium album L.; genome report, Tables 2–3 and methods.
