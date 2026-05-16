# 发布指南

这个目录包含 6 个可发布的、从 `CC` 衍生出来的 portable skill bundle。

## 推荐命名

推荐的 GitHub 仓库名：

- `agent-harness-skills`

推荐的公开 skill 名称：

| Slug | Public name |
| --- | --- |
| `dream-memory` | CC Dream Memory |
| `memory-extractor` | CC Memory Extractor |
| `verification-gate` | CC Verification Gate |
| `swarm-coordinator` | CC Swarm Coordinator |
| `structured-context-compressor` | CC Context Compressor |
| `kairos-lite` | CC Kairos Lite |

保持 slug 稳定。品牌展示放在显示名称里，不要改目录名。

<details>
<summary>English</summary>

# Publishing Guide

This directory contains the public release bundles for the six portable `CC`-derived skills.

## Recommended Naming

Recommended GitHub repo name:

- `agent-harness-skills`

Recommended public skill names:

| Slug | Public name |
| --- | --- |
| `dream-memory` | CC Dream Memory |
| `memory-extractor` | CC Memory Extractor |
| `verification-gate` | CC Verification Gate |
| `swarm-coordinator` | CC Swarm Coordinator |
| `structured-context-compressor` | CC Context Compressor |
| `kairos-lite` | CC Kairos Lite |

Keep the slugs stable. Put branding in the display name, not the directory name.

</details>

## Bundle 结构

```text
<skill-name>/
  SKILL.md
  README.md
  references/
    prompt-template.md
    source-notes.md
  scripts/
    ...
```

<details>
<summary>English</summary>

## Bundle Layout

```text
<skill-name>/
  SKILL.md
  README.md
  references/
    prompt-template.md
    source-notes.md
  scripts/
    ...
```

</details>

## 发布顺序

按以下顺序发布：

1. `dream-memory`
2. `memory-extractor`
3. `structured-context-compressor`
4. `verification-gate`
5. `swarm-coordinator`
6. `kairos-lite`

原因：

- 前三个最容易理解和安装
- `verification-gate` 放在 memory pair 之后，能讲清楚质量和安全价值
- `swarm-coordinator` 更进阶，适合放在前面内容之后
- `kairos-lite` 需要最谨慎，应该最后发布

<details>
<summary>English</summary>

## Release Order

Release in this order:

1. `dream-memory`
2. `memory-extractor`
3. `structured-context-compressor`
4. `verification-gate`
5. `swarm-coordinator`
6. `kairos-lite`

Why this order:

- the first three are the easiest to understand and install
- `verification-gate` is a strong quality/safety story after the memory pair
- `swarm-coordinator` is more advanced and benefits from the earlier context
- `kairos-lite` should come last because proactive behavior needs the most caution

</details>

## 发布标签规划

- `v0.1.0`：6 个 skill 的第一次公开发布
- `v0.1.x`：README、prompt 和 script 的修复，不改变工作流
- `v0.2.0`：一个或多个 skill 的工作流发生实质性变化

<details>
<summary>English</summary>

## Release Tag Plan

- `v0.1.0`: first public batch of all six skills
- `v0.1.x`: README, prompt, and script fixes with no workflow redesign
- `v0.2.0`: material workflow change in one or more skills

</details>

## 本地检查

```bash
bash ./skills/check_all.sh
```

<details>
<summary>English</summary>

## Local Checks

```bash
bash ./skills/check_all.sh
```

</details>

## 安装示例

Claude Code：

```bash
mkdir -p ~/.claude/skills
cp -R ./skills/dream-memory ~/.claude/skills/
```

Codex：

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/dream-memory ~/.codex/skills/
```

OpenClaw：

```bash
mkdir -p ~/.openclaw/workspace/skills
cp -R ./skills/dream-memory ~/.openclaw/workspace/skills/
```

<details>
<summary>English</summary>

## Install Examples

Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -R ./skills/dream-memory ~/.claude/skills/
```

Codex:

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/dream-memory ~/.codex/skills/
```

OpenClaw:

```bash
mkdir -p ~/.openclaw/workspace/skills
cp -R ./skills/dream-memory ~/.openclaw/workspace/skills/
```

</details>

## ClawHub 发布

如有需要，先安装 CLI：

```bash
npm i -g clawhub
```

发布单个 skill：

```bash
clawhub publish ./skills/dream-memory \
  --slug dream-memory \
  --name "CC Dream Memory" \
  --version 0.1.0 \
  --tags latest,memory,agent
```

批量发布命令：

```bash
bash ./skills/publish_all.sh 0.1.0
```

<details>
<summary>English</summary>

## ClawHub Publish

Install the CLI if needed:

```bash
npm i -g clawhub
```

Publish a single skill:

```bash
clawhub publish ./skills/dream-memory \
  --slug dream-memory \
  --name "CC Dream Memory" \
  --version 0.1.0 \
  --tags latest,memory,agent
```

Publish the full batch:

```bash
bash ./skills/publish_all.sh 0.1.0
```

</details>

## 相关文档

- 发布文案和顺序：[RELEASE_PLAN.md](RELEASE_PLAN.md)
- smoke test 结果：[TEST_REPORT.md](TEST_REPORT.md)

<details>
<summary>English</summary>

## Related Docs

- Release copy and order: [RELEASE_PLAN.md](RELEASE_PLAN.md)
- Smoke-test results: [TEST_REPORT.md](TEST_REPORT.md)

</details>

