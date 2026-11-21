# Contracts: a checkout made on Windows starts the stack

**Slice**: `specs/216-windows-checkout-start` · **Phase 1** · **Written**: 2026-11-21

**None.** The slice exposes no HTTP route, no API payload and no launcher sub-command: `up.sh` and
`up.ps1` keep their arguments (`--print`, `--build`, any compose sub-command), their default command
(`up -d`) and their exit status.

One command *inside* the launchers changes — the `sh -c` the post-start check runs — but it is an
implementation detail between the launcher and the container, consumed by nothing else, and the
launcher's own interface is what the operator types.

Recorded as an explicit `none` rather than silently absent (SDD-12).
