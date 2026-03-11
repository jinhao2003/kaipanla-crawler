#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试板块连板梯队获取功能

测试 get_sector_limit_up_ladder() 函数
"""

import sys
sys.path.append('.')

from kaipanla_crawler import KaipanlaCrawler


def test_historical_sector_ladder():
    """测试获取历史板块连板梯队"""
    print("=" * 80)
    print("测试历史板块连板梯队获取")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    
    # 测试日期
    test_date = "2026-01-16"
    
    print(f"\n正在获取 {test_date} 的板块连板梯队...")
    print("-" * 80)
    
    try:
        data = crawler.get_sector_limit_up_ladder(test_date)
        
        print(f"\n✅ 数据获取成功！")
        print(f"\n📅 日期: {data['date']}")
        print(f"⏰ 数据类型: {'实时' if data['is_realtime'] else '历史'}")
        print(f"📊 板块数量: {len(data['sectors'])}个")
        
        if data['sectors']:
            print(f"\n📈 板块连板梯队详情:")
            print("-" * 80)
            
            # 按涨停数量排序
            sorted_sectors = sorted(data['sectors'], key=lambda x: x['limit_up_count'], reverse=True)
            
            for i, sector in enumerate(sorted_sectors, 1):
                print(f"\n{i}. {sector['sector_name']} ({sector['limit_up_count']}只涨停)")
                
                # 显示正常连板股票（前5只）
                display_count = min(5, len(sector['stocks']))
                for j, stock in enumerate(sector['stocks'][:display_count], 1):
                    consecutive_text = f"{stock['consecutive_days']}连板" if stock['consecutive_days'] > 1 else "首板"
                    height_mark = " [打开高度]" if stock.get('is_height_mark') else ""
                    print(f"   {j}. {stock['stock_code']} {stock['stock_name']} - {consecutive_text}{height_mark}")
                
                if len(sector['stocks']) > display_count:
                    print(f"   ... 还有 {len(sector['stocks']) - display_count} 只股票")
                
                # 显示反包板股票
                if sector.get('broken_stocks'):
                    print(f"   🔄 反包板 ({len(sector['broken_stocks'])}只):")
                    for j, stock in enumerate(sector['broken_stocks'][:3], 1):
                        tips_str = f" - {stock['tips']}" if stock.get('tips') else ""
                        print(f"      {j}. {stock['stock_code']} {stock['stock_name']}{tips_str}")
                    if len(sector['broken_stocks']) > 3:
                        print(f"      ... 还有 {len(sector['broken_stocks']) - 3} 只")
        else:
            print("\n  无板块连板数据")
        
        print("\n" + "=" * 80)
        print("✅ 测试完成！")
        print("=" * 80)
        
        return data
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_realtime_sector_ladder():
    """测试获取实时板块连板梯队"""
    print("\n" + "=" * 80)
    print("测试实时板块连板梯队获取")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    
    print(f"\n正在获取实时板块连板梯队...")
    print("-" * 80)
    
    try:
        data = crawler.get_sector_limit_up_ladder()
        
        print(f"\n✅ 数据获取成功！")
        print(f"\n📅 日期: {data['date']}")
        print(f"⏰ 数据类型: {'实时' if data['is_realtime'] else '历史'}")
        print(f"📊 板块数量: {len(data['sectors'])}个")
        
        if data['sectors']:
            print(f"\n📈 热门板块 TOP 5:")
            print("-" * 80)
            
            # 按涨停数量排序，显示前5个
            sorted_sectors = sorted(data['sectors'], key=lambda x: x['limit_up_count'], reverse=True)
            
            for i, sector in enumerate(sorted_sectors[:5], 1):
                print(f"\n{i}. {sector['sector_name']} ({sector['limit_up_count']}只涨停)")
                
                # 显示前3只股票
                for j, stock in enumerate(sector['stocks'][:3], 1):
                    consecutive_text = f"{stock['consecutive_days']}连板" if stock['consecutive_days'] > 1 else "首板"
                    print(f"   {j}. {stock['stock_code']} {stock['stock_name']} - {consecutive_text}")
        else:
            print("\n  无板块连板数据（可能是非交易时间）")
        
        print("\n" + "=" * 80)
        print("✅ 测试完成！")
        print("=" * 80)
        
        return data
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_sector_statistics():
    """测试板块统计分析"""
    print("\n" + "=" * 80)
    print("测试板块统计分析")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    test_date = "2026-01-16"
    
    print(f"\n正在分析 {test_date} 的板块数据...")
    
    try:
        data = crawler.get_sector_limit_up_ladder(test_date)
        
        if not data['sectors']:
            print("无数据可分析")
            return
        
        # 统计分析（排除反包板）
        total_sectors = len(data['sectors'])
        total_normal_stocks = sum(len(sector['stocks']) for sector in data['sectors'])
        total_broken_stocks = sum(len(sector.get('broken_stocks', [])) for sector in data['sectors'])
        
        # 找出最热板块
        hottest_sector = max(data['sectors'], key=lambda x: x['limit_up_count'])
        
        # 统计连板分布（只统计正常连板，不包括反包板）
        consecutive_stats = {}
        for sector in data['sectors']:
            for stock in sector['stocks']:
                days = stock['consecutive_days']
                consecutive_stats[days] = consecutive_stats.get(days, 0) + 1
        
        print(f"\n📊 统计结果:")
        print("-" * 80)
        print(f"板块总数: {total_sectors}个")
        print(f"正常涨停: {total_normal_stocks}只")
        print(f"反包板: {total_broken_stocks}只")
        print(f"总涨停数: {total_normal_stocks + total_broken_stocks}只")
        print(f"平均每板块: {total_normal_stocks / total_sectors:.1f}只")
        
        print(f"\n🔥 最热板块: {hottest_sector['sector_name']}")
        print(f"   涨停数: {hottest_sector['limit_up_count']}只")
        
        print(f"\n📈 连板分布（不含反包板）:")
        for days in sorted(consecutive_stats.keys(), reverse=True):
            count = consecutive_stats[days]
            print(f"   {days}连板: {count}只")
        
        # 显示反包板信息
        if total_broken_stocks > 0:
            print(f"\n🔄 反包板详情:")
            for sector in data['sectors']:
                if sector.get('broken_stocks'):
                    print(f"   {sector['sector_name']}: {len(sector['broken_stocks'])}只")
                    for stock in sector['broken_stocks'][:3]:  # 显示前3只
                        print(f"      - {stock['stock_name']} ({stock['tips']})")
        
        print("\n" + "=" * 80)
        print("✅ 分析完成！")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 测试历史数据
    print("\n【测试1】历史板块连板梯队")
    test_historical_sector_ladder()
    
    # 测试实时数据
    print("\n\n【测试2】实时板块连板梯队")
    test_realtime_sector_ladder()
    
    # 测试统计分析
    print("\n\n【测试3】板块统计分析")
    test_sector_statistics()
