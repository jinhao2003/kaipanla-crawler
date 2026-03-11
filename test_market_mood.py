#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 get_realtime_market_mood() 函数
"""

import sys
sys.path.insert(0, '.')

from kaipanla_crawler import KaipanlaCrawler

def test_market_mood():
    """测试获取实时市场情绪数据"""
    
    print("=" * 60)
    print("测试 get_realtime_market_mood() 函数")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 获取实时市场情绪
    print("\n获取实时市场情绪数据...")
    mood = crawler.get_realtime_market_mood()
    
    if mood:
        print("\n✓ 成功获取市场情绪数据")
        print("\n【涨跌停统计】")
        print(f"  涨停: {mood['涨停家数']}家")
        print(f"  跌停: {mood['跌停家数']}家")
        
        print("\n【上涨下跌统计】")
        print(f"  上涨: {mood['上涨家数']}家")
        print(f"  下跌: {mood['下跌家数']}家")
        print(f"  涨跌比: {mood['涨跌比']}")
        
        print("\n【市场流通量】")
        print(f"  全市场流通量: {mood['全市场流通量']:,}")
        print(f"  前日流通量: {mood['前日流通量']:,}")
        
        print("\n【市场状态】")
        market_status = "上涨(红色)" if mood['市场颜色'] == 1 else "下跌(绿色)"
        print(f"  市场颜色: {market_status}")
        
        # 计算市场情绪指标
        total_stocks = mood['上涨家数'] + mood['下跌家数']
        if total_stocks > 0:
            up_ratio = (mood['上涨家数'] / total_stocks) * 100
            print(f"\n【情绪指标】")
            print(f"  上涨占比: {up_ratio:.2f}%")
            
            if up_ratio > 60:
                emotion = "强势"
            elif up_ratio > 40:
                emotion = "中性"
            else:
                emotion = "弱势"
            print(f"  市场情绪: {emotion}")
        
    else:
        print("\n✗ 未获取到数据")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_market_mood()
