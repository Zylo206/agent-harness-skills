# structured-context-compressor / 结构化上下文压缩器

`structured-context-compressor` is the context snapshot lifecycle sample for this repository.

`structured-context-compressor` 是本仓库的 context snapshot lifecycle 样例。

It turns long conversation history into a structured task snapshot so future runs can resume without losing constraints, failed attempts, or next steps.

它会把长对话历史整理成结构化 task snapshot，方便后续恢复，并尽量保留约束、失败尝试和下一步。

## Output Shape / 输出结构

The runtime emits a JSON snapshot with:

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

runtime 输出的 JSON snapshot 包含：

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

## Usage / 使用方式

Single run:

```powershell
python tools/skill_runner.py skills/structured-context-compressor skills/structured-context-compressor/tests/cases/001-basic-task.input.json
```

单个运行：

```powershell
python tools/skill_runner.py skills/structured-context-compressor skills/structured-context-compressor/tests/cases/001-basic-task.input.json
```

Batch tests:

```powershell
python tools/run_skill_tests.py skills/structured-context-compressor
```

批量测试：

```powershell
python tools/run_skill_tests.py skills/structured-context-compressor
```

## Safety Boundary / 安全边界

- preserve user constraints and failed attempts / 保留用户约束和失败尝试
- do not invent missing technical facts / 不臆造不存在的技术事实
- do not modify source code / 不修改源码
- do not execute shell commands / 不执行 shell 命令

