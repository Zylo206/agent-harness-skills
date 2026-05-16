# 轻量主动任务

`kairos-lite` 是本仓库的主动任务生命周期样例。

它会规划轻量主动任务，并提供调度、权限边界、摘要输出和过期控制。但它不是后台守护进程，也不会真正执行任务。

## 输出结构

```json
{
  "job_goal": "",
  "job_status": "PLANNED",
  "lifecycle_stage": "schedule",
  "schedule": {},
  "permission_level": "observe",
  "allowed_actions": [],
  "forbidden_actions": [],
  "requires_user_approval": true,
  "execution_mode": "plan_only",
  "job_plan": [],
  "brief": "",
  "expiry": "",
  "is_expired": false,
  "risks": [],
  "next_step": ""
}
```

## 使用方式

单个运行：

```powershell
python tools/skill_runner.py skills/kairos-lite skills/kairos-lite/tests/cases/001-observe-job.input.json
```

批量测试：

```powershell
python tools/run_skill_tests.py skills/kairos-lite
```

## 安全边界

- 不创建无限后台任务
- 没有授权时不执行
- 不修改源码
- 不执行 shell，不 commit，不 push

<details>
<summary>English</summary>

# kairos-lite

`kairos-lite` is the proactive job lifecycle sample for this repository.

It plans lightweight proactive jobs with schedule, permission boundary, draft/brief output, and expiry control. It is not a background daemon and does not actually execute jobs.

## Output Shape

```json
{
  "job_goal": "",
  "job_status": "PLANNED",
  "lifecycle_stage": "schedule",
  "schedule": {},
  "permission_level": "observe",
  "allowed_actions": [],
  "forbidden_actions": [],
  "requires_user_approval": true,
  "execution_mode": "plan_only",
  "job_plan": [],
  "brief": "",
  "expiry": "",
  "is_expired": false,
  "risks": [],
  "next_step": ""
}
```

## Usage

Single run:

```powershell
python tools/skill_runner.py skills/kairos-lite skills/kairos-lite/tests/cases/001-observe-job.input.json
```

Batch tests:

```powershell
python tools/run_skill_tests.py skills/kairos-lite
```

## Safety Boundary

- no infinite background jobs
- no execution without authorization
- no source-code modification
- no shell execution, commit, or push

</details>
