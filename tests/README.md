# 测试文件说明

## 核心测试文件

### test_verify_fields.py
验证涨停原因板块数据的字段映射是否正确。

**用途：** 确保所有字段都正确对齐

**运行：**
```bash
python tests/test_verify_fields.py
```

### test_limit_up_sectors.py
完整的涨停原因板块功能测试。

**用途：** 测试get_limit_up_sectors()函数的完整功能

**运行：**
```bash
python tests/test_limit_up_sectors.py
```

### test_new_high.py
百日新高数据功能测试。

**用途：** 测试get_new_high_data()函数的完整功能，包括单日查询、范围查询和数据分析

**运行：**
```bash
python tests/test_new_high.py
```

## 调试工具

### test_data_alignment.py
数据对齐调试工具，用于查看原始API返回的数据结构。

### test_field_mapping.py
字段映射分析工具，用于确认每个索引对应的字段含义。

### test_sector_direct.py
直接测试API请求，不经过爬虫类。

## 其他测试文件

其他test_*.py文件是开发过程中的测试文件，已归档保留。

## 运行所有测试

```bash
# 运行核心测试
python tests/test_verify_fields.py
python tests/test_limit_up_sectors.py

# 运行调试工具
python tests/test_data_alignment.py
python tests/test_field_mapping.py
```

## 测试数据

测试生成的数据文件保存在 `../data/` 目录中。
