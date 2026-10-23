# Releases and citation

No tag or DOI is created by the v0.1 implementation. CITATION.cff attributes the
repository organization; it does not infer individual authors or affiliations.

A maintainer can prepare a release after human authorization:

1. Review the diff, source currency, schema compatibility and draft labels.
   Confirm the governance policy and reviewer responsibilities. A foundation
   release may contain clearly labeled drafts; do not imply expert approval.
2. Run the documented validator and tests on the release candidate. Test an
   installation in a new temporary destination. Check the original LICENSE.
3. Update CHANGELOG, the skill metadata version and citation version/date for
   the actual release. Resolve or explicitly carry scientific uncertainties.
4. With authorization, commit the release metadata and create a signed or
   annotated tag such as v0.1.0 on main; publish release notes describing
   review coverage and limitations. Never rewrite published tags.
5. If archiving with Zenodo is authorized, connect the public GitHub repository
   using the owner's account, enable release archiving, and inspect the
   resulting archive metadata. Verify the actual assigned version DOI and
   concept DOI before adding them to CITATION.cff or documentation. Do not
   invent a DOI or publish unpublished materials.
6. Retain historical tags. Breaking schema changes need a documented migration
   path; scientific corrections need scope and behavior notes, even when
   the schema stays compatible.

Installed copies record commit, dirty state and hashes. A dirty checkout's
commit alone is insufficient provenance; preserve its manifest and local diff.
For a source archive without Git metadata, the installer records null commit
and dirty status, with file hashes instead. Report that limitation.
