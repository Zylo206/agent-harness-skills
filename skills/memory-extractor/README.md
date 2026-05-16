# 记忆提取器

`memory-extractor` 是本仓库记忆生命周期的前半段。

它会从对话和笔记中提取候选记忆，进行分类和校验，但不会写入真实记忆存储。

## 输出结构

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

## 使用方式

单个运行：

```powershell
python tools/skill_runner.py skills/memory-extractor skills/memory-extractor/tests/cases/001-user-preference.input.json
```

批量测试：

```powershell
python tools/run_skill_tests.py skills/memory-extractor
```

## 安全边界

- 当策略要求时拒绝临时状态
- 当策略要求时拒绝敏感内容
- 不修改源码
- 不写入真实记忆存储

<details>
<summary>English</summary>

# memory-extractor

`memory-extractor` is the first half of the Memory Lifecycle in this repository.

It extracts candidate memories from conversation and notes, classifies them, and validates whether they should be kept. It does not write to a real memory store.

## Output Shape

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

## Usage

Single run:

```powershell
python tools/skill_runner.py skills/memory-extractor skills/memory-extractor/tests/cases/001-user-preference.input.json
```

Batch tests:

```powershell
python tools/run_skill_tests.py skills/memory-extractor
```

## Safety Boundary

- reject temporary state when policy says so
- reject sensitive content when policy says so
- do not modify source code
- do not write to real memory stores

</details>
