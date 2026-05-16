# agent-harness-skills: Agent Skill Bundle System

本仓库将面向 `Claude Code`、`Codex` 和 `OpenClaw` 的 prompt-only skills，升级为一个轻量级 `Agent Skill Bundle System`。  
每个 skill 现在都包含：

- `SKILL.md`
- `skill.yaml`
- JSON input/output schema
- lightweight runtime script
- declarative permission boundary
- benchmark test cases
- shared runner

## 为什么要做这个项目

纯 prompt 的 skill 容易阅读，但很难稳定验证、测试和复用。这个项目主要解决 AI coding agent 常见的失效模式：

- 口头说“做完了”，但没有真实验证证据
- 长上下文压缩时丢失用户约束或失败尝试
- 多 Agent 协作时任务边界不清、容易失控
- memory 写入了低价值、过期或冲突数据
- proactive job 缺少 schedule、权限和过期控制，容易变得不安全

## 为什么这 6 个 Skill 重要

| Skill | 解决的问题 |
|---|---|
| `verification-gate` | 防止 agent 没有测试或验证证据就声称任务完成。 |
| `structured-context-compressor` | 防止长上下文压缩时丢失用户约束、失败尝试、当前状态和下一步。 |
| `swarm-coordinator` | 防止多 Agent 协作变得无边界或含糊，要求明确 worker 角色、交接规则、验收标准和验证计划。 |
| `memory-extractor` | 防止把短期任务状态、敏感内容或低价值信息写成长期记忆。 |
| `dream-memory` | 防止 memory store 里堆积重复、过期、失效或冲突的记忆。 |
| `kairos-lite` | 防止 proactive job 因缺少 schedule、权限边界、brief、审批状态和 expiry 控制而变得不安全。 |

Prompt-only skills are easy to read but difficult to verify, test, and reuse reliably. This project upgrades each skill into a structured Agent Skill Bundle so that common AI coding-agent failure modes can be handled with explicit schemas, runtime contracts, permission boundaries, and benchmark cases.

## Skill 总览

| Skill | Lifecycle | 用途 |
|---|---|---|
| `verification-gate` | verification lifecycle | 检查 AI coding task 是否真的完成。 |
| `structured-context-compressor` | context snapshot lifecycle | 生成可恢复的任务快照。 |
| `swarm-coordinator` | coordination lifecycle | 生成多 Agent 任务计划。 |
| `memory-extractor` | memory extract / classify / validate | 提取并校验候选记忆。 |
| `dream-memory` | memory merge / expire / retrieve | 合并、过期、冲突检测和检索记忆。 |
| `kairos-lite` | proactive job lifecycle | 规划轻量主动任务并控制权限与过期。 |

## 标准结构

```text
skills/<skill-name>/
  SKILL.md
  README.md
  skill.yaml
  schemas/
    input.schema.json
    output.schema.json
  scripts/
    run.py
  tests/
    cases/
    expected/
```

## 使用方式

单个运行：

```powershell
python tools/skill_runner.py skills/verification-gate skills/verification-gate/tests/cases/001-no-test-log.input.json
```

批量测试单个 skill：

```powershell
python tools/run_skill_tests.py skills/verification-gate
```

运行全部工程化 skill：

```powershell
python tools/run_all_skill_tests.py
```

## 设计原则

- 保持原有 `SKILL.md` 使用方式兼容
- 以 schema 为先定义输入输出契约
- 使用轻量级本地 runtime
- 在 `skill.yaml` 中声明权限边界
- 每个工程化 skill 都配备 benchmark case
- runtime 不依赖外部 LLM API
- 未明确允许时不修改源码
- skill runtime 不执行 commit 或 push

## 二开方向

- 把 `verification-gate` 接到真实 CI，做 PR precheck
- 把 `structured-context-compressor` 用作会话恢复快照
- 把 `swarm-coordinator` 接入真实多 Agent runtime
- 把 `memory-extractor` 和 `dream-memory` 接入真实 memory store
- 把 `kairos-lite` 接到外部 scheduler，但保留权限和过期控制
- 增加 Web Dashboard 或 TUI 查看测试状态
- 增加 skill registry 或 marketplace

## 项目边界

本仓库不是：

- 完整的 agent runtime
- 后台 daemon
- CI 替代品
- memory database
- 多 Agent 执行器

它是一个轻量级 `Agent Skill Bundle System`：

- `schema + runtime + permission + verification + benchmark` 模板

## 文档

