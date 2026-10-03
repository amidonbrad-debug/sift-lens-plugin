# Install or update Sift Lens

Use the existing Sift Lens package and connection. If it is already installed, update that
installation rather than creating a duplicate app.

1. **Add the marketplace if it is not already configured.** In the target desktop app's plugin
   browser, add `https://github.com/amidonbrad-debug/sift-lens-plugin.git`, branch `main`,
   with no sparse-path restriction. The marketplace is **Sift** and the plugin is **Sift Lens**.
   The equivalent CLI command for adding this marketplace is:

       codex plugin marketplace add amidonbrad-debug/sift-lens-plugin --ref main

2. **Install or update and enable Sift Lens in the target app.** For an existing Git marketplace,
   inspect `codex plugin marketplace list`, then refresh its actual configured name with
   `codex plugin marketplace upgrade <name>`. Use the app's existing install/update flow,
   reload the desktop app, and check the installed plugin version. A repository update or a
   CLI check on another computer does not establish what the target app loaded.
   See [OpenAI's package guidance](https://developers.openai.com/plugins/build/plugins).

3. **Check the existing tool connection.** Package updates and the registered connection's
   tool catalog are separate. If this is a developer-mode connection, refresh that existing
   connection in ChatGPT Plugins and start a new conversation. Published connections follow
   their update/review process. Confirm which tools the target conversation actually exposes;
   do not create a replacement registration just because `open_lens` is absent.
   See [OpenAI's connection guidance](https://developers.openai.com/plugins/deploy/connect-chatgpt).

4. **Open Lens.** In a conversation, choose or mention **Sift Lens**, then submit the message
   (Enter) without adding a question. Selecting the plugin without submitting does not run
   it. You can also type **Open Sift Lens** as an equivalent request. When `open_lens` is
   available and the host supports its view, verify a dated board actually
   appears. Open a company, return to the board, and ask one question. Answers currently
   return in chat. If only an actual-data visual fallback is available, the assistant should
   identify that limit rather than call it the full workspace.

The existing endpoint is `https://sift-lens.amidonbrad.workers.dev/mcp`; it is a tool endpoint,
not a web dashboard. Do not use the held legacy root page, a saved wireframe or raw widget
HTML as proof that Lens launched. No personal token for that legacy page is part of this
installation procedure.

Sift is experimental fake-money research. Nothing here is a recommendation or an order path.
