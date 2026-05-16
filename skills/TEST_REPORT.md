# 烟雾测试报告

日期：2026-04-01

范围：

- `dream-memory`
- `memory-extractor`
- `verification-gate`
- `swarm-coordinator`
- `structured-context-compressor`
- `kairos-lite`

## 总结

- Bundle structure 检查：通过
- Python helper script 编译：通过
- Claude Code skill 可用性：6 个全部通过
- OpenClaw skill 可用性：6 个全部通过
- Codex skill 可用性：受本地运行时认证限制而阻塞

## 运行命令

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

Claude Code availability test:

```bash
printf 'Use /dream-memory and reply AVAILABLE or UNAVAILABLE only.\n' \
  | claude -p --model sonnet --setting-sources user,project,local --allowedTools Read,Grep,Glob
```

OpenClaw availability test:

```bash
openclaw skills info dream-memory
```

Codex isolated smoke test:

```bash
HOME="$tmp/home" CODEX_HOME="$tmp/codex-home" \
  codex exec --skip-git-repo-check --sandbox read-only --model gpt-5 --cd "$tmp" \
  'Use /dream-memory. Reply AVAILABLE or UNAVAILABLE only.'
```

<details>
<summary>English</summary>

# Smoke Test Report

Date: April 1, 2026

Scope:

- `dream-memory`
- `memory-extractor`
- `verification-gate`
- `swarm-coordinator`
- `structured-context-compressor`
- `kairos-lite`

## Summary

- Bundle structure checks: passed
- Python helper script compilation: passed
- Claude Code skill availability: passed for all six
- OpenClaw skill availability: passed for all six
- Codex skill availability: blocked by runtime authentication in the local environment

## Commands Run

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

Claude Code availability test:

```bash
printf 'Use /dream-memory and reply AVAILABLE or UNAVAILABLE only.\n' \
  | claude -p --model sonnet --setting-sources user,project,local --allowedTools Read,Grep,Glob
```

OpenClaw availability test:

```bash
openclaw skills info dream-memory
```

Codex isolated smoke test:

```bash
HOME="$tmp/home" CODEX_HOME="$tmp/codex-home" \
  codex exec --skip-git-repo-check --sandbox read-only --model gpt-5 --cd "$tmp" \
  'Use /dream-memory. Reply AVAILABLE or UNAVAILABLE only.'
```

</details>

