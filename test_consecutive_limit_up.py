#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试连板梯队获取功能

测试 get_consecutive_limit_up() 函数
"""

import sys
sys.path.append('.')

from kaipanla_crawler import KaipanlaCrawler


def test_consecutive_limit_up():
    """测试获取连板梯队"""
    print("=" * 80)
    print("测试连板梯队获取功能")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    
    # 测试日期
    test_date = "2026-01-19"
    
    print(f"\n正在获取 {test_date} 的连板梯队数据...")
    print("-" * 80)
    
    try:
        data = crawler.get_consecutive_limit_up(test_date)
        
        print(f"\n✅ 数据获取成功！")
        print(f"\n📅 日期: {data['date']}")
        print(f"🔝 最高连板: {data['max_consecutive']}连板")
        print(f"📈 最高板个股: {data['max_consecutive_stocks']}")
        print(f"🏷️  最高板题材: {data['max_consecutive_concepts']}")
        
        print(f"\n📊 连板梯队详情:")
        print("-" * 80)
        
        if data['ladder']:
            # 按连板高度从高到低排序
            sorted_ladder = sorted(data['ladder'].items(), key=lambda x: x[0], reverse=True)
            
            for consecutive, stocks in sorted_ladder:
                print(f"\n{consecutive}连板 ({len(stocks)}只):")
                for i, stock in enumerate(stocks, 1):
                    concepts = []
                    if stock.get('题材'):
                        concepts.append(stock['题材'])
                    if stock.get('概念'):
                        concepts.append(stock['概念'])
                    concept_str = "、".join(concepts) if concepts else "无"
                    
                    print(f"  {i}. {stock['股票代码']} {stock['股票名称']} - {concept_str}")
        else:
            print("  无连板数据")
        
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
    print("测试多个日期的连板梯队")
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
            data = crawler.get_consecutive_limit_up(date)
            results.append(data)
            print(f"  ✅ {date}: {data['max_consecutive']}连板 - {data['max_consecutive_stocks']}")
        except Exception as e:
            print(f"  ❌ {date}: 获取失败 - {e}")
    
    print("\n" + "=" * 80)
    print("多日期测试完成")
    print("=" * 80)
    
    return results


if __name__ == "__main__":
    # 测试单日
    print("\n【测试1】单日连板梯队获取")
    test_consecutive_limit_up()
    
    # 测试多日
    print("\n\n【测试2】多日连板梯队获取")
    test_multiple_dates()
