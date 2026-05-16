# agent-harness-skills: Agent Skill Bundle System

From prompt-only coding-agent skills to schema-based, executable, verifiable Agent Skill Bundles.

本仓库将面向 `Claude Code`、`Codex` 和 `OpenClaw` 的 prompt-only skills，升级为一个轻量级 `Agent Skill Bundle System`。每个 skill 现在都包含：

- `SKILL.md`
- `skill.yaml`
- JSON input/output schema
- lightweight runtime script
- declarative permission boundary
- benchmark test cases
- shared runner

## Why This Exists / 为什么要做这个项目

Prompt-only skills are easy to read but hard to verify, test, and reuse consistently.

纯 prompt 的 skill 虽然容易阅读，但很难稳定验证、测试和复用。

This project addresses the common failure modes that show up in AI coding-agent workflows:

- claimed completion without real verification
- long-context compression that loses user constraints or failed attempts
- multi-agent coordination that becomes ambiguous or unbounded
- memory workflows that store low-value, stale, or conflicting data
- proactive jobs that become unsafe without schedule, permission, and expiry controls

本项目针对 AI coding agent 常见失效模式进行结构化处理：

- 口头说“做完了”，但没有真实验证证据
- 长上下文压缩时丢失用户约束或失败尝试
- 多 Agent 协作时任务边界不清、容易失控
- memory 写入了低价值、过期或冲突数据
- proactive job 缺少 schedule、权限和过期控制，容易变得不安全

Prompt-only skills are easy to read but difficult to verify, test, and reuse reliably. This project upgrades each skill into a structured Agent Skill Bundle so that common AI coding-agent failure modes can be handled with explicit schemas, runtime contracts, permission boundaries, and benchmark cases.

纯 prompt 的 skill 容易写，但难以稳定验证、测试和复用。这个项目把每个 skill 升级为结构化 `Agent Skill Bundle`，通过显式 schema、runtime contract、权限边界和 benchmark case 来处理常见 AI coding-agent 失效模式。

## Why These Skills Matter / 为什么这 6 个 Skill 重要

| Skill | Problem Addressed |
|---|---|
| `verification-gate` | Prevents the agent from claiming a coding task is complete without test or verification evidence. |
| `structured-context-compressor` | Prevents important user constraints, failed attempts, current state, and next steps from being lost during long-context compression. |
| `swarm-coordinator` | Prevents multi-agent work from becoming unbounded or ambiguous by defining worker roles, handoff rules, acceptance criteria, and verification plans. |
| `memory-extractor` | Prevents short-lived task states, sensitive content, or low-value information from being written as long-term memory. |
| `dream-memory` | Prevents memory stores from accumulating duplicate, stale, expired, or conflicting memories without review. |
| `kairos-lite` | Prevents proactive jobs from becoming unsafe background tasks by requiring schedule, permission boundary, brief output, approval state, and expiry control. |

## Skill Overview / Skill 总览

| Skill | Lifecycle | Purpose |
|---|---|---|
| `verification-gate` | verification lifecycle | Checks whether an AI coding task is actually complete. |
| `structured-context-compressor` | context snapshot lifecycle | Produces a recoverable task snapshot for long sessions. |
| `swarm-coordinator` | coordination lifecycle | Generates a bounded multi-agent task plan. |
| `memory-extractor` | memory extract / classify / validate | Extracts and validates candidate memories. |
| `dream-memory` | memory merge / expire / retrieve | Merges, expires, and retrieves memories. |
| `kairos-lite` | proactive job lifecycle | Plans lightweight proactive jobs with permission and expiry controls. |

## Standard Skill Bundle Structure / 标准结构

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

## Usage / 使用方式

Single skill runtime:

```powershell
python tools/skill_runner.py skills/verification-gate skills/verification-gate/tests/cases/001-no-test-log.input.json
```

运行单个 skill：

```powershell
python tools/skill_runner.py skills/verification-gate skills/verification-gate/tests/cases/001-no-test-log.input.json
```

Batch test one skill:

```powershell
python tools/run_skill_tests.py skills/verification-gate
```

批量测试单个 skill：

```powershell
python tools/run_skill_tests.py skills/verification-gate
```

Run all engineered skills:

```powershell
python tools/run_all_skill_tests.py
```

运行全部工程化 skill：

```powershell
python tools/run_all_skill_tests.py
```

## Design Principles / 设计原则

- Backward compatible with existing `SKILL.md` usage / 保持原有 `SKILL.md` 使用方式兼容
- Schema-first input/output contracts / 以 schema 为先定义输入输出契约
- Lightweight local runtime scripts / 使用轻量级本地 runtime
- Declarative permission boundaries in `skill.yaml` / 在 `skill.yaml` 中声明权限边界
- Benchmark cases for every engineered skill / 每个工程化 skill 都配备 benchmark case
- No external LLM API required by runtime scripts / runtime 不依赖外部 LLM API
- No source-code modification unless explicitly allowed / 未明确允许时不修改源码
- No commit / push from skill runtime / skill runtime 不执行 commit 或 push

## Extension Ideas / 二开方向

- Connect `verification-gate` to a real CI pipeline as a PR precheck / 把 `verification-gate` 接到真实 CI，做 PR precheck
- Use `structured-context-compressor` as a session resume snapshot / 把 `structured-context-compressor` 用作会话恢复快照
- Plug `swarm-coordinator` into a real multi-agent runtime / 把 `swarm-coordinator` 接入真实多 Agent runtime
- Connect `memory-extractor` and `dream-memory` to a persistent memory store / 把 `memory-extractor` 和 `dream-memory` 接入真实 memory store
- Attach `kairos-lite` to an external scheduler while preserving permission and expiry controls / 把 `kairos-lite` 接到外部 scheduler，但保留权限和过期控制
- Add a web dashboard or TUI for skill test status / 增加 Web Dashboard 或 TUI 查看测试状态
- Add a skill registry or marketplace for discoverable bundles / 增加 skill registry 或 marketplace

## Project Boundary / 项目边界

This repository is not:

- a full agent runtime
- a background daemon
- a CI replacement
- a memory database
- a multi-agent executor

本仓库不是：

- 完整的 agent runtime
- 后台 daemon
- CI 替代品
- memory database
- 多 Agent 执行器

It is a lightweight Agent Skill Bundle System:

- schema + runtime + permission + verification + benchmark template

它是一个轻量级 `Agent Skill Bundle System`：

- `schema + runtime + permission + verification + benchmark` 模板

## Documentation / 文档

- [Skill Bundle Specification](docs/SKILL_BUNDLE_SPEC.md)
- [Project Overview](docs/PROJECT_OVERVIEW.md)
- [Release Checklist](docs/RELEASE_CHECKLIST.md)
