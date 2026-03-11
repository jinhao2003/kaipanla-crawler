#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试全市场连板梯队实时数据获取功能

测试 get_market_limit_up_ladder() 函数的实时数据支持
"""

import sys
sys.path.append('.')

from kaipanla_crawler import KaipanlaCrawler


def test_realtime_market_ladder():
    """测试获取实时全市场连板梯队"""
    print("=" * 80)
    print("测试实时全市场连板梯队获取功能")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    
    print(f"\n正在获取实时全市场连板梯队...")
    print("-" * 80)
    
    try:
        # 不传date参数，获取实时数据
        data = crawler.get_market_limit_up_ladder()
        
        print(f"\n✅ 数据获取成功！")
        print(f"\n📅 日期: {data['date']}")
        print(f"📡 数据类型: {'实时' if data['is_realtime'] else '历史'}")
        print(f"📊 总涨停数: {data['statistics']['total_limit_up']}只")
        print(f"🔝 最高连板: {data['statistics']['max_consecutive']}连板")
        print(f"🔄 反包板数: {len(data['broken_stocks'])}只")
        print(f"📍 打开高度标注: {len(data['height_marks'])}只")
        
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
        
        # 显示打开高度标注股票
        if data['height_marks']:
            print(f"\n📍 打开高度标注股票 ({len(data['height_marks'])}只):")
            print("-" * 80)
            
            display_count = min(10, len(data['height_marks']))
            for i, stock in enumerate(data['height_marks'][:display_count], 1):
                tips_str = f" - {stock['tips']}" if stock.get('tips') else ""
                print(f"  {i}. {stock['stock_code']} {stock['stock_name']}{tips_str}")
            
            if len(data['height_marks']) > display_count:
                print(f"  ... 还有 {len(data['height_marks']) - display_count} 只股票")
        
        print("\n" + "=" * 80)
        print("✅ 测试完成！")
        print("=" * 80)
        
        return data
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_realtime_vs_historical():
    """对比实时数据和历史数据"""
    print("\n" + "=" * 80)
    print("对比实时数据和历史数据")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    
    print("\n正在获取实时数据...")
    try:
        realtime_data = crawler.get_market_limit_up_ladder()
        print(f"✅ 实时数据:")
        print(f"   日期: {realtime_data['date']}")
        print(f"   is_realtime: {realtime_data['is_realtime']}")
        print(f"   总涨停: {realtime_data['statistics']['total_limit_up']}只")
        print(f"   最高板: {realtime_data['statistics']['max_consecutive']}连板")
    except Exception as e:
        print(f"❌ 实时数据获取失败: {e}")
        realtime_data = None
    
    print("\n正在获取历史数据 (2026-01-16)...")
    try:
        historical_data = crawler.get_market_limit_up_ladder("2026-01-16")
        print(f"✅ 历史数据:")
        print(f"   日期: {historical_data['date']}")
        print(f"   is_realtime: {historical_data['is_realtime']}")
        print(f"   总涨停: {historical_data['statistics']['total_limit_up']}只")
        print(f"   最高板: {historical_data['statistics']['max_consecutive']}连板")
    except Exception as e:
        print(f"❌ 历史数据获取失败: {e}")
        historical_data = None
    
    print("\n" + "=" * 80)
    print("对比测试完成")
    print("=" * 80)
    
    return realtime_data, historical_data


def test_data_structure():
    """测试返回数据结构完整性"""
    print("\n" + "=" * 80)
    print("测试数据结构完整性")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    
    print("\n正在获取实时数据...")
    try:
        data = crawler.get_market_limit_up_ladder()
        
        print("\n检查必需字段:")
        required_fields = ['date', 'is_realtime', 'ladder', 'broken_stocks', 'height_marks', 'statistics']
        for field in required_fields:
            exists = field in data
            print(f"  {'✅' if exists else '❌'} {field}: {exists}")
        
        print("\n检查statistics字段:")
        stats_fields = ['total_limit_up', 'max_consecutive', 'ladder_distribution']
        for field in stats_fields:
            exists = field in data.get('statistics', {})
            print(f"  {'✅' if exists else '❌'} {field}: {exists}")
        
        print("\n检查数据类型:")
        print(f"  date: {type(data.get('date')).__name__}")
        print(f"  is_realtime: {type(data.get('is_realtime')).__name__}")
        print(f"  ladder: {type(data.get('ladder')).__name__}")
        print(f"  broken_stocks: {type(data.get('broken_stocks')).__name__}")
        print(f"  height_marks: {type(data.get('height_marks')).__name__}")
        print(f"  statistics: {type(data.get('statistics')).__name__}")
        
        print("\n" + "=" * 80)
        print("✅ 数据结构检查完成！")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 测试实时数据获取
    print("\n【测试1】实时全市场连板梯队获取")
    test_realtime_market_ladder()
    
    # 测试实时 vs 历史
    print("\n\n【测试2】实时数据 vs 历史数据")
    test_realtime_vs_historical()
    
    # 测试数据结构
    print("\n\n【测试3】数据结构完整性")
    test_data_structure()
