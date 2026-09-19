# Sift Lens plugin

One install gives ChatGPT (and Codex) the Sift Lens: tonight's board, a company's record with its
chart, what is fresh since the lock, the night waterfall and the outcome ledgers, rendered in the
chat and questioned on your own account.

## Install

Two halves, both one-time, on your own accounts.

**chatgpt.com (the part that renders the board in the chat).** Settings → Plugins → Developer mode
→ on → Create: name `Sift Lens`, URL `https://sift-lens.amidonbrad.workers.dev/mcp`, no
authentication. Then in any chat: `+` → Sift Lens → ask "What stands out on tonight's board?".

**ChatGPT desktop / Codex (the plugin with the skill).** From this repository:

    codex plugin marketplace add amidonbrad-debug/sift-lens-plugin

or Plugins → Add → Add a marketplace → `https://github.com/amidonbrad-debug/sift-lens-plugin.git`,
branch `main`, sparse paths empty. Then Browse directory → Sift → Sift Lens → Install.

No token or login is needed for the read-only connector. The Lens web page
(https://sift-lens.amidonbrad.workers.dev) asks for a personal token, which the Sift owner hands out;
that token also keeps your saved views and notes yours.

Why two halves: an MCP server becomes a ChatGPT "app" only once it is registered on chatgpt.com in
Developer mode, and that registration is per account until the owner publishes the app to a
workspace or the directory. `plugins/sift-lens/.app.json` maps this plugin to the owner's
registration.

## What is inside

    .agents/plugins/marketplace.json   the catalog this repository publishes
    plugins/sift-lens/plugin.json       the plugin manifest
    plugins/sift-lens/mcp.json          the connector: https://sift-lens.amidonbrad.workers.dev/mcp
    plugins/sift-lens/skills/sift-lens/SKILL.md   how the assistant uses the tools and the rules it keeps

## Tools

rules · board · company · fresh · waterfall · night_results · outcomes · search · fetch

Every tool renders its own view in the chat; cards are tappable and open a company's record.

## Rules the assistant keeps

Only what the record holds; anything after the lock is said to be "outside the record"; the
vocabulary of the board (Top Pick, Qualified Pick, gap to value, big-move odds); never a
recommendation; never the words edge or alpha.
