# 开盘啦APP数据爬虫

一个用于获取开盘啦APP数据的Python爬虫工具，支持获取市场行情、涨停板块、连板梯队等多种数据。

## 功能特性

### 核心功能

1. **市场行情数据** (`get_daily_data`)
   - 获取单日或日期范围的完整交易数据
   - 包含涨停数、跌停数、上证指数等关键指标

2. **百日新高数据** (`get_new_high_data`)
   - 获取百日新高股票的今日新增数量
   - 支持单日查询和日期范围查询
   - 返回Series格式，便于数据分析

3. **板块分时数据** (`get_sector_intraday`)
   - 获取板块的分时价格、成交量、成交额数据
   - 包含每分钟的详细数据
   - 支持时间段分析和趋势判断

4. **个股分时数据** (`get_stock_intraday`)
   - 获取个股的分时价格、均价、成交量、成交额
   - 包含主力资金流向数据（每分钟净流入）
   - 支持价格与均价对比分析

5. **异动个股** (`get_abnormal_stocks`)
   - 获取实时异动股票信息
   - 包含盘中异动和收盘异动
   - 提供异动原因、偏离值、连续天数等详细信息
   - 支持风险等级分类

6. **多头空头风向标** (`get_sentiment_indicator`)
   - 获取市场多空情绪风向标
   - 识别多头风向标（前3只）和空头风向标（后3只）
   - 支持自定义股票列表
   - 实时数据，反映市场情绪

7. **指数分时** (`get_index_intraday`)
   - 获取指数分时数据（上证、深证、创业板等）
   - 包含价格、均价、成交量、涨跌标志
   - 每分钟级别的详细数据
   - 支持多个指数查询

8. **板块排行** (`get_sector_ranking`)
   - 获取板块排行数据（DataFrame格式）
   - 包含板块涨跌幅、成交额、主力资金等

9. **涨停原因板块** (`get_limit_up_sectors`)
   - 获取涨停原因板块详细数据（字典格式）
   - 包含每个板块的涨停股票列表及详细信息
   - 涨停原因、概念标签、连板信息等

10. **其他功能**
   - 市场情绪统计
   - 大盘指数数据
   - 连板梯队数据
   - 大幅回撤股票

## 快速开始

### 安装依赖

```bash
pip install requests pandas urllib3
```

### 基本使用

```python
from kaipanla_crawler import KaipanlaCrawler

# 创建爬虫实例
crawler = KaipanlaCrawler()

# 1. 获取单日市场数据
data = crawler.get_daily_data("2026-01-16")
print(data)

# 2. 获取日期范围数据
df = crawler.get_daily_data("2026-01-16", "2026-01-10")
print(df)

# 3. 获取百日新高数据
new_high = crawler.get_new_high_data("2026-01-16")
print(f"今日新增新高: {new_high} 只")

# 4. 获取最近一周新高数据
new_high_series = crawler.get_new_high_data("2026-01-16", "2026-01-10")
print(new_high_series)

# 5. 获取板块分时数据
intraday = crawler.get_sector_intraday("801346", "2026-01-16")
print(intraday['data'])

# 6. 获取个股分时数据
stock_intraday = crawler.get_stock_intraday("002498", "2026-01-16")
print(stock_intraday['data'])
print(f"主力净流入: {stock_intraday['total_main_inflow']}")

# 7. 获取异动个股（实时）
abnormal = crawler.get_abnormal_stocks()
print(f"异动股票数: {abnormal['total_count']}")
print(abnormal['intraday'])  # 盘中异动
print(abnormal['closed'])    # 收盘异动

# 8. 获取多头空头风向标
sentiment = crawler.get_sentiment_indicator()
print(f"多头风向标: {sentiment['bullish_codes']}")
print(f"空头风向标: {sentiment['bearish_codes']}")

# 9. 获取板块排行
sector_df = crawler.get_sector_ranking("2026-01-16")
print(sector_df)

# 10. 获取涨停原因板块
limit_up_data = crawler.get_limit_up_sectors("2026-01-16")
print(f"涨停数: {limit_up_data['summary']['涨停数']}")
for sector in limit_up_data['sectors']:
    print(f"{sector['sector_name']}: {sector['stock_count']}只涨停")
```

## 详细文档

- [百日新高功能说明](docs/README_NEW_HIGH.md)
- [板块分时功能说明](docs/README_SECTOR_INTRADAY.md)
- [涨停原因板块功能说明](docs/README_LIMIT_UP_SECTORS.md)
- [多头空头风向标功能说明](docs/README_SENTIMENT_INDICATOR.md)
- [功能实现总结](docs/SUMMARY_涨停原因板块功能.md)

## 项目结构

