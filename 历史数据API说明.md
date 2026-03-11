# 板块资金历史数据API说明

## 更新日期
2026-01-20

## API端点区别

### 实时数据API
```
URL: https://apphwhq.longhuvip.com/w1/api/index.php
参数: Day='' (空字符串)
返回: 当前交易日的实时数据
```

### 历史数据API
```
URL: https://apphis.longhuvip.com/w1/api/index.php
参数: Day='2026-01-19' (指定日期)
返回: 指定日期的历史数据
```

## 数据格式差异

### 实时数据pankou数组（12个元素）
```python
[
    成交额,           # pankou[0] - 元
    涨跌幅,           # pankou[1] - %
    市值,            # pankou[2] - 亿元
    主力净额,         # pankou[3] - 元
    主卖,            # pankou[4] - 元
    净额,            # pankou[5] - 元
    上涨家数,         # pankou[6] - 只
    下跌家数,         # pankou[7] - 只
    平盘家数,         # pankou[8] - 只
    流通市值,         # pankou[9] - 元
    总市值,          # pankou[10] - 元
    换手率           # pankou[11] - %
]
```

### 历史数据pankou数组（11个元素）
```python
[
    成交额,           # pankou[0] - 元
    涨跌幅,           # pankou[1] - %
    市值,            # pankou[2] - 亿元
    主力净额,         # pankou[3] - 元
    主卖,            # pankou[4] - 元
    净额,            # pankou[5] - 元
    上涨家数,         # pankou[6] - 只
    下跌家数,         # pankou[7] - 只
    平盘家数,         # pankou[8] - 只
    流通市值,         # pankou[9] - 元
    总市值           # pankou[10] - 元
]
```

**注意**: 历史数据**没有换手率字段**（pankou[11]）

## 代码实现

`get_sector_capital_data()` 函数会自动根据是否传入日期参数来选择正确的API：

```python
def get_sector_capital_data(self, sector_code, date=None, timeout=60):
    # 根据是否传入日期，选择不同的API地址和headers
    if date:
        # 历史数据：使用 apphis.longhuvip.com
        url = self.base_url
        headers = self.headers
    else:
        # 实时数据：使用 apphwhq.longhuvip.com
        url = self.sector_base_url
        headers = self.sector_headers
    
    # ... 其余代码
```

## 使用示例

### 获取实时数据
```python
from kaipanla_crawler import KaipanlaCrawler

crawler = KaipanlaCrawler()

# 不传date参数，获取实时数据
data = crawler.get_sector_capital_data("801346")

print(f"日期: {data['date']}")  # 当前交易日
print(f"成交额: {data['turnover'] / 100000000:.2f}亿元")
print(f"换手率: {data['turnover_rate']:.2f}%")  # 实时数据有换手率
```

### 获取历史数据
```python
from kaipanla_crawler import KaipanlaCrawler

crawler = KaipanlaCrawler()

# 传入date参数，获取历史数据
data = crawler.get_sector_capital_data("801346", "2026-01-19")

print(f"日期: {data['date']}")  # 2026-01-19
print(f"成交额: {data['turnover'] / 100000000:.2f}亿元")
print(f"换手率: {data['turnover_rate']:.2f}%")  # 历史数据换手率为0
```

## 测试结果

### 测试1: 历史数据和实时数据对比
```
测试板块: 801346 (电力设备)

1. 获取历史数据 (2026-01-19)...
✓ 历史数据获取成功
  日期: 2026-01-19
  成交额: 3776.44亿元
  涨跌幅: 4.10%
  主力净额: 565.56亿元
  上涨家数: 370
  下跌家数: 77

2. 获取实时数据...
✓ 实时数据获取成功
  日期: 2026-01-20
  成交额: 3775.54亿元
  涨跌幅: 4.13%
  主力净额: 532.86亿元
  上涨家数: 162
  下跌家数: 282

3. 数据对比:
  历史日期: 2026-01-19
  实时日期: 2026-01-20
  ✓ 日期不同，说明历史和实时API工作正常
```

### 测试2: 历史数据完整性
```
获取 801346 在 2026-01-19 的数据...

验证数据字段:
  ✓ sector_code: 801346
  ✓ date: 2026-01-19
  ✓ turnover: 377644155126.0
  ✓ change_pct: 4.10354
  ✓ market_cap: 134.696
  ✓ main_net_inflow: 56555582971.0
  ✓ main_sell: -49410616918.0
  ✓ net_amount: 7144966053.0
  ✓ up_count: 370
  ✓ down_count: 77
  ✓ flat_count: 3
  ✓ circulating_market_cap: 9202884637632.0
  ✓ total_market_cap: 10361511229952.0
  ✓ turnover_rate: 0  # 历史数据换手率为0
  ✓ main_net_inflow_pct: 14.98%

✓ 所有字段完整
```

## 错误码说明

### errcode: 1020
表示数据不可用，可能的原因：
- 非交易日（周末、节假日）
- 该日期数据尚未生成
- 板块代码不存在

### 处理建议
```python
data = crawler.get_sector_capital_data("801235", "2026-01-18")

if not data:
    print("数据获取失败，可能是非交易日")
else:
    print(f"成交额: {data['turnover'] / 100000000:.2f}亿元")
```

## 注意事项

1. **换手率字段**: 历史数据的换手率字段为0，实时数据才有真实值
2. **API地址**: 实时和历史使用不同的API地址
3. **日期格式**: 必须是 `YYYY-MM-DD` 格式
4. **交易日**: 只能查询交易日数据
5. **超时设置**: 默认60秒，可以调整timeout参数

## 完整示例

```python
from kaipanla_crawler import KaipanlaCrawler
from datetime import datetime, timedelta

crawler = KaipanlaCrawler()

# 获取最近5个交易日的数据
sector_code = "801346"  # 电力设备
end_date = datetime.now()

print(f"{'日期':<12} {'成交额(亿)':<12} {'涨跌幅(%)':<10} {'主力净额(亿)':<12}")
print("-" * 50)

for i in range(10):  # 尝试10天，确保获取到5个交易日
    date = (end_date - timedelta(days=i)).strftime("%Y-%m-%d")
    data = crawler.get_sector_capital_data(sector_code, date)
    
    if data:
        print(f"{data['date']:<12} "
              f"{data['turnover'] / 100000000:<12.2f} "
              f"{data['change_pct']:<10.2f} "
              f"{data['main_net_inflow'] / 100000000:<12.2f}")
```

## 更新日志

- **2026-01-20**: 
  - ✅ 修复历史数据API支持
  - ✅ 自动区分实时和历史API端点
  - ✅ 处理历史数据pankou数组只有11个元素的情况
  - ✅ 换手率字段在历史数据中默认为0
