# 发布检查清单

## 发布前验证

- 运行全部 skill 测试：

```powershell
python tools/run_all_skill_tests.py
```

- 需要时单独运行某个 skill 的测试：

```powershell
python tools/run_skill_tests.py skills/verification-gate
python tools/run_skill_tests.py skills/structured-context-compressor
python tools/run_skill_tests.py skills/swarm-coordinator
python tools/run_skill_tests.py skills/memory-extractor
python tools/run_skill_tests.py skills/dream-memory
python tools/run_skill_tests.py skills/kairos-lite
```

<details>
<summary>English</summary>

- Run all skill tests:

```powershell
python tools/run_all_skill_tests.py
```

- Run individual skill tests when necessary:

```powershell
python tools/run_skill_tests.py skills/verification-gate
python tools/run_skill_tests.py skills/structured-context-compressor
python tools/run_skill_tests.py skills/swarm-coordinator
python tools/run_skill_tests.py skills/memory-extractor
python tools/run_skill_tests.py skills/dream-memory
python tools/run_skill_tests.py skills/kairos-lite
```

</details>

## Schema 校验

确保每个工程化 skill 都包含：

- `skill.yaml`
- `schemas/input.schema.json`
- `schemas/output.schema.json`
- `scripts/run.py`
- `tests/cases`
- `tests/expected`

<details>
<summary>English</summary>

Ensure every engineered skill has:

- `skill.yaml`
- `schemas/input.schema.json`
- `schemas/output.schema.json`
- `scripts/run.py`
- `tests/cases`
- `tests/expected`

</details>

## 向后兼容

- 每个 skill 目录都要保留 `SKILL.md`
- README 文字要和当前 runtime 行为一致
- 不要破坏现有 Claude Code / Codex / OpenClaw 的 skill 使用方式

<details>
<summary>English</summary>

- Keep `SKILL.md` in every skill directory
- Keep README wording aligned with the current runtime behavior
- Do not break existing Claude Code / Codex / OpenClaw skill usage

</details>

## 安全与权限审查

- 检查 `skill.yaml` 中的 permissions
- 相关场景下确保 forbidden actions 包含危险操作
- 确保 runtime 脚本不会在未明确允许时 commit、push、删除文件或修改源码

<details>
<summary>English</summary>

- Check `skill.yaml` permissions
- Ensure forbidden actions include dangerous operations where relevant
- Ensure runtime scripts do not commit, push, delete files, or modify source unless explicitly allowed

</details>

## 文档审查

- 根目录 `README.md` 已更新
- 各 skill 的 README 已更新
- `docs/SKILL_BUNDLE_SPEC.md` 已更新
- 示例命令与实际行为一致

<details>
<summary>English</summary>

- Root `README.md` updated
- Skill README files updated
- `docs/SKILL_BUNDLE_SPEC.md` updated
- Examples still match actual commands

</details>

## 版本管理

- 当行为变化时更新 `skill.yaml` 版本号
- 在 release notes 中提到修改过的 skills

<details>
<summary>English</summary>

- Update `skill.yaml` version when behavior changes
- Mention modified skills in release notes

</details>

## 已知限制

- Runtime 脚本是轻量级、基于规则的
- 权限模型是声明式的，不是沙箱
- Benchmark case 只是 smoke test，不是完整评估
- 默认不会调用外部 LLM API

<details>
<summary>English</summary>

- Runtime scripts are lightweight and rule-based
- Permission model is declarative, not a sandbox
- Benchmark cases are smoke tests, not full evaluations
- No external LLM API is called by default

</details>

