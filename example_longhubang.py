#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
龙虎榜功能使用示例
"""

from kaipanla_crawler import KaipanlaCrawler
from datetime import datetime, timedelta

def example_stock_list():
    """示例1: 获取龙虎榜上榜个股列表"""
    print("=" * 60)
    print("示例1: 获取龙虎榜上榜个股列表")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 获取当日龙虎榜
    print("\n获取当日龙虎榜...")
    result = crawler.get_longhubang_stock_list()
    
    print(f"\n日期: {result['date']}")
    print(f"上榜个股数量: {result['total_count']}")
    
    if result['stocks']:
        print("\n前10只上榜个股:")
        for i, stock in enumerate(result['stocks'][:10], 1):
            print(f"{i}. {stock['stock_name']} ({stock['stock_code']})")
            print(f"   涨跌幅: {stock['change_pct']}%")
            print(f"   上榜原因: {stock['reason_type']}")
            print(f"   买入金额: {stock['buy_amount']:,.0f}")
            print(f"   换手率: {stock['turnover_ratio']}%")
            print()

def example_stock_detail():
    """示例2: 获取个股龙虎榜详细数据"""
    print("=" * 60)
    print("示例2: 获取个股龙虎榜详细数据")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 先获取上榜个股列表
    list_result = crawler.get_longhubang_stock_list()
    
    if not list_result['stocks']:
        print("当前没有上榜个股")
        return
    
    # 获取第一只个股的详细数据
    first_stock = list_result['stocks'][0]
    stock_code = first_stock['stock_code']
    
    print(f"\n获取 {first_stock['stock_name']} ({stock_code}) 的详细数据...")
    
    detail = crawler.get_longhubang_stock_detail(stock_code)
    
    if detail:
        print(f"\n股票: {detail['stock_name']} ({detail['stock_code']})")
        print(f"日期: {detail['date']}")
        print(f"当前价: {detail['current_price']}")
        print(f"涨跌幅: {detail['change_pct']}%")
        print(f"换手率: {detail['turnover_ratio']}%")
        print(f"净买入: {detail['net_buy_amount']:,.0f}")
        print(f"上榜次数: {detail['on_list_count']}")
        
        # 显示买卖数据
        for idx, data in enumerate(detail['buy_sell_data'], 1):
            print(f"\n--- 上榜记录 {idx} ---")
            print(f"上榜原因: {', '.join(data['up_reason'])}")
            print(f"买入总额: {data['buy_total']:,.0f}")
            print(f"卖出总额: {data['sell_total']:,.0f}")
            
            print("\n买入前五:")
            for seat in data['buy_list'][:5]:
                print(f"  {seat['seat_name']}: {seat['buy_amount']:,.0f}")
                if seat['group_icon']:
                    print(f"    标签: {', '.join(seat['group_icon'])}")
            
            print("\n卖出前五:")
            for seat in data['sell_list'][:5]:
                print(f"  {seat['seat_name']}: {seat['sell_amount']:,.0f}")

def example_historical_data():
    """示例3: 获取历史龙虎榜数据"""
    print("=" * 60)
    print("示例3: 获取历史龙虎榜数据")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 获取昨天的日期
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"\n获取 {yesterday} 的龙虎榜数据...")
    result = crawler.get_longhubang_stock_list(yesterday)
    
    print(f"\n日期: {result['date']}")
    print(f"上榜个股数量: {result['total_count']}")
    
    if result['stocks']:
        print("\n涨幅前5名:")
        sorted_stocks = sorted(result['stocks'], 
                              key=lambda x: float(x['change_pct']) if x['change_pct'] else 0, 
                              reverse=True)
        
        for i, stock in enumerate(sorted_stocks[:5], 1):
            print(f"{i}. {stock['stock_name']} ({stock['stock_code']}): {stock['change_pct']}%")

def example_dataframe():
    """示例4: 使用DataFrame格式分析数据"""
    print("=" * 60)
    print("示例4: 使用DataFrame格式分析数据")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    print("\n获取龙虎榜DataFrame...")
    df = crawler.get_longhubang_dataframe()
    
    if df.empty:
        print("当前没有龙虎榜数据")
        return
    
    print(f"\n数据概览:")
    print(f"上榜个股数量: {len(df)}")
    
    # 转换数值类型
    df['change_pct_float'] = df['change_pct'].astype(float)
    df['turnover_ratio_float'] = df['turnover_ratio'].astype(float)
    
    print(f"平均涨跌幅: {df['change_pct_float'].mean():.2f}%")
    print(f"平均换手率: {df['turnover_ratio_float'].mean():.2f}%")
    print(f"总买入金额: {df['buy_amount'].sum():,.0f}")
    
    # 筛选高换手率个股
    print(f"\n换手率>20%的个股:")
    high_turnover = df[df['turnover_ratio_float'] > 20]
    if not high_turnover.empty:
        for _, row in high_turnover.iterrows():
            print(f"  {row['stock_name']} ({row['stock_code']}): "
                  f"涨幅{row['change_pct']}%, 换手{row['turnover_ratio']}%")
    else:
        print("  无")
    
    # 统计上榜原因
    print(f"\n上榜原因统计:")
    reason_counts = df['reason_type'].value_counts()
    for reason, count in reason_counts.items():
        print(f"  {reason}: {count}只")

if __name__ == "__main__":
    # 运行所有示例
    example_stock_list()
    print("\n" * 2)
    
    example_stock_detail()
    print("\n" * 2)
    
    example_historical_data()
    print("\n" * 2)
    
    example_dataframe()