```
kaipanla_crawler/
├── kaipanla_crawler.py      # 主爬虫模块
├── __init__.py               # 包初始化文件
├── README.md                 # 项目说明文档
├── examples/                 # 示例代码
├── tests/                    # 测试文件
├── docs/                     # 文档
├── data/                     # 数据文件
└── archive/                  # 历史版本
```

## API参考

### KaipanlaCrawler 类

#### get_daily_data(end_date, start_date=None)
获取交易日数据

**参数：**
- `end_date` (str): 结束日期，格式"YYYY-MM-DD"
- `start_date` (str, 可选): 起始日期，格式"YYYY-MM-DD"

**返回：**
- 只传end_date: 返回Series（单日数据）
- 传start_date和end_date: 返回DataFrame（日期范围数据）

#### get_new_high_data(end_date, start_date=None)
获取百日新高数据

**参数：**
- `end_date` (str): 结束日期，格式"YYYY-MM-DD"
- `start_date` (str, 可选): 起始日期，格式"YYYY-MM-DD"

**返回：**
- 只传end_date: 返回单日值（int）
- 传start_date和end_date: 返回Series（日期范围数据）

**示例：**
```python
# 单日数据
count = crawler.get_new_high_data("2026-01-16")
print(f"今日新增: {count} 只")

# 日期范围数据
series = crawler.get_new_high_data("2026-01-16", "2026-01-10")
print(series)
print(f"平均: {series.mean():.1f}")
```

#### get_sector_intraday(sector_code, date=None)
获取板块分时数据

**参数：**
- `sector_code` (str): 板块代码，如 "801346"
- `date` (str, 可选): 日期，格式"YYYY-MM-DD"，默认当前日期

**返回：**
- dict: 包含分时数据
  - `date`: 日期
  - `sector_code`: 板块代码
  - `open`: 开盘价
  - `close`: 收盘价
  - `high`: 最高价
  - `low`: 最低价
  - `preclose`: 昨收价
  - `data`: DataFrame（分时数据）
    - `time`: 时间
    - `price`: 价格
    - `volume`: 成交量
    - `turnover`: 成交额
    - `trend`: 涨跌标志 (0=跌, 1=涨, 2=平)

**示例：**
```python
# 获取板块分时数据
data = crawler.get_sector_intraday("801346", "2026-01-16")
print(f"开盘: {data['open']}, 收盘: {data['close']}")
print(data['data'])  # 分时DataFrame

# 数据分析
df = data['data']
print(f"总成交量: {df['volume'].sum()}")
print(f"平均价格: {df['price'].mean()}")
```

#### get_sentiment_indicator(plate_id="801225", stocks=None)
获取多头空头风向标

**参数：**
- `plate_id` (str, 可选): 板块ID，默认"801225"
- `stocks` (list, 可选): 股票代码列表，不提供则使用默认列表

**返回：**
- dict: 包含多头和空头风向标
  - `date`: 日期
  - `plate_id`: 板块ID
  - `bullish_codes`: 多头风向标股票代码列表（前3只）
  - `bearish_codes`: 空头风向标股票代码列表（后3只）
  - `all_stocks`: 所有股票代码列表

**示例：**
```python
# 使用默认股票列表
data = crawler.get_sentiment_indicator()
print(f"多头风向标: {data['bullish_codes']}")
print(f"空头风向标: {data['bearish_codes']}")

# 使用自定义股票列表
custom_stocks = ["600519", "000858", "601318", "600036", "000333", "601888"]
data = crawler.get_sentiment_indicator(stocks=custom_stocks)
```

#### get_sector_ranking(date=None, order=1, zstype=7, limit=30)
获取板块排行数据

**参数：**
- `date` (str, 可选): 日期，默认当前日期
- `order` (int): 排序方式，1=涨幅
- `zstype` (int): 板块类型，7=精选板块
- `limit` (int): 返回数量

**返回：** DataFrame

#### get_limit_up_sectors(date=None, index=0)
获取涨停原因板块数据

**参数：**
- `date` (str, 可选): 日期，默认当前日期
- `index` (int): 分页索引

**返回：** dict，包含summary和sectors

## 示例

查看 `examples/` 目录获取更多示例代码。

## 测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python tests/test_verify_fields.py
```

## 注意事项

1. 请合理控制请求频率，避免对服务器造成压力
2. 数据仅供学习研究使用
3. 建议在交易日收盘后获取数据，数据更完整

## 更新日志

### v1.2.0 (2026-01-19)
- ✅ 新增百日新高数据功能 (`get_new_high_data`)
- ✅ 支持单日和日期范围查询
- ✅ 返回Series格式便于数据分析

### v1.1.0 (2026-01-19)
- ✅ 新增涨停原因板块功能 (`get_limit_up_sectors`)
- ✅ 修复字段映射错误
- ✅ 优化代码结构
- ✅ 完善文档

### v1.0.0
- 初始版本
- 基础市场数据获取功能

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
