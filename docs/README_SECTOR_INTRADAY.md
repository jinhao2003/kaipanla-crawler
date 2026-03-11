# 板块分时数据功能说明

## 功能概述

`get_sector_intraday()` 函数用于获取板块的分时数据，包括每分钟的价格、成交量、成交额等详细信息。该功能可以帮助分析板块的日内走势和资金流向。

## API说明

### 函数签名

```python
def get_sector_intraday(self, sector_code, date=None):
    """
    获取板块分时数据
    
    Args:
        sector_code: 板块代码，如 "801346"
        date: 日期，格式YYYY-MM-DD，默认为当前日期
        
    Returns:
        dict: 包含分时价格和成交量数据
    """
```

### 参数说明

- **sector_code** (必需): 板块代码
  - 示例: "801346" (半导体板块)
  - 需要使用申万行业代码
  
- **date** (可选): 日期，格式为 "YYYY-MM-DD"
  - 如果不传，默认为当前日期
  - 只能查询交易日数据

### 返回值

返回一个字典，包含以下字段：

- **date**: 日期
- **sector_code**: 板块代码
- **open**: 开盘价
- **close**: 收盘价
- **high**: 最高价
- **low**: 最低价
- **preclose**: 昨收价
- **data**: DataFrame，包含分时数据
  - **time**: 时间（格式：HH:MM）
  - **price**: 价格
  - **volume**: 成交量（手）
  - **turnover**: 成交额（元）
  - **trend**: 涨跌标志
    - 0 = 下跌
    - 1 = 上涨
    - 2 = 平盘

## 使用示例

### 1. 基本用法

```python
from kaipanla_crawler import KaipanlaCrawler

crawler = KaipanlaCrawler()

# 获取半导体板块分时数据
data = crawler.get_sector_intraday("801346", "2026-01-16")

# 查看基本信息
print(f"开盘价: {data['open']}")
print(f"收盘价: {data['close']}")
print(f"涨跌幅: {(data['close'] - data['preclose']) / data['preclose'] * 100:.2f}%")

# 查看分时数据
print(data['data'])
```

### 2. 数据分析

```python
# 获取数据
data = crawler.get_sector_intraday("801346", "2026-01-16")
df = data['data']

# 价格统计
print(f"平均价: {df['price'].mean():.2f}")
print(f"最高价: {df['price'].max():.2f}")
print(f"最低价: {df['price'].min():.2f}")

# 成交统计
print(f"总成交量: {df['volume'].sum():,} 手")
print(f"总成交额: {df['turnover'].sum() / 1e8:.2f} 亿元")

# 涨跌统计
trend_counts = df['trend'].value_counts()
print(f"上涨分钟数: {trend_counts.get(1, 0)}")
print(f"下跌分钟数: {trend_counts.get(0, 0)}")
```

### 3. 时间段分析

```python
# 获取数据
data = crawler.get_sector_intraday("801346", "2026-01-16")
df = data['data']

# 早盘分析 (09:30-11:30)
morning = df[df['time'] <= '11:30']
print(f"早盘成交量: {morning['volume'].sum():,}")
print(f"早盘成交额: {morning['turnover'].sum() / 1e8:.2f} 亿元")

# 午盘分析 (13:00-15:00)
afternoon = df[df['time'] >= '13:00']
print(f"午盘成交量: {afternoon['volume'].sum():,}")
print(f"午盘成交额: {afternoon['turnover'].sum() / 1e8:.2f} 亿元")
```

### 4. 关键时刻识别

```python
# 获取数据
data = crawler.get_sector_intraday("801346", "2026-01-16")
df = data['data']

# 找出最高价时刻
max_price_idx = df['price'].idxmax()
max_price_time = df.loc[max_price_idx, 'time']
max_price = df.loc[max_price_idx, 'price']
print(f"最高价时刻: {max_price_time} ({max_price:.2f})")

# 找出最大成交量时刻
max_vol_idx = df['volume'].idxmax()
max_vol_time = df.loc[max_vol_idx, 'time']
max_vol = df.loc[max_vol_idx, 'volume']
print(f"最大成交量时刻: {max_vol_time} ({max_vol:,} 手)")
```

### 5. 趋势分析

```python
# 获取数据
data = crawler.get_sector_intraday("801346", "2026-01-16")
df = data['data']

# 计算移动平均
df['ma5'] = df['price'].rolling(5).mean()
df['ma10'] = df['price'].rolling(10).mean()

# 判断趋势
if df['ma5'].iloc[-1] > df['ma10'].iloc[-1]:
    print("短期趋势向上")
else:
    print("短期趋势向下")

# 计算涨跌幅
df['change_pct'] = (df['price'] - data['preclose']) / data['preclose'] * 100
print(f"当前涨跌幅: {df['change_pct'].iloc[-1]:.2f}%")
```

## 数据说明

### 数据来源

数据来自开盘啦APP的两个接口：

1. **GetTrendIncremental**: 获取价格分时数据
2. **GetVolTurIncremental**: 获取成交量成交额数据

