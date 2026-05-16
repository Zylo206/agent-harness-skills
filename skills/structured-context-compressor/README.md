# 结构化上下文压缩器

`structured-context-compressor` 是本仓库的上下文快照生命周期样例。

它会把长对话历史整理成结构化任务快照，方便后续恢复，并尽量保留约束、失败尝试和下一步。

## 输出结构

```json
{
  "primary_request": "",
  "user_constraints": [],
  "technical_context": [],
  "files_and_artifacts": [],
  "completed_work": [],
  "failed_attempts": [],
  "do_not_repeat": [],
  "pending_tasks": [],
  "current_state": "",
  "next_step": ""
}
```

## 使用方式

单个运行：

```powershell
python tools/skill_runner.py skills/structured-context-compressor skills/structured-context-compressor/tests/cases/001-basic-task.input.json
```

批量测试：

```powershell
python tools/run_skill_tests.py skills/structured-context-compressor
```

## 安全边界

- 保留用户约束和失败尝试
- 不臆造不存在的技术事实
- 不修改源码
- 不执行 shell 命令

<details>
<summary>English</summary>

# structured-context-compressor

`structured-context-compressor` is the context snapshot lifecycle sample for this repository.

It turns long conversation history into a structured task snapshot so future runs can resume without losing constraints, failed attempts, or next steps.

## Output Shape

```json
{
  "primary_request": "",
  "user_constraints": [],
  "technical_context": [],
  "files_and_artifacts": [],
  "completed_work": [],
  "failed_attempts": [],
  "do_not_repeat": [],
  "pending_tasks": [],
  "current_state": "",
  "next_step": ""
}
```

## Usage

Single run:

```powershell
python tools/skill_runner.py skills/structured-context-compressor skills/structured-context-compressor/tests/cases/001-basic-task.input.json
```

Batch tests:

```powershell
python tools/run_skill_tests.py skills/structured-context-compressor
```

## Safety Boundary

- preserve user constraints and failed attempts
- do not invent missing technical facts
- do not modify source code
- do not execute shell commands

</details>
