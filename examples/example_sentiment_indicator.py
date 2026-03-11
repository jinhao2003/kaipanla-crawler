# -*- coding: utf-8 -*-
"""
多头空头风向标功能示例

展示如何使用 get_sentiment_indicator() 函数获取市场风向标数据
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaipanla_crawler import KaipanlaCrawler

def example_basic():
    """基本使用示例"""
    print("=" * 80)
    print("示例1: 获取多头空头风向标")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_sentiment_indicator()
    
    print(f"\n日期: {data['date']}")
    print(f"板块ID: {data['plate_id']}")
    print(f"股票总数: {len(data['all_stocks'])}")
    
    print("\n【多头风向标】（前3只）")
    print("-" * 80)
    for i, code in enumerate(data['bullish_codes'], 1):
        print(f"{i}. {code}")
    
    print("\n【空头风向标】（后3只）")
    print("-" * 80)
    for i, code in enumerate(data['bearish_codes'], 1):
        print(f"{i}. {code}")

def example_custom_stocks():
    """自定义股票列表示例"""
    print("\n" + "=" * 80)
    print("示例2: 使用自定义股票列表")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    
    # 使用自定义股票列表（例如：白酒、银行、地产等）
    custom_stocks = [
        "600519",  # 贵州茅台
        "000858",  # 五粮液
        "601318",  # 中国平安
        "600036",  # 招商银行
        "000333",  # 美的集团
        "601888"   # 中国中免
    ]
    
    data = crawler.get_sentiment_indicator(stocks=custom_stocks)
    
    print(f"\n自定义股票数: {len(custom_stocks)}")
    print(f"返回股票数: {len(data['all_stocks'])}")
    
    print("\n多头风向标:")
    for i, code in enumerate(data['bullish_codes'], 1):
        print(f"  {i}. {code}")
    
    print("\n空头风向标:")
    for i, code in enumerate(data['bearish_codes'], 1):
        print(f"  {i}. {code}")

def example_analysis():
    """数据分析示例"""
    print("\n" + "=" * 80)
    print("示例3: 风向标数据分析")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_sentiment_indicator()
    
    print(f"\n多头风向标股票: {', '.join(data['bullish_codes'])}")
    print(f"空头风向标股票: {', '.join(data['bearish_codes'])}")
    
    print(f"\n所有股票数量: {len(data['all_stocks'])}")
    print(f"前5只: {', '.join(data['all_stocks'][:5])}")
    print(f"后5只: {', '.join(data['all_stocks'][-5:])}")
    
    # 可以结合其他函数获取股票详细信息
    print("\n提示: 可以使用返回的股票代码结合其他API获取详细信息")

if __name__ == "__main__":
    example_basic()
    example_custom_stocks()
    example_analysis()
    
    print("\n" + "=" * 80)
    print("✅ 所有示例运行完成！")
    print("=" * 80)
