# 发布计划

## 推荐公开标识

- 仓库名：`agent-harness-skills`
- GitHub 副标题：`Portable agent skills inspired by the public CC codebase patterns.`
- 一句话介绍：`Memory, verification, coordination, compression, and proactive-agent skills for Claude Code, Codex, and OpenClaw.`
- GitHub release 标题：`v0.1.0: First Portable CC Harness Skills`

<details>
<summary>English</summary>

## Recommended Public Identity

- Repo name: `agent-harness-skills`
- GitHub subtitle: `Portable agent skills inspired by the public CC codebase patterns.`
- One-line pitch: `Memory, verification, coordination, compression, and proactive-agent skills for Claude Code, Codex, and OpenClaw.`
- GitHub release title: `v0.1.0: First Portable CC Harness Skills`

</details>

## 推荐 GitHub Topics

- `ai-agent`
- `coding-agent`
- `agent-harness`
- `agent-memory`
- `multi-agent`
- `prompt-engineering`
- `context-compression`
- `developer-tools`
- `codex`
- `openclaw`

<details>
<summary>English</summary>

## Recommended GitHub Topics

- `ai-agent`
- `coding-agent`
- `agent-harness`
- `agent-memory`
- `multi-agent`
- `prompt-engineering`
- `context-compression`
- `developer-tools`
- `codex`
- `openclaw`

</details>

## 发布顺序

首批发布顺序：

1. `dream-memory`
2. `memory-extractor`
3. `structured-context-compressor`
4. `verification-gate`
5. `swarm-coordinator`
6. `kairos-lite`

建议首个公开 tag：`v0.1.0`

<details>
<summary>English</summary>

## Publish Order

Release order for the first batch:

1. `dream-memory`
2. `memory-extractor`
3. `structured-context-compressor`
4. `verification-gate`
5. `swarm-coordinator`
6. `kairos-lite`

Suggested first public tag:

- `v0.1.0`

</details>

## GitHub Release 文案

### 仓库简介

`CC Harness Skills` 将公开镜像的 `CC` agent codebase 中的 6 个 portable skill 重新整理为适用于 `Claude Code`、`Codex` 和 `OpenClaw` 的 bundle。每个 bundle 都包含通用的 `SKILL.md`、prompt template、source notes 和小型 helper script。

### 发布说明

`v0.1.0` 为首个公开版本，包含：

- `CC Dream Memory`
- `CC Memory Extractor`
- `CC Context Compressor`
- `CC Verification Gate`
- `CC Swarm Coordinator`
- `CC Kairos Lite`

这个版本聚焦可移植的 prompts 和 scripts，而不是特定平台的 runtime hook。目标是在加入更深的平台集成之前，先让这些模式能跨主要 coding-agent host 使用。

推荐仓库简介：

`Portable CC-inspired skills for memory, verification, multi-agent coordination, context compression, and proactive coding-agent workflows.`

<details>
<summary>English</summary>

## GitHub Release Copy

### Repo Intro

`CC Harness Skills` packages six portable skills extracted from a publicly mirrored `CC` agent codebase and rewritten for `Claude Code`, `Codex`, and `OpenClaw`. Each bundle ships with a host-agnostic `SKILL.md`, a prompt template, source notes, and a small helper script.

### v0.1.0 Release Notes

First public release of the `CC Harness Skills` pack.

Included in `v0.1.0`:

- `CC Dream Memory`
- `CC Memory Extractor`
- `CC Context Compressor`
- `CC Verification Gate`
- `CC Swarm Coordinator`
- `CC Kairos Lite`

This release focuses on portable prompts and scripts, not host-specific runtime hooks. The goal is to make the patterns usable across major coding-agent hosts before adding deeper platform integrations.

Recommended short repo description:

`Portable CC-inspired skills for memory, verification, multi-agent coordination, context compression, and proactive coding-agent workflows.`

</details>

## ClawHub 列表文案

### `dream-memory`

`把最近会话、日志和主题 memory 合并为一个简短稳定的 memory 索引，同时避免保存过期的代码事实。`

### `memory-extractor`

`从最近对话中提取稳定的用户偏好、反馈、项目和参考记忆，同时避免把脆弱的代码状态细节写进去。`

### `structured-context-compressor`

`把长 coding session 压缩为九段式 continuation summary，并保留请求、文件、错误、用户消息和下一步。`

### `verification-gate`

`在实现后执行只读 verification pass，将 verified、unverified 和 failed 工作明确区分。`

### `swarm-coordinator`

`通过 research、synthesis、implementation 和 verification 的边界化 worker 分工来协调多个 agent。`

### `kairos-lite`

`添加轻量 proactive job，并提供 schedule、sleep、brief 和 expiry 规则，但不做完整 daemon 平台。`

<details>
<summary>English</summary>

## ClawHub Listing Copy

### `dream-memory`

`Consolidate recent sessions, logs, and topic memories into a short durable memory index without storing stale code facts.`

### `memory-extractor`

`Extract durable user, feedback, project, and reference memories from recent turns while avoiding fragile code-state details.`

### `structured-context-compressor`

`Compress a long coding session into a nine-part continuation summary that preserves request, files, errors, user messages, and the next step.`

### `verification-gate`

`Run a read-only verification pass after implementation so verified, unverified, and failed work are clearly separated.`

### `swarm-coordinator`

`Coordinate multiple agents through research, synthesis, implementation, and verification with bounded worker ownership.`

### `kairos-lite`

`Add lightweight proactive jobs with schedule, sleep, brief, and expiry rules without committing to a full daemon platform.`

</details>

## 发布检查清单

1. 运行 `bash ./skills/check_all.sh`。
2. 确认 `TEST_REPORT.md` 中的最新 smoke test 结果。
3. 将 `v0.1.0` 发布到 GitHub。
4. 按顺序发布到 ClawHub。
5. 每个 skill 页面复用上面的单行 listing 文案。

<details>
<summary>English</summary>

## Release Checklist

1. Run `bash ./skills/check_all.sh`.
2. Confirm the latest smoke-test report in `TEST_REPORT.md`.
3. Publish `v0.1.0` to GitHub.
4. Publish to ClawHub in the listed order.
5. Reuse the one-line listing copy above for each skill page.

</details>

