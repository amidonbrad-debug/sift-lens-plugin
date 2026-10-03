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
4. Preserve the publication night, read time and explicit absent value (including BC's null) as
   separate facts. The board's CURRENT flag describes that snapshot's assessment, not today's
   refresh. Displayed prices/values carry no assumed currency when the response omits it. A
   research question is not a saved finding or a new accepted core record.

5. Keep the recorded pick label and valuation status visible together. Missing current value,
   multiple current valuations, provisional value and delivered pick holds are distinct states;
   a Top Pick label is not financial approval. Preserve the source label and all value safeguards.

If the host lacks the documented visualization capability, explain that limitation in one or two
sentences. A visual dashboard request is not satisfied by a text table; provide one only if the
user asks for that fallback. Do not promise automatic iframe rendering, invent a display
directive, reinstall the plugin or silently build a website. Renderer output and a browser test
are separate from observed rendering in the actual Codex conversation. Installed distribution
availability must be checked separately from this source file's existence.
