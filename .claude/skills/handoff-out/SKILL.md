---
name: handoff-out
description: Release this session’s lane to a sponsor-designated successor in the resolved Backend or Lens lane; explicit requests only, never installation or discussion.
disable-model-invocation: true
user-invocable: true
---

Mode: **outgoing**. No required arguments. This is a session-to-session handoff;
Claude → Claude, Codex → Codex and cross-provider transfers use the same process. Provider,
account and configuration root are observed identity metadata, not routing defaults.

Before following startup pointers or selecting a baton, locate the project checkout and
read `docs/memory/durable-rules/cross-model-continuity-process.md`, starting with
**Lane selection — before startup or baton discovery** and **Provider-neutral commands and
session identity**. If either section is absent, obtain the accepted matching command and
procedure revision before proceeding. Never default to Backend, infer a lane from the
provider/account alone, or assume outgoing means “switch to the other model.”

Read `docs/memory/durable-rules/sponsor-operating-doctrine.md` and carry the complete working
approach and learning sources with their concrete application in the selected lane.
Installation and inspection do not execute a handoff. If the outgoing release is already
published, follow the separately authorized supplement path; do not release again.

For **Lens**, follow the canonical Lens-only path. Do not execute Backend registry/transfer
mechanics, rebind its routines, select its baton or emit a BACKEND release/ACK.
For **Backend**, also read and follow
`ops/ai-trading-pilot-continuity/skills/shared/backend-out.md`
from the same accepted project revision before acting; it contains the existing complete
checkpoint/routine mechanics. Do not select a Lens baton. Counterpart coordination messages
are dependencies, not custody. A missing required source leaves the transition unresolved.
