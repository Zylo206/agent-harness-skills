# agent-harness-skills

一个面向 `Claude Code`、`Codex` 和 `OpenClaw` 的轻量级智能体技能包系统。

这个仓库把原本只有 `SKILL.md` 的提示词型 skill，升级为包含：

- `SKILL.md`
- `skill.yaml`
- JSON 输入输出结构定义
- 本地可执行运行脚本
- 声明式权限边界
- 基准测试样例
- 统一运行器和测试入口

## 为什么要做这个项目

AI 编码智能体在真实工作里最常见的问题，不是“不会说”，而是“说得像做完了，但实际上不可验证”。

这个项目主要针对以下失效模式：

- 没有测试或验证证据，却声称任务已经完成
- 长上下文压缩时丢失用户约束、失败尝试和下一步
- 多智能体协作时任务边界不清、交接规则缺失
- 记忆系统写入低价值、过期或冲突内容
- 主动任务缺少调度、权限、审批和过期控制

## 这 6 个 Skill 解决什么问题

| Skill | 解决的问题 |
|---|---|
| `verification-gate` | 防止智能体在没有测试或验证证据时声称编码任务已完成。 |
| `structured-context-compressor` | 防止长上下文压缩时丢失用户约束、失败尝试、当前状态和下一步。 |
| `swarm-coordinator` | 防止多智能体协作变得无边界或含糊，要求明确分工、交接规则、验收标准和验证计划。 |
| `memory-extractor` | 防止把短期状态、敏感内容或低价值信息写成长期记忆。 |
| `dream-memory` | 防止记忆存储持续堆积重复、过期、失效或冲突的记忆。 |
| `kairos-lite` | 防止主动任务在缺少调度、权限、审批和过期控制时变成不安全后台任务。 |

## Skill 总览

| Skill | 生命周期 | 用途 |
|---|---|---|
| `verification-gate` | 验证生命周期 | 检查 AI 编码任务是否真的完成。 |
| `structured-context-compressor` | 上下文快照生命周期 | 生成可恢复的任务快照。 |
| `swarm-coordinator` | 协调生命周期 | 生成多智能体任务计划。 |
| `memory-extractor` | 记忆提取 / 分类 / 校验 | 提取并校验候选记忆。 |
| `dream-memory` | 记忆合并 / 过期 / 检索 | 合并、过期、冲突检测和检索记忆。 |
| `kairos-lite` | 主动任务生命周期 | 规划轻量主动任务并控制权限与过期。 |

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

批量测试单个技能包：

```powershell
python tools/run_skill_tests.py skills/verification-gate
```

运行全部 skill：

```powershell
python tools/run_all_skill_tests.py
```

## 设计原则

- 保持原有 `SKILL.md` 使用方式兼容
- 以结构定义为先定义输入输出契约
- 运行脚本保持轻量、本地、可执行
- 在 `skill.yaml` 中声明权限边界
- 每个工程化 skill 都提供基准测试样例
- 运行脚本默认不调用外部 LLM API
- 未明确允许时不修改源码
- 运行脚本不执行 commit 或 push

## 二开方向

- 把 `verification-gate` 接到真实 CI，做 PR precheck
- 把 `structured-context-compressor` 用作会话恢复快照
- 把 `swarm-coordinator` 接入真实多智能体运行时
- 把 `memory-extractor` 和 `dream-memory` 接入真实记忆存储
- 把 `kairos-lite` 接到外部调度器，但保留权限和过期控制
- 增加 Web 面板或 TUI 查看 skill 测试状态
- 增加 skill 注册表或市场

## 项目边界

这个仓库不是：

- 完整自治智能体运行时
- 后台守护进程
- CI 替代品
- 记忆数据库
- 多智能体执行器

它是：

- 轻量级智能体技能包系统
- 一套 `schema + runtime + permission + verification + benchmark` 模板

## 文档

- [技能包规范](docs/SKILL_BUNDLE_SPEC.md)
- [项目概览](docs/PROJECT_OVERVIEW.md)
- [发布检查清单](docs/RELEASE_CHECKLIST.md)

