# 开盘啦爬虫更新日志

## 2026-01-20 - v1.1.0

### 新增功能

#### 1. 全市场连板梯队实时数据支持
- `get_market_limit_up_ladder()` 函数现在支持实时和历史数据
- **实时数据**: 不传 `date` 参数即可获取当前交易日实时连板情况
- **历史数据**: 传入 `date` 参数获取指定交易日连板情况

```python
# 获取实时数据
realtime_data = crawler.get_market_limit_up_ladder()

# 获取历史数据
historical_data = crawler.get_market_limit_up_ladder("2026-01-16")
```

#### 2. 打开高度标注识别
- 新增 `height_marks` 字段，单独记录打开高度标注股票（Tip=9）
- 打开高度标注股票不计入连板梯队统计
- 返回结构中新增 `is_height_mark` 标识

#### 3. 数据类型标识
- 新增 `is_realtime` 字段，标识数据是实时还是历史
- 便于区分数据来源和使用场景

### 修复问题

#### 1. 板块连板梯队 TDType 处理
- **修复前**: TDType=0 和 TDType=9 被错误地计入连板梯队
- **修复后**: 
  - TDType=0（反包板）单独记录在 `broken_stocks`，不计入连板梯队
  - TDType=9（打开高度标注）标记为 `is_height_mark=True`，不计入统计
  - 从 Tips 字段正确解析反包板的连板天数（如"3天2板" → 2连板）

#### 2. 全市场连板梯队异常处理
- 修复异常情况下返回结构不一致的问题
- 统一返回格式，包含所有必需字段

#### 3. 统计逻辑修正
- 排除反包板后再统计连板梯队分布
- 确保 `total_limit_up` 只统计正常连板股票
- 修正连板率计算逻辑

### API 变更

#### get_market_limit_up_ladder()

**新增返回字段**:
```python
{
    "date": "2026-01-20",
    "is_realtime": True,  # 新增：标识是否为实时数据
    "ladder": {...},
    "broken_stocks": [...],
    "height_marks": [...],  # 新增：打开高度标注股票列表
    "statistics": {...}
}
```

**API 端点**:
- 实时数据: `https://apphwhq.longhuvip.com/w1/api/index.php`
- 历史数据: `https://apphis.longhuvip.com/w1/api/index.php`

#### get_sector_limit_up_ladder()

**修复返回结构**:
```python
{
    "date": "2026-01-16",
    "is_realtime": False,
    "sectors": [
        {
            "sector_name": "板块名称",
            "stocks": [...],  # 正常连板股票
            "broken_stocks": [...]  # 反包板股票（不计入连板梯队）
        }
    ]
}
```

### 测试覆盖

新增测试文件:
- `test_realtime_market_ladder.py`: 测试实时数据获取
- `test_broken_board_handling.py`: 测试反包板处理逻辑
- 更新 `test_sector_limit_up_ladder.py`: 修正统计测试

测试结果:
- ✅ 实时数据获取正常
- ✅ 历史数据获取正常
- ✅ 反包板正确识别和排除
- ✅ 打开高度标注正确识别
- ✅ 数据结构完整性验证通过
- ✅ 统计逻辑正确

### 文档更新

- 更新 `全市场连板梯队功能说明.md`
  - 新增实时数据使用示例
  - 新增打开高度标注说明
  - 更新返回数据结构文档
  - 新增实时 vs 历史数据对比说明

- 更新主模块帮助文本
  - 标注实时和历史数据支持
  - 更新使用示例

### 向后兼容性

✅ 完全向后兼容
- 原有调用方式不受影响
- 新增字段不影响现有代码
- 默认行为保持一致

### 升级建议

如果您使用了以下功能，建议更新代码以利用新特性:

1. **全市场连板梯队**:
   ```python
   # 旧代码（仍然有效）
   data = crawler.get_market_limit_up_ladder("2026-01-16")
   
   # 新代码（支持实时）
   realtime = crawler.get_market_limit_up_ladder()  # 实时数据
   historical = crawler.get_market_limit_up_ladder("2026-01-16")  # 历史数据
   
   # 检查数据类型
   if data['is_realtime']:
       print("这是实时数据")
   ```

2. **处理打开高度标注**:
   ```python
   data = crawler.get_market_limit_up_ladder()
   
   # 新增：处理打开高度标注
   if data['height_marks']:
       print(f"打开高度标注: {len(data['height_marks'])}只")
       for stock in data['height_marks']:
           print(f"  {stock['stock_name']}")
   ```

3. **板块连板梯队反包板处理**:
   ```python
   data = crawler.get_sector_limit_up_ladder("2026-01-16")
   
   for sector in data['sectors']:
       # 正常连板股票
       print(f"{sector['sector_name']}: {len(sector['stocks'])}只")
       
       # 新增：反包板股票
       if sector.get('broken_stocks'):
           print(f"  反包板: {len(sector['broken_stocks'])}只")
   ```

### 已知问题

- 2026-01-17 的历史数据返回错误码 1020（可能是非交易日或数据未更新）

### 下一步计划

- [ ] 添加更多板块分析功能
- [ ] 支持批量日期查询优化
- [ ] 添加数据缓存机制
- [ ] 支持更多市场指标

---

## 2026-01-19 - v1.0.0

### 初始版本

- 实现基础数据爬取功能
- 支持涨跌统计、大盘指数、连板梯队等数据获取
- 支持板块和个股分时数据
- 支持异动个股监控
- 支持多头空头风向标
- 支持涨停原因板块数据
