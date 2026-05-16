# memory-extractor / 记忆提取器

`memory-extractor` is the first half of the Memory Lifecycle in this repository.

`memory-extractor` 是本仓库 Memory Lifecycle 的前半段。

It extracts candidate memories from conversation and notes, classifies them, and validates whether they should be kept. It does not write to a real memory store.

它会从对话和笔记中提取候选 memory，进行分类和校验，但不会写入真实 memory store。

## Output Shape / 输出结构

The runtime emits JSON with:

```json
{
  "candidates": [],
  "rejected": [],
  "summary": {
    "extracted_count": 0,
    "rejected_count": 0,
    "policy_notes": []
  }
}
```

runtime 输出的 JSON 包含：

```json
{
  "candidates": [],
  "rejected": [],
  "summary": {
    "extracted_count": 0,
    "rejected_count": 0,
    "policy_notes": []
  }
}
```

## Usage / 使用方式

Single run:

```powershell
python tools/skill_runner.py skills/memory-extractor skills/memory-extractor/tests/cases/001-user-preference.input.json
```

单个运行：

```powershell
python tools/skill_runner.py skills/memory-extractor skills/memory-extractor/tests/cases/001-user-preference.input.json
```

Batch tests:

```powershell
python tools/run_skill_tests.py skills/memory-extractor
```

批量测试：

```powershell
python tools/run_skill_tests.py skills/memory-extractor
```

## Safety Boundary / 安全边界

- reject temporary state when policy says so / 当策略要求时拒绝临时状态
- reject sensitive content when policy says so / 当策略要求时拒绝敏感内容
- do not modify source code / 不修改源码
- do not write to real memory stores / 不写入真实 memory store

