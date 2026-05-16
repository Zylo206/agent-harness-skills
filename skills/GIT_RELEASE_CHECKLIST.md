# Git 和发布检查清单

把这个文件作为 `v0.1.0` 的最终发布前检查清单。

## 推荐提交信息

短提交标题：

```text
release: prepare v0.1.0 CC harness skill pack
```

较长提交说明：

```text
release: prepare v0.1.0 CC harness skill pack

- add public repo homepage for the portable skill pack
- add per-skill READMEs for all six bundles
- add release plan, GitHub release copy, and ClawHub listing copy
- add smoke-test report for Claude Code and OpenClaw
- document Codex runtime auth as the remaining verification blocker
```

<details>
<summary>English</summary>

# Git And Release Checklist

Use this file as the final pre-publish checklist for `v0.1.0`.

## Recommended Commit Message

Short commit title:

```text
release: prepare v0.1.0 CC harness skill pack
```

Longer commit body:

```text
release: prepare v0.1.0 CC harness skill pack

- add public repo homepage for the portable skill pack
- add per-skill READMEs for all six bundles
- add release plan, GitHub release copy, and ClawHub listing copy
- add smoke-test report for Claude Code and OpenClaw
- document Codex runtime auth as the remaining verification blocker
```

</details>

## 提交前检查

运行：

```bash
bash ./skills/check_all.sh
```

确认：

- [ ] 6 个 bundle 都包含 `SKILL.md`、`README.md`、`references/` 和 `scripts/`
- [ ] `TEST_REPORT.md` 是最新的
- [ ] `RELEASE_PLAN.md` 与预期发布顺序一致
- [ ] 没有把本地 token、临时安装文件或私有配置文件加入 git

<details>
<summary>English</summary>

## Pre-Commit Check

Run:

```bash
bash ./skills/check_all.sh
```

Confirm:

- [ ] the six bundles each contain `SKILL.md`, `README.md`, `references/`, and `scripts/`
- [ ] `TEST_REPORT.md` is current
- [ ] `RELEASE_PLAN.md` matches the intended release order
- [ ] no local tokens, temp installs, or private config files were added to git

</details>

## Git 步骤

```bash
git status
git add README.md .gitignore skills
git commit -m "release: prepare v0.1.0 CC harness skill pack"
git tag -a v0.1.0 -m "First Portable CC Harness Skills"
```

<details>
<summary>English</summary>

## Git Steps

```bash
git status
git add README.md .gitignore skills
git commit -m "release: prepare v0.1.0 CC harness skill pack"
git tag -a v0.1.0 -m "First Portable CC Harness Skills"
```

</details>

## GitHub Release 步骤

1. Push branch and tag.
2. Create release `v0.1.0`.
3. Use title: `v0.1.0: First Portable CC Harness Skills`
4. Paste body from `GITHUB_RELEASE_v0.1.0.md`
5. Add topics from `RELEASE_PLAN.md`

<details>
<summary>English</summary>

## GitHub Release Steps

1. Push branch and tag.
2. Create release `v0.1.0`.
3. Use title: `v0.1.0: First Portable CC Harness Skills`
4. Paste body from `GITHUB_RELEASE_v0.1.0.md`
5. Add topics from `RELEASE_PLAN.md`

</details>

## ClawHub 发布步骤

按以下顺序发布：

1. `dream-memory`
2. `memory-extractor`
3. `structured-context-compressor`
4. `verification-gate`
5. `swarm-coordinator`
6. `kairos-lite`

批量发布命令：

```bash
bash ./skills/publish_all.sh 0.1.0
```

<details>
<summary>English</summary>

## ClawHub Release Steps

Publish in this order:

1. `dream-memory`
2. `memory-extractor`
3. `structured-context-compressor`
4. `verification-gate`
5. `swarm-coordinator`
6. `kairos-lite`

Batch publish command:

```bash
bash ./skills/publish_all.sh 0.1.0
```

</details>

## 最终发布门槛

只有在 `Codex` 认证问题解决并重新运行 smoke test 之后，才可以说这次发布已经在三端完全验证。

<details>
<summary>English</summary>

## Final Release Gate

Only say the release is fully verified across all three hosts if the `Codex` auth issue has been resolved and the smoke test has been rerun.

</details>

