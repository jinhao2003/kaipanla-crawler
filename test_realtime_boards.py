#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试实时连板数据获取功能

测试内容：
1. 获取实时连板梯队指数
2. 获取实时实际涨跌停数据
3. 获取实时首板股票
4. 获取实时所有连板股票
"""

from kaipanla_crawler import KaipanlaCrawler


def test_realtime_limit_up_index():
    """测试1: 获取实时连板梯队指数"""
    print("=" * 60)
    print("测试1: 获取实时连板梯队指数")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    print("\n获取实时连板梯队指数...\n")
    
    data = crawler.get_realtime_limit_up_index()
    
    if not data:
        print("✗ 获取数据失败")
        return False
    
    print("✓ 成功获取数据\n")
    print(f"首板: {data.get('first_board', 0)}只")
    print(f"二板: {data.get('second_board', 0)}只")
    print(f"三板: {data.get('third_board', 0)}只")
    print(f"四板以上: {data.get('fourth_board_plus', 0)}只")
    print(f"总涨停数: {data.get('total_limit_up', 0)}只")
    print(f"连板率: {data.get('consecutive_rate', 0):.2f}%")
    
    return True


def test_realtime_actual_limit_up_down():
    """测试2: 获取实时实际涨跌停数据"""
    print("\n" + "=" * 60)
    print("测试2: 获取实时实际涨跌停数据")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    print("\n获取实时实际涨跌停数据...\n")
    
    data = crawler.get_realtime_actual_limit_up_down()
    
    if not data:
        print("✗ 获取数据失败")
        return False
    
    print("✓ 成功获取数据\n")
    print(f"实际涨停: {data.get('actual_limit_up', 0)}只")
    print(f"实际跌停: {data.get('actual_limit_down', 0)}只")
    print(f"涨停（含一字板）: {data.get('limit_up', 0)}只")
    print(f"跌停（含一字板）: {data.get('limit_down', 0)}只")
    
    return True


def test_realtime_board_stocks():
    """测试3: 获取实时各连板股票"""
    print("\n" + "=" * 60)
    print("测试3: 获取实时各连板股票")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    board_names = {
        1: "首板",
        2: "二板",
        3: "三板",
        4: "四板",
        5: "五板及以上"
    }
    
    print("\n获取各连板股票...\n")
    
    results = {}
    for board_type, board_name in board_names.items():
        print(f"获取{board_name}股票...")
        stocks = crawler.get_realtime_board_stocks(board_type)
        results[board_type] = stocks
        print(f"  ✓ {board_name}: {len(stocks)}只")
        
        # 显示前3只股票
        if stocks:
            for i, stock in enumerate(stocks[:3], 1):
                print(f"    {i}. {stock['stock_name']} ({stock['stock_code']})")
    
    total = sum(len(stocks) for stocks in results.values())
    print(f"\n总计: {total}只涨停股票")
    
    return total > 0


def test_realtime_all_boards_stocks():
    """测试4: 获取实时所有连板股票（一次性）"""
    print("\n" + "=" * 60)
    print("测试4: 获取实时所有连板股票（一次性）")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    print("\n")
    
    data = crawler.get_realtime_all_boards_stocks()
    
    if not data:
        print("✗ 获取数据失败")
        return False
    
    print("\n✓ 成功获取数据\n")
    
    stats = data.get('statistics', {})
    print(f"首板: {stats.get('first_board_count', 0)}只")
    print(f"二板: {stats.get('second_board_count', 0)}只")
    print(f"三板: {stats.get('third_board_count', 0)}只")
    print(f"四板: {stats.get('fourth_board_count', 0)}只")
    print(f"五板以上: {stats.get('fifth_board_plus_count', 0)}只")
    print(f"总计: {stats.get('total_stocks', 0)}只")
    print(f"连板率: {stats.get('consecutive_rate', 0):.2f}%")
    
    # 显示五板以上的股票（龙头）
    if data.get('fifth_board_plus'):
        print(f"\n五板以上股票（龙头）:")
        for stock in data['fifth_board_plus']:
            print(f"  - {stock['stock_name']} ({stock['stock_code']})")
    
    return True


def test_compare_with_daily_data():
    """测试5: 对比实时数据和历史数据"""
    print("\n" + "=" * 60)
    print("测试5: 对比实时数据和历史数据")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    print("\n获取实时和历史数据进行对比...\n")
    
    # 获取实时连板数据
    realtime_boards = crawler.get_realtime_all_boards_stocks()
    
    # 获取今日历史数据
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    daily_data = crawler.get_daily_data(today)
    
    if not realtime_boards or daily_data is None or daily_data.empty:
        print("✗ 数据获取失败")
        return False
    
    print("✓ 数据对比\n")
    
    realtime_stats = realtime_boards.get('statistics', {})
    
    print(f"{'数据源':<15} {'涨停数':<10} {'首板':<10} {'连板率':<10}")
    print("-" * 50)
    print(f"{'实时数据':<15} "
          f"{realtime_stats.get('total_stocks', 0):<10} "
          f"{realtime_stats.get('first_board_count', 0):<10} "
          f"{realtime_stats.get('consecutive_rate', 0):<10.2f}%")
    
    if not daily_data.empty:
        print(f"{'历史数据':<15} "
              f"{daily_data.get('涨停数', 0):<10} "
              f"{daily_data.get('首板数量', 0):<10} "
              f"{daily_data.get('连板率', 0):<10.2f}%")
    
    return True


if __name__ == "__main__":
    print("开始测试实时连板数据获取功能\n")
    
    tests = [
        ("获取实时连板梯队指数", test_realtime_limit_up_index),
        ("获取实时实际涨跌停数据", test_realtime_actual_limit_up_down),
        ("获取实时各连板股票", test_realtime_board_stocks),
        ("获取实时所有连板股票", test_realtime_all_boards_stocks),
        ("对比实时数据和历史数据", test_compare_with_daily_data),
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
