# Sift Lens plugin

One install gives ChatGPT (and Codex) the Sift Lens: tonight's board, a company's record with its
chart, what is fresh since the lock, the night waterfall and the outcome ledgers, rendered in the
chat and questioned on your own account.

## Install

ChatGPT desktop / Codex, from this repository:

    codex plugin marketplace add <owner>/<this-repo>

Then open Plugins → Browse directory → Sift → Sift Lens → Install.

No token or login is needed for the read-only connector. The Lens web page
(https://sift-lens.amidonbrad.workers.dev) asks for a personal token, which the Sift owner hands out;
that token also keeps your saved views and notes yours.

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
