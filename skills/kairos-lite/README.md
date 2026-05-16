# kairos-lite / 轻量主动任务

`kairos-lite` is the proactive job lifecycle sample for this repository.

`kairos-lite` 是本仓库的 proactive job lifecycle 样例。

It plans lightweight proactive jobs with schedule, permission boundary, draft/brief output, and expiry control. It is not a background daemon and does not actually execute jobs.

它会规划轻量 proactive job，并提供 schedule、权限边界、draft/brief 输出和 expiry 控制。但它不是后台 daemon，也不会真正执行任务。

## Output Shape / 输出结构

The runtime emits JSON with:

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

runtime 输出的 JSON 包含：

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

## Usage / 使用方式

Single run:

```powershell
python tools/skill_runner.py skills/kairos-lite skills/kairos-lite/tests/cases/001-observe-job.input.json
```

单个运行：

```powershell
python tools/skill_runner.py skills/kairos-lite skills/kairos-lite/tests/cases/001-observe-job.input.json
```

Batch tests:

```powershell
python tools/run_skill_tests.py skills/kairos-lite
```

批量测试：

```powershell
python tools/run_skill_tests.py skills/kairos-lite
```

## Safety Boundary / 安全边界

- no infinite background jobs / 不创建无限后台任务
- no execution without authorization / 没有授权时不执行
- no source-code modification / 不修改源码
- no shell execution, commit, or push / 不执行 shell，不 commit，不 push

