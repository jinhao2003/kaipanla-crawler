#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
板块竞价异动功能使用示例
"""

import sys
sys.path.insert(0, '.')

from kaipanla_crawler import KaipanlaCrawler

def example_1_realtime_bidding():
    """示例1：获取实时竞价异动"""
    print("=" * 100)
    print("示例1：获取实时竞价异动")
    print("=" * 100)
    
    crawler = KaipanlaCrawler()
    
    # 获取实时竞价异动
    data = crawler.get_sector_bidding_anomaly()
    
    print(f"\n日期: {data['date']}")
    print(f"是否实时: {data['is_realtime']}")
    print(f"总异动板块: {data['total_count']} 个")
    print(f"  今日新增: {len(data['list1'])} 个")
    print(f"  昨日延续: {len(data['list2'])} 个")
    print(f"  其他异动: {len(data['list3'])} 个")
    
    # 显示今日新增异动板块
    if data['list1']:
        print(f"\n今日新增竞价异动板块:")
        for i, sector in enumerate(data['list1'], 1):
            code = sector[0]
            name = sector[1]
            volume_ratio = sector[2]
            amount = sector[3]
            strength = sector[4]
            main_net = sector[5]
            
            print(f"  {i}. {code} {name}")
            print(f"     竞价爆量: {volume_ratio}")
            print(f"     异动金额: {amount/100000000:.2f}亿")
            print(f"     板块强度: {strength}")
            print(f"     主力净额: {main_net/100000000:.2f}亿")

def example_2_historical_bidding():
    """示例2：获取历史竞价异动"""
    print("\n" + "=" * 100)
    print("示例2：获取历史竞价异动")
    print("=" * 100)
    
    crawler = KaipanlaCrawler()
    
    # 获取历史竞价异动
    data = crawler.get_sector_bidding_anomaly("2026-02-10")
    
    print(f"\n日期: {data['date']}")
    print(f"是否实时: {data['is_realtime']}")
    print(f"总异动板块: {data['total_count']} 个")
    
    # 显示昨日延续板块
    if data['list2']:
        print(f"\n昨日爆发板块延续异动:")
        for i, sector in enumerate(data['list2'], 1):
            code = sector[0]
            name = sector[1]
            volume_ratio = sector[2]
            strength = sector[4]
            
            print(f"  {i}. {code} {name}: 爆量{volume_ratio} 强度{strength}")

def example_3_filter_strong_sectors():
    """示例3：筛选强势板块"""
    print("\n" + "=" * 100)
    print("示例3：筛选强势板块")
    print("=" * 100)
    
    crawler = KaipanlaCrawler()
    
    # 获取实时竞价异动
    data = crawler.get_sector_bidding_anomaly()
    
    # 筛选强势板块（竞价爆量>5 且 板块强度>0）
    strong_sectors = []
    all_sectors = data['list1'] + data['list2'] + data['list3']
    
    for sector in all_sectors:
        volume_ratio = sector[2]
        strength = sector[4]
        
        if volume_ratio > 5 and strength > 0:
            strong_sectors.append({
                'code': sector[0],
                'name': sector[1],
                'volume_ratio': volume_ratio,
                'amount': sector[3],
                'strength': strength,
                'main_net': sector[5]
            })
    
    # 按板块强度排序
    strong_sectors.sort(key=lambda x: x['strength'], reverse=True)
    
    print(f"\n强势板块: {len(strong_sectors)} 个")
    print(f"筛选条件: 竞价爆量>5 且 板块强度>0")
    print("-" * 100)
    
    for i, s in enumerate(strong_sectors, 1):
        print(f"{i}. {s['name']}")
        print(f"   爆量: {s['volume_ratio']}, 强度: {s['strength']}, 主力净额: {s['main_net']/100000000:.2f}亿")

def example_4_compare_new_and_continued():
    """示例4：对比今日新增和昨日延续"""
    print("\n" + "=" * 100)
    print("示例4：对比今日新增和昨日延续")
    print("=" * 100)
    
    crawler = KaipanlaCrawler()
    
    # 获取实时竞价异动
    data = crawler.get_sector_bidding_anomaly()
    
    print(f"\n日期: {data['date']}")
    print("=" * 100)
    
    print(f"\n今日新增异动板块 ({len(data['list1'])} 个):")
    for sector in data['list1']:
        name = sector[1]
        volume_ratio = sector[2]
        strength = sector[4]
        print(f"  {name}: 爆量{volume_ratio} 强度{strength}")
    
    print(f"\n昨日延续异动板块 ({len(data['list2'])} 个):")
    for sector in data['list2']:
        name = sector[1]
        volume_ratio = sector[2]
        strength = sector[4]
        print(f"  {name}: 爆量{volume_ratio} 强度{strength}")
    
    # 分析
    print("\n分析:")
    if len(data['list2']) > 0:
        print("  ✓ 有昨日延续板块，市场热点有延续性")
    else:
        print("  ⚠️ 无昨日延续板块，市场热点切换")
    
    if len(data['list1']) > len(data['list2']):
        print("  ✓ 新增板块多于延续板块，市场活跃度高")
    else:
        print("  ⚠️ 新增板块少于延续板块，市场热点集中")

def example_5_capital_flow_analysis():
    """示例5：资金流向分析"""
    print("\n" + "=" * 100)
    print("示例5：资金流向分析")
    print("=" * 100)
    
    crawler = KaipanlaCrawler()
    
    # 获取实时竞价异动
    data = crawler.get_sector_bidding_anomaly()
    
    # 统计资金流向
    all_sectors = data['list1'] + data['list2'] + data['list3']
    
    # 按主力净额排序
    sorted_by_main = sorted(all_sectors, 
                            key=lambda x: x[5], 
                            reverse=True)
    
    print(f"\n主力净流入前5:")
    for i, sector in enumerate(sorted_by_main[:5], 1):
        name = sector[1]
        main_net = sector[5]
        volume_ratio = sector[2]
        strength = sector[4]
        print(f"  {i}. {name}: {main_net/100000000:.2f}亿 (爆量{volume_ratio}, 强度{strength})")
    
    print(f"\n主力净流出前5:")
    for i, sector in enumerate(sorted_by_main[-5:], 1):
        name = sector[1]
        main_net = sector[5]
        volume_ratio = sector[2]
        strength = sector[4]
        print(f"  {i}. {name}: {main_net/100000000:.2f}亿 (爆量{volume_ratio}, 强度{strength})")
    
    # 统计
    inflow_count = sum(1 for s in all_sectors if s[5] > 0)
    outflow_count = sum(1 for s in all_sectors if s[5] < 0)
    
    print(f"\n资金流向统计:")
    print(f"  净流入板块: {inflow_count} 个")
    print(f"  净流出板块: {outflow_count} 个")
    print(f"  流入/流出比: {inflow_count/outflow_count:.2f}" if outflow_count > 0 else "  流入/流出比: N/A")

def example_6_multi_day_comparison():
    """示例6：多日对比分析"""
    print("\n" + "=" * 100)
    print("示例6：多日对比分析")
    print("=" * 100)
    
    crawler = KaipanlaCrawler()
    
    # 获取最近3天的竞价异动
    dates = ["2026-02-11", "2026-02-10", "2026-02-09"]
    
    print("\n最近3天竞价异动对比:")
    print("=" * 100)
    print(f"{'日期':<12} {'今日新增':<10} {'昨日延续':<10} {'其他异动':<10} {'总计':<10}")
    print("-" * 100)
    
    for date in dates:
        data = crawler.get_sector_bidding_anomaly(date)
        
        list1_count = len(data['list1'])
        list2_count = len(data['list2'])
        list3_count = len(data['list3'])
        total = data['total_count']
        
        print(f"{date:<12} {list1_count:<10} {list2_count:<10} {list3_count:<10} {total:<10}")
        
        if data['list1']:
            top3 = ', '.join([s[1] for s in data['list1'][:3]])
            print(f"  新增板块: {top3}")

if __name__ == "__main__":
    # 运行所有示例
    example_1_realtime_bidding()
    example_2_historical_bidding()
    example_3_filter_strong_sectors()
    example_4_compare_new_and_continued()
    example_5_capital_flow_analysis()
    example_6_multi_day_comparison()
    
    print("\n" + "=" * 100)
    print("所有示例运行完成！")
    print("=" * 100)
