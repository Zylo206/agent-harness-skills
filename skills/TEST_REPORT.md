# Smoke Test Report / 烟雾测试报告

Date: April 1, 2026

日期：2026-04-01

Scope:

- `dream-memory`
- `memory-extractor`
- `verification-gate`
- `swarm-coordinator`
- `structured-context-compressor`
- `kairos-lite`

范围：

- `dream-memory`
- `memory-extractor`
- `verification-gate`
- `swarm-coordinator`
- `structured-context-compressor`
- `kairos-lite`

## Summary / 总结

- Bundle structure checks: passed
- Python helper script compilation: passed
- Claude Code skill availability: passed for all six
- OpenClaw skill availability: passed for all six
- Codex skill availability: blocked by runtime authentication in the local environment

- Bundle structure 检查：通过
- Python helper script 编译：通过
- Claude Code skill 可用性：6 个全部通过
- OpenClaw skill 可用性：6 个全部通过
- Codex skill 可用性：受本地运行时认证限制而阻塞

## Commands Run / 运行命令

Bundle checks:

```bash
bash ./skills/check_all.sh
python3 -m py_compile \
  skills/dream-memory/scripts/dream_memory.py \
  skills/memory-extractor/scripts/memory_manifest.py \
  skills/verification-gate/scripts/verification_context.py \
  skills/swarm-coordinator/scripts/task_board.py \
  skills/structured-context-compressor/scripts/render_template.py \
  skills/kairos-lite/scripts/job_spec.py
```

Bundle 检查：

```bash
bash ./skills/check_all.sh
python3 -m py_compile \
  skills/dream-memory/scripts/dream_memory.py \
  skills/memory-extractor/scripts/memory_manifest.py \
  skills/verification-gate/scripts/verification_context.py \
  skills/swarm-coordinator/scripts/task_board.py \
  skills/structured-context-compressor/scripts/render_template.py \
  skills/kairos-lite/scripts/job_spec.py
```

Claude Code availability test:

```bash
printf 'Use /dream-memory and reply AVAILABLE or UNAVAILABLE only.\n' \
  | claude -p --model sonnet --setting-sources user,project,local --allowedTools Read,Grep,Glob
```

Claude Code 可用性测试：

```bash
printf 'Use /dream-memory and reply AVAILABLE or UNAVAILABLE only.\n' \
  | claude -p --model sonnet --setting-sources user,project,local --allowedTools Read,Grep,Glob
```

The same pattern was run for all six skills.

同样的方式也用于另外五个 skill。

OpenClaw availability test:

```bash
openclaw skills info dream-memory
```

OpenClaw 可用性测试：

```bash
openclaw skills info dream-memory
```

The same pattern was run for all six skills.

同样的方式也用于另外五个 skill。

Codex isolated smoke test:

```bash
HOME="$tmp/home" CODEX_HOME="$tmp/codex-home" \
  codex exec --skip-git-repo-check --sandbox read-only --model gpt-5 --cd "$tmp" \
  'Use /dream-memory. Reply AVAILABLE or UNAVAILABLE only.'
```

Codex 隔离 smoke test：

```bash
HOME="$tmp/home" CODEX_HOME="$tmp/codex-home" \
  codex exec --skip-git-repo-check --sandbox read-only --model gpt-5 --cd "$tmp" \
  'Use /dream-memory. Reply AVAILABLE or UNAVAILABLE only.'
```

## Results / 结果

### Bundle Checks / Bundle 检查

`bash ./skills/check_all.sh` returned:

```text
All skill bundles passed basic checks.
```

`bash ./skills/check_all.sh` 的结果：

```text
All skill bundles passed basic checks.
```

### Claude Code

All six skills returned `AVAILABLE` when invoked through `claude -p` after installation into `~/.claude/skills`.

通过 `claude -p` 调用并安装到 `~/.claude/skills` 后，6 个 skill 都返回了 `AVAILABLE`。

### OpenClaw

All six skills returned `Ready` from `openclaw skills info <slug>` after installation into `~/.openclaw/workspace/skills`.

安装到 `~/.openclaw/workspace/skills` 后，`openclaw skills info <slug>` 对 6 个 skill 都返回了 `Ready`。

Observed note:

- the local OpenClaw environment emits repeated `Skipping skill path that resolves outside its configured root.` warnings while scanning other workspace-linked skills
- those warnings did not block any of the six tested skills from resolving as `Ready`

观察到的情况：

- 本地 OpenClaw 环境在扫描其他 workspace-linked skills 时，会重复输出 `Skipping skill path that resolves outside its configured root.` 警告
- 这些警告没有阻止 6 个被测试 skill 正常解析为 `Ready`

### Codex

The initial local test was blocked by unrelated malformed installed skills outside this repo.

第一次本地测试被仓库外部的损坏 installed skills 阻塞。

A second isolated test used a temporary `HOME` and `CODEX_HOME` containing only the six skill bundles. That removed the unrelated skill parsing issue, but the request still failed because the local Codex runtime could not authenticate to the OpenAI Responses API:

第二次隔离测试使用临时的 `HOME` 和 `CODEX_HOME`，只放入这 6 个 skill bundle。这样消除了无关 skill 的解析问题，但本地 Codex runtime 仍然因为无法认证 OpenAI Responses API 而失败：

```text
ERROR: unexpected status 401 Unauthorized: Missing bearer or basic authentication in header
```

Interpretation:

- bundle loading is no longer blocked by foreign skills once `HOME` and `CODEX_HOME` are isolated
- end-to-end Codex invocation remains unverified in this environment until valid local auth is configured

解释：

- 一旦隔离 `HOME` 和 `CODEX_HOME`，bundle 加载就不再被外部 skill 阻塞
- 在配置有效的本地认证前，这个环境里的 Codex 端到端调用仍未验证

## Release Readiness / 发布就绪度

Current release recommendation:

- safe to publish for `Claude Code` and `OpenClaw`
- publish for `Codex` with an explicit note that local smoke verification is still pending valid auth
- do not claim full three-host runtime verification in the release notes until the Codex auth issue is cleared

当前发布建议：

- 对 `Claude Code` 和 `OpenClaw` 来说已可以发布
- 对 `Codex` 可以发布，但需要明确说明本地 smoke 验证仍在等待有效认证
- 在 Codex 认证问题解决前，不要在 release notes 中声称已经完成三端完整 runtime 验证

