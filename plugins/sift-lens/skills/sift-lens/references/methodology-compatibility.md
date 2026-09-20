# Read rank and receipt-time context

Use the actual version and fields returned by the connector. An implemented producer or a new
guide does not mean a new core snapshot has been delivered.

For a valuation question, identify the methodology of that particular analysis from its retrieved
content. A modern retained analyst answer may carry `identity.fvf_version`; an older package may
carry its original policy in `identity.original_archive_identity.policy_version`. Cite the exact
field and package. Do not substitute `board_rules.version`, the connector's software version, or
a runtime release name for the analysis methodology. If the package does not disclose a version,
say that it is unavailable. A methodology label alone does not establish that every later
correction was applied; use the specific retained inputs, calculations and verification evidence.

Report progress separately when relevant: source refresh, completed analysis, accepted output,
and installed connector delivery. `company_research` index/snapshot identity dates the delivered
research; its source-generation identity and cutoff bind original inputs. Section dates and
their missing reasons describe evidence age. `rules.freshness` explains examination-age flags,
not whether all supporting sources refreshed successfully. `fresh.built` dates the enrichment
view, not the latest market session. Do not infer automatic refresh delivery from a successful
request, a recent build, or a local test. When no refresh receipt is delivered, its success/failure
and automatic delivery state remain unknown to that assistant.

Canonical card `high_convexity.rank_value` is the supplied `within_stratum_percentile` in [0,1].
Zero is valid; null is unavailable with its reason. Preserve `stratum_level` (including fallback)
or the supplied suppression size/reason. Do not infer a missing grouping. `as_of` dates the scoring
artifact, and `price_at_scoring` is its historical price, not today's quote or the thesis lock.
Currency needs source support; the numeric price alone does not establish it. Legacy `hc.rank`
and canonical `rank_in_bucket` remain whole-population context, not this within-group percentile.
Neither raw score nor percentile is a calibrated probability or valuation input.

Canonical ranking does not change FVF values, verdicts or pick classes. It orders within board
tiers and can affect which Qualified Picks fall beyond the cap. Read the supplied `board_rank`
and `board_rules.qualified_cap_dropped` pairs; an empty list means none were dropped for that
reason. A tool may sort its displayed rows by gap, so returned row position is not the canonical
board rank. Do not silently recompute or reorder the accepted record.

Receipt timing diagnostics concern self-declared source times. `RECEIPT_AFTER_CUTOFF_SELF_DECLARED`
and `RECEIPT_UNDATED` are UNVERIFIED, not FAIL or proof of unreliable financial content. Preserve
whether the compared field was publication_time or effective_time: a future scheduled event is
not automatically look-ahead. `RECEIPT_SELF_DECLARED_TIME_AT_OR_BEFORE_CUTOFF` passes this timing
comparison only, not source truth. A date without a clock compares days, not exact instants.

For undated receipts, preserve `sentinel`: a runner placeholder differs from an unparseable date
someone declared. The counters `receipt_undated` and `receipt_undated_declared` differ accordingly.
Likewise preserve the separate after-cutoff total, publication-time count and load-bearing count.
Here load-bearing covers citations in calculated valuation inputs, not every decision citation.

An old accepted result keeps its original verification. A later offline verification needs its
own input/result identity and date; discuss it as a subsequent diagnostic. Do not present that
diagnostic as the verification used for the original published result or silently update the
original disposition. Readiness and spot-check reports are bounded operational observations,
not stock research evidence or proof of complete universe coverage.
