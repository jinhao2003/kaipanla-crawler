# -*- coding: utf-8 -*-
"""
百日新高数据示例
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaipanla_crawler import KaipanlaCrawler

def main():
    crawler = KaipanlaCrawler()
    
    print("=" * 80)
    print("百日新高数据示例")
    print("=" * 80)
    
    # 1. 获取单日新高数据
    print("\n【1. 获取单日新高数据】")
    print("-" * 80)
    data = crawler.get_new_high_data("2026-01-16")
    print(f"2026-01-16 今日新增: {data} 只")
    
    # 2. 获取最近一周的新高数据
    print("\n【2. 获取最近一周新高数据】")
    print("-" * 80)
    data = crawler.get_new_high_data("2026-01-16", "2026-01-09")
    print(data)
    
    # 3. 数据分析
    print("\n【3. 数据分析】")
    print("-" * 80)
    print(f"平均每日新增: {data.mean():.1f} 只")
    print(f"最大新增: {data.max()} 只 (日期: {data.idxmax()})")
    print(f"最小新增: {data.min()} 只 (日期: {data.idxmin()})")
    print(f"总计新增: {data.sum()} 只")
    
    # 4. 趋势分析
    print("\n【4. 趋势分析】")
    print("-" * 80)
    if data.iloc[-1] > data.iloc[0]:
        print(f"📈 新高数量呈上升趋势 ({data.iloc[0]} → {data.iloc[-1]})")
    else:
        print(f"📉 新高数量呈下降趋势 ({data.iloc[0]} → {data.iloc[-1]})")

if __name__ == "__main__":
    main()
