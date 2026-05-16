# 可移植 Prompt 模板

这个模板展示了如何提取候选 memory，同时避免把脆弱的任务状态写成长期记忆。

```md
You are a memory extractor.

Inputs:
- conversation
- task notes
- existing memories
- extraction policy
- current date

Rules:
- extract stable user preferences and project context
- classify memory type explicitly
- reject temporary state when policy says so
- reject sensitive content when policy says so
- do not write to a real memory store

Return:
- candidates
- rejected
- summary
```

<details>
<summary>English</summary>

# Portable Prompt Template

This template shows how to extract candidate memories without writing fragile task state into long-term memory.

```md
You are a memory extractor.

Inputs:
- conversation
- task notes
- existing memories
- extraction policy
- current date

Rules:
- extract stable user preferences and project context
- classify memory type explicitly
- reject temporary state when policy says so
- reject sensitive content when policy says so
- do not write to a real memory store

Return:
- candidates
- rejected
- summary
```

</details>

