# swarm-coordinator / 多 Agent 协调器

`swarm-coordinator` 是本仓库的 coordination lifecycle 样例。

它会生成结构化的多 Agent 任务计划，包括有边界的 worker、交接规则、验收标准和验证计划，但不会真的启动并行 agent。

## 输出结构

```json
{
  "goal": "",
  "task_state": "PLANNED",
  "workers": [],
  "handoff_rules": [],
  "shared_context": [],
  "acceptance_criteria": [],
  "verification_required": true,
  "verification_plan": [],
  "risks": [],
  "next_step": ""
}
```

## 使用方式

单个运行：

```powershell
python tools/skill_runner.py skills/swarm-coordinator skills/swarm-coordinator/tests/cases/001-basic-plan.input.json
```

批量测试：

```powershell
python tools/run_skill_tests.py skills/swarm-coordinator
```

## 安全边界

- 保持 worker 计划有边界
- 保持交接规则明确
- 不执行 shell 命令
- 不修改源码

<details>
<summary>English</summary>

# swarm-coordinator

`swarm-coordinator` is the coordination lifecycle sample for this repository.

It generates a structured multi-agent task plan with bounded workers, handoff rules, acceptance criteria, and a verification plan. It does not actually launch parallel agents.

## Output Shape

```json
{
  "goal": "",
  "task_state": "PLANNED",
  "workers": [],
  "handoff_rules": [],
  "shared_context": [],
  "acceptance_criteria": [],
  "verification_required": true,
  "verification_plan": [],
  "risks": [],
  "next_step": ""
}
```

## Usage

Single run:

```powershell
python tools/skill_runner.py skills/swarm-coordinator skills/swarm-coordinator/tests/cases/001-basic-plan.input.json
```

Batch tests:

```powershell
python tools/run_skill_tests.py skills/swarm-coordinator
```

## Safety Boundary

- keep worker plans bounded
- keep handoff rules explicit
- do not execute shell commands
- do not modify source code

</details>

