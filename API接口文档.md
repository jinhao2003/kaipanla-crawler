# 开盘啦数据接口文档

## 📚 目录

- [基础数据接口](#基础数据接口)
- [涨停数据接口](#涨停数据接口)
- [板块数据接口](#板块数据接口)
- [实时数据接口](#实时数据接口)
- [分时数据接口](#分时数据接口)
- [新闻资讯接口](#新闻资讯接口)
- [其他接口](#其他接口)

---

## 基础数据接口

### 1. get_daily_data()
**功能**：获取交易日数据（涨跌统计、指数、连板梯队等）

**参数**：
- `end_date` (str): 结束日期，格式 YYYY-MM-DD
- `start_date` (str, 可选): 起始日期，格式 YYYY-MM-DD

**返回**：
- 只传 `end_date`: 返回 Series（单日数据）
- 传 `start_date` 和 `end_date`: 返回 DataFrame（日期范围数据）

**数据字段**：
- 日期、涨停数、实际涨停、跌停数、实际跌停
- 上涨家数、下跌家数、平盘家数
- 上证指数、涨跌幅、成交额
- 首板数量、2连板数量、3连板数量、4连板以上数量
- 连板率、大幅回撤家数

**示例**：
```python
# 获取单日数据
data = crawler.get_daily_data("2026-01-16")

# 获取日期范围数据
df = crawler.get_daily_data("2026-01-16", "2026-01-10")
```

---

### 2. get_new_high_data()
**功能**：获取百日新高数据

**参数**：
- `end_date` (str): 结束日期
- `start_date` (str, 可选): 起始日期
- `timeout` (int): 超时时间，默认1600秒

**返回**：
- 只传 `end_date`: 返回单个值（今日新增新高数量）
- 传 `start_date` 和 `end_date`: 返回 Series（日期范围数据）

**示例**：
```python
# 获取单日数据
count = crawler.get_new_high_data("2026-01-16")

# 获取日期范围数据
series = crawler.get_new_high_data("2026-01-16", "2026-01-10")
```

---

### 3. get_market_sentiment()
**功能**：获取涨跌统计数据

**参数**：
- `date` (str, 可选): 日期，默认今天

**返回**：DataFrame，包含涨停数、跌停数、上涨下跌家数等

**示例**：
```python
df = crawler.get_market_sentiment("2026-01-16")
```

---

### 4. get_market_index()
**功能**：获取大盘指数数据

**参数**：
- `date` (str, 可选): 日期，默认今天

**返回**：DataFrame，包含各指数的最新价、涨跌幅、成交额等

**示例**：
```python
df = crawler.get_market_index("2026-01-16")
```

---

## 涨停数据接口

### 5. get_limit_up_ladder()
**功能**：获取连板梯队数据

**参数**：
- `date` (str, 可选): 日期，默认今天

**返回**：DataFrame，包含一板、二板、三板、高度板数量及连板率等

**示例**：
```python
df = crawler.get_limit_up_ladder("2026-01-16")
```

---

### 6. get_consecutive_limit_up()
**功能**：获取指定日期的连板梯队情况

**参数**：
- `date` (str, 可选): 日期，默认今天
- `timeout` (int): 超时时间，默认1600秒

**返回**：dict，包含：
- `date`: 日期
- `max_consecutive`: 最高连板高度
- `max_consecutive_stocks`: 最高连板个股名称
- `max_consecutive_concepts`: 最高连板个股题材
- `ladder`: 连板梯队详细数据

**示例**：
```python
data = crawler.get_consecutive_limit_up("2026-01-19")
print(f"最高板: {data['max_consecutive']}连板")
print(f"最高板个股: {data['max_consecutive_stocks']}")
```

---

### 7. get_market_limit_up_ladder()
**功能**：获取全市场连板梯队（历史或实时）

**参数**：
- `date` (str, 可选): 日期，默认 None（获取实时数据）
- `timeout` (int): 超时时间，默认1600秒

**返回**：dict，包含：
- `date`: 日期
- `is_realtime`: 是否为实时数据
- `ladder`: 连板梯队数据（字典，键为连板数）
- `broken_stocks`: 反包板股票列表
- `height_marks`: 打开高度标注股票列表
- `statistics`: 统计信息

**示例**：
```python
# 获取历史数据
data = crawler.get_market_limit_up_ladder("2026-01-16")

# 获取实时数据
data = crawler.get_market_limit_up_ladder()

print(f"总涨停数: {data['statistics']['total_limit_up']}")
print(f"最高连板: {data['statistics']['max_consecutive']}")
```

---

### 8. get_sector_ranking()
**功能**：获取涨停原因板块数据

**参数**：
- `date` (str, 可选): 日期，默认今天
- `index` (int): 分页索引，默认0
- `timeout` (int): 超时时间，默认1600秒

**返回**：dict，包含：
- `summary`: 市场概况
- `sectors`: 板块列表（每个板块包含涨停股票详情）

**注意**：此接口不支持历史日期查询，总是返回实时数据

**示例**：
```python
data = crawler.get_sector_ranking("2026-01-16")

for sector in data['sectors']:
    print(f"板块: {sector['sector_name']}, 涨停数: {sector['stock_count']}")
```

---

### 9. get_sharp_withdrawal()
**功能**：获取大幅回撤股票数据

**参数**：
- `date` (str, 可选): 日期，默认今天

**返回**：DataFrame，包含股票代码、名称、涨跌幅、回撤幅度等

**示例**：
```python
df = crawler.get_sharp_withdrawal("2026-01-16")
```

---

## 板块数据接口

### 10. get_sector_limit_up_ladder()
**功能**：获取板块连板梯队（历史或实时）

**参数**：
- `date` (str, 可选): 日期，默认 None（获取实时数据）
- `timeout` (int): 超时时间，默认1600秒

**返回**：dict，包含：
- `date`: 日期
- `is_realtime`: 是否为实时数据
- `sectors`: 板块列表（每个板块包含涨停股票和连板信息）

**示例**：
```python
# 获取历史数据
data = crawler.get_sector_limit_up_ladder("2026-01-16")

# 获取实时数据
data = crawler.get_sector_limit_up_ladder()
```

---

### 11. get_sector_capital_data()
**功能**：获取板块资金成交额数据

**参数**：
- `sector_code` (str): 板块代码，如 "801235"（化工）
- `date` (str, 可选): 日期，默认为空（获取实时数据）
- `timeout` (int): 超时时间，默认1600秒

**返回**：dict，包含：
- 成交额、涨跌幅、市值
- 主力净额、主卖、净额
- 上涨家数、下跌家数、平盘家数
- 流通市值、总市值、换手率
- 主力净占比

**示例**：
```python
# 获取化工板块实时数据
data = crawler.get_sector_capital_data("801235")
print(f"成交额: {data['turnover'] / 100000000:.2f}亿")
print(f"主力净额: {data['main_net_inflow'] / 100000000:.2f}亿")
```

---

### 12. get_sector_strength_ndays()
**功能**：获取N日板块强度排名数据

**参数**：
- `end_date` (str): 结束日期
- `num_days` (int): 获取天数，默认7天
- `timeout` (int): 超时时间，默认1600秒

**返回**：DataFrame，包含：
- 日期、板块代码、板块名称
- 涨停数、涨停股票列表

**示例**：
```python
# 获取最近7日板块强度
df = crawler.get_sector_strength_ndays("2026-01-20", num_days=7)

# 分析板块热度趋势
sector_trend = df.groupby('板块名称')['涨停数'].sum().sort_values(ascending=False)
print("7日最强板块:")
print(sector_trend.head(10))
```

---

### 13. get_sentiment_indicator()
**功能**：获取多头空头风向标

**参数**：
- `plate_id` (str): 板块ID，默认 "801225"
- `stocks` (list, 可选): 股票代码列表
- `timeout` (int): 超时时间，默认1600秒

**返回**：dict，包含：
- `date`: 日期
- `plate_id`: 板块ID
- `bullish_codes`: 多头风向标股票代码列表（前3只）
- `bearish_codes`: 空头风向标股票代码列表（后3只）
- `all_stocks`: 所有股票代码列表

**示例**：
```python
data = crawler.get_sentiment_indicator()
print("多头风向标:", data['bullish_codes'])
print("空头风向标:", data['bearish_codes'])
```

---

## 实时数据接口

### 14. get_realtime_market_mood()
**功能**：获取实时市场情绪数据

**参数**：
- `timeout` (int): 超时时间，默认1600秒

**返回**：dict，包含：
- 上涨家数、下跌家数
- 涨停家数、跌停家数
- 全市场流通量、前日流通量
- 涨跌比、市场颜色

**示例**：
```python
mood = crawler.get_realtime_market_mood()
print(f"涨停: {mood['涨停家数']}家")
print(f"跌停: {mood['跌停家数']}家")
print(f"涨跌比: {mood['涨跌比']}")
```

---

### 15. get_realtime_actual_limit_up_down()
**功能**：获取实时实际涨跌停数据

**参数**：
- `timeout` (int): 超时时间，默认1600秒

**返回**：dict，包含：
- `actual_limit_up`: 实际涨停数
- `actual_limit_down`: 实际跌停数
- `limit_up`: 涨停数（包含一字板）
- `limit_down`: 跌停数（包含一字板）

**示例**：
```python
data = crawler.get_realtime_actual_limit_up_down()
print(f"实际涨停: {data['actual_limit_up']}只")
```

---

### 16. get_realtime_board_stocks()
**功能**：获取实时指定连板的股票列表

**参数**：
- `board_type` (int): 连板类型（1=首板, 2=二板, 3=三板...）
- `timeout` (int): 超时时间，默认1600秒

**返回**：list，股票列表，每个股票包含：
- 股票代码、股票名称、连板天数
- 涨停原因、成交额、市值
- 主力净额、封单额、概念标签等

**示例**：
```python
# 获取首板股票
first_board = crawler.get_realtime_board_stocks(board_type=1)
print(f"首板股票: {len(first_board)}只")

# 获取二板股票
second_board = crawler.get_realtime_board_stocks(board_type=2)
```

---

### 17. get_realtime_all_boards_stocks()
**功能**：获取实时所有连板的股票列表（首板到五板以上）

**参数**：
- `timeout` (int): 超时时间，默认1600秒

**返回**：dict，包含：
- `first_board`: 首板股票列表
- `second_board`: 二板股票列表
- `third_board`: 三板股票列表
- `fourth_board`: 四板股票列表
- `fifth_board_plus`: 五板及以上股票列表
- `statistics`: 统计信息

**示例**：
```python
data = crawler.get_realtime_all_boards_stocks()

print(f"首板: {len(data['first_board'])}只")
print(f"二板: {len(data['second_board'])}只")
print(f"三板: {len(data['third_board'])}只")
```

---

### 18. get_board_stocks_count_and_list()
**功能**：获取指定连板的个股数量和个股列表

**参数**：
- `board_type` (int): 连板类型
- `timeout` (int): 超时时间，默认1600秒

**返回**：tuple (count, stocks)
- `count`: 个股数量
- `stocks`: 个股列表

**示例**：
```python
count, stocks = crawler.get_board_stocks_count_and_list(1)
print(f"首板: {count}只")
```

---

### 19. get_realtime_index_trend()
**功能**：获取实时指数趋势数据

**参数**：
- `stock_id` (str): 指数代码，默认 "801900"（昨日涨停今日表现）
  - 801900: 昨日涨停今日表现
  - 801903: 昨日断板今日表现
- `time` (str): 时间点，默认 "15:00"
- `timeout` (int): 超时时间，默认1600秒

**返回**：dict，包含指数值、涨跌幅、分时数据等

**示例**：
```python
# 获取昨日涨停今日表现
data = crawler.get_realtime_index_trend(stock_id="801900")
print(f"昨日涨停今表现: {data['value']}")

# 获取昨日断板今日表现
data = crawler.get_realtime_index_trend(stock_id="801903")
```

---

### 20. get_realtime_index_list()
**功能**：获取实时指数列表数据（批量获取多个指数）

**参数**：
- `stock_ids` (list, 可选): 指数代码列表，默认主要指数
  - SH000001: 上证指数
  - SZ399001: 深证成指
  - SZ399006: 创业板指
  - SH000688: 科创50
- `timeout` (int): 超时时间，默认1600秒

**返回**：dict，包含各指数数据

**示例**：
```python
data = crawler.get_realtime_index_list()
for index in data['indexes']:
    print(f"{index['name']}: {index['change_pct']:.2f}%")
```

---

### 21. get_realtime_sharp_withdrawal()
**功能**：获取实时大幅回撤股票数据

**参数**：
- `timeout` (int): 超时时间，默认1600秒

**返回**：dict，包含：
- `date`: 日期
- `count`: 大幅回撤股票数量
- `stocks`: 股票列表

**示例**：
```python
data = crawler.get_realtime_sharp_withdrawal()
print(f"大幅回撤: {data['count']}只")
```

---

### 22. get_realtime_rise_fall_analysis()
**功能**：获取实时涨跌分析数据

**参数**：
- `timeout` (int): 超时时间，默认1600秒

**返回**：dict，包含：
- `date`: 日期
- `limit_up_count`: 涨停数
- `limit_down_count`: 跌停数
- `blown_limit_up_count`: 炸板数
- `blown_limit_up_rate`: 炸板率 (%)
- `yesterday_limit_up_performance`: 昨日涨停今表现 (%)

**示例**：
```python
data = crawler.get_realtime_rise_fall_analysis()
print(f"涨停: {data['limit_up_count']}只")
print(f"炸板率: {data['blown_limit_up_rate']:.2f}%")
```

---

## 分时数据接口

### 23. get_sector_intraday()
**功能**：获取板块分时数据

**参数**：
- `sector_code` (str): 板块代码，如 "801346"（半导体）
- `date` (str, 可选): 日期，默认 None（获取实时数据）
- `timeout` (int): 超时时间，默认60秒

**返回**：dict，包含：
- 板块代码、日期
- 开盘价、收盘价、最高价、最低价、昨收价
- `data`: DataFrame（分时数据）

**示例**：
```python
# 获取历史分时数据
data = crawler.get_sector_intraday("801346", "2026-01-16")
print(f"收盘价: {data['close']}")

# 分析分时数据
df = data['data']
print(f"总成交量: {df['volume'].sum():,} 手")
```

---

### 24. get_stock_intraday()
**功能**：获取个股分时数据

**参数**：
- `stock_code` (str): 股票代码，如 "002498"
- `date` (str, 可选): 日期，默认 None（获取实时数据）
- `timeout` (int): 超时时间，默认60秒

**返回**：dict，包含：
- 股票代码、日期
- 主力净流入总额、主力净流出总额
- `data`: DataFrame（分时数据）

**示例**：
```python
data = crawler.get_stock_intraday("002498", "2026-01-16")
print(f"主力净额: {(data['total_main_inflow'] + data['total_main_outflow']) / 1e8:.2f} 亿")
```

---

### 25. get_index_intraday()
**功能**：获取大盘指数分时数据

**参数**：
- `index_code` (str): 指数代码，默认 "SH000001"（上证指数）
- `date` (str, 可选): 日期，默认 None（获取实时数据）
- `timeout` (int): 超时时间，默认60秒

**返回**：dict，包含：
- 指数代码、指数名称、日期
- 开盘价、收盘价、最高价、最低价、昨收价、涨跌幅
- `data`: DataFrame（分时数据）

**示例**：
```python
# 获取上证指数实时分时数据
data = crawler.get_index_intraday("SH000001")
print(f"当前价: {data['close']:.2f}")
print(f"涨跌幅: {data['change_pct']:.2f}%")

# 识别关键变盘点
df = data['data']
min_idx = df['pct_change'].idxmin()
print(f"最低点时间: {df.loc[min_idx, 'time']}")
```

---

## 新闻资讯接口

### 26. get_plate_news()
**功能**：获取指定板块的最新要闻

**参数**：
- `plate_id` (str): 板块代码，如 "801070"（化工）
- `index` (int): 分页索引，默认0
- `page_size` (int): 每页数量，默认30条
- `timeout` (int): 超时时间，默认1600秒

**返回**：dict，包含：
- `plate_id`: 板块代码
- `news_list`: 要闻列表
- `total_count`: 总数量

**示例**：
```python
# 获取化工板块要闻
news = crawler.get_plate_news("801070")

for item in news['news_list']:
    print(f"[{item['datetime']}] {item['content'][:50]}...")

# 获取第二页
news_page2 = crawler.get_plate_news("801070", index=30)
```

---

### 27. get_plate_news_dataframe()
**功能**：获取指定板块的最新要闻（返回DataFrame格式）

**参数**：
- `plate_id` (str): 板块代码
- `max_pages` (int): 最大页数，默认3页
- `page_size` (int): 每页数量，默认30条
- `timeout` (int): 超时时间，默认1600秒

**返回**：DataFrame，包含 id、title、content、datetime、type_name

**示例**：
```python
# 获取化工板块要闻（最多3页，共90条）
df = crawler.get_plate_news_dataframe("801070", max_pages=3)

# 查看最新10条
print(df.head(10))

# 筛选快讯
flash_news = df[df['type_name'] == '快讯']
```

---

## 其他接口

### 27. get_ths_hot_rank()
**功能**：获取同花顺热榜30个股数据

**参数**：
- `headless` (bool): 是否无头模式，默认 True
- `wait_time` (int): 等待时间，默认5秒
- `timeout` (int): 超时时间，默认60秒

**返回**：DataFrame 或 Series

**注意**：此接口需要使用浏览器自动化，可能需要额外配置

---

## 📊 接口分类汇总

### 历史数据接口（支持指定日期）
1. get_daily_data() - 交易日数据
2. get_new_high_data() - 百日新高
3. get_market_sentiment() - 涨跌统计
4. get_market_index() - 大盘指数
5. get_limit_up_ladder() - 连板梯队
6. get_consecutive_limit_up() - 连板梯队详情
7. get_market_limit_up_ladder() - 全市场连板梯队
8. get_sharp_withdrawal() - 大幅回撤
9. get_sector_limit_up_ladder() - 板块连板梯队
10. get_sector_capital_data() - 板块资金数据
11. get_sector_intraday() - 板块分时
12. get_stock_intraday() - 个股分时
13. get_index_intraday() - 指数分时

### 实时数据接口（仅当天）
1. get_realtime_market_mood() - 市场情绪
2. get_realtime_actual_limit_up_down() - 实际涨跌停
3. get_realtime_board_stocks() - 指定连板股票
4. get_realtime_all_boards_stocks() - 所有连板股票
5. get_board_stocks_count_and_list() - 连板数量和列表
6. get_realtime_index_trend() - 指数趋势
7. get_realtime_index_list() - 指数列表
8. get_realtime_sharp_withdrawal() - 大幅回撤
9. get_realtime_rise_fall_analysis() - 涨跌分析

### 混合接口（支持历史和实时）
1. get_sector_ranking() - 板块排名（⚠️ 不支持历史日期）
2. get_sentiment_indicator() - 风向标

### 资讯接口
1. get_plate_news() - 板块要闻
2. get_plate_news_dataframe() - 板块要闻（DataFrame）

### 其他接口
1. get_ths_hot_rank() - 同花顺热榜

---

## 🔍 使用建议

### 每日分析
推荐使用实时接口：
- get_realtime_all_boards_stocks() - 获取所有涨停股票
- get_realtime_rise_fall_analysis() - 获取涨跌分析
- get_realtime_market_mood() - 获取市场情绪

### 历史回测
推荐使用历史接口：
- get_daily_data() - 获取交易日数据
- get_market_limit_up_ladder() - 获取连板梯队
- get_consecutive_limit_up() - 获取连板详情

### 板块分析
推荐使用板块接口：
- get_sector_strength_ndays() - N日板块强度
- get_sector_capital_data() - 板块资金数据
- get_plate_news() - 板块要闻

---

## ⚠️ 注意事项

1. **历史数据限制**：
   - 部分接口只返回连板股票，不包含首板
   - get_sector_ranking() 不支持历史日期查询

2. **超时设置**：
   - 建议设置较长的超时时间（1600秒）
   - 分时数据接口可以使用较短超时（60秒）

3. **数据完整性**：
   - 实时接口数据最完整
   - 历史接口可能缺少首板数据

4. **API限制**：
   - 注意请求频率
   - 避免短时间内大量请求

---

## 📝 更新日志

- 2026-02-06: 创建接口文档
- 包含28个公共接口
- 分类整理并添加详细说明
