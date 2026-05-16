# Agent Skill Bundle Specification v0.1

## Overview / 概述

The goal of an Agent Skill Bundle is to upgrade a prompt-only skill into a machine-readable, executable, verifiable, and testable bundle that can be used by AI coding agents without depending on a heavy agent framework.

Agent Skill Bundle 的目标，是把 prompt-only skill 升级为机器可读、可执行、可验证、可测试的 bundle，让 AI coding agent 可以在不依赖复杂框架的情况下使用。

The bundle keeps the existing natural-language skill entrypoint, but adds a structured contract for metadata, schema validation, runtime execution, permission boundaries, and benchmark cases.

Bundle 保留原有自然语言 skill 入口，同时补充元数据、schema 校验、runtime 执行、权限边界和 benchmark case 的结构化契约。

## Standard Directory Layout / 标准目录结构

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

## Required Files / 必需文件

### `SKILL.md`

Natural-language behavior instructions for the AI agent. This remains the compatibility layer for Claude Code, Codex, and OpenClaw.

给 AI agent 阅读的自然语言行为说明。它仍然是 Claude Code、Codex 和 OpenClaw 的兼容层。

### `README.md`

Human-readable bundle usage notes, example commands, and a short description of the skill lifecycle.

给人类阅读的使用说明、示例命令和 skill 生命周期简介。

### `skill.yaml`

Machine-readable metadata for:

- `name`
- `version`
- `description`
- `category`
- `trigger`
- `runtime`
- `inputs`
- `outputs`
- `permissions`
- `verification`
- `benchmark`

机器可读元数据，包含：

- `name`
- `version`
- `description`
- `category`
- `trigger`
- `runtime`
- `inputs`
- `outputs`
- `permissions`
- `verification`
- `benchmark`

### `schemas/input.schema.json`

Defines the JSON input accepted by the runtime and is used by the runner for validation.

定义 runtime 接受的 JSON 输入，并由 runner 用于校验。

### `schemas/output.schema.json`

Defines the JSON output emitted by the runtime and is used by the runner for validation.

定义 runtime 输出的 JSON 结构，并由 runner 用于校验。

### `scripts/run.py`

The minimal executable runtime. It reads `input.json`, performs rule-based processing, and emits structured JSON.

最小可执行 runtime。它读取 `input.json`，进行规则化处理，并输出结构化 JSON。

### `tests/cases/`

Benchmark input samples for the skill.

skill 的 benchmark 输入样例。

### `tests/expected/`

Key expected output fields for each case. These are not full JSON snapshots; they are the important assertions for the bundle.

每个 case 的关键期望输出。它们不是完整 JSON 快照，而是用于断言的关键字段。

## skill.yaml Specification / `skill.yaml` 规范

Recommended fields:

- `name`
- `version`
- `description`
- `category`
- `trigger`
- `runtime`
- `inputs`
- `outputs`
- `permissions`
- `verification`
- `benchmark`

推荐字段：

- `name`
- `version`
- `description`
- `category`
- `trigger`
- `runtime`
- `inputs`
- `outputs`
- `permissions`
- `verification`
- `benchmark`

### Field Meaning / 字段含义

- `name`: stable bundle name. / 稳定的 bundle 名称。
- `version`: bundle version, updated when behavior changes. / bundle 版本，行为变化时更新。
- `description`: short human-readable summary. / 简短的人类可读描述。
- `category`: grouping label such as verification, context-management, coordination, memory-lifecycle, or proactive-job-lifecycle. / 分组标签，例如 verification、context-management、coordination、memory-lifecycle、proactive-job-lifecycle。
- `trigger`: when the skill should be considered. / skill 何时应被触发。
- `runtime`: how to execute the bundle. / bundle 的执行方式。
- `inputs`: required and optional inputs. / 必填和可选输入。
- `outputs`: output format and schema reference. / 输出格式和 schema 引用。
- `permissions`: declared read / execute / write / forbidden boundary. / 声明式 read / execute / write / forbidden 边界。
- `verification`: required checks the bundle should satisfy. / bundle 需要满足的验证项。
- `benchmark`: dataset location and evaluation metrics. / 数据集位置和评估指标。

## Permission Model / 权限模型

`permissions` is declarative. It documents intent and guardrails, but it is not a full sandbox.

`permissions` 是声明式约束，它表达意图和边界，但不是完整沙箱。

Recommended structure:

```yaml
permissions:
  read: []
  execute: []
  write: []
  forbidden: []
```

推荐结构：

```yaml
permissions:
  read: []
  execute: []
  write: []
  forbidden: []
```

The lists describe what the skill may inspect, what it may attempt to execute, what it may write, and what it must not do.

这些列表分别表示 skill 可以读取什么、可以尝试执行什么、可以写什么、以及绝对不能做什么。

## Runtime Contract / Runtime 契约

The runtime script must:

- read the input from `input.json`
- emit JSON that matches `schemas/output.schema.json`
- avoid external services unless the skill explicitly allows them
- avoid modifying source code unless the skill explicitly allows it
- return a non-zero exit code on invalid input, missing files, or malformed JSON
- never commit or push code

