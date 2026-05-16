# Project Overview / 项目概览

## Project Positioning / 项目定位

This project is a lightweight Agent Skill Bundle System for AI coding agents. It upgrades prompt-only skills into schema-based, executable, verifiable, and benchmarkable bundles.

本项目是面向 AI coding agent 的轻量级 `Agent Skill Bundle System`。它把 prompt-only skill 升级为基于 schema、可执行、可验证、可 benchmark 的 bundle。

## Core Problem / 解决的问题

AI coding agents often fail in the same ways:

- verification gaps: the agent claims completion without evidence
- context loss: key constraints or failed attempts disappear during compression
- coordination ambiguity: multi-agent work becomes unbounded or unclear
- memory pollution: low-value, stale, or sensitive data gets stored as memory
- proactive job safety: background-style actions lack permission and expiry control

AI coding agent 常见失效模式包括：

- verification gap：没有证据就声称完成
- context loss：压缩上下文时丢失关键约束或失败尝试
- coordination ambiguity：多 Agent 任务边界不清、容易失控
- memory pollution：memory 里保存了低价值、过期或敏感数据
- proactive job safety：后台式动作缺少权限和过期控制

## Architecture / 架构

```text
SKILL.md
-> skill.yaml
-> input schema
-> runtime script
-> output schema
-> benchmark cases
-> test runner
```

## Six Skill Lifecycles / 六个 Skill 生命周期

### verification-gate

Verification lifecycle for checking whether an AI coding task is actually complete.

用于检查 AI coding task 是否真的完成。

### structured-context-compressor

Context snapshot lifecycle for preserving the important parts of a long conversation or handoff.

用于在长对话或交接中保留关键任务快照。

### swarm-coordinator

Coordination lifecycle for turning a complex task into bounded worker plans, handoff rules, and verification criteria.

用于把复杂任务拆成有边界的 worker 计划、交接规则和验证标准。

### memory-extractor

Memory extract / classify / validate lifecycle for building candidate memory items from conversation and notes.

用于从对话和笔记中提取候选 memory，并进行分类与校验。

### dream-memory

Memory merge / expire / retrieve lifecycle for consolidating memory items and preventing stale or conflicting memory growth.

用于合并 memory、清理过期项，并避免 memory 冲突增长。

### kairos-lite

Proactive job lifecycle for planning a lightweight proactive task with schedule, permission, brief output, and expiry control.

用于规划轻量 proactive job，并控制 schedule、权限、brief 和 expiry。

## Why These Skills Matter / 为什么这些 Skill 重要

| Skill | Problem Addressed |
|---|---|
| `verification-gate` | Prevents unverified completion claims. |
| `structured-context-compressor` | Prevents loss of constraints and task state during context compression. |
| `swarm-coordinator` | Prevents ambiguous multi-agent task decomposition. |
| `memory-extractor` | Prevents low-value or sensitive data from becoming long-term memory. |
| `dream-memory` | Prevents duplicate, stale, expired, or conflicting memories from accumulating. |
| `kairos-lite` | Prevents unsafe proactive background behavior without schedule, permission, approval, and expiry. |

Prompt-only skills are easy to read but difficult to verify, test, and reuse reliably. This project upgrades each skill into a structured Agent Skill Bundle so that common AI coding-agent failure modes can be handled with explicit schemas, runtime contracts, permission boundaries, and benchmark cases.

纯 prompt skill 容易阅读，但很难稳定验证、测试和复用。这个项目把每个 skill 升级为结构化 `Agent Skill Bundle`，用显式 schema、runtime contract、权限边界和 benchmark case 来应对常见 AI coding-agent 失效模式。

## Engineering Highlights / 工程亮点

- Schema-first skill interface
- Lightweight runtime abstraction
- Declarative permission boundary
- JSON-based verification report
- Benchmark-driven skill validation
- Backward compatible with existing prompt-only skill systems
- Cross-skill test runner
- Memory Lifecycle design
- Proactive Job Lifecycle safety model

## Extension Opportunities / 二开方向

- Real CI integration
- Agent runtime integration
- Memory store integration
- Scheduler integration
- Skill registry
- Web dashboard or TUI
- More benchmark cases
- Stronger permission enforcement

## Limitations / 项目边界

- Not a full autonomous agent runtime
- Not a real sandbox
- Not a background daemon
- Not a complete benchmark suite
- Rule-based runtime does not replace LLM reasoning

## Suggested Resume / Portfolio Description / 简历或作品集描述

### Chinese

将 prompt-only 的 AI coding agent 技能包改造为轻量级 Agent Skill Bundle System，为每个 skill 增加 `skill.yaml` 元数据、JSON 输入输出 Schema、Runtime 脚本、权限边界和 Benchmark 测试样例，实现 verification、context snapshot、multi-agent coordination、memory lifecycle 和 proactive job lifecycle 等能力的结构化与可验证化。

### English

Refactored prompt-only AI coding-agent skills into a lightweight Agent Skill Bundle System with machine-readable manifests, JSON schemas, executable runtimes, declarative permission boundaries, benchmark cases, and cross-skill test runners. The system covers verification, context snapshots, multi-agent coordination, memory lifecycle management, and proactive job planning.

