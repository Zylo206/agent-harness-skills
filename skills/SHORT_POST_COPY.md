# 短帖文案

适合发一篇短图文时直接引用。

## 总标题

我把一套从 `CC` coding-agent 工程里提炼出来的 6 个 Skill，整理成了可公开下载的跨宿主版本。

支持方向：

- 记忆整理
- 偏好提取
- 上下文压缩
- 完成后验证
- 多 Agent 编排
- 轻量主动模式

GitHub：

- `LearnPrompt/agent-harness-skills`

## 六个 Skill 的一句话用法和好处

### `CC Dream Memory`

用法：当对话和记忆文件越堆越乱时，用它把最近会话、日志和旧记忆合并成一份短小稳定的长期记忆。

好处：让 agent 记住真正长期有效的东西，而不是被过期信息和重复笔记拖垮。

### `CC Memory Extractor`

用法：当一轮协作结束后，用它从最近对话里提取用户偏好、反馈、项目约束和参考资料。

好处：把“这个人喜欢怎么合作”沉淀下来，下次不用重新磨合。

### `CC Context Compressor`

用法：当会话太长、准备切上下文或交给别的 agent 时，用它把当前进展压成 9 段式结构化摘要。

好处：最大限度保留用户原话、关键文件、错误和下一步，减少压缩后跑偏。

### `CC Verification Gate`

用法：当任务看起来已经做完时，用它再拉一轮只读验证视角，专门检查“是不是真的完成了”。

好处：减少 AI 假装完成、没跑验证却说通过、漏边界条件这类常见问题。

### `CC Swarm Coordinator`

用法：当任务太大、太杂、跨很多文件时，用它把工作拆成 research、implementation、verification 几个边界清楚的 worker。

好处：让多 Agent 协作更像一个有组织的团队，而不是一堆互相污染上下文的并发请求。

### `CC Kairos Lite`

用法：当你想让 agent 做轻量主动检查、后续跟进或生成简报时，用它先定义 schedule、权限、brief 和过期时间。

好处：先拿到主动模式的收益，但不需要一上来就做一个危险的常驻 daemon。

## 这是怎么工作的

我把 prompt-only 的 AI coding-agent 技能包，整理成了 `schema + runtime + permission + verification + benchmark` 的轻量级 `Agent Skill Bundle System`。

<details>
<summary>Click to expand English version</summary>

## Headline

I turned a set of 6 skills distilled from a `CC` coding-agent codebase into a portable release for multiple hosts.

Supported areas:

- memory organization
- preference extraction
- context compression
- post-change verification
- multi-agent coordination
- lightweight proactive workflows

GitHub:

- `LearnPrompt/agent-harness-skills`

### One-line usage and benefit for each skill

#### `CC Dream Memory`

Use it when conversation logs and memory files get messy, and you want to merge recent sessions, logs, and old memory into a short stable long-term memory.

Benefit: keeps the agent focused on genuinely durable information instead of stale data and duplicate notes.

#### `CC Memory Extractor`

Use it after a collaboration round to extract user preferences, feedback, project constraints, and references from recent turns.

Benefit: preserves how the person likes to work so you do not have to relearn it every time.

#### `CC Context Compressor`

Use it when the conversation gets too long and you need to hand it off or resume later with a structured 9-part snapshot.

Benefit: preserves user wording, key files, errors, and next steps so compression does not derail the task.

#### `CC Verification Gate`

Use it when a task looks done and you want a read-only second pass focused on whether it is actually complete.

Benefit: reduces fake completion claims, skipped validation, and missed edge cases.

#### `CC Swarm Coordinator`

Use it when a task is large, messy, or spans many files, and you want to split it into bounded research, implementation, and verification workers.

Benefit: keeps multi-agent coordination organized instead of turning the context into noise.

#### `CC Kairos Lite`

Use it when you want lightweight proactive checks, follow-ups, or briefs, but need schedule, permission, and expiry control first.

Benefit: gets you the value of proactive behavior without building a dangerous always-on daemon.

### How it works

I reorganized prompt-only AI coding-agent skills into a lightweight `Agent Skill Bundle System` with `schema + runtime + permission + verification + benchmark`.

</details>