runtime script 必须：

- 从 `input.json` 读取输入
- 输出符合 `schemas/output.schema.json` 的 JSON
- 除非 skill 明确允许，否则不要调用外部服务
- 除非 skill 明确允许，否则不要修改源码
- 遇到非法输入、文件缺失或 JSON 解析失败时返回非零 exit code
- 不得 commit 或 push 代码

In this repository, the runtime is intentionally lightweight and local. The current skills are rule-based bundle runtimes, not autonomous background agents.

在本仓库中，runtime 是刻意保持轻量且本地化的。当前这些 skill 是基于规则的 bundle runtime，不是自治后台 agent。

## Schema Contract / Schema 契约

- `schemas/input.schema.json` validates the runtime input.
- `schemas/output.schema.json` validates the runtime output.
- The runner should warn and continue if `jsonschema` is unavailable.
- Schemas should be stable enough to support incremental skill evolution without breaking compatibility too often.

- `schemas/input.schema.json` 用于校验 runtime 输入。
- `schemas/output.schema.json` 用于校验 runtime 输出。
- 如果 `jsonschema` 不可用，runner 应该给出 warning 并继续运行。
- schema 应尽量稳定，避免频繁破坏兼容。

## Benchmark Contract / Benchmark 契约

The benchmark folder provides the minimal evaluation surface for a skill bundle.

benchmark 目录提供了 skill bundle 的最小评估面。

- `tests/cases/*.input.json` are the benchmark inputs
- `tests/expected/*.expected.json` are the key expected outputs
- expected files do not need to match the full runtime output
- the batch runner supports:
  - exact field matching
  - `_non_empty` assertions
  - nested key access such as `summary.extracted_count`
  - `_min` assertions such as `summary.extracted_count_min`

- `tests/cases/*.input.json` 是 benchmark 输入
- `tests/expected/*.expected.json` 是关键期望输出
- expected 文件不需要和完整 runtime 输出完全一致
- batch runner 支持：
  - 精确字段匹配
  - `_non_empty` 断言
  - 嵌套 key 访问，例如 `summary.extracted_count`
  - `_min` 断言，例如 `summary.extracted_count_min`

## Lifecycle Categories / 生命周期分类

The repository currently uses six lifecycle categories:

- verification lifecycle
- context snapshot lifecycle
- coordination lifecycle
- memory extract / classify / validate
- memory merge / expire / retrieve
- proactive job lifecycle

本仓库当前使用六类 lifecycle：

- verification lifecycle
- context snapshot lifecycle
- coordination lifecycle
- memory extract / classify / validate
- memory merge / expire / retrieve
- proactive job lifecycle

## Backward Compatibility / 向后兼容

`SKILL.md` remains in place and keeps the existing skill usage flow compatible with Claude Code, Codex, and OpenClaw.

`SKILL.md` 会继续保留，并保持与 Claude Code、Codex、OpenClaw 的原有 skill 使用方式兼容。

The new bundle files are an enhancement layer, not a replacement layer.

新增的 bundle 文件是增强层，不是替代层。

## Adding a New Skill / 新增 Skill 的流程

Checklist:

1. Create `skills/<skill-name>/`
2. Write or preserve `SKILL.md`
3. Add `skill.yaml`
4. Add `schemas/input.schema.json`
5. Add `schemas/output.schema.json`
6. Add `scripts/run.py`
7. Add `tests/cases/`
8. Add `tests/expected/`
9. Update the skill `README.md`
10. Run `python tools/run_skill_tests.py skills/<skill-name>`

检查清单：

1. 创建 `skills/<skill-name>/`
2. 编写或保留 `SKILL.md`
3. 添加 `skill.yaml`
4. 添加 `schemas/input.schema.json`
5. 添加 `schemas/output.schema.json`
6. 添加 `scripts/run.py`
7. 添加 `tests/cases/`
8. 添加 `tests/expected/`
9. 更新该 skill 的 `README.md`
10. 运行 `python tools/run_skill_tests.py skills/<skill-name>`

## Skill Family Notes / 各生命周期说明

### verification lifecycle

Use when the skill exists to check whether a coding task is actually done.

当 skill 的职责是检查 coding task 是否真的完成时使用。

### context snapshot lifecycle

Use when the skill must preserve task state across long conversations or handoffs.

当 skill 需要在长对话或交接中保留任务状态时使用。

### coordination lifecycle

Use when the skill must produce bounded worker plans and handoff rules.

当 skill 需要输出有边界的 worker 计划和交接规则时使用。

### memory extract / classify / validate

Use when the skill must derive candidate memory items from conversations or notes.

当 skill 需要从对话或笔记中提取候选 memory 时使用。

### memory merge / expire / retrieve

Use when the skill must consolidate memory items, remove stale items, and answer retrieval queries.

当 skill 需要合并 memory、清理过期项，并支持检索时使用。

### proactive job lifecycle

Use when the skill must plan a bounded proactive job with schedule, permission, expiry, and a brief.

当 skill 需要规划一个带有 schedule、权限、过期时间和 brief 的轻量 proactive job 时使用。

