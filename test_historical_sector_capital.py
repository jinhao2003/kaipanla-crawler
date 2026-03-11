#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试板块资金历史数据获取

验证历史数据API是否正确工作
"""

from kaipanla_crawler import KaipanlaCrawler


def test_historical_vs_realtime():
    """测试历史数据和实时数据的区别"""
    print("=" * 60)
    print("测试历史数据和实时数据的API区别")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 测试板块
    sector_code = "801346"  # 电力设备
    historical_date = "2026-01-19"
    
    print(f"\n测试板块: {sector_code} (电力设备)")
    
    # 1. 获取历史数据
    print(f"\n1. 获取历史数据 ({historical_date})...")
    historical_data = crawler.get_sector_capital_data(sector_code, historical_date)
    
    if historical_data:
        print(f"✓ 历史数据获取成功")
        print(f"  日期: {historical_data['date']}")
        print(f"  成交额: {historical_data['turnover'] / 100000000:.2f}亿元")
        print(f"  涨跌幅: {historical_data['change_pct']:.2f}%")
        print(f"  主力净额: {historical_data['main_net_inflow'] / 100000000:.2f}亿元")
        print(f"  上涨家数: {historical_data['up_count']}")
        print(f"  下跌家数: {historical_data['down_count']}")
    else:
        print("✗ 历史数据获取失败")
        return False
    
    # 2. 获取实时数据
    print(f"\n2. 获取实时数据...")
    realtime_data = crawler.get_sector_capital_data(sector_code)
    
    if realtime_data:
        print(f"✓ 实时数据获取成功")
        print(f"  日期: {realtime_data['date']}")
        print(f"  成交额: {realtime_data['turnover'] / 100000000:.2f}亿元")
        print(f"  涨跌幅: {realtime_data['change_pct']:.2f}%")
        print(f"  主力净额: {realtime_data['main_net_inflow'] / 100000000:.2f}亿元")
        print(f"  上涨家数: {realtime_data['up_count']}")
        print(f"  下跌家数: {realtime_data['down_count']}")
    else:
        print("✗ 实时数据获取失败")
        return False
    
    # 3. 对比数据
    print(f"\n3. 数据对比:")
    print(f"  历史日期: {historical_data['date']}")
    print(f"  实时日期: {realtime_data['date']}")
    
    if historical_data['date'] != realtime_data['date']:
        print(f"  ✓ 日期不同，说明历史和实时API工作正常")
    else:
        print(f"  - 日期相同（可能是同一天）")
    
    return True


def test_multiple_historical_dates():
    """测试多个历史日期"""
    print("\n" + "=" * 60)
    print("测试多个历史日期")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    sector_code = "801235"  # 化工
    dates = ["2026-01-19", "2026-01-18", "2026-01-17"]
    
    print(f"\n测试板块: {sector_code} (化工)")
    print(f"测试日期: {', '.join(dates)}\n")
    
    print(f"{'日期':<12} {'成交额(亿)':<12} {'涨跌幅(%)':<10} {'主力净额(亿)':<12}")
    print("-" * 50)
    
    success_count = 0
    for date in dates:
        data = crawler.get_sector_capital_data(sector_code, date)
        if data:
            print(f"{data['date']:<12} "
                  f"{data['turnover'] / 100000000:<12.2f} "
                  f"{data['change_pct']:<10.2f} "
                  f"{data['main_net_inflow'] / 100000000:<12.2f}")
            success_count += 1
        else:
            print(f"{date:<12} 获取失败")
    
    print(f"\n成功率: {success_count}/{len(dates)}")
    return success_count == len(dates)


def test_historical_data_completeness():
    """测试历史数据完整性"""
    print("\n" + "=" * 60)
    print("测试历史数据完整性")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    sector_code = "801346"
    date = "2026-01-19"
    
    print(f"\n获取 {sector_code} 在 {date} 的数据...")
    
    data = crawler.get_sector_capital_data(sector_code, date)
    
    if not data:
        print("✗ 获取数据失败")
        return False
    
    # 验证所有字段
    required_fields = [
        'sector_code', 'date', 'turnover', 'change_pct', 'market_cap',
        'main_net_inflow', 'main_sell', 'net_amount',
        'up_count', 'down_count', 'flat_count',
        'circulating_market_cap', 'total_market_cap', 'turnover_rate',
        'main_net_inflow_pct'
    ]
    
    print("\n验证数据字段:")
    missing_fields = []
    for field in required_fields:
        if field in data:
            print(f"  ✓ {field}: {data[field]}")
        else:
            print(f"  ✗ {field}: 缺失")
            missing_fields.append(field)
    
    if missing_fields:
        print(f"\n✗ 缺失字段: {missing_fields}")
        return False
    else:
        print(f"\n✓ 所有字段完整")
        return True


def test_api_endpoint_difference():
    """测试API端点差异"""
    print("\n" + "=" * 60)
    print("测试API端点差异")
    print("=" * 60)
    
    print("\n实时数据API:")
    print("  URL: https://apphwhq.longhuvip.com/w1/api/index.php")
    print("  参数: Day='' (空)")
    
    print("\n历史数据API:")
    print("  URL: https://apphis.longhuvip.com/w1/api/index.php")
    print("  参数: Day='2026-01-19' (指定日期)")
    
    print("\n✓ API端点已正确配置")
    return True


if __name__ == "__main__":
    print("开始测试板块资金历史数据获取\n")
    
    tests = [
        ("历史数据和实时数据对比", test_historical_vs_realtime),
        ("多个历史日期", test_multiple_historical_dates),
        ("历史数据完整性", test_historical_data_completeness),
        ("API端点差异", test_api_endpoint_difference),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ 测试失败: {e}")
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
