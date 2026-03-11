# 多头空头风向标功能说明

## 功能概述

`get_sentiment_indicator()` 函数用于获取市场多头空头风向标数据，通过分析特定板块的股票排序，识别市场情绪的多空方向。

## API接口

**接口名称**: `PlateIntroduction_Info`

**请求方式**: POST

**接口地址**: `https://apphwhq.longhuvip.com/w1/api/index.php`

## 函数签名

```python
def get_sentiment_indicator(self, plate_id="801225", stocks=None)
```

## 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| plate_id | str | 否 | "801225" | 板块ID |
| stocks | list | 否 | None | 股票代码列表，不提供则使用默认列表 |

### 默认股票列表

如果不提供 `stocks` 参数，函数将使用以下默认股票列表（27只）：

```python
[
    "002112", "603667", "600550", "601179", "600089", "600879", "603986",
    "002156", "002202", "002050", "002865", "002413", "002716", "000559",
    "000981", "002131", "603938", "603650", "000547", "600362", "600266",
    "600410", "002195", "603000", "001255", "000681", "002465"
]
```

## 返回值

返回一个字典，包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| date | str | 日期（格式：YYYY-MM-DD） |
| plate_id | str | 板块ID |
| bullish_codes | list | 多头风向标股票代码列表（前3只） |
| bearish_codes | list | 空头风向标股票代码列表（后3只） |
| all_stocks | list | 所有股票代码列表 |

## 使用示例

### 示例1: 基本使用

```python
from kaipanla_crawler import KaipanlaCrawler

crawler = KaipanlaCrawler()
data = crawler.get_sentiment_indicator()

print(f"日期: {data['date']}")
print(f"多头风向标: {data['bullish_codes']}")
print(f"空头风向标: {data['bearish_codes']}")
```

**输出示例**:
```
日期: 2026-01-19
多头风向标: ['002112', '603667', '600550']
空头风向标: ['001255', '000681', '002465']
```

### 示例2: 使用自定义股票列表

```python
# 使用自定义股票列表（例如：白酒、银行、地产等）
custom_stocks = [
    "600519",  # 贵州茅台
    "000858",  # 五粮液
    "601318",  # 中国平安
    "600036",  # 招商银行
    "000333",  # 美的集团
    "601888"   # 中国中免
]

data = crawler.get_sentiment_indicator(stocks=custom_stocks)

print("多头风向标:")
for code in data['bullish_codes']:
    print(f"  {code}")

print("\n空头风向标:")
for code in data['bearish_codes']:
    print(f"  {code}")
```

### 示例3: 遍历所有股票

```python
data = crawler.get_sentiment_indicator()

print(f"股票总数: {len(data['all_stocks'])}")
print(f"所有股票: {', '.join(data['all_stocks'])}")
```

## 数据说明

### 多头风向标（Bullish Indicators）

- 定义：股票列表中排名前3的股票
- 含义：这些股票通常表现较强，代表市场多头力量
- 用途：可作为市场情绪的正向参考指标

### 空头风向标（Bearish Indicators）

- 定义：股票列表中排名后3的股票
- 含义：这些股票通常表现较弱，代表市场空头力量
- 用途：可作为市场情绪的反向参考指标

## 应用场景

1. **市场情绪分析**
   - 通过对比多头和空头风向标的表现，判断市场整体情绪
   - 观察风向标股票的涨跌幅变化

2. **板块轮动分析**
   - 跟踪不同板块的风向标变化
   - 识别资金流向和板块轮动趋势

3. **风险预警**
   - 当多头风向标转弱时，可能预示市场风险
   - 当空头风向标转强时，可能预示市场反转

## 注意事项

1. **数据时效性**
   - 函数返回的是实时数据
   - 建议在交易时间内调用以获取最新数据

2. **股票代码格式**
   - 股票代码不需要加市场前缀（如SH、SZ）
   - 直接使用6位数字代码即可

3. **API限制**
   - 请合理控制请求频率
   - 避免短时间内大量请求

4. **数据完整性**
   - 函数只返回股票代码，不包含股票名称、价格等详细信息
   - 如需详细信息，可结合其他API接口获取

## 错误处理

函数内置了错误处理机制：

- 网络请求失败时，返回空列表
- API返回错误时，打印错误信息并返回空列表
- 数据解析失败时，使用输入的股票列表作为备选

## 相关函数

- `get_daily_data()`: 获取市场整体数据
- `get_sector_ranking()`: 获取板块排行
- `get_abnormal_stocks()`: 获取异动股票

## 完整示例

查看 `examples/example_sentiment_indicator.py` 获取完整的使用示例。

## 测试

运行测试文件验证功能：

```bash
python tests/test_sentiment_indicator.py
```

## 更新日志

- **v1.6.0** (2026-01-19): 首次发布多头空头风向标功能
