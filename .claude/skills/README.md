# Handoff commands installed for this Claude Code host

Installed from `amidonbrad-debug/ai-equity-platform`, branch `codex/handoff-working-principles`,
commit `d26f9bfbdd94d236f7a66a09b515fe6d3e589f08` (2026-09-26 10:09:12 -0400), per `ops/ai-trading-pilot-continuity/skills/README.md` at that revision.
Files are byte-identical copies of `ops/ai-trading-pilot-continuity/skills/claude/<name>/SKILL.md`.

| Command | Folder | sha256 |
| --- | --- | --- |
| `/handoff-in` (primary) | `.claude/skills/handoff-in/` | `f1ceef31acfde4d46041b3c328a9d66e4c6fb097da068db7e294ac466b1c78ec` |
| `/handoff-out` (primary) | `.claude/skills/handoff-out/` | `af0789a7d86716680162f4d7acc294a42f4767caa65b01f66755e4b86c4af6c5` |
| `/claude-in` (compatibility alias) | `.claude/skills/claude-in/` | `5a59fc7d6fdcf6b4af78faedb34e60566c060f5c3dff9377c1bf11d35f4426b3` |
| `/claude-out` (compatibility alias) | `.claude/skills/claude-out/` | `3a8968636b5d614f6c887c2ab0c699b02668d92d9d6929b41b09427dbbbd4e0d` |

Host: Claude Code cloud session (config root `~/.claude`, no `CLAUDE_CONFIG_DIR`). The per-container copy under
`~/.claude/skills/` does not survive the container; this project copy is the durable one for sessions on this repo.
The shared procedures (`docs/memory/durable-rules/cross-model-continuity-process.md`, `sponsor-operating-doctrine.md`,
`ops/ai-trading-pilot-continuity/skills/shared/backend-{in,out}.md`) stay in the ai-equity-platform checkout and are read
from there at the same accepted revision; they are not installed as skills. Repository edits to the source skills do not
update these copies: repeat the copy and byte comparison after accepted command changes.

Installation only. No handoff was executed, no lane claimed, no routine changed.
