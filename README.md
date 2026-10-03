# Sift Lens plugin

Sift Lens helps your assistant investigate dated equity research: the published board,
company records, available supporting evidence and questions that challenge the analysis.
Snapshot dates and missing-data limits stay explicit. Sift is experimental fake-money research,
not an order path or a recommendation.

## Install and open

Follow [INSTALL.md](INSTALL.md) to install or update the existing Sift Lens plugin. In a
conversation, choose or mention **Sift Lens**, then submit the message (Enter) without adding
a question. This requests the visual board. Selecting the plugin without submitting does
not run it. You can also type **Open Sift Lens** as an equivalent request. A specific research
question can be asked directly; it does not need another dashboard.

When the host exposes `open_lens`, that tool requests the connected visual workspace. Company
navigation and ordinary research use the data tools without opening another workspace.
Questions currently receive answers in the host chat, not inside the workspace.

If the host exposes only the data tools or cannot mount the workspace, the skill can use the
host's visualization capability to show a limited board from an actual connector response.
That fallback is identified as such. A successful data request alone does not prove a view
rendered. See the [display guide](plugins/sift-lens/skills/sift-lens/references/codex-display.md).

The service's root web page is a held legacy page, not a Lens launch destination. The `/mcp`
URL below is a tool connection, not a browser dashboard. Neither a saved wireframe nor raw
widget HTML substitutes for the connected workspace.

## What is inside

    .agents/plugins/marketplace.json   the existing Sift marketplace catalog
    plugins/sift-lens/plugin.json     the plugin manifest
    plugins/sift-lens/mcp.json         the existing MCP connection
    plugins/sift-lens/skills/sift-lens/SKILL.md   the assistant's research and display instructions

The package preserves the existing app registration in `plugins/sift-lens/.app.json` and the
MCP endpoint `https://sift-lens.amidonbrad.workers.dev/mcp`. Installing an update does not
require creating a replacement app or changing that endpoint.

## Tools and research limits

`open_lens` requests the workspace when available. `rules`, `board`, `company`, `fresh`,
`waterfall`, `night_results`, `outcomes`, `search` and `fetch` return data. They do not each
request a new rendered view. Installed tool availability depends on the host's connection.

The assistant distinguishes the dated core record, external source evidence and its own
interpretation. Published pick labels, current valuation availability and financial review
are separate. Missing values remain unavailable; basis labels identify calculations without
establishing financial acceptance. This connector provides research reads and no order path.
