# Contributing

Small contributions that prevent a concrete scientific error are especially
useful. All scientific additions start as draft, including human-authored
entries until reviewed. Read [SOURCE_POLICY.md](SOURCE_POLICY.md) and
[GOVERNANCE.md](GOVERNANCE.md). Agents must also read [AGENTS.md](AGENTS.md).

## A practical workflow

1. Inspect Git status and existing files. Search `skills/weed-genomics/index.yaml`
   for the taxon, aliases and topic, then check existing source and assembly IDs.
   Reuse a record when its scope fits; do not create duplicate facts.
2. Choose [a template](templates/README.md). Shared concepts go in
   `references/shared/`, families in `references/families/`, species,
   assembly exceptions and annotation records in `references/species/`,
   methods in `references/workflows/`, and tool-selection guidance in
   `references/tools/`. Keep all runtime material inside the skill.
3. Use stable, descriptive IDs. Read the
   [schema guide](skills/weed-genomics/data/README.md). Fill required metadata,
   replace placeholders, keep `review_status: draft` and leave review fields
   empty. A topic should answer when the issue matters, what context is needed,
   the likely mistake, its consequence, the safer action and the evidence.
4. Read the original supporting material. Add a source registry row with its
   actual DOI/accession/URL, verification scope and reuse terms. Cite its ID
   at the relevant claim, not merely at the end of a long document. Distinguish
   observations in a paper from your methodological interpretation.
5. Add the minimal discovery entry to the index. Register an assembly only
   after confirming its accession/version and specimen. Each assembly gets
   one row. Annotation releases are separate scoped topic metadata, not new
   copies of the assembly row. Preserve unknown and conflicting states.
6. Add a case to `tests/biological_edge_cases.yaml` when behavior should change.
   Include a positive control where justified analysis can proceed; avoid
   teaching agents to refuse every task.
7. Run the README's environment setup, `python scripts/validate.py` and
   `python -m unittest discover -s tests -v`. Fix metadata errors without
   inventing facts. Review warnings and explain unresolved ones in the PR.
8. Submit a focused pull request with sources, scope, AI assistance, validation
   results and scientific-review needs. Do not claim reviews that did not
   happen. Maintainers may merge clearly labeled drafts after checking scope
   and provenance; promotion is a separate human scientific decision.

Do not commit/push from an agent session unless the user authorized it.
Use main as the only permanent branch; external PR branches are temporary.
Do not overwrite or remove existing scientific material without approval.

## Example of a useful AI-assisted contribution

“Table 2 of the public genome note identifies this alternate assembly accession.
I added a draft registry row tied to the same specimen, left its annotation
release unknown, cited the table, and added a case prohibiting chromosome
numbers from being treated as subgenome labels.”

An unacceptable contribution says “all Chenopodium album genomes have this
ploidy,” invents an accession or gene crosswalk, copies a restricted database,
or marks itself reviewed because an LLM or CI agrees.

A useful agent prompt is: “Read AGENTS.md. Find existing entries for this topic.
Verify this public source, propose a narrowly scoped draft correction, update
the index and evaluation if necessary, and run local checks. Preserve unrelated
work. Do not commit, push or promote review status.”

## Corrections, disagreements and retirement

For a minor factual correction, show the before/after interpretation, cite the
new evidence, preserve the prior record in Git history and return changed
scientific content to draft. An agent proposing a revision to reviewed text
must clear current review fields and describe why; prior approval remains in
Git/PR history and does not automatically cover the new claim.

For materially different scope or replaced guidance, add a new stable record
and set the old record's `deprecated: true`, `superseded_by` and
`deprecation_reason`. Keep it indexed and readable; never reuse its ID.
If there is no replacement, use an empty supersession list and explain why.
Conflicting evidence is not supersession: retain both sources, describe their
samples/methods and label the uncertainty `conflicting`. Ask a subject expert
to assess the smallest disputed claim.

Source metadata is a dated observation, not a guarantee of current availability.
Recheck URLs and terms when touching affected content. Record access failures
without erasing the source or pretending its findings have been reverified.
