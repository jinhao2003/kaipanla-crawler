#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试ETF榜单功能
"""

import sys
sys.path.insert(0, '.')

from kaipanla_crawler import KaipanlaCrawler

def test_etf_ranking():
    """测试ETF榜单"""
    print("=" * 100)
    print("测试：ETF榜单功能")
    print("=" * 100)
    
    crawler = KaipanlaCrawler()
    
    # 测试实时ETF榜单
    print("\n1. 获取实时ETF榜单（第一页）")
    print("-" * 100)
    data = crawler.get_etf_ranking()
    
    print(f"日期: {data['date']}")
    print(f"是否实时: {data['is_realtime']}")
    print(f"ETF总数: {data['total_count']}")
    print(f"当前页: {data['page_count']} 个")
    
    if data['etfs']:
        print(f"\n涨幅前10:")
        for i, etf in enumerate(data['etfs'][:10], 1):
            code = etf[0]
            name = etf[1]
            price = etf[2]
            change = etf[3]
            turnover = etf[4]
            print(f"  {i}. {code} {name}: {price} ({change:+.2f}%) 成交额{turnover/100000000:.2f}亿")
    
    # 测试历史ETF榜单
    print("\n2. 获取历史ETF榜单")
    print("-" * 100)
    data = crawler.get_etf_ranking("2026-02-09")
    
    print(f"日期: {data['date']}")
    print(f"ETF总数: {data['total_count']}")
    print(f"当前页: {data['page_count']} 个")
    
    # 测试获取所有ETF（前3页）
    print("\n3. 获取所有ETF（前3页）")
    print("-" * 100)
    data = crawler.get_all_etf_ranking(max_pages=3)
    
    print(f"ETF总数（API）: {data['total_count']}")
    print(f"实际获取: {len(data['etfs'])} 个")
    print(f"获取页数: {data['pages_fetched']} 页")
    
    # 分析ETF数据
    print("\n4. ETF数据分析")
    print("-" * 100)
    
    if data['etfs']:
        # 按涨幅排序
        sorted_by_change = sorted(data['etfs'], key=lambda x: x[3], reverse=True)
        
        print(f"\n涨幅前5:")
        for i, etf in enumerate(sorted_by_change[:5], 1):
            name = etf[1]
            change = etf[3]
            week_return = etf[9]
            month_return = etf[10]
            print(f"  {i}. {name}: {change:+.2f}% (周{week_return:+.2f}% 月{month_return:+.2f}%)")
        
        print(f"\n跌幅前5:")
        for i, etf in enumerate(sorted_by_change[-5:], 1):
            name = etf[1]
            change = etf[3]
            week_return = etf[9]
            month_return = etf[10]
            print(f"  {i}. {name}: {change:+.2f}% (周{week_return:+.2f}% 月{month_return:+.2f}%)")
        
        # 按成交额排序
        sorted_by_turnover = sorted(data['etfs'], key=lambda x: x[4], reverse=True)
        
        print(f"\n成交额前5:")
        for i, etf in enumerate(sorted_by_turnover[:5], 1):
            name = etf[1]
            turnover = etf[4]
            change = etf[3]
            print(f"  {i}. {name}: {turnover/100000000:.2f}亿 ({change:+.2f}%)")

if __name__ == "__main__":
    test_etf_ranking()
