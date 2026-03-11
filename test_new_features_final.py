#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试所有新增功能 - 最终版本
"""

import sys
sys.path.insert(0, '.')

from kaipanla_crawler import KaipanlaCrawler

def test_all_new_features():
    """测试所有新增功能"""
    
    print("=" * 70)
    print("kaipanla_crawler v1.2.0 - 新功能测试")
    print("=" * 70)
    
    crawler = KaipanlaCrawler()
    
    # 功能1: 实时市场情绪
    print("\n【功能1: 实时市场情绪】")
    mood = crawler.get_realtime_market_mood()
    if mood:
        print(f"✓ 涨停: {mood['涨停家数']}家, 跌停: {mood['跌停家数']}家")
        print(f"  上涨: {mood['上涨家数']}家, 下跌: {mood['下跌家数']}家")
        print(f"  涨跌比: {mood['涨跌比']}")
    
    # 功能2: 昨日涨停表现
    print("\n【功能2: 昨日涨停表现】")
    limit_up = crawler.get_yesterday_performance("limit_up")
    if limit_up:
        current = limit_up['trend'][-1][1]
        change = ((current - limit_up['preclose_px']) / limit_up['preclose_px']) * 100
        print(f"✓ 昨收: {limit_up['preclose_px']:.2f}, 现价: {current:.2f}")
        print(f"  涨跌幅: {change:+.2f}%")
    
    # 功能3: 昨日连板表现
    print("\n【功能3: 昨日连板表现】")
    consecutive = crawler.get_yesterday_performance("consecutive")
    if consecutive:
        current = consecutive['trend'][-1][1]
        change = ((current - consecutive['preclose_px']) / consecutive['preclose_px']) * 100
        print(f"✓ 昨收: {consecutive['preclose_px']:.2f}, 现价: {current:.2f}")
        print(f"  涨跌幅: {change:+.2f}%")
    
    # 功能4: 昨日破板表现
    print("\n【功能4: 昨日破板表现】")
    broken = crawler.get_yesterday_performance("broken")
    if broken:
        current = broken['trend'][-1][1]
        change = ((current - broken['preclose_px']) / broken['preclose_px']) * 100
        print(f"✓ 昨收: {broken['preclose_px']:.2f}, 现价: {current:.2f}")
        print(f"  涨跌幅: {change:+.2f}%")
    
    # 功能5: 板块资金数据
    print("\n【功能5: 板块资金数据】")
    sector_data = crawler.get_sector_capital_data("801235")  # 计算机设备
    if sector_data:
        print(f"✓ 成交额: {sector_data.get('成交额', 0) / 1e8:.2f}亿")
        print(f"  主力净额: {sector_data.get('主力净额', 0) / 1e8:.2f}亿")
    
    # 功能6: N日板块强度
    print("\n【功能6: N日板块强度】")
    df = crawler.get_sector_strength_ndays("2026-01-20", num_days=3)
    if not df.empty:
        print(f"✓ 获取{len(df)}条数据")
        top_sector = df.groupby('板块名称')['涨停数'].sum().idxmax()
        print(f"  最强板块: {top_sector}")
    
    # 功能7: 连板股票列表
    print("\n【功能7: 连板股票列表】")
    count, stocks = crawler.get_board_stocks_count_and_list(1)
    print(f"✓ 首板共 {count} 只股票")
    if stocks:
        print(f"  示例: {stocks[0]['stock_name']} - {stocks[0]['limit_up_reason']}")
    
    print("\n" + "=" * 70)
    print("所有功能测试完成！")
    print("=" * 70)

if __name__ == "__main__":
    test_all_new_features()
