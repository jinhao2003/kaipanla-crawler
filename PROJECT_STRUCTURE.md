# 项目结构说明

## 目录结构

```
kaipanla_crawler/
│
├── kaipanla_crawler.py          # 主爬虫模块（核心代码）
├── __init__.py                   # 包初始化文件
├── README.md                     # 项目主文档
├── PROJECT_STRUCTURE.md          # 本文件（项目结构说明）
│
├── examples/                     # 示例代码目录
│   ├── example_basic.py          # 基础使用示例
│   └── example_limit_up_analysis.py  # 涨停板块分析示例
│
├── tests/                        # 测试文件目录
│   ├── README.md                 # 测试说明文档
│   ├── test_verify_fields.py    # 字段验证测试（推荐）
│   ├── test_limit_up_sectors.py # 涨停板块功能测试（推荐）
│   ├── test_data_alignment.py   # 数据对齐调试工具
│   ├── test_field_mapping.py    # 字段映射分析工具
│   └── test_*.py                 # 其他测试文件
│
├── docs/                         # 文档目录
│   ├── README_LIMIT_UP_SECTORS.md      # 涨停原因板块功能文档
│   └── SUMMARY_涨停原因板块功能.md     # 功能实现总结
│
├── data/                         # 数据文件目录
│   ├── *.json                    # JSON数据文件
│   └── *.csv                     # CSV数据文件
│
├── archive/                      # 历史版本归档
│   ├── kaipanla_crawler_old.py  # 旧版本爬虫
│   ├── kaipanla_crawler_v2.py   # V2版本
│   └── *.py                      # 其他历史文件
│
└── .kiro/                        # Kiro配置目录
    └── specs/                    # 规格说明
```

## 核心文件说明

### kaipanla_crawler.py
主爬虫模块，包含所有核心功能：
- `get_daily_data()` - 获取市场行情数据
- `get_sector_ranking()` - 获取板块排行
- `get_limit_up_sectors()` - 获取涨停原因板块
- 其他辅助功能

### __init__.py
包初始化文件，定义导出的类和函数。

## 目录说明

### examples/ - 示例代码
包含各种使用示例，帮助快速上手：
- `example_basic.py` - 基础功能演示
- `example_limit_up_analysis.py` - 涨停板块分析

### tests/ - 测试文件
包含所有测试代码：
- **推荐测试**：
  - `test_verify_fields.py` - 验证字段映射
  - `test_limit_up_sectors.py` - 完整功能测试
- **调试工具**：
  - `test_data_alignment.py` - 数据对齐检查
  - `test_field_mapping.py` - 字段映射分析
- **其他测试**：开发过程中的各种测试文件

### docs/ - 文档
项目文档：
- `README_LIMIT_UP_SECTORS.md` - 涨停板块功能详细说明
- `SUMMARY_涨停原因板块功能.md` - 功能实现和问题修复总结

### data/ - 数据文件
存放测试和示例生成的数据文件：
- JSON格式：完整的结构化数据
- CSV格式：表格数据

### archive/ - 历史版本
存放旧版本代码和废弃文件，仅供参考。

## 快速开始

1. **查看文档**：阅读 `README.md`
2. **运行示例**：执行 `examples/example_basic.py`
3. **运行测试**：执行 `tests/test_verify_fields.py`
4. **开始使用**：导入 `kaipanla_crawler` 模块

## 文件命名规范

- **核心模块**：`kaipanla_crawler.py`
- **示例代码**：`example_*.py`
- **测试文件**：`test_*.py`
- **文档文件**：`*.md`
- **数据文件**：`*.json`, `*.csv`

## 版本历史

- **v1.1.0** (当前版本)
  - 新增涨停原因板块功能
  - 修复字段映射问题
  - 优化项目结构

- **v1.0.0**
  - 初始版本
  - 基础功能实现