- [Skill Bundle Specification](docs/SKILL_BUNDLE_SPEC.md)
- [Project Overview](docs/PROJECT_OVERVIEW.md)
- [Release Checklist](docs/RELEASE_CHECKLIST.md)

## English

<details>
<summary>Click to expand English version</summary>

This repository upgrades prompt-only skills for `Claude Code`, `Codex`, and `OpenClaw` into a lightweight `Agent Skill Bundle System`. Each skill includes:

- `SKILL.md`
- `skill.yaml`
- JSON input/output schema
- a lightweight runtime script
- a declarative permission boundary
- benchmark test cases
- a shared runner

### Why This Exists

Prompt-only skills are easy to read but hard to verify, test, and reuse consistently. This project addresses common AI coding-agent failure modes:

- claimed completion without real verification
- long-context compression that loses user constraints or failed attempts
- multi-agent coordination that becomes ambiguous or unbounded
- memory workflows that store low-value, stale, or conflicting data
- proactive jobs that become unsafe without schedule, permission, and expiry controls

### Why These Skills Matter

| Skill | Problem Addressed |
|---|---|
| `verification-gate` | Prevents the agent from claiming completion without test or verification evidence. |
| `structured-context-compressor` | Prevents important user constraints, failed attempts, current state, and next steps from being lost during long-context compression. |
| `swarm-coordinator` | Prevents multi-agent work from becoming unbounded or ambiguous by defining worker roles, handoff rules, acceptance criteria, and verification plans. |
| `memory-extractor` | Prevents short-lived task states, sensitive content, or low-value information from being written as long-term memory. |
| `dream-memory` | Prevents memory stores from accumulating duplicate, stale, expired, or conflicting memories without review. |
| `kairos-lite` | Prevents proactive jobs from becoming unsafe background tasks by requiring schedule, permission boundary, brief output, approval state, and expiry control. |

### Skill Overview

| Skill | Lifecycle | Purpose |
|---|---|---|
| `verification-gate` | verification lifecycle | Checks whether an AI coding task is actually complete. |
| `structured-context-compressor` | context snapshot lifecycle | Produces a recoverable task snapshot for long sessions. |
| `swarm-coordinator` | coordination lifecycle | Generates a bounded multi-agent task plan. |
| `memory-extractor` | memory extract / classify / validate | Extracts and validates candidate memories. |
| `dream-memory` | memory merge / expire / retrieve | Merges, expires, and retrieves memories. |
| `kairos-lite` | proactive job lifecycle | Plans lightweight proactive jobs with permission and expiry controls. |

### Standard Structure

```text
skills/<skill-name>/
  SKILL.md
  README.md
  skill.yaml
  schemas/
    input.schema.json
    output.schema.json
  scripts/
    run.py
  tests/
    cases/
    expected/
```

### Usage

Single skill:

```powershell
python tools/skill_runner.py skills/verification-gate skills/verification-gate/tests/cases/001-no-test-log.input.json
```

Batch tests:

```powershell
python tools/run_skill_tests.py skills/verification-gate
```

Run all engineered skills:

```powershell
python tools/run_all_skill_tests.py
```

### Design Principles

- Backward compatible with existing `SKILL.md`
- Schema-first input/output contracts
- Lightweight local runtime scripts
- Declarative permission boundaries in `skill.yaml`
- Benchmark cases for every engineered skill
- No external LLM API required by runtime scripts
- No source-code modification unless explicitly allowed
- No commit / push from skill runtime

### Extension Ideas

- Connect `verification-gate` to a real CI pipeline as a PR precheck
- Use `structured-context-compressor` as a session resume snapshot
- Plug `swarm-coordinator` into a real multi-agent runtime
- Connect `memory-extractor` and `dream-memory` to a persistent memory store
- Attach `kairos-lite` to an external scheduler while preserving permission and expiry controls
- Add a web dashboard or TUI for skill test status
- Add a skill registry or marketplace for discoverable bundles

### Project Boundary

This repository is not:

- a full agent runtime
- a background daemon
- a CI replacement
- a memory database
- a multi-agent executor

It is a lightweight Agent Skill Bundle System:

- schema + runtime + permission + verification + benchmark template

### Documentation

- [Skill Bundle Specification](docs/SKILL_BUNDLE_SPEC.md)
- [Project Overview](docs/PROJECT_OVERVIEW.md)
- [Release Checklist](docs/RELEASE_CHECKLIST.md)

</details>
