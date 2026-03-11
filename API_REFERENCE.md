# 开盘啦爬虫 API 参考文档

## 目录

1. [核心数据接口](#核心数据接口)
2. [连板梯队接口](#连板梯队接口)
3. [板块和个股接口](#板块和个股接口)
4. [市场监控接口](#市场监控接口)
5. [传统接口（向后兼容）](#传统接口向后兼容)

---

## 核心数据接口

### 1. get_daily_data()
**获取交易日完整数据（推荐使用）**

```python
def get_daily_data(end_date, start_date=None)
```

**功能**: 获取指定日期或日期范围的完整交易数据，包含涨跌统计、大盘指数、连板梯队、大幅回撤等所有核心指标。

**参数**:
- `end_date` (str): 结束日期，格式 `YYYY-MM-DD`
- `start_date` (str, 可选): 起始日期，格式 `YYYY-MM-DD`

**返回**:
- 只传 `end_date`: 返回 `pd.Series`（单日数据）
- 传 `start_date` 和 `end_date`: 返回 `pd.DataFrame`（日期范围数据）

**返回字段**:
- 日期、涨停数、实际涨停、跌停数、实际跌停
- 上涨家数、下跌家数、平盘家数
- 上证指数、最新价、涨跌幅、成交额
- 首板数量、2连板数量、3连板数量、4连板以上数量、连板率
- 大幅回撤家数

**示例**:
```python
crawler = KaipanlaCrawler()

# 获取单日数据
data = crawler.get_daily_data("2026-01-16")
print(f"涨停数: {data['涨停数']}")
print(f"连板率: {data['连板率']}%")

# 获取日期范围数据
df = crawler.get_daily_data("2026-01-16", "2026-01-10")
print(df[['日期', '涨停数', '连板率']])
```

---

### 2. get_new_high_data()
**获取百日新高数据**

```python
def get_new_high_data(end_date, start_date=None, timeout=60)
```

**功能**: 获取百日新高股票数量（今日新增）。

**参数**:
- `end_date` (str): 结束日期，格式 `YYYY-MM-DD`
- `start_date` (str, 可选): 起始日期，格式 `YYYY-MM-DD`
- `timeout` (int): 超时时间（秒），默认60秒

**返回**:
- 只传 `end_date`: 返回单个值（今日新增新高数量）
- 传 `start_date` 和 `end_date`: 返回 `pd.Series`（日期范围数据）

**示例**:
```python
# 获取单日新高数量
new_high = crawler.get_new_high_data("2026-01-16")
print(f"今日新增新高: {new_high}只")

# 获取日期范围数据
series = crawler.get_new_high_data("2026-01-16", "2026-01-10")
print(series)
```

---

## 连板梯队接口

### 3. get_market_limit_up_ladder() ⭐
**获取全市场连板梯队（实时/历史）**

```python
def get_market_limit_up_ladder(date=None, timeout=60)
```

**功能**: 获取全市场连板梯队情况，支持实时和历史数据。

**参数**:
- `date` (str, 可选): 日期，格式 `YYYY-MM-DD`
  - 不传: 获取实时数据
  - 传入日期: 获取历史数据
- `timeout` (int): 超时时间（秒），默认60秒

**返回**: `dict`
```python
{
    "date": "2026-01-20",
    "is_realtime": True,  # 是否为实时数据
    "ladder": {
        1: [...],  # 首板股票列表
        2: [...],  # 2连板股票列表
        3: [...],  # 3连板股票列表
        # ...
    },
    "broken_stocks": [...],  # 反包板股票列表
    "height_marks": [...],   # 打开高度标注股票列表
    "statistics": {
        "total_limit_up": 15,      # 总涨停数
        "max_consecutive": 6,       # 最高连板
        "ladder_distribution": {    # 连板分布
            1: 5,
            2: 4,
            3: 3,
            6: 3
        }
    }
}
```

**股票信息结构**:
```python
{
    "stock_code": "600785",
    "stock_name": "新华百货",
    "consecutive_days": 4,
    "tips": ""
}
```

**示例**:
```python
# 获取实时数据
realtime = crawler.get_market_limit_up_ladder()
print(f"实时涨停: {realtime['statistics']['total_limit_up']}只")
print(f"最高板: {realtime['statistics']['max_consecutive']}连板")

# 获取历史数据
historical = crawler.get_market_limit_up_ladder("2026-01-16")
print(f"历史涨停: {historical['statistics']['total_limit_up']}只")

# 遍历连板梯队
for consecutive, stocks in sorted(realtime['ladder'].items(), reverse=True):
    print(f"{consecutive}连板: {len(stocks)}只")
    for stock in stocks[:3]:  # 显示前3只
        print(f"  {stock['stock_code']} {stock['stock_name']}")

# 查看反包板
for stock in realtime['broken_stocks']:
    print(f"反包板: {stock['stock_name']} - {stock['tips']}")
```

---

### 4. get_sector_limit_up_ladder()
**获取板块连板梯队（实时/历史）**

```python
def get_sector_limit_up_ladder(date=None, timeout=60)
```

**功能**: 获取各板块的连板梯队情况，支持实时和历史数据。

**参数**:
- `date` (str, 可选): 日期，格式 `YYYY-MM-DD`
  - 不传: 获取实时数据
  - 传入日期: 获取历史数据
- `timeout` (int): 超时时间（秒），默认60秒

**返回**: `dict`
```python
{
    "date": "2026-01-16",
    "is_realtime": False,
    "sectors": [
        {
            "sector_code": "801346",
            "sector_name": "电力设备",
            "limit_up_count": 5,
            "stocks": [
                {
                    "stock_code": "600785",
                    "stock_name": "新华百货",
                    "consecutive_days": 4,
                    "tips": ""
                },
                # ...
            ],
            "broken_stocks": [  # 反包板股票
                {
                    "stock_code": "002636",
                    "stock_name": "金安国纪",
                    "consecutive_days": 2,
                    "tips": "3天2板",
                    "is_broken": True
                }
            ]
        },
        # ...
    ]
}
```

**示例**:
```python
# 获取实时板块连板梯队
data = crawler.get_sector_limit_up_ladder()

for sector in data['sectors']:
    print(f"\n{sector['sector_name']}: {sector['limit_up_count']}只涨停")
    
    # 正常连板股票
    for stock in sector['stocks']:
        print(f"  {stock['stock_code']} {stock['stock_name']} {stock['consecutive_days']}连板")
    
    # 反包板股票
    if sector.get('broken_stocks'):
        print(f"  反包板: {len(sector['broken_stocks'])}只")
```

---

### 5. get_consecutive_limit_up()
**获取连板梯队详细信息（含题材）**

```python
def get_consecutive_limit_up(date=None, timeout=60)
```

**功能**: 获取指定日期的连板梯队情况，包含最高板个股名称和题材信息。

**参数**:
- `date` (str, 可选): 日期，格式 `YYYY-MM-DD`，默认当前日期
- `timeout` (int): 超时时间（秒），默认60秒

**返回**: `dict`
```python
{
    "date": "2026-01-19",
    "max_consecutive": 5,
    "max_consecutive_stocks": "博菲电气",
    "max_consecutive_concepts": "电力设备、新能源",
    "ladder": {
        2: [
            {
                "股票代码": "002796",
                "股票名称": "世嘉科技",
                "连板天数": 2,
                "题材": "游戏",
                "概念": "元宇宙、VR"
            },
            # ...
        ],
        3: [...],
        5: [...]
    }
}
```

**示例**:
```python
data = crawler.get_consecutive_limit_up("2026-01-19")

print(f"最高板: {data['max_consecutive']}连板")
print(f"最高板个股: {data['max_consecutive_stocks']}")
print(f"最高板题材: {data['max_consecutive_concepts']}")

# 遍历连板梯队
for consecutive, stocks in sorted(data['ladder'].items(), reverse=True):
    print(f"\n{consecutive}连板:")
    for stock in stocks:
        print(f"  {stock['股票名称']} - {stock['题材']}")
```

---

## 板块和个股接口

### 6. get_sector_ranking()
**获取涨停原因板块数据**

```python
def get_sector_ranking(date=None, index=0, timeout=60)
```

**功能**: 获取按涨停原因分类的板块数据，包含每个板块的涨停股票详情。

**参数**:
- `date` (str, 可选): 日期，格式 `YYYY-MM-DD`，默认当前日期
- `index` (int): 分页索引，默认0（第一页）
- `timeout` (int): 超时时间（秒），默认60秒

**返回**: `dict`
```python
{
    "summary": {
        "日期": "2026-01-16",
        "上涨家数": 2500,
        "下跌家数": 1800,
        "涨停数": 50,
        "跌停数": 10,
        "涨跌比": 1.39,
        "昨日涨跌比": 1.25
    },
    "sectors": [
        {
            "sector_code": "801346",
            "sector_name": "电力设备",
            "stock_count": 5,
            "stocks": [
                {
                    "股票代码": "600785",
                    "股票名称": "新华百货",
                    "涨停价": 15.50,
                    "成交额": 50000000,
                    "流通市值": 2000000000,
                    "连板天数": 4,
                    "连板描述": "4连板",
                    "连板次数": 1,
                    "概念标签": "新能源、电力设备",
                    "封单额": 100000000,
                    "总市值": 3000000000,
                    "涨停时间": "09:30:00",
                    "主力资金": 20000000,
                    "主题": "新能源",
                    "涨停原因": "政策利好",
                    "是否首板": 0
                },
                # ...
            ]
        },
        # ...
    ]
}
```

**示例**:
```python
data = crawler.get_sector_ranking("2026-01-16")

# 查看市场概况
print(data['summary'])

# 遍历板块
for sector in data['sectors']:
    print(f"\n{sector['sector_name']}: {sector['stock_count']}只涨停")
    for stock in sector['stocks']:
        print(f"  {stock['股票代码']} {stock['股票名称']}")
        print(f"    涨停原因: {stock['涨停原因']}")
        print(f"    连板: {stock['连板描述']}")
```

---

### 7. get_index_intraday()
**获取大盘指数分时数据**

```python
def get_index_intraday(index_code="SH000001", date=None, timeout=60)
```

**功能**: 获取大盘指数的分时数据，用于盘面联动分析、识别共振点等。

**参数**:
- `index_code` (str): 指数代码，默认 `"SH000001"`（上证指数）
  - `SH000001`: 上证指数
  - `SZ399001`: 深证成指
  - `SZ399006`: 创业板指
  - `SH000300`: 沪深300
- `date` (str, 可选): 日期，格式 `YYYY-MM-DD`，默认为None（获取实时数据）
- `timeout` (int): 超时时间（秒），默认60秒

**返回**: `dict`
- `index_code`: 指数代码
- `index_name`: 指数名称
- `date`: 日期
- `open`: 开盘价
- `close`: 收盘价
- `high`: 最高价
- `low`: 最低价
- `preclose`: 昨收价
- `change_pct`: 涨跌幅（%）
- `data`: DataFrame，包含分时数据
  - `time`: 时间（HH:MM格式）
  - `timestamp`: 时间戳（datetime对象）
  - `price`: 价格
  - `pct_change`: 涨跌幅（相对昨收，%）
  - `volume`: 成交量（手）
  - `turnover`: 成交额（元）

**示例**:
```python
# 获取上证指数实时分时数据
data = crawler.get_index_intraday("SH000001")
print(f"指数: {data['index_name']}")
print(f"当前价: {data['close']:.2f}")
print(f"涨跌幅: {data['change_pct']:.2f}%")

# 获取历史分时数据
data = crawler.get_index_intraday("SH000001", "2026-01-20")

# 分析分时数据
df = data['data']
print(f"最高涨幅: {df['pct_change'].max():.2f}%")
print(f"最低涨幅: {df['pct_change'].min():.2f}%")

# 识别关键变盘点（用于盘面联动分析）
min_idx = df['pct_change'].idxmin()
print(f"最低点时间: {df.loc[min_idx, 'time']}, 涨跌幅: {df.loc[min_idx, 'pct_change']:.2f}%")
```

---

### 8. get_sector_intraday()
**获取板块分时数据**

```python
def get_sector_intraday(sector_code, date=None)
```

**功能**: 获取指定板块的分时数据（价格、成交量、成交额）。

**参数**:
- `sector_code` (str): 板块代码，如 `"801346"`
- `date` (str, 可选): 日期，格式 `YYYY-MM-DD`，默认当前日期

**返回**: `pd.DataFrame`

**示例**:
```python
# 获取电力设备板块分时数据
df = crawler.get_sector_intraday("801346", "2026-01-16")
print(df.head())
```

---

### 9. get_stock_intraday()
**获取个股分时数据**

```python
def get_stock_intraday(stock_code, date=None)
```

**功能**: 获取指定个股的分时数据，包含主力资金流向。

**参数**:
- `stock_code` (str): 股票代码，如 `"002498"`
- `date` (str, 可选): 日期，格式 `YYYY-MM-DD`，默认当前日期

**返回**: `pd.DataFrame`

**示例**:
```python
# 获取汉缆股份分时数据
df = crawler.get_stock_intraday("002498", "2026-01-16")
print(df.head())
```

---

## 市场监控接口

### 10. get_abnormal_stocks()
**获取异动个股（实时）**

```python
def get_abnormal_stocks()
```

**功能**: 获取实时异动个股数据，区分盘中异动和收盘异动。

**返回**: `dict`

**示例**:
```python
data = crawler.get_abnormal_stocks()
print(data)
```

---

### 10. get_sentiment_indicator()
**获取多头空头风向标**

```python
def get_sentiment_indicator(plate_id="801225", stocks=None, timeout=60)
```

**功能**: 获取指定板块的多头空头风向标，识别市场情绪方向。

**参数**:
- `plate_id` (str): 板块ID，默认 `"801225"`
- `stocks` (list, 可选): 股票代码列表，不提供则使用默认列表
- `timeout` (int): 超时时间（秒），默认60秒

**返回**: `dict`
```python
{
    "date": "2026-01-20",
    "plate_id": "801225",
    "bullish_codes": ["002112", "603667", "600550"],  # 多头风向标（前3只）
    "bearish_codes": ["000681", "002465", "001255"],  # 空头风向标（后3只）
    "all_stocks": [...]  # 所有股票代码
}
```

**示例**:
```python
data = crawler.get_sentiment_indicator()
print(f"多头风向标: {data['bullish_codes']}")
print(f"空头风向标: {data['bearish_codes']}")
```

---

## 传统接口（向后兼容）

以下接口保留用于向后兼容，推荐使用上述新接口。

### 11. get_market_sentiment()
**获取涨跌统计数据**

```python
def get_market_sentiment(date=None)
```

**返回**: `pd.DataFrame`

---

### 12. get_market_index()
**获取大盘指数数据**

```python
def get_market_index(date=None)
```

**返回**: `pd.DataFrame`

---

### 13. get_limit_up_ladder()
**获取连板梯队数据**

```python
def get_limit_up_ladder(date=None)
```

**返回**: `pd.DataFrame`

---

### 14. get_sharp_withdrawal()
**获取大幅回撤股票数据**

```python
def get_sharp_withdrawal(date=None)
```

**返回**: `pd.DataFrame`

---

## 快速开始

```python
from kaipanla_crawler import KaipanlaCrawler

# 创建爬虫实例
crawler = KaipanlaCrawler()

# 1. 获取今日完整数据
today_data = crawler.get_daily_data("2026-01-20")
print(f"涨停数: {today_data['涨停数']}, 连板率: {today_data['连板率']}%")

# 2. 获取实时全市场连板梯队
market_ladder = crawler.get_market_limit_up_ladder()
print(f"实时涨停: {market_ladder['statistics']['total_limit_up']}只")
print(f"最高板: {market_ladder['statistics']['max_consecutive']}连板")

# 3. 获取板块连板梯队
sector_ladder = crawler.get_sector_limit_up_ladder()
for sector in sector_ladder['sectors'][:5]:  # 显示前5个板块
    print(f"{sector['sector_name']}: {sector['limit_up_count']}只")

# 4. 获取涨停原因板块
sector_ranking = crawler.get_sector_ranking("2026-01-20")
print(f"市场概况: {sector_ranking['summary']}")

# 5. 获取多头空头风向标
sentiment = crawler.get_sentiment_indicator()
print(f"多头: {sentiment['bullish_codes']}")
print(f"空头: {sentiment['bearish_codes']}")
```

---

## 核心概念

### 连板梯队
- **首板（1连板）**: 当日首次涨停
- **N连板**: 连续N天涨停
- **反包板**: 涨停后打开再封板（不计入连板梯队）
- **打开高度标注**: 曾达到某连板高度但后来打开（不计入连板梯队）

### 连板率
```
连板率 = (连板股票数 / 总涨停数) × 100%
连板股票数 = 总涨停数 - 首板数
```

### 数据类型
- **实时数据**: 盘中实时更新，适合监控
- **历史数据**: 收盘后固定，适合复盘分析

---

## 注意事项

1. **日期格式**: 必须是 `YYYY-MM-DD` 格式
2. **交易日**: 只能查询交易日数据，非交易日会返回错误
3. **超时设置**: 默认60秒，网络不稳定时可增加
4. **数据来源**: 开盘啦APP，准确率99%+
5. **实时数据**: 不传 `date` 参数获取实时，传 `date` 获取历史

---

## 版本信息

- **当前版本**: v1.1.0
- **更新日期**: 2026-01-20
- **Python版本**: 3.6+
- **依赖**: requests, pandas, urllib3

---

## 相关文档

- [全市场连板梯队功能说明](./全市场连板梯队功能说明.md)
- [更新日志](./CHANGELOG.md)
- [测试文件](./test_market_limit_up_ladder.py)
