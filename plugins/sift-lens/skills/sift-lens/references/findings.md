# Significant findings and later retrieval

Use this when a discovery merits persistence or when revisiting earlier research. The shared
repository contract is `sift-lens-evidence-exchange/v2`, additive to v1. Available hosts may expose
only the older snapshot tools; discover current capability instead of assuming the extension is
installed. This guide is an authoring aid, not permission to change core stores or schemas.

## Select and attribute

A useful record has a specific claim or question, supporting source references and an explanation
of why someone might revisit it. Preserve meaningful disagreement, unresolved uncertainty and
contrary evidence. Do not save every conversational thought or whole transcripts. Exclude secrets
and private user notes.

This compact template also works as a prepared candidate when the host cannot save it:

```text
Finding ID and title:
Author/task and recorded time:
Optional companies/topics:
Core reference: snapshot/record/field, or explicitly no matching record; scope searched:
Source claims: what each source actually supports, using source IDs:
Sources: ID, publisher/author, URL or retained reference;
         publication/event/retrieval dates (unknown and why when needed);
         body/excerpt/metadata access and supporting content or reference:
Lens interpretation: significance, affected assumptions and alternatives:
Counterevidence / uncertainty / next verification:
Verification: UNVERIFIED or DISPUTED unless source corroboration supports VERIFIED_SOURCE:
Submission: local candidate, published submission, or canonical retention (actual receipt):
Review: SUBMITTED_FOR_REVIEW only after submission; no shared review status for an unsaved draft:
Core admission: NOT_ADMITTED:
Related findings, prior revisions, Backend disposition or admission receipt:
Requested action and urgency:
```

`VERIFIED_SOURCE` concerns source corroboration; it does not make a claim an accepted core input.
Keep the supplied verification and review status visible when retrieving an existing record.
Sources may be reference-only. A URL or provided digest does not prove retained content exists
or that this session read it. Distinguish original source text from a Lens-authored summary; do
not present the summary's digest as the source document's digest. Respect source access and
quotation limits. A new observation may have no company tag or accepted core reference.

## Publish through the available shared path

In the repository host, the existing path is `docs/sift-lens/findings/`. Structured retained
records use `sift-retained-research/v1`; use the actual shared reader's validated shape, including
separate source dates, `claim`, `interpretation`, verification/review status and `NOT_ADMITTED`.
The reader searches committed JSON. Markdown-only notes are not automatically in that library.
Large existing captures remain in their authorized retained locations and are referenced in place.

Lens writes only its assigned branch/worktree. Commit and publish the exact candidate, then use
the existing `docs/coordination/updates/lens/` lane to name the commit, finding IDs, urgency and
requested Backend action. Record the latest counterpart update actually read. Backend owns
retention/integration and responds in `docs/coordination/updates/backend/`; it alone changes main.
An acknowledged submission, canonical retention and core admission are different receipts.
Routine review does not require truth resolution before retaining an unresolved observation.

Keep submitted versions immutable. Correct them with a new stable ID linked by `supersedes`;
link new evidence, interpretations and later dispositions. A Backend rejection of core use does
not erase the source or disagreement. A prior record remains retrievable as history; explain any
newer revision when present. Only an actual Backend/core admission receipt establishes admission.

If the host has no authorized writer, prepare the candidate without saying “saved.” If a write
fails or is only local, report that state and preserve the candidate for the available handoff.
Do not silently substitute personal-state notes, an invented tool or a new service for shared
retention. Existing user authorization governs routine persistence; do not add an approval step.

## Rediscover in a later context

Search the available retained collection using the question, entity, event or topic, then fetch
the returned stable ID. The additive Lens adapter uses `evidence:<record-id>`; legacy `headline:N`
and `filing:N` IDs are snapshot positions and are not durable across refreshes. Inspect paging
and truncation before concluding a result set is complete. Follow relevant revision/disposition
links using available retrieval, reporting a missing link instead of inventing its contents.

The current structured-record search matches a case-insensitive text substring. A narrow phrase
can miss a related revision even when each word appears separately. Try a short entity, ticker
or topic query and inspect related versions before concluding nothing was retained. A historical
finding's old access limitation describes that earlier observation; check the current response's
coverage instead of carrying the old limitation forward automatically.

State collection coverage and revision. The initial collection is
`STRUCTURED_RESEARCH_RECORDS_ONLY`; an empty result does not search all retained databases or the
web. `LIBRARY_UNAVAILABLE` differs from a verified `EMPTY` collection and a `NOT_FOUND` ID. A
reference-only source differs from retained body text. Recheck current external claims when the
question needs current information; preserving an old observation does not refresh its truth.

Read back a newly saved significant finding when possible and report the actual ID/revision and
retention state. Later retrieval should recover the sources, uncertainty and status without the
original conversation. The accepted core's snapshot, labels and values remain unchanged.
