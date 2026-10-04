# Show the existing Lens board inside Codex

When the user submits Sift Lens alone or asks to show/open/render its dashboard **in the chat**, produce a
visible board, not only a description of available tools. A successful MCP data call does not
establish that the host mounted its optional UI resource. The existing remote widget remains
available to compatible hosts; this explicit Codex path uses the same returned board data.

The private navigation-preview Site is a sample wireframe, not Lens. The service's root website
is a held legacy page; the MCP endpoint is a tool connection, not a browser dashboard. Opening
either, or a raw widget URL without its host bridge, does not launch the connected workspace.
Use `open_lens` when exposed. If only the data tools are installed, this guide's actual-data
visualization is a limited fallback; say so rather than presenting it as the full Lens workspace.

1. Call the installed `board` tool with `set: "board"`. Keep the exact returned structured result
   and record when that call completed. Do not substitute repository fixtures, a cached result
   from an older request, hand-entered prices or a file URL as the source of another user's data.
2. If Codex's in-chat visualization capability is available, read its current skill instructions.
   Save the actual response in the task's output location and use this skill's bundled renderer:

   ```sh
   python3 <skill-directory>/scripts/render_board.py \
     --input <actual-board-response.json> \
     --output <task-visualization-directory>/sift-board.html \
     --read-at <actual-retrieval-time-with-timezone>
   ```

3. Include the visualization content reference required by the host in the same final answer.
   Writing the HTML, returning its filename or linking a separate page does not display it.
   Use the current visualization skill's actual delivery mechanism, not a remembered directive
   or a remote machine's localhost link. Do not precede or follow it with a duplicate Markdown
   board. Keep the answer concise and let the user inspect the board. The bundled fragment needs no
   API request, credentials or financial-model call. Its company selection is local; its labelled
   investigation button hands a question to the user's assistant only after the user clicks it.
   It starts with the list only. Choosing a company replaces that list in place; Back to results
   restores the list and focus to the original company control instead of stacking another card.
4. Preserve the publication night, read time and explicit absent value (including BC's null) as
   separate facts. The board's CURRENT flag describes that snapshot's assessment, not today's
   refresh. Displayed prices/values carry no assumed currency when the response omits it. A
   research question is not a saved finding or a new accepted core record.

5. Keep the recorded pick label and valuation status visible together. Missing current value,
   multiple current valuations, provisional value and delivered pick holds are distinct states;
   a Top Pick label is not financial approval. Preserve the source label and all value safeguards.

For an explicitly selected independent lens, request `board` with its delivered `method_id` when
the installed tool supports it, then give that exact response to the same renderer. It accepts
the versioned method board's `records` as well as the existing board's `rows`. The method view
shows that method's conclusions, completion/review states and dates; it never fills missing
values or ranks from the existing board. Incomplete results are labelled, not treated as picks.
The full raw result is not part of the summary: its investigation action hands the selected
method/result reference to the assistant for retrieval. The fallback does not fetch another
method or reproduce the connected workspace's navigation. Retrieve another actual method board
through the assistant when requested; never populate a method switcher with fabricated results.

Backend's delivered overlap classification appears in both the list and selected-company area.
Its accessible disclosure lists qualifying methods, analysis dates, different conclusions and
unknown coverage. Contradictory, unapproved or unavailable metadata is labelled unavailable.
The badge is additional context; the existing board's labels, ordering and financial safeguards
are unchanged. Missing overlap is not a stock disqualification.

If the host lacks the documented visualization capability, explain that limitation in one or two
sentences. A visual dashboard request is not satisfied by a text table; provide one only if the
user asks for that fallback. Do not promise automatic iframe rendering, invent a display
directive, reinstall the plugin or silently build a website. Renderer output and a browser test
are separate from observed rendering in the actual Codex conversation. Installed distribution
availability must be checked separately from this source file's existence.

For one company the user has selected, the renderer can preload a **single exact method result**
from the existing installed `fetch` tool. Save that response unchanged and its actual retrieval
completion time. Supply both optional arguments before rendering the same board:

```sh
python3 <skill-directory>/scripts/render_board.py \
  --input <actual-method-board-response.json> \
  --method-result <actual-selected-framework-fetch-response.json> \
  --method-result-read-at <actual-detail-retrieval-time-with-timezone> \
  --read-at <actual-board-retrieval-time-with-timezone> \
  --output <task-visualization-directory>/sift-board.html
```

The selected company's **Valuation and entry references** button opens that preloaded detail in
place; Company summary and Back to results restore context and keyboard focus. Other companies
remain summaries. Do not prefetch every row or regenerate a dashboard automatically on each
company click. This remains a limited local display, not connected in-place retrieval: its host
bridge only hands an explicitly requested investigation to the assistant, which must retrieve
that exact method/result. No new network or authentication path is introduced.

The detail must match the board's methodology revision, all snapshot identity fields and exact
selected summary, then the raw result bytes, company, cutoff, card and package. The two saved
input hashes and numerical/forecast crossbinding must match. Absent or mismatched detail shows
its reason while the board, summary and overlap stay usable. These checks establish identity,
**not financial acceptance, currentness, publication eligibility or a completed methodology**.

The reference preserves partial calculations, unperformed financial review, unavailable
conclusions, conditional entry, unverified quotes/opening balances and any synthetic provenance.
Current fundamental references are separate from dated scenario targets. Current fundamental
currency is inherited only from its unique reference-date horizon when all three scenarios have
the same validated forecast currency. The reviewed calculation uses a dimensionless discount;
no new valuation is calculated. Missing, conflicting or unsupported currency leaves the monetary
display unavailable. This v1 forecast supports USD only; there is no assumed currency or FX.
Scenario currency requires the bound forecast currency and its referenced metric/cash/debt/share
rows, dates and financial basis. Missing units
or malformed decimals cannot become money. Conditional entry and policy-qualified entry remain
separate; null remains unavailable, zero remains a source value. No gap, blended score, return,
probability or inferred qualification is calculated. Primary amounts use a labelled two-decimal HALF_EVEN display default, not a declaration of
research precision. Exact source decimals remain available in the corresponding disclosures. Assumptions and source dates are expandable; quoted notes never override structured
review status. Original NOT_PERFORMED is labelled as generation-stage financial review; later
external review is separate and cannot override incomplete-method status. The summary does not
provide the external receipt date or scope; neither is invented. A numerical engineering fixture
is not a live financial publication.
