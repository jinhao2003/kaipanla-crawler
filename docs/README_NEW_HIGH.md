# 百日新高数据功能说明

## 功能概述

`get_new_high_data()` 函数用于获取百日新高股票的今日新增数量数据。该功能可以帮助分析市场强度和趋势。

## API说明

### 函数签名

```python
def get_new_high_data(self, end_date, start_date=None):
    """
    获取百日新高数据
    
    Args:
        end_date: 结束日期，格式YYYY-MM-DD
        start_date: 起始日期，格式YYYY-MM-DD，可选
        
    Returns:
        pd.Series: 索引为日期，值为今日新增新高数量
    """
```

### 参数说明

- **end_date** (必需): 结束日期，格式为 "YYYY-MM-DD"
- **start_date** (可选): 起始日期，格式为 "YYYY-MM-DD"
  - 如果不传，返回单日数值
  - 如果传入，返回日期范围的Series

### 返回值

- **单日查询**: 返回整数值，表示当日新增的百日新高股票数量
- **范围查询**: 返回pandas Series，索引为日期，值为每日新增数量

## 使用示例

### 1. 获取单日数据

```python
from kaipanla_crawler import KaipanlaCrawler

crawler = KaipanlaCrawler()
count = crawler.get_new_high_data("2026-01-16")
print(f"2026-01-16 今日新增: {count} 只")
# 输出: 2026-01-16 今日新增: 127 只
```

### 2. 获取日期范围数据

```python
data = crawler.get_new_high_data("2026-01-16", "2026-01-10")
print(data)
# 输出:
# 日期
# 2026-01-10    143
# 2026-01-13    130
# 2026-01-14    161
# 2026-01-15     98
# 2026-01-16    127
# Name: 今日新增, dtype: int64
```

### 3. 数据分析

```python
# 获取最近一周数据
data = crawler.get_new_high_data("2026-01-16", "2026-01-09")

# 统计分析
print(f"平均每日新增: {data.mean():.1f} 只")
print(f"最大新增: {data.max()} 只")
print(f"最小新增: {data.min()} 只")
print(f"总计: {data.sum()} 只")

# 找出新增最多的日期
max_date = data.idxmax()
print(f"新增最多的日期: {max_date} ({data[max_date]} 只)")
```

### 4. 趋势分析

```python
# 获取数据
data = crawler.get_new_high_data("2026-01-16", "2026-01-09")

# 计算变化
change = data.iloc[-1] - data.iloc[0]
change_pct = (change / data.iloc[0]) * 100

if change > 0:
    print(f"📈 新高数量上升 {change} 只 ({change_pct:+.1f}%)")
else:
    print(f"📉 新高数量下降 {abs(change)} 只 ({change_pct:+.1f}%)")
```

## 数据说明

### 数据来源

数据来自开盘啦APP的百日新高接口，包含：
- **日期**: 交易日期
- **新高数量**: 当日创百日新高的股票总数
- **今日新增**: 当日新增的百日新高股票数量（本函数返回此字段）

### 数据格式

API返回的原始数据格式为：
```
"20260116_478_127_0"
```

字段说明：
- `20260116`: 日期（2026年1月16日）
- `478`: 百日新高股票总数
- `127`: 今日新增数量（本函数提取此值）
- `0`: 保留字段

### 数据特点

1. **只包含交易日**: 周末和节假日没有数据
2. **实时更新**: 数据在交易日实时更新
3. **历史数据**: 可以查询历史任意交易日的数据

## 应用场景

### 1. 市场强度分析

```python
# 获取最近一个月数据
data = crawler.get_new_high_data("2026-01-16", "2025-12-16")

# 判断市场强度
avg = data.mean()
if avg > 200:
    print("🔥 市场强势，新高股票数量较多")
elif avg > 100:
    print("📊 市场中性")
else:
    print("❄️ 市场偏弱")
```

### 2. 趋势判断

```python
# 获取数据
data = crawler.get_new_high_data("2026-01-16", "2026-01-02")

# 计算移动平均
ma5 = data.rolling(5).mean()
ma10 = data.rolling(10).mean()

# 判断趋势
if ma5.iloc[-1] > ma10.iloc[-1]:
    print("📈 短期趋势向上")
else:
    print("📉 短期趋势向下")
```

### 3. 异常检测

```python
# 获取数据
data = crawler.get_new_high_data("2026-01-16", "2025-12-01")

# 计算标准差
std = data.std()
mean = data.mean()

# 检测异常值
for date, value in data.items():
    if value > mean + 2 * std:
        print(f"⚠️ {date}: 新高数量异常偏高 ({value} 只)")
    elif value < mean - 2 * std:
        print(f"⚠️ {date}: 新高数量异常偏低 ({value} 只)")
```

## 注意事项

1. **日期格式**: 必须使用 "YYYY-MM-DD" 格式
2. **交易日**: 只有交易日才有数据，周末和节假日会被自动过滤
3. **数据延迟**: 建议在收盘后查询，数据更完整
4. **请求频率**: 合理控制请求频率，避免对服务器造成压力

## 完整示例

参见 `examples/example_new_high.py` 文件，包含完整的使用示例和数据分析代码。

## 相关功能

- `get_daily_data()`: 获取完整的市场行情数据
- `get_limit_up_sectors()`: 获取涨停板块数据
- `get_sector_ranking()`: 获取板块排行数据

## 更新日志

- **v1.2.0** (2026-01-19): 新增百日新高数据功能
