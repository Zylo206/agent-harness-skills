# 项目概览

## 项目定位

本项目是面向 AI coding agent 的轻量级 `Agent Skill Bundle System`。它把 prompt-only skill 升级为基于 schema、可执行、可验证、可 benchmark 的 bundle。

<details>
<summary>English</summary>

This project is a lightweight Agent Skill Bundle System for AI coding agents. It upgrades prompt-only skills into schema-based, executable, verifiable, and benchmarkable bundles.

</details>

## 解决的问题

AI coding agent 常见失效模式包括：

- verification gap：没有证据就声称完成
- context loss：压缩上下文时丢失关键约束或失败尝试
- coordination ambiguity：多 Agent 任务边界不清、容易失控
- memory pollution：memory 里保存了低价值、过期或敏感数据
- proactive job safety：后台式动作缺少权限和过期控制

<details>
<summary>English</summary>

AI coding agents often fail in the same ways:

- verification gaps: the agent claims completion without evidence
- context loss: key constraints or failed attempts disappear during compression
- coordination ambiguity: multi-agent work becomes unbounded or unclear
- memory pollution: low-value, stale, or sensitive data gets stored as memory
- proactive job safety: background-style actions lack permission and expiry control

</details>

## 架构

```text
SKILL.md
-> skill.yaml
-> input schema
-> runtime script
-> output schema
-> benchmark cases
-> test runner
```

<details>
<summary>English</summary>

```text
SKILL.md
-> skill.yaml
-> input schema
-> runtime script
-> output schema
-> benchmark cases
-> test runner
```

</details>

## 六个 Skill 生命周期

### verification-gate

用于检查 AI coding task 是否真的完成。

### structured-context-compressor

用于在长对话或交接中保留关键任务快照。

### swarm-coordinator

用于把复杂任务拆成有边界的 worker 计划、交接规则和验证标准。

### memory-extractor

用于从对话和笔记中提取候选 memory，并进行分类与校验。

### dream-memory

用于合并 memory、清理过期项，并避免 memory 冲突增长。

### kairos-lite

用于规划轻量 proactive job，并控制 schedule、权限、brief 和 expiry。

<details>
<summary>English</summary>

### verification-gate

Verification lifecycle for checking whether an AI coding task is actually complete.

### structured-context-compressor

Context snapshot lifecycle for preserving the important parts of a long conversation or handoff.

### swarm-coordinator

Coordination lifecycle for turning a complex task into bounded worker plans, handoff rules, and verification criteria.

### memory-extractor

Memory extract / classify / validate lifecycle for building candidate memory items from conversation and notes.

### dream-memory

Memory merge / expire / retrieve lifecycle for consolidating memory items and preventing stale or conflicting memory growth.

### kairos-lite

Proactive job lifecycle for planning a lightweight proactive task with schedule, permission, brief output, and expiry control.

</details>

## 为什么这些 Skill 重要

| Skill | 解决的问题 |
|---|---|
| `verification-gate` | 防止 agent 没有测试或验证证据就声称任务完成。 |
| `structured-context-compressor` | 防止长上下文压缩时丢失用户约束、失败尝试、当前状态和下一步。 |
| `swarm-coordinator` | 防止多 Agent 协作变得无边界或含糊，要求明确 worker 角色、交接规则、验收标准和验证计划。 |
| `memory-extractor` | 防止把短期任务状态、敏感内容或低价值信息写成长期记忆。 |
| `dream-memory` | 防止 memory store 里堆积重复、过期、失效或冲突的记忆。 |
| `kairos-lite` | 防止 proactive job 因缺少 schedule、权限边界、brief、审批状态和 expiry 控制而变得不安全。 |

Prompt-only skills are easy to read but difficult to verify, test, and reuse reliably. This project upgrades each skill into a structured Agent Skill Bundle so that common AI coding-agent failure modes can be handled with explicit schemas, runtime contracts, permission boundaries, and benchmark cases.

<details>
<summary>English</summary>

| Skill | Problem Addressed |
|---|---|
| `verification-gate` | Prevents unverified completion claims. |
| `structured-context-compressor` | Prevents loss of constraints and task state during context compression. |
| `swarm-coordinator` | Prevents ambiguous multi-agent task decomposition. |
| `memory-extractor` | Prevents low-value or sensitive data from becoming long-term memory. |
| `dream-memory` | Prevents duplicate, stale, expired, or conflicting memories from accumulating. |
| `kairos-lite` | Prevents unsafe proactive background behavior without schedule, permission, approval, and expiry. |

Prompt-only skills are easy to read but difficult to verify, test, and reuse reliably. This project upgrades each skill into a structured Agent Skill Bundle so that common AI coding-agent failure modes can be handled with explicit schemas, runtime contracts, permission boundaries, and benchmark cases.

</details>

## 工程亮点

- Schema-first skill interface
- Lightweight runtime abstraction
- Declarative permission boundary
- JSON-based verification report
- Benchmark-driven skill validation
- Backward compatible with existing prompt-only skill systems
- Cross-skill test runner
- Memory Lifecycle design
- Proactive Job Lifecycle safety model

<details>
<summary>English</summary>

- Schema-first skill interface
- Lightweight runtime abstraction
- Declarative permission boundary
- JSON-based verification report
- Benchmark-driven skill validation
- Backward compatible with existing prompt-only skill systems
- Cross-skill test runner
- Memory Lifecycle design
- Proactive Job Lifecycle safety model

</details>

## 二开方向

- 接入真实 CI，把 `verification-gate` 变成 PR precheck
- 把 `structured-context-compressor` 作为 session resume snapshot
- 把 `swarm-coordinator` 接入真实 multi-agent runtime
- 把 `memory-extractor` 和 `dream-memory` 接入真实 memory store
- 把 `kairos-lite` 接到外部 scheduler，但必须保留权限和 expiry
- 增加 web dashboard 或 TUI 查看 skill test 状态
- 增加 skill registry / marketplace

<details>
<summary>English</summary>

- Real CI integration
- Agent runtime integration
- Memory store integration
- Scheduler integration
- Skill registry
- Web dashboard or TUI
- More benchmark cases
- Stronger permission enforcement

</details>

## 项目边界

- 不是真正的 full agent runtime
- 不是 background daemon
- 不是 CI replacement
- 不是 memory database
- 不是 multi-agent executor

它是：

- lightweight Agent Skill Bundle System
- `schema + runtime + permission + verification + benchmark` template

<details>
<summary>English</summary>

- Not a full autonomous agent runtime
- Not a real sandbox
- Not a background daemon
- Not a complete benchmark suite
- Rule-based runtime does not replace LLM reasoning

It is a lightweight Agent Skill Bundle System:

- schema + runtime + permission + verification + benchmark template

</details>

## 简历 / 作品集描述

### 中文

将 prompt-only 的 AI coding agent 技能包改造为轻量级 Agent Skill Bundle System，为每个 skill 增加 `skill.yaml` 元数据、JSON 输入输出 Schema、Runtime 脚本、权限边界和 Benchmark 测试样例，实现 verification、context snapshot、multi-agent coordination、memory lifecycle 和 proactive job lifecycle 等能力的结构化与可验证化。

### English

Refactored prompt-only AI coding-agent skills into a lightweight Agent Skill Bundle System with machine-readable manifests, JSON schemas, executable runtimes, declarative permission boundaries, benchmark cases, and cross-skill test runners. The system covers verification, context snapshots, multi-agent coordination, memory lifecycle management, and proactive job planning.

