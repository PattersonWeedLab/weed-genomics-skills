# Validation and biological evaluation

Run `python scripts/validate.py` and
`python -m unittest discover -s tests -v` from the repository root.
The validator is read-only and offline. Tests use temporary fixture copies;
they do not rewrite scientific content.

Unit tests inject broken paths, provenance, scopes, review claims and
supersession into fixtures and require rejection. Installation tests compare
file hashes, ensure LICENSE/provenance inclusion and refuse existing targets.

[biological_edge_cases.yaml](biological_edge_cases.yaml) is a vendor-neutral
evaluation specification. Each case includes a question, supplied context,
supporting record/source IDs, required behaviors and prohibited assumptions.
The contexts explicitly distinguish synthetic controls from real observations.
Cases are draft; they need scientific review. Passing schema checks is **not**
a pass by an AI model. No model evaluation has been run.

## A reproducible manual or future automated benchmark

1. Freeze the knowledge commit and case file hash. Choose models/client versions,
   prompts, sampling settings, permitted tools/network access and repeats before
   examining results.
2. Present only question and context to the model. In the skill condition supply
   the skill through normal discovery; in the baseline use the same tools and
   data without this skill. Keep expected/prohibited fields hidden.
3. Save exact prompts, responses, tool traces, retrieved records, costs/timing
   and environment. Use the [run template](../templates/evaluation-run.yaml).
4. Have qualified human scorers assess each required behavior independently:
   0 absent/wrong, 1 partial/qualified, 2 satisfied. Mark each prohibited
   assumption present/absent; any present is a case failure. Full pass requires
   all required behaviors at 2 and no prohibited assumption. Report partial
   scores, disagreements, abstentions and positive-control failures.
5. Compare paired outcomes, include all repeats and limitations, and retain
   raw evidence before claiming improvement. LLM judgments can assist but
   cannot certify biological correctness or promote human review status.

No model API keys, vendor runner or network calls are part of default CI.
The current schema deliberately fixes evaluation review_status to draft;
a future human-approved evaluation-release process should extend it explicitly.
