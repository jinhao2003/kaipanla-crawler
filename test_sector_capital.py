#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试板块资金成交额数据获取功能

测试内容：
1. 获取板块实时资金数据
2. 获取板块历史资金数据
3. 数据格式验证
"""

from kaipanla_crawler import KaipanlaCrawler
from datetime import datetime


def test_realtime_sector_capital():
    """测试1: 获取板块实时资金数据"""
    print("=" * 60)
    print("测试1: 获取板块实时资金数据")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 测试化工板块（801235）
    sector_code = "801235"
    print(f"\n获取板块 {sector_code} 的实时资金数据...")
    
    data = crawler.get_sector_capital_data(sector_code)
    
    if not data:
        print("❌ 获取数据失败")
        return False
    
    print(f"\n✓ 成功获取数据")
    print(f"板块代码: {data['sector_code']}")
    print(f"日期: {data['date']}")
    print(f"成交额: {data['turnover'] / 100000000:.2f}亿元")
    print(f"涨跌幅: {data['change_pct']:.2f}%")
    print(f"市值: {data['market_cap']:.2f}亿元")
    print(f"主力净额: {data['main_net_inflow'] / 100000000:.2f}亿元")
    print(f"主力净占比: {data['main_net_inflow_pct']:.2f}%")
    print(f"上涨家数: {data['up_count']}")
    print(f"下跌家数: {data['down_count']}")
    print(f"平盘家数: {data['flat_count']}")
    print(f"流通市值: {data['circulating_market_cap'] / 100000000:.2f}亿元")
    print(f"总市值: {data['total_market_cap'] / 100000000:.2f}亿元")
    print(f"换手率: {data['turnover_rate']:.2f}%")
    
    return True


def test_historical_sector_capital():
    """测试2: 获取板块历史资金数据"""
    print("\n" + "=" * 60)
    print("测试2: 获取板块历史资金数据")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 测试化工板块（801235）
    sector_code = "801235"
    date = "2026-01-16"
    print(f"\n获取板块 {sector_code} 在 {date} 的资金数据...")
    
    data = crawler.get_sector_capital_data(sector_code, date)
    
    if not data:
        print("❌ 获取数据失败")
        return False
    
    print(f"\n✓ 成功获取数据")
    print(f"板块代码: {data['sector_code']}")
    print(f"日期: {data['date']}")
    print(f"成交额: {data['turnover'] / 100000000:.2f}亿元")
    print(f"涨跌幅: {data['change_pct']:.2f}%")
    print(f"主力净额: {data['main_net_inflow'] / 100000000:.2f}亿元")
    
    return True


def test_multiple_sectors():
    """测试3: 获取多个板块的资金数据"""
    print("\n" + "=" * 60)
    print("测试3: 获取多个板块的资金数据")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 测试多个板块
    sectors = {
        "801235": "化工",
        "801346": "电力设备",
        "801225": "机械设备"
    }
    
    print(f"\n获取 {len(sectors)} 个板块的实时资金数据...\n")
    
    results = []
    for sector_code, sector_name in sectors.items():
        data = crawler.get_sector_capital_data(sector_code)
        if data:
            results.append({
                "板块名称": sector_name,
                "板块代码": sector_code,
                "成交额(亿)": data['turnover'] / 100000000,
                "涨跌幅(%)": data['change_pct'],
                "主力净额(亿)": data['main_net_inflow'] / 100000000,
                "主力净占比(%)": data['main_net_inflow_pct']
            })
    
    if not results:
        print("❌ 未获取到任何数据")
        return False
    
    print("✓ 成功获取数据\n")
    print(f"{'板块名称':<10} {'成交额(亿)':<12} {'涨跌幅(%)':<10} {'主力净额(亿)':<12} {'主力净占比(%)':<12}")
    print("-" * 70)
    for r in results:
        print(f"{r['板块名称']:<10} {r['成交额(亿)']:<12.2f} {r['涨跌幅(%)']:<10.2f} {r['主力净额(亿)']:<12.2f} {r['主力净占比(%)']:<12.2f}")
    
    return True


def test_data_validation():
    """测试4: 数据格式验证"""
    print("\n" + "=" * 60)
    print("测试4: 数据格式验证")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    sector_code = "801235"
    data = crawler.get_sector_capital_data(sector_code)
    
    if not data:
        print("❌ 获取数据失败")
        return False
    
    # 验证必需字段
    required_fields = [
        'sector_code', 'date', 'turnover', 'change_pct', 'market_cap',
        'main_net_inflow', 'up_count', 'down_count', 'flat_count',
        'circulating_market_cap', 'total_market_cap', 'turnover_rate',
        'main_net_inflow_pct'
    ]
    
    print("\n验证数据字段...")
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    
    if missing_fields:
        print(f"❌ 缺失字段: {missing_fields}")
        return False
    
    print("✓ 所有必需字段完整")
    
    # 验证数据类型
    print("\n验证数据类型...")
    type_checks = [
        ('turnover', (int, float)),
        ('change_pct', (int, float)),
        ('market_cap', (int, float)),
        ('main_net_inflow', (int, float)),
        ('up_count', int),
        ('down_count', int),
        ('flat_count', int),
    ]
    
    for field, expected_type in type_checks:
        if not isinstance(data[field], expected_type):
            print(f"❌ 字段 {field} 类型错误: 期望 {expected_type}, 实际 {type(data[field])}")
            return False
    
    print("✓ 所有字段类型正确")
    
    # 验证数值范围
    print("\n验证数值范围...")
    if data['turnover'] < 0:
        print(f"❌ 成交额不应为负数: {data['turnover']}")
        return False
    
    if data['up_count'] < 0 or data['down_count'] < 0 or data['flat_count'] < 0:
        print(f"❌ 涨跌家数不应为负数")
        return False
    
    print("✓ 数值范围合理")
    
    return True


if __name__ == "__main__":
    print("开始测试板块资金成交额数据获取功能\n")
    
    tests = [
        ("获取板块实时资金数据", test_realtime_sector_capital),
        ("获取板块历史资金数据", test_historical_sector_capital),
        ("获取多个板块的资金数据", test_multiple_sectors),
        ("数据格式验证", test_data_validation),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # 输出测试总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\n通过率: {passed}/{total} ({passed/total*100:.1f}%)")
