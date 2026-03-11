# -*- coding: utf-8 -*-
"""
测试多头空头风向标功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaipanla_crawler import KaipanlaCrawler

def test_basic():
    """测试基本功能"""
    print("=" * 80)
    print("测试1: 获取多头空头风向标")
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
    
    assert len(data['bullish_codes']) > 0, "应该有多头风向标数据"
    assert len(data['bearish_codes']) > 0, "应该有空头风向标数据"
    print("\n✅ 基本功能测试通过")

def test_analysis():
    """测试数据分析"""
    print("\n" + "=" * 80)
    print("测试2: 数据分析")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_sentiment_indicator()
    
    print(f"\n多头风向标股票: {', '.join(data['bullish_codes'])}")
    print(f"空头风向标股票: {', '.join(data['bearish_codes'])}")
    print(f"\n所有股票数量: {len(data['all_stocks'])}")
    print(f"前5只: {', '.join(data['all_stocks'][:5])}")
    print(f"后5只: {', '.join(data['all_stocks'][-5:])}")
    
    print("\n✅ 数据分析测试通过")

def test_custom_stocks():
    """测试自定义股票列表"""
    print("\n" + "=" * 80)
    print("测试3: 自定义股票列表")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    
    # 使用自定义股票列表
    custom_stocks = ["600519", "000858", "601318", "600036", "000333", "601888"]
    data = crawler.get_sentiment_indicator(stocks=custom_stocks)
    
    print(f"\n自定义股票数: {len(custom_stocks)}")
    print(f"返回股票数: {len(data['all_stocks'])}")
    
    print("\n多头风向标:")
    for i, code in enumerate(data['bullish_codes'], 1):
        print(f"  {i}. {code}")
    
    print("\n空头风向标:")
    for i, code in enumerate(data['bearish_codes'], 1):
        print(f"  {i}. {code}")
    
    print("\n✅ 自定义股票列表测试通过")

if __name__ == "__main__":
    test_basic()
    test_analysis()
    test_custom_stocks()
    
    print("\n" + "=" * 80)
    print("✅ 所有测试通过！")
    print("=" * 80)
