# v0.1.0：首个 Portable CC Harness Skills 发布

`CC Harness Skills` 的首次公开发布。

这个仓库把公开镜像的 `CC` coding-agent codebase 中的 6 个 portable skill 重新整理出来，并改写为可以安装到 `Claude Code`、`Codex` 和 `OpenClaw` 的版本，不依赖私有 runtime internals。

`v0.1.0` 包含：

- `CC Dream Memory`
- `CC Memory Extractor`
- `CC Context Compressor`
- `CC Verification Gate`
- `CC Swarm Coordinator`
- `CC Kairos Lite`

每个 bundle 包含：

- 可移植的 `SKILL.md`
- 从源内容整理出来的 prompt template
- source notes
- 与 host 无关的 helper script

本次 release 的 smoke-test 状态：

- `Claude Code`：6 个 skill 都已在本地验证
- `OpenClaw`：6 个 skill 都已在本地验证
- `Codex`：bundle 结构已验证；端到端 runtime smoke test 仍在等待有效本地认证

从这里开始：

- 发布指南：`skills/README.md`
- 发布顺序：`skills/RELEASE_PLAN.md`
- smoke-test 报告：`skills/TEST_REPORT.md`

<details>
<summary>English</summary>

# v0.1.0: First Portable CC Harness Skills

First public release of `CC Harness Skills`.

This repo packages six portable skills extracted from a publicly mirrored `CC` coding-agent codebase and rewritten so they can be installed in `Claude Code`, `Codex`, and `OpenClaw` without relying on private runtime internals.

Included in `v0.1.0`:

- `CC Dream Memory`
- `CC Memory Extractor`
- `CC Context Compressor`
- `CC Verification Gate`
- `CC Swarm Coordinator`
- `CC Kairos Lite`

What ships in each bundle:

- portable `SKILL.md`
- source-derived prompt template
- source notes
- host-agnostic helper script

Smoke-test status for this release:

- `Claude Code`: verified locally for all six skills
- `OpenClaw`: verified locally for all six skills
- `Codex`: bundle structure verified; end-to-end runtime smoke test still pending valid local auth

Start here:

- Publisher guide: `skills/README.md`
- Release order: `skills/RELEASE_PLAN.md`
- Smoke-test report: `skills/TEST_REPORT.md`

</details>

