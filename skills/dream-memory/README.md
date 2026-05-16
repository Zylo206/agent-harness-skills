# dream-memory / 梦境记忆

`dream-memory` is the second half of the Memory Lifecycle in this repository.

`dream-memory` 是本仓库 Memory Lifecycle 的后半段。

It consolidates existing memories and new candidates by merging duplicates, expiring stale items, and retrieving relevant memories. It does not write to a real memory store.

它会合并已有 memory 和新候选项，处理重复、过期和检索相关内容，但不会写入真实 memory store。

## Output Shape / 输出结构

The runtime emits JSON with:

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

runtime 输出的 JSON 包含：

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

## Usage / 使用方式

Single run:

```powershell
python tools/skill_runner.py skills/dream-memory skills/dream-memory/tests/cases/001-merge-duplicates.input.json
```

单个运行：

```powershell
python tools/skill_runner.py skills/dream-memory skills/dream-memory/tests/cases/001-merge-duplicates.input.json
```

Batch tests:

```powershell
python tools/run_skill_tests.py skills/dream-memory
```

批量测试：

```powershell
python tools/run_skill_tests.py skills/dream-memory
```

## Safety Boundary / 安全边界

- merge duplicates instead of silently copying them / 合并重复项，而不是静默复制
- expire stale items instead of keeping them forever / 让过期项失效，而不是永久保留
- detect conflicts instead of overwriting them / 检测冲突，而不是静默覆盖
- do not modify source code / 不修改源码

