# 梦境记忆

`dream-memory` 是本仓库记忆生命周期的后半段。

它会合并已有记忆和新候选项，处理重复、过期和检索相关内容，但不会写入真实记忆存储。

## 输出结构

```json
{
  "active_memories": [],
  "merged_memories": [],
  "expired_memories": [],
  "conflicts": [],
  "retrieved_memories": [],
  "summary": {
    "active_count": 0,
    "merged_count": 0,
    "expired_count": 0,
    "conflict_count": 0,
    "retrieved_count": 0
  }
}
```

## 使用方式

单个运行：

```powershell
python tools/skill_runner.py skills/dream-memory skills/dream-memory/tests/cases/001-merge-duplicates.input.json
```

批量测试：

```powershell
python tools/run_skill_tests.py skills/dream-memory
```

## 安全边界

- 合并重复项，而不是静默复制
- 让过期项失效，而不是永久保留
- 检测冲突，而不是静默覆盖
- 不修改源码

<details>
<summary>English</summary>

# dream-memory

`dream-memory` is the second half of the Memory Lifecycle in this repository.

It consolidates existing memories and new candidates by merging duplicates, expiring stale items, and retrieving relevant memories. It does not write to a real memory store.

## Output Shape

```json
{
  "active_memories": [],
  "merged_memories": [],
  "expired_memories": [],
  "conflicts": [],
  "retrieved_memories": [],
  "summary": {
    "active_count": 0,
    "merged_count": 0,
    "expired_count": 0,
    "conflict_count": 0,
    "retrieved_count": 0
  }
}
```

## Usage

Single run:

```powershell
python tools/skill_runner.py skills/dream-memory skills/dream-memory/tests/cases/001-merge-duplicates.input.json
```

Batch tests:

```powershell
python tools/run_skill_tests.py skills/dream-memory
```

## Safety Boundary

- merge duplicates instead of silently copying them
- expire stale items instead of keeping them forever
- detect conflicts instead of overwriting them
- do not modify source code

</details>
