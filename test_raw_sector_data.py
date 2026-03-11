#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试原始板块数据结构，查看实际的数组索引
"""

from kaipanla_crawler import KaipanlaCrawler

def test_raw_sector_data():
    """测试原始板块数据"""
    crawler = KaipanlaCrawler()
    
    # 获取最近一个交易日的板块数据
    result = crawler.get_sector_ranking(date="20250117")
    
    if not result or "sectors" not in result or not result["sectors"]:
        print("未获取到板块数据")
        return
    
    # 获取第一个板块的第一只股票
    first_sector = result["sectors"][0]
    print(f"板块名称: {first_sector['sector_name']}")
    print(f"板块股票数: {len(first_sector['stocks'])}")
    print()
    
    # 打印第一只股票的原始数据（在解析前）
    # 我们需要修改crawler代码来输出原始数据
    # 但现在我们可以通过查看已解析的数据来推断
    
    first_stock = first_sector["stocks"][0]
    print("第一只股票的已解析数据:")
    for key, value in first_stock.items():
        print(f"  {key}: {value}")
    print()
    
    # 分析字段内容
    print("字段内容分析:")
    print(f"1. 连板天数 = '{first_stock['连板天数']}' (应该是 'X连板' 格式)")
    print(f"2. 连板次数 = '{first_stock['连板次数']}' (应该是数字)")
    print(f"3. 概念标签 = '{first_stock['概念标签']}' (应该是概念文字)")
    print(f"4. 主题 = '{first_stock['主题'][:50]}...' (应该是长文本)")
    print(f"5. 涨停原因 = '{first_stock['涨停原因'][:50]}...' (应该是原因文字)")
    print()
    
    # 根据内容推断正确的映射
    print("推断的字段映射问题:")
    if "连板" in str(first_stock['连板天数']):
        print("✓ 连板天数 (index 9) 正确")
    
    if isinstance(first_stock['连板次数'], (int, str)) and len(str(first_stock['连板次数'])) < 5:
        print("✓ 连板次数 (index 10) 正确 (数字)")
    else:
        print("✗ 连板次数 (index 10) 不是数字")
    
    if "、" in str(first_stock['概念标签']) or len(str(first_stock['概念标签'])) > 5:
        print("✓ 概念标签 (index 11) 正确 (包含概念文字)")
    else:
        print("✗ 概念标签 (index 11) 不包含概念文字")
    
    if len(str(first_stock['主题'])) > 50:
        print("✓ 主题 (index 16) 正确 (长文本)")
    else:
        print("✗ 主题 (index 16) 不是长文本")
    
    if len(str(first_stock['涨停原因'])) > 50:
        print("✓ 涨停原因 (index 17) 正确 (长文本)")
    else:
        print("✗ 涨停原因 (index 17) 不是长文本")

if __name__ == "__main__":
    test_raw_sector_data()
