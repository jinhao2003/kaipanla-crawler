# -*- coding: utf-8 -*-
"""
基础使用示例
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaipanla_crawler import KaipanlaCrawler

def main():
    # 创建爬虫实例
    crawler = KaipanlaCrawler()
    
    print("=" * 80)
    print("开盘啦爬虫 - 基础使用示例")
    print("=" * 80)
    
    # 1. 获取单日市场数据
    print("\n【1. 获取单日市场数据】")
    print("-" * 80)
    data = crawler.get_daily_data("2026-01-16")
    print(f"日期: {data['日期']}")
    print(f"涨停数: {data['涨停数']}")
    print(f"跌停数: {data['跌停数']}")
    print(f"上证指数: {data['上证指数']}")
    print(f"首板数量: {data['首板数量']}")
    print(f"连板率: {data['连板率']}%")
    
    # 2. 获取板块排行（前5个）
    print("\n【2. 获取板块排行】")
    print("-" * 80)
    sector_df = crawler.get_sector_ranking("2026-01-16", limit=5)
    print(sector_df[['板块名称', '涨跌幅(%)', '成交额(元)', '主力净流入(元)']])
    
    # 3. 获取涨停原因板块
    print("\n【3. 获取涨停原因板块】")
    print("-" * 80)
    limit_up_data = crawler.get_limit_up_sectors("2026-01-16")
    
    print(f"市场概况:")
    print(f"  涨停数: {limit_up_data['summary']['涨停数']}")
    print(f"  跌停数: {limit_up_data['summary']['跌停数']}")
    print(f"  涨跌比: {limit_up_data['summary']['涨跌比']}")
    
    print(f"\n板块列表（前3个）:")
    for i, sector in enumerate(limit_up_data['sectors'][:3], 1):
        print(f"  {i}. {sector['sector_name']}: {sector['stock_count']}只涨停")
        # 显示第一只股票
        if sector['stocks']:
            stock = sector['stocks'][0]
            print(f"     代表股: {stock['股票代码']} {stock['股票名称']} ({stock['连板描述']})")

if __name__ == "__main__":
    main()
