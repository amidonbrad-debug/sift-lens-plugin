# Retrieve the evidence behind a company analysis

Use when someone asks why a stock received its value, what informed an assumption, or what
challenges the case. This is an on-demand read path. The user's own assistant reasons over the
returned material; retrieval never starts a financial refresh or stock-model analysis on the
sponsor's account. Availability depends on what the connector actually delivers, not this guide.
Access to already-retained supporting material is part of the core experience, including older
analyses. A newer snapshot or methodology does not make that original evidence optional.

## Discover the exact research package

Start with `company(ticker)` for the compact published record and `company_research` discovery.
If the host exposes only `search` and `fetch`, use `fetch("company:TICKER")` for that same
company response. Follow the exact research IDs it returns. Fetch the returned
`delivery_context_id` (`context:delivery`) for the same rules, delivery binding, refresh
observation and supplemental coverage available through `rules`. Do not assume every named
Worker tool or this extension is installed in a particular host. If neither `rules` nor the
supplied context reference is available, disclose that refresh-status access is unavailable;
do not infer success from a working content fetch or invent a different context identifier.

Keep the observation's accepted snapshot night separate from the newer attempted generation.
`accepted_methodology_versions` reports the original examination-contract or archived legacy-policy
version for each record. These are different version families, not a common valuation methodology
or proof that a later correction ran. Retrieve the actual retained analysis for its valuation
methodology. Missing provenance stays UNKNOWN. Source HELD, analysis PENDING, delivery PENDING,
missing receipts and unverified release bindings remain explicit even when old evidence is readable.
The package index identifies the snapshot, record, examination batch and package version, with
coverage and status. Default discovery selects the accepted record for that snapshot. Separately
retained unpublished work needs an explicitly identified package and remains unpublished.

If discovery returns an index-v2 `CURRENT_ACCEPTED` membership, fetch its exact
`current_publication_id` as well as the original package. That small publication supplies the
current snapshot's verified record, qualification, adversary attachment and findings revision;
the package preserves the original inputs and reasoning. Check the publication's
`active_membership`: an older immutable publication can still be fetched, but does not establish
the active result. A `HISTORICAL_ACCEPTED` package remains available through explicit search and
fetch when it leaves current membership. Multiple current matches are an identity gap, not a
choice for the assistant to guess.

Do not take today's qualification or adversary state from the original package's metadata.
For legacy records, `current_fvf_methodology_not_applied: true` means precisely that: a current
legacy-card classification does not assert a modern FVF run. Its `adversarial_verdict` observation
is not a newly generated adversary report. If no current attachment is retained, disclose the
absence rather than filling it from the old package. The returned literal record text preserves
its exact numeric representation; no independent shadow record or recalculation is authoritative.
`TOO_LARGE` is an unavailable response requiring paged delivery, never permission to invent or
silently summarize content that the connector did not return. Older index-v1 delivery retains
its original snapshot binding; do not assume v2 support from this guide alone.

When available, older packages retain source-assigned thesis IDs, their original methodology/model
and examination date. A missing original batch or input can have a recorded missing reason while
frozen reasoning remains retrievable. Do not relabel an older thesis as modern FVF, substitute
today's inputs, or infer that an unlocated file was absent during the original analysis. Coverage
of every company does not establish coverage of every historical analysis. Keep package identity
separate from a different compact record for the same ticker; use explicit discovery when needed.

`search` can discover delivered package identities as well as snapshot metadata and structured
findings. These are separate collections with separate coverage/paging. It does not search the
web or every document body. An unfamiliar topic may still be searchable in retained findings or
investigated with host tools even if there is no company package. Search matches text, not IDs:
a known `evidence:<record-id>` or `research:<package-id>` is fetched directly, and searching for
the ID string returns nothing. Matching is a case-insensitive substring, so a two-word phrase must
appear verbatim; a single distinctive word (a ticker, "currency") finds more than a phrase. An
unfiltered package listing with a large `limit` reads every listed package's manifest and can be
slow; prefer a ticker or a narrow query.

Fetch the returned `research:<package-id>` manifest. Required sections cover the published record,
financial history, estimates, valuation inputs/workings, peers, prices, events, sources, retained
analyst and adversary answers, and Lens finding links. Additional held history and document bodies
can be separate sections. A manifest is an inventory; fetching it does not mean their content
was read. Authentication failure, unsupported delivery and missing evidence are distinct.

