# -*- coding: utf-8 -*-
"""
涨停板块分析示例
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaipanla_crawler import KaipanlaCrawler
import json

def analyze_limit_up_sectors(date):
    """分析涨停板块数据"""
    crawler = KaipanlaCrawler()
    data = crawler.get_limit_up_sectors(date)
    
    print("=" * 80)
    print(f"涨停板块分析 - {date}")
    print("=" * 80)
    
    # 市场概况
    summary = data['summary']
    print(f"\n【市场概况】")
    print(f"涨停数: {summary['涨停数']}, 跌停数: {summary['跌停数']}")
    print(f"上涨家数: {summary['上涨家数']}, 下跌家数: {summary['下跌家数']}")
    print(f"涨跌比: {summary['涨跌比']}")
    
    # 板块统计
    sectors = data['sectors']
    total_stocks = sum(s['stock_count'] for s in sectors)
    print(f"\n【板块统计】")
    print(f"板块数量: {len(sectors)}")
    print(f"涨停股票总数: {total_stocks}")
    
    # 热门板块（涨停数量最多的前5个）
    print(f"\n【热门板块 TOP5】")
    sorted_sectors = sorted(sectors, key=lambda x: x['stock_count'], reverse=True)
    for i, sector in enumerate(sorted_sectors[:5], 1):
        print(f"{i}. {sector['sector_name']}: {sector['stock_count']}只")
        
        # 统计连板情况
        if sector['stocks']:
            lianban_count = {}
            for stock in sector['stocks']:
                desc = stock['连板描述']
                lianban_count[desc] = lianban_count.get(desc, 0) + 1
            
            print(f"   连板分布: {dict(sorted(lianban_count.items()))}")
    
    # 高连板股票（3连板及以上）
    print(f"\n【高连板股票】")
    high_lianban = []
    for sector in sectors:
        for stock in sector['stocks']:
            if stock['连板次数'] >= 3:
                high_lianban.append({
                    'sector': sector['sector_name'],
                    'code': stock['股票代码'],
                    'name': stock['股票名称'],
                    'lianban': stock['连板次数'],
                    'desc': stock['连板描述']
                })
    
    high_lianban.sort(key=lambda x: x['lianban'], reverse=True)
    for stock in high_lianban[:10]:
        print(f"{stock['code']} {stock['name']}: {stock['desc']} ({stock['sector']})")
    
    # 保存详细数据
    output_file = f"limit_up_analysis_{date}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n详细数据已保存到: {output_file}")

if __name__ == "__main__":
    analyze_limit_up_sectors("2026-01-16")
