#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
板块分析综合示例

演示如何使用板块资金和强度功能进行板块分析
"""

from kaipanla_crawler import KaipanlaCrawler
from datetime import datetime


def example_1_sector_capital_monitor():
    """示例1: 板块资金监控"""
    print("=" * 60)
    print("示例1: 板块资金监控")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 监控多个板块的资金流向
    sectors = {
        "801235": "化工",
        "801346": "电力设备",
        "801225": "机械设备",
        "801750": "计算机",
        "801760": "传媒"
    }
    
    print(f"\n{'板块名称':<10} {'成交额(亿)':<12} {'涨跌幅(%)':<10} {'主力净额(亿)':<12} {'主力净占比(%)':<12}")
    print("-" * 70)
    
    for sector_code, sector_name in sectors.items():
        data = crawler.get_sector_capital_data(sector_code)
        if data:
            print(f"{sector_name:<10} "
                  f"{data['turnover'] / 100000000:<12.2f} "
                  f"{data['change_pct']:<10.2f} "
                  f"{data['main_net_inflow'] / 100000000:<12.2f} "
                  f"{data['main_net_inflow_pct']:<12.2f}")


def example_2_sector_strength_trend():
    """示例2: 板块强度趋势分析"""
    print("\n" + "=" * 60)
    print("示例2: 板块强度趋势分析")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 获取7日板块强度数据
    end_date = "2026-01-20"
    df = crawler.get_sector_strength_ndays(end_date, num_days=7)
    
    if df.empty:
        print("获取数据失败")
        return
    
    # 分析板块热度
    sector_trend = df.groupby('板块名称')['涨停数'].sum().sort_values(ascending=False)
    
    print(f"\n7日最强板块 TOP 10:\n")
    print(f"{'排名':<6} {'板块名称':<15} {'总涨停数':<10}")
    print("-" * 40)
    for i, (sector_name, total_count) in enumerate(sector_trend.head(10).items(), 1):
        print(f"{i:<6} {sector_name:<15} {total_count:<10}")


def example_3_sector_rotation_analysis():
    """示例3: 板块轮动分析"""
    print("\n" + "=" * 60)
    print("示例3: 板块轮动分析")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 获取7日板块强度数据
    end_date = "2026-01-20"
    df = crawler.get_sector_strength_ndays(end_date, num_days=7)
    
    if df.empty:
        print("获取数据失败")
        return
    
    # 计算最近3日和前4日的涨停数
    dates = sorted(df['日期'].unique(), reverse=True)
    recent_3days = dates[:3]
    previous_4days = dates[3:7]
    
    recent_strength = df[df['日期'].isin(recent_3days)].groupby('板块名称')['涨停数'].sum()
    previous_strength = df[df['日期'].isin(previous_4days)].groupby('板块名称')['涨停数'].sum()
    
    # 找出强度上升的板块
    strength_change = recent_strength - previous_strength
    rising_sectors = strength_change.sort_values(ascending=False)
    
    print("\n强度上升的板块（可能的轮动机会）:\n")
    print(f"{'板块名称':<15} {'前4日涨停数':<12} {'近3日涨停数':<12} {'变化':<10}")
    print("-" * 55)
    for sector_name, change in rising_sectors.head(10).items():
        prev = previous_strength.get(sector_name, 0)
        recent = recent_strength.get(sector_name, 0)
        print(f"{sector_name:<15} {prev:<12.0f} {recent:<12.0f} {change:+.0f}")


def example_4_sector_persistence_analysis():
    """示例4: 板块持续性分析"""
    print("\n" + "=" * 60)
    print("示例4: 板块持续性分析")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 获取7日板块强度数据
    end_date = "2026-01-20"
    df = crawler.get_sector_strength_ndays(end_date, num_days=7)
    
    if df.empty:
        print("获取数据失败")
        return
    
    # 计算每个板块的持续性（有涨停的天数）
    sector_persistence = df[df['涨停数'] > 0].groupby('板块名称').size()
    sector_persistence = sector_persistence.sort_values(ascending=False)
    
    print("\n持续强势板块（7日内有涨停的天数）:\n")
    print(f"{'板块名称':<15} {'有涨停天数':<12} {'总涨停数':<10} {'平均涨停数':<10}")
    print("-" * 55)
    for sector_name, days in sector_persistence.head(10).items():
        total = df[df['板块名称'] == sector_name]['涨停数'].sum()
        avg = total / days
        print(f"{sector_name:<15} {days:<12} {total:<10} {avg:<10.2f}")


def example_5_sector_capital_strength_combined():
    """示例5: 资金+强度综合分析"""
    print("\n" + "=" * 60)
    print("示例5: 资金+强度综合分析")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 获取7日板块强度数据
    end_date = "2026-01-20"
    df = crawler.get_sector_strength_ndays(end_date, num_days=7)
    
    if df.empty:
        print("获取数据失败")
        return
    
    # 找出最强的5个板块
    sector_trend = df.groupby('板块名称')['涨停数'].sum().sort_values(ascending=False)
    top_sectors = sector_trend.head(5).index.tolist()
    
    # 获取这些板块的板块代码（从最新一天的数据中获取）
    latest_date = sorted(df['日期'].unique(), reverse=True)[0]
    latest_data = df[df['日期'] == latest_date]
    
    print(f"\nTOP 5板块的资金+强度综合分析:\n")
    print(f"{'板块名称':<12} {'7日涨停数':<10} {'成交额(亿)':<12} {'主力净额(亿)':<12} {'综合评分':<10}")
    print("-" * 70)
    
    for sector_name in top_sectors:
        # 获取板块代码
        sector_row = latest_data[latest_data['板块名称'] == sector_name]
        if sector_row.empty:
            continue
        
        sector_code = sector_row.iloc[0]['板块代码']
        total_limit_up = sector_trend[sector_name]
        
        # 获取资金数据
        capital_data = crawler.get_sector_capital_data(sector_code)
        
        if capital_data:
            turnover = capital_data['turnover'] / 100000000
            main_net = capital_data['main_net_inflow'] / 100000000
            
            # 计算综合评分（简单加权）
            # 涨停数权重40%，主力净额权重30%，成交额权重30%
            score = (total_limit_up * 0.4 + 
                    (main_net / 10) * 0.3 + 
                    (turnover / 1000) * 0.3)
            
            print(f"{sector_name:<12} {total_limit_up:<10} {turnover:<12.2f} {main_net:<12.2f} {score:<10.2f}")


def example_6_specific_sector_detail():
    """示例6: 特定板块详细分析"""
    print("\n" + "=" * 60)
    print("示例6: 特定板块详细分析")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 分析化工板块
    sector_code = "801235"
    sector_name = "化工"
    
    print(f"\n{sector_name}板块详细分析:\n")
    
    # 1. 获取资金数据
    capital_data = crawler.get_sector_capital_data(sector_code)
    
    if capital_data:
        print("【资金情况】")
        print(f"  成交额: {capital_data['turnover'] / 100000000:.2f}亿元")
        print(f"  涨跌幅: {capital_data['change_pct']:.2f}%")
        print(f"  主力净额: {capital_data['main_net_inflow'] / 100000000:.2f}亿元")
        print(f"  主力净占比: {capital_data['main_net_inflow_pct']:.2f}%")
        print(f"  上涨家数: {capital_data['up_count']}")
        print(f"  下跌家数: {capital_data['down_count']}")
        print(f"  换手率: {capital_data['turnover_rate']:.2f}%")
    
    # 2. 获取7日强度数据
    end_date = "2026-01-20"
    df = crawler.get_sector_strength_ndays(end_date, num_days=7)
    
    if not df.empty:
        sector_data = df[df['板块名称'] == sector_name].sort_values('日期')
        
        print("\n【7日强度趋势】")
        print(f"  总涨停数: {sector_data['涨停数'].sum()}")
        print(f"  平均涨停数: {sector_data['涨停数'].mean():.2f}")
        print(f"  最高涨停数: {sector_data['涨停数'].max()}")
        print(f"  最低涨停数: {sector_data['涨停数'].min()}")
        
        print("\n  每日涨停数:")
        for _, row in sector_data.iterrows():
            print(f"    {row['日期']}: {row['涨停数']}只")
    
    # 3. 综合评价
    print("\n【综合评价】")
    if capital_data:
        if capital_data['main_net_inflow'] > 0 and capital_data['change_pct'] > 0:
            print("  ✓ 资金面: 强势（主力净流入 + 板块上涨）")
        elif capital_data['main_net_inflow'] < 0 and capital_data['change_pct'] < 0:
            print("  ✗ 资金面: 弱势（主力净流出 + 板块下跌）")
        else:
            print("  - 资金面: 中性")
    
    if not df.empty:
        avg_limit_up = sector_data['涨停数'].mean()
        if avg_limit_up > 10:
            print("  ✓ 强度面: 强势（平均涨停数>10）")
        elif avg_limit_up > 5:
            print("  - 强度面: 中性（平均涨停数5-10）")
        else:
            print("  ✗ 强度面: 弱势（平均涨停数<5）")


if __name__ == "__main__":
    print("板块分析综合示例\n")
    
    examples = [
        example_1_sector_capital_monitor,
        example_2_sector_strength_trend,
        example_3_sector_rotation_analysis,
        example_4_sector_persistence_analysis,
        example_5_sector_capital_strength_combined,
        example_6_specific_sector_detail,
    ]
    
    for example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n示例执行失败: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("示例演示完成")
    print("=" * 60)