## Read usable data and source text

Choose the sections needed for the question and use their exact `content_id` or `first_page_id`.
Pages return actual text; `content_kind: JSON` means concatenate the unchanged chunks before
interpreting complete structured values. Follow `next_id` as needed. `truncated: true` means
there are more pages, not that the rest was read. Report the reading's scope when stopping early.
For a complete reconstruction, page count, UTF-8 digest and total byte/character counts must match.
Never invent an ID from a ticker or accept an arbitrary file path as a remote content substitute.

Use the sources section to connect analyst citations, original filing views and additional held
bodies to their manifest content IDs. Preserve source IDs, titles, URLs, source dates and roles.
An original supplied excerpt and an additional full body are different evidence contexts, even
when they describe the same filing. Stable IDs remain tied to their original content and context;
a later corrected version does not rewrite the earlier cited package.

Read the actual operands and assumptions before explaining a valuation. Retained authored analyst
and adversary answers are interpretations, not independently verified facts. Explain the strongest
challenge and at least one plausible alternative when relevant; identify what evidence could
distinguish them. Cite the fetched section/source next to the claim rather than implying access
to unread linked documents. Paraphrase appropriately; fetching a body is not permission to reproduce
an entire third-party article in the answer.

For “why this valuation and what challenges it,” connect the published value to the retrieved
valuation operands and assumptions, the relevant financial/estimate/peer evidence and dated price,
and the retained analyst/adversary reasoning. Fetch relevant filing or event text where available.
An arithmetic result does not independently verify its input or an authored multiple assumption;
keep that attribution even when both appear in a valuation section. Explain contradictions and
unavailable material alongside the cited reasoning. Identify the analysis methodology from the
actual retained content as described in the methodology guide. Do not stop at the compact
summary when the supporting sections are retrievable.

## Preserve limits and the accepted record

- Keep snapshot night, examination date, price lock, source publication/event/observation/capture
  dates and analysis cutoff separate. Old original inputs may be exactly the right evidence for
  explaining an old decision; they do not establish today's conditions.
- When returned, `rules.delivery` identifies projection construction and `rules.refresh_delivery`
  gives a dated publisher observation. Read source refresh, accepted analysis and delivery states
  independently, together with their source dates, actual methodology versions and pending
  corrections. A newer price or successful projection does not prove a revised analysis ran.
  `UNKNOWN` or `DELIVERY_STATE_UNVERIFIED` may reflect a missing report, mismatched release IDs or
  an observation older than the projection; preserve both identities and the reason. Even
  `CONSISTENT_WITH_ACTIVE_ROOT` means only that these observations agree, not that a separate
  user's assistant passed acceptance. `supplemental_context` separately discloses absent or older
  context; its absence does not make available research packages inaccessible.
- Use each section's units and currency qualifications. A USD equity price does not establish the
  reporting currency of financial history or estimates. Unknown units remain unknown with reason.
- Check price adjustment columns as well as dates. The legacy compact chart builder prefers
  `closeadj` with a `close` fallback, but its global basis label does not identify each point's
  adjustment history. Use available retained price columns to distinguish split-only from
  dividend/spinoff adjustments. A historical adjusted point differing from the locked price does
  not by itself disprove a latest/lock price-only comparison. Do not replace the accepted lock or
  call that comparison total return.
- Inspect availability independently of page count. NOT_HELD may have an explanatory JSON page;
  that page does not make the absent estimates, filing or adversary review available. PARTIAL_VIEW,
  REFERENCE_ONLY, FAILED and identity mismatch must retain their actual explanation.
- Preserve any conflict between the accepted qualification and newly located retained input.
  State both and flag it for review. A narrative estimate or a retained calculated row cannot fill
  a null accepted fair value. Retrieval does not recalculate or repair the published record.
- Lens findings remain separately versioned with verification, review and admission states.
  Follow their evidence IDs and later review links. “Retained,” “needs evidence” and “accepted for
  review” are not accepted core facts. If a reference cannot be fetched, disclose that limitation.

If detailed retrieval is unavailable, answer from the material actually accessible and identify
what is missing. Do not replace this requirement with a local path, claim that a summary contains
all retained evidence, or initiate a sponsor-funded model run. Use the finding guide to preserve
significant disagreements through an available authorized retention path; a connector without a
shared writer can prepare a candidate but cannot truthfully claim that it saved one.
