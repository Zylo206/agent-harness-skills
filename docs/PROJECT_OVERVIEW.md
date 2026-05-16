# 项目概览

## 项目定位

本项目是面向 AI 编码智能体的轻量级智能体技能包系统。它把提示词型 skill 升级为基于结构定义、可执行、可验证、可基准测试的 bundle。

## 解决的问题

AI 编码智能体常见失效模式包括：

- 验证缺口：没有证据就声称完成
- 上下文丢失：压缩上下文时丢失关键约束或失败尝试
- 协调歧义：多智能体任务边界不清、容易失控
- 记忆污染：记忆系统里保存了低价值、过期或敏感数据
- 主动任务安全：后台式动作缺少权限和过期控制

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

## 六个技能生命周期

### verification-gate

用于检查 AI 编码任务是否真的完成。

### structured-context-compressor

用于在长对话或交接中保留关键任务快照。

### swarm-coordinator

用于把复杂任务拆成有边界的分工计划、交接规则和验证标准。

### memory-extractor

用于从对话和笔记中提取候选记忆，并进行分类与校验。

### dream-memory

用于合并记忆、清理过期项，并避免记忆冲突增长。

### kairos-lite

用于规划轻量主动任务，并控制调度、权限、摘要和过期。

## 为什么这些技能重要

| Skill | 解决的问题 |
|---|---|
| `verification-gate` | 防止智能体没有测试或验证证据就声称任务完成。 |
| `structured-context-compressor` | 防止长上下文压缩时丢失用户约束、失败尝试、当前状态和下一步。 |
| `swarm-coordinator` | 防止多智能体协作变得无边界或含糊，要求明确分工、交接规则、验收标准和验证计划。 |
| `memory-extractor` | 防止把短期任务状态、敏感内容或低价值信息写成长期记忆。 |
| `dream-memory` | 防止记忆存储里堆积重复、过期、失效或冲突的记忆。 |
| `kairos-lite` | 防止主动任务因缺少调度、权限边界、摘要、审批状态和过期控制而变得不安全。 |

纯提示词 skill 容易阅读，但很难稳定验证、测试和复用。这个项目把每个 skill 升级为结构化智能体技能包，用显式结构定义、运行契约、权限边界和基准测试样例来应对常见 AI 编码智能体失效模式。

## 工程亮点

- 以结构定义为先的技能接口
- 轻量运行时抽象
- 声明式权限边界
- 基于 JSON 的验证报告
- 以基准测试驱动的技能校验
- 与现有提示词型 skill 系统保持兼容
- 跨技能测试运行器
- 记忆生命周期设计
- 主动任务生命周期安全模型

## 二开方向

- 接入真实 CI，把 `verification-gate` 变成 PR precheck
- 把 `structured-context-compressor` 作为会话恢复快照
- 把 `swarm-coordinator` 接入真实多智能体运行时
- 把 `memory-extractor` 和 `dream-memory` 接入真实记忆存储
- 把 `kairos-lite` 接到外部调度器，但必须保留权限和过期控制
- 增加 Web 面板或 TUI 查看 skill 测试状态
- 增加 skill 注册表或市场

## 项目边界

- 不是真正的完整智能体运行时
- 不是后台守护进程
- 不是 CI 替代品
- 不是记忆数据库
- 不是多智能体执行器

它是：

- 轻量级智能体技能包系统
- 一套 `schema + runtime + permission + verification + benchmark` 模板

## 简历与作品集描述

将 prompt-only 的 AI coding agent 技能包改造为轻量级 Agent Skill Bundle System，为每个 skill 增加 `skill.yaml` 元数据、JSON 输入输出 Schema、Runtime 脚本、权限边界和 Benchmark 测试样例，实现 verification、context snapshot、multi-agent coordination、memory lifecycle 和 proactive job lifecycle 等能力的结构化与可验证化。

<details>
<summary>English</summary>

# Project Overview

## Project Positioning

This project is a lightweight Agent Skill Bundle System for AI coding agents. It upgrades prompt-only skills into schema-based, executable, verifiable, and benchmarkable bundles.

## Core Problem

AI coding agents often fail in the same ways:

- verification gaps: the agent claims completion without evidence
- context loss: key constraints or failed attempts disappear during compression
- coordination ambiguity: multi-agent work becomes unbounded or unclear
- memory pollution: low-value, stale, or sensitive data gets stored as memory
- proactive job safety: background-style actions lack permission and expiry control

## Architecture

```text
SKILL.md
-> skill.yaml
-> input schema
-> runtime script
-> output schema
-> benchmark cases
-> test runner
```

## Six Skill Lifecycles

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

## Why These Skills Matter

| Skill | Problem Addressed |
|---|---|
| `verification-gate` | Prevents unverified completion claims. |
| `structured-context-compressor` | Prevents loss of constraints and task state during context compression. |
| `swarm-coordinator` | Prevents ambiguous multi-agent task decomposition. |
| `memory-extractor` | Prevents low-value or sensitive data from becoming long-term memory. |
| `dream-memory` | Prevents duplicate, stale, expired, or conflicting memories from accumulating. |
| `kairos-lite` | Prevents unsafe proactive background behavior without schedule, permission, approval, and expiry. |

Prompt-only skills are easy to read but difficult to verify, test, and reuse reliably. This project upgrades each skill into a structured Agent Skill Bundle so that common AI coding-agent failure modes can be handled with explicit schemas, runtime contracts, permission boundaries, and benchmark cases.

## Engineering Highlights

- Schema-first skill interface
- Lightweight runtime abstraction
- Declarative permission boundary
- JSON-based verification report
- Benchmark-driven skill validation
- Backward compatible with existing prompt-only skill systems
- Cross-skill test runner
- Memory Lifecycle design
- Proactive Job Lifecycle safety model

## Extension Opportunities

- Real CI integration
- Agent runtime integration
- Memory store integration
- Scheduler integration
- Skill registry
- Web dashboard or TUI
- More benchmark cases
- Stronger permission enforcement

## Project Boundary

- Not a full autonomous agent runtime
- Not a real sandbox
- Not a background daemon
- Not a complete benchmark suite
- Rule-based runtime does not replace LLM reasoning

It is:

- a lightweight Agent Skill Bundle System
- a `schema + runtime + permission + verification + benchmark` template

## Suggested Resume / Portfolio Description

### Chinese

将 prompt-only 的 AI coding agent 技能包改造为轻量级 Agent Skill Bundle System，为每个 skill 增加 `skill.yaml` 元数据、JSON 输入输出 Schema、Runtime 脚本、权限边界和 Benchmark 测试样例，实现 verification、context snapshot、multi-agent coordination、memory lifecycle 和 proactive job lifecycle 等能力的结构化与可验证化。

### English

Refactored prompt-only AI coding-agent skills into a lightweight Agent Skill Bundle System with machine-readable manifests, JSON schemas, executable runtimes, declarative permission boundaries, benchmark cases, and cross-skill test runners. The system covers verification, context snapshots, multi-agent coordination, memory lifecycle management, and proactive job planning.

</details>
