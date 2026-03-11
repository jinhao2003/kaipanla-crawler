#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试全市场连板梯队获取功能

测试 get_market_limit_up_ladder() 函数
"""

import sys
sys.path.append('.')

from kaipanla_crawler import KaipanlaCrawler


def test_market_limit_up_ladder():
    """测试获取全市场连板梯队"""
    print("=" * 80)
    print("测试全市场连板梯队获取功能")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    
    # 测试日期
    test_date = "2026-01-16"
    
    print(f"\n正在获取 {test_date} 的全市场连板梯队...")
    print("-" * 80)
    
    try:
        data = crawler.get_market_limit_up_ladder(test_date)
        
        print(f"\n✅ 数据获取成功！")
        print(f"\n📅 日期: {data['date']}")
        print(f"📊 总涨停数: {data['statistics']['total_limit_up']}只")
        print(f"🔝 最高连板: {data['statistics']['max_consecutive']}连板")
        print(f"🔄 反包板数: {len(data['broken_stocks'])}只")
        
        print(f"\n📈 连板分布:")
        print("-" * 80)
        
        # 按连板高度从高到低排序
        ladder_dist = data['statistics']['ladder_distribution']
        for consecutive in sorted(ladder_dist.keys(), reverse=True):
            count = ladder_dist[consecutive]
            print(f"  {consecutive}连板: {count}只")
        
        print(f"\n📋 连板梯队详情:")
        print("-" * 80)
        
        # 显示每个连板高度的前5只股票
        for consecutive in sorted(data['ladder'].keys(), reverse=True):
            stocks = data['ladder'][consecutive]
            print(f"\n{consecutive}连板 ({len(stocks)}只):")
            
            # 显示前5只
            display_count = min(5, len(stocks))
            for i, stock in enumerate(stocks[:display_count], 1):
                tips_str = f" - {stock['tips']}" if stock.get('tips') else ""
                print(f"  {i}. {stock['stock_code']} {stock['stock_name']}{tips_str}")
            
            if len(stocks) > display_count:
                print(f"  ... 还有 {len(stocks) - display_count} 只股票")
        
        # 显示反包板股票
        if data['broken_stocks']:
            print(f"\n🔄 反包板股票 ({len(data['broken_stocks'])}只):")
            print("-" * 80)
            
            display_count = min(10, len(data['broken_stocks']))
            for i, stock in enumerate(data['broken_stocks'][:display_count], 1):
                tips_str = f" - {stock['tips']}" if stock.get('tips') else ""
                print(f"  {i}. {stock['stock_code']} {stock['stock_name']}{tips_str}")
            
            if len(data['broken_stocks']) > display_count:
                print(f"  ... 还有 {len(data['broken_stocks']) - display_count} 只股票")
        
        print("\n" + "=" * 80)
        print("✅ 测试完成！")
        print("=" * 80)
        
        return data
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_multiple_dates():
    """测试多个日期"""
    print("\n" + "=" * 80)
    print("测试多个日期的全市场连板梯队")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    
    test_dates = [
        "2026-01-17",
        "2026-01-16",
        "2026-01-15"
    ]
    
    results = []
    
    for date in test_dates:
        print(f"\n正在获取 {date} 的数据...")
        try:
            data = crawler.get_market_limit_up_ladder(date)
            results.append(data)
            
            stats = data['statistics']
            print(f"  ✅ {date}:")
            print(f"     总涨停: {stats['total_limit_up']}只")
            print(f"     最高板: {stats['max_consecutive']}连板")
            print(f"     反包板: {len(data['broken_stocks'])}只")
            
        except Exception as e:
            print(f"  ❌ {date}: 获取失败 - {e}")
    
    print("\n" + "=" * 80)
    print("多日期测试完成")
    print("=" * 80)
    
    return results


def test_statistics_analysis():
    """测试统计分析"""
    print("\n" + "=" * 80)
    print("测试统计分析")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    test_date = "2026-01-16"
    
    print(f"\n正在分析 {test_date} 的数据...")
    
    try:
        data = crawler.get_market_limit_up_ladder(test_date)
        
        stats = data['statistics']
        ladder = data['ladder']
        
        print(f"\n📊 详细统计:")
        print("-" * 80)
        print(f"日期: {data['date']}")
        print(f"总涨停数: {stats['total_limit_up']}只")
        print(f"最高连板: {stats['max_consecutive']}连板")
        print(f"反包板数: {len(data['broken_stocks'])}只")
        
        # 计算连板率
        if stats['total_limit_up'] > 0:
            first_board = ladder.get(1, [])
            multi_board = stats['total_limit_up'] - len(first_board)
            consecutive_rate = (multi_board / stats['total_limit_up']) * 100
            print(f"\n连板率: {consecutive_rate:.2f}%")
            print(f"  首板: {len(first_board)}只")
            print(f"  连板: {multi_board}只")
        
        # 找出最强板块（假设有板块信息）
        print(f"\n📈 连板梯队分布:")
        for consecutive in sorted(ladder.keys(), reverse=True):
            count = len(ladder[consecutive])
            percentage = (count / stats['total_limit_up']) * 100
            print(f"  {consecutive}连板: {count}只 ({percentage:.1f}%)")
        
        print("\n" + "=" * 80)
        print("✅ 分析完成！")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 测试单日
    print("\n【测试1】单日全市场连板梯队获取")
    test_market_limit_up_ladder()
    
    # 测试多日
    print("\n\n【测试2】多日全市场连板梯队获取")
    test_multiple_dates()
    
    # 测试统计分析
    print("\n\n【测试3】统计分析")
    test_statistics_analysis()
