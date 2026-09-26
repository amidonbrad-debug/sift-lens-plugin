# Handoff commands installed for this Claude Code host

Set up per `ops/ai-trading-pilot-continuity/skills/README.md` in `amidonbrad-debug/ai-equity-platform`
at the accepted shared revision on `main`: commit `30996a0bc7108a6d3b41b79d5a48053feb136275`
(2026-09-26 10:22 EDT, merge of PR #3 from `codex/handoff-working-principles`). The files below are
byte-identical copies of `ops/ai-trading-pilot-continuity/skills/claude/<name>/SKILL.md` at that revision,
which are also what `main` commits at `.claude/skills/handoff-in/` and `.claude/skills/handoff-out/` in that repo.

| Command | Role | Folder | sha256 |
| --- | --- | --- | --- |
| `/handoff-in` | primary | `.claude/skills/handoff-in/` | `f1ceef31acfde4d46041b3c328a9d66e4c6fb097da068db7e294ac466b1c78ec` |
| `/handoff-out` | primary | `.claude/skills/handoff-out/` | `af0789a7d86716680162f4d7acc294a42f4767caa65b01f66755e4b86c4af6c5` |
| `/claude-in` | compatibility alias | `.claude/skills/claude-in/` | `5a59fc7d6fdcf6b4af78faedb34e60566c060f5c3dff9377c1bf11d35f4426b3` |
| `/claude-out` | compatibility alias | `.claude/skills/claude-out/` | `3a8968636b5d614f6c887c2ab0c699b02668d92d9d6929b41b09427dbbbd4e0d` |

Why this repo carries a copy: the guide prefers the committed project skills, which travel with the
`ai-equity-platform` checkout. A cloud session opened on this repo does not contain that checkout until it
is attached, so this project copy gives the same commands here. The aliases are the guide's optional
compatibility names at the same revision, not the retired Backend-only versions.

Host: Claude Code cloud session (config root `~/.claude`, no `CLAUDE_CONFIG_DIR`). Any per-container copy
under `~/.claude/skills/` is optional, must stay byte-identical to the accepted revision, and does not survive
the container. The shared procedures (`docs/memory/durable-rules/cross-model-continuity-process.md`,
`sponsor-operating-doctrine.md`, `ops/ai-trading-pilot-continuity/skills/shared/backend-{in,out}.md`) are read
from the `ai-equity-platform` checkout at the same accepted revision and are not installed as skills.
Repository edits to the source skills do not update these copies: repeat the copy and byte comparison after
accepted command changes.

Setup only. No handoff was executed, no custody accepted, no routine changed, no published release rerun.