<details>
<summary>English</summary>

# agent-harness-skills

A lightweight `Agent Skill Bundle System` for `Claude Code`, `Codex`, and `OpenClaw`.

This repository upgrades prompt-only skills into structured bundles that include:

- `SKILL.md`
- `skill.yaml`
- JSON input/output schemas
- local executable runtime scripts
- declarative permission boundaries
- benchmark test cases
- shared runners and test entrypoints

## Why This Exists

The real failure mode for coding agents is not poor wording. It is claiming work is done when the result is not executable or verifiable.

This project targets the common failure cases:

- completion claims without test or verification evidence
- long-context compression that loses user constraints, failed attempts, or next steps
- multi-agent coordination without clear worker boundaries or handoff rules
- memory workflows that keep low-value, stale, or conflicting information
- proactive jobs without schedule, permission, approval, or expiry control

## What These 6 Skills Address

| Skill | Problem Addressed |
|---|---|
| `verification-gate` | Prevents the agent from claiming a coding task is complete without test or verification evidence. |
| `structured-context-compressor` | Prevents important user constraints, failed attempts, current state, and next steps from being lost during long-context compression. |
| `swarm-coordinator` | Prevents multi-agent work from becoming unbounded or ambiguous by defining workers, handoff rules, acceptance criteria, and verification plans. |
| `memory-extractor` | Prevents short-lived task states, sensitive content, or low-value information from being written as long-term memory. |
| `dream-memory` | Prevents memory stores from accumulating duplicate, stale, expired, or conflicting memories without review. |
| `kairos-lite` | Prevents proactive jobs from becoming unsafe background tasks without schedule, permission, approval, and expiry control. |

## Skill Overview

| Skill | Lifecycle | Purpose |
|---|---|---|
| `verification-gate` | verification lifecycle | Checks whether an AI coding task is actually complete. |
| `structured-context-compressor` | context snapshot lifecycle | Produces a recoverable task snapshot. |
| `swarm-coordinator` | coordination lifecycle | Generates bounded multi-agent task plans. |
| `memory-extractor` | memory extract / classify / validate | Extracts and validates candidate memories. |
| `dream-memory` | memory merge / expire / retrieve | Merges, expires, detects conflicts, and retrieves memories. |
| `kairos-lite` | proactive job lifecycle | Plans lightweight proactive jobs with permission and expiry control. |

## Standard Structure

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

## Usage

Single skill:

```powershell
python tools/skill_runner.py skills/verification-gate skills/verification-gate/tests/cases/001-no-test-log.input.json
```

Single-skill batch tests:

```powershell
python tools/run_skill_tests.py skills/verification-gate
```

Run all skills:

```powershell
python tools/run_all_skill_tests.py
```

## Design Principles

- Backward compatible with existing `SKILL.md` usage
- Schema-first input/output contracts
- Lightweight local executable runtimes
- Declarative permission boundaries in `skill.yaml`
- Benchmark cases for every engineered skill
- No external LLM API required by runtime scripts
- No source-code modification unless explicitly allowed
- No commit or push from skill runtimes

## Extension Ideas

- Connect `verification-gate` to real CI as a PR precheck
- Use `structured-context-compressor` for session resume snapshots
- Plug `swarm-coordinator` into a real multi-agent runtime
- Connect `memory-extractor` and `dream-memory` to a persistent memory store
- Attach `kairos-lite` to an external scheduler while preserving permission and expiry control
- Add a web dashboard or TUI for skill test status
- Add a skill registry or marketplace

## Project Boundary

This repository is not:

- a full autonomous agent runtime
- a background daemon
- a CI replacement
- a memory database
- a multi-agent executor

It is:

- a lightweight `Agent Skill Bundle System`
- a `schema + runtime + permission + verification + benchmark` template

## Documentation

- [Skill Bundle Specification](docs/SKILL_BUNDLE_SPEC.md)
- [Project Overview](docs/PROJECT_OVERVIEW.md)
- [Release Checklist](docs/RELEASE_CHECKLIST.md)

</details>
