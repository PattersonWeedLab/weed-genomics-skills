# Governance

This is a proposed v0.1 operating policy for the PattersonWeedLab repository.
Repository administrators retain administrative authority; no named scientific
editorial board or IWGC-wide adoption is asserted. Maintainers should publicly
confirm the policy and reviewer roster before promoting scientific content.

## Roles and review

Contributors propose sourced records, corrections and evaluations. Maintainers
manage repository integrity, scope, CI and releases. Subject-matter reviewers
assess biological reasoning, sample/reference scope and source support.
Maintainers may request a reviewer with relevant expertise; being a maintainer
does not automatically establish expertise in every taxon.

Evidence type describes the supporting material. Review status describes human
curation of the local record. A peer-reviewed source can support a draft entry.

| Status | Required local review |
| --- | --- |
| draft | Proposed content with no completed human scientific approval. |
| reviewed | At least one appropriately qualified human records approval, scope and rationale in a public review. |
| verified | At least two independent qualified humans check the claims and references; document independent checks and relevant evaluation review. |
| consensus | At least two qualified humans document an authoritative external standard or broad demonstrated consensus and why this designation is appropriate. |

Record reviewer handles/names, date, public review links and a concise note.
The schema checks presence and distinct reviewers, not their identity,
independence or expertise. An AI, automated test or simulated reviewer never
qualifies as a human reviewer. AI-authored changes cannot self-promote.
Consensus is conservative and still revisable; it is not a popularity vote.

## Decisions and disputes

A maintainer checks structure and provenance before merging. Drafts may be
merged with explicit labeling; scientific promotion requires the human review
above. Review approval applies to the cited content revision, not future edits.
No automatic merging of unreviewed scientific changes.

For disagreement, identify the claim, scope, methods and conflicting evidence
in an issue or PR. Seek another qualified reviewer if needed. Preserve both
interpretations when evidence is insufficient. Maintainers decide repository
placement and wording with a public rationale; they cannot turn unresolved
biology into a fact by administrative decision. Contributors can request
reconsideration with new evidence. Declare relevant conflicts of interest and
seek independent review where they matter.

Maintainers should protect main, require passing checks and human PR review,
and document who can release. These settings are recommendations and have not
been configured by this implementation. Organizational appointments, access
permissions and release approval remain human decisions.