### 数据特点

1. **时间频率**: 每分钟一条数据
2. **交易时间**: 
   - 早盘: 09:30-11:30
   - 午盘: 13:00-15:00
   - 共241条数据（包括集合竞价）
3. **实时性**: 交易日实时更新
4. **历史数据**: 可查询历史任意交易日

### 涨跌标志说明

- **0**: 下跌 - 当前价格低于前一分钟
- **1**: 上涨 - 当前价格高于前一分钟
- **2**: 平盘 - 当前价格等于前一分钟

## 常见板块代码

以下是一些常用的申万行业板块代码：

| 板块代码 | 板块名称 |
|---------|---------|
| 801346 | 半导体 |
| 801780 | 银行 |
| 801890 | 房地产 |
| 801010 | 农林牧渔 |
| 801020 | 采掘 |
| 801030 | 化工 |
| 801040 | 钢铁 |
| 801050 | 有色金属 |
| 801080 | 电子 |
| 801110 | 家用电器 |
| 801120 | 食品饮料 |
| 801130 | 纺织服装 |
| 801140 | 轻工制造 |
| 801150 | 医药生物 |
| 801160 | 公用事业 |
| 801170 | 交通运输 |
| 801180 | 房地产 |
| 801200 | 商业贸易 |
| 801210 | 休闲服务 |
| 801230 | 综合 |
| 801710 | 建筑材料 |
| 801720 | 建筑装饰 |
| 801730 | 电气设备 |
| 801740 | 国防军工 |
| 801750 | 计算机 |
| 801760 | 传媒 |
| 801770 | 通信 |
| 801790 | 非银金融 |
| 801880 | 汽车 |

## 应用场景

### 1. 盘中监控

```python
import time

crawler = KaipanlaCrawler()

while True:
    # 获取最新分时数据
    data = crawler.get_sector_intraday("801346")
    df = data['data']
    
    # 获取最新价格
    latest_price = df['price'].iloc[-1]
    change_pct = (latest_price - data['preclose']) / data['preclose'] * 100
    
    print(f"最新价: {latest_price:.2f}, 涨跌幅: {change_pct:+.2f}%")
    
    # 每分钟更新一次
    time.sleep(60)
```

### 2. 资金流向分析

```python
# 获取数据
data = crawler.get_sector_intraday("801346", "2026-01-16")
df = data['data']

# 计算主动买入和卖出
df['buy_amount'] = df.apply(lambda x: x['turnover'] if x['trend'] == 1 else 0, axis=1)
df['sell_amount'] = df.apply(lambda x: x['turnover'] if x['trend'] == 0 else 0, axis=1)

# 统计资金流向
total_buy = df['buy_amount'].sum()
total_sell = df['sell_amount'].sum()
net_inflow = total_buy - total_sell

print(f"主动买入: {total_buy / 1e8:.2f} 亿元")
print(f"主动卖出: {total_sell / 1e8:.2f} 亿元")
print(f"净流入: {net_inflow / 1e8:.2f} 亿元")
```

### 3. 异常波动检测

```python
# 获取数据
data = crawler.get_sector_intraday("801346", "2026-01-16")
df = data['data']

# 计算价格变化
df['price_change'] = df['price'].pct_change() * 100

# 检测异常波动（涨跌幅超过0.5%）
abnormal = df[abs(df['price_change']) > 0.5]

if len(abnormal) > 0:
    print("检测到异常波动:")
    for idx, row in abnormal.iterrows():
        print(f"  {row['time']}: {row['price_change']:+.2f}%")
```

### 4. 成交量异常检测

```python
# 获取数据
data = crawler.get_sector_intraday("801346", "2026-01-16")
df = data['data']

# 计算成交量均值和标准差
vol_mean = df['volume'].mean()
vol_std = df['volume'].std()

# 检测异常成交量（超过2倍标准差）
df['vol_zscore'] = (df['volume'] - vol_mean) / vol_std
abnormal_vol = df[abs(df['vol_zscore']) > 2]

if len(abnormal_vol) > 0:
    print("检测到异常成交量:")
    for idx, row in abnormal_vol.iterrows():
        print(f"  {row['time']}: {row['volume']:,} 手 (Z-score: {row['vol_zscore']:.2f})")
```

## 注意事项

1. **板块代码**: 需要使用正确的申万行业代码
2. **交易日**: 只有交易日才有数据
3. **数据延迟**: 实时数据可能有1-2分钟延迟
4. **请求频率**: 合理控制请求频率，避免对服务器造成压力
5. **数据完整性**: 收盘后数据更完整，建议收盘后查询

## 完整示例

参见 `examples/example_sector_intraday.py` 文件，包含完整的使用示例和数据分析代码。

## 相关功能

- `get_daily_data()`: 获取完整的市场行情数据
- `get_sector_ranking()`: 获取板块排行数据
- `get_limit_up_sectors()`: 获取涨停板块数据

## 更新日志

- **v1.3.0** (2026-01-19): 新增板块分时数据功能
