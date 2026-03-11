# -*- coding: utf-8 -*-
"""
个股分时数据示例
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaipanla_crawler import KaipanlaCrawler

def main():
    crawler = KaipanlaCrawler()
    
    print("=" * 80)
    print("个股分时数据示例")
    print("=" * 80)
    
    # 获取个股分时数据
    stock_code = "002498"  # 汉缆股份
    date = "2026-01-16"
    
    print(f"\n正在获取股票 {stock_code} 在 {date} 的分时数据...")
    data = crawler.get_stock_intraday(stock_code, date)
    
    # 1. 基本信息
    print("\n【1. 基本信息】")
    print("-" * 80)
    print(f"股票代码: {data['stock_code']}")
    print(f"日期: {data['date']}")
    
    df = data['data']
    open_price = df['price'].iloc[0]
    close_price = df['price'].iloc[-1]
    high_price = df['price'].max()
    low_price = df['price'].min()
    
    print(f"开盘价: {open_price:.2f}")
    print(f"收盘价: {close_price:.2f}")
    print(f"最高价: {high_price:.2f}")
    print(f"最低价: {low_price:.2f}")
    print(f"涨跌幅: {((close_price - open_price) / open_price * 100):+.2f}%")
    print(f"振幅: {((high_price - low_price) / open_price * 100):.2f}%")
    
    # 2. 成交统计
    print("\n【2. 成交统计】")
    print("-" * 80)
    total_volume = df['volume'].sum()
    total_turnover = df['turnover'].sum()
    
    print(f"总成交量: {total_volume:,} 手")
    print(f"总成交额: {total_turnover / 1e8:.2f} 亿元")
    print(f"平均每分钟成交量: {df['volume'].mean():.0f} 手")
    print(f"平均每分钟成交额: {df['turnover'].mean() / 1e6:.2f} 百万元")
    
    # 3. 主力资金
    print("\n【3. 主力资金】")
    print("-" * 80)
    total_inflow = data['total_main_inflow']
    total_outflow = data['total_main_outflow']
    net_flow = total_inflow + total_outflow
    
    print(f"主力净流入: {total_inflow:,} 元 ({total_inflow / 1e8:.2f} 亿)")
    print(f"主力净流出: {total_outflow:,} 元 ({total_outflow / 1e8:.2f} 亿)")
    print(f"主力净额: {net_flow:,} 元 ({net_flow / 1e8:.2f} 亿)")
    
    # 分钟级统计
    inflow_minutes = df[df['main_net_inflow'] > 0]
    outflow_minutes = df[df['main_net_inflow'] < 0]
    
    print(f"\n分钟级统计:")
    print(f"  净流入分钟数: {len(inflow_minutes)} ({len(inflow_minutes)/len(df)*100:.1f}%)")
    print(f"  净流出分钟数: {len(outflow_minutes)} ({len(outflow_minutes)/len(df)*100:.1f}%)")
    
    # 4. 价格与均价对比
    print("\n【4. 价格与均价对比】")
    print("-" * 80)
    flag_counts = df['flag'].value_counts()
    
    above_avg = flag_counts.get(1, 0)
    below_avg = flag_counts.get(0, 0)
    limit_up = flag_counts.get(2, 0)
    
    print(f"现价>=均价: {above_avg} 分钟 ({above_avg/len(df)*100:.1f}%)")
    print(f"现价<均价: {below_avg} 分钟 ({below_avg/len(df)*100:.1f}%)")
    print(f"涨停: {limit_up} 分钟 ({limit_up/len(df)*100:.1f}%)")
    
    # 5. 时段分析
    print("\n【5. 时段分析】")
    print("-" * 80)
    
    morning = df[df['time'] <= '11:30']
    afternoon = df[df['time'] >= '13:00']
    
    print(f"早盘 (09:30-11:30):")
    print(f"  成交量: {morning['volume'].sum():,} 手 ({morning['volume'].sum()/total_volume*100:.1f}%)")
    print(f"  成交额: {morning['turnover'].sum() / 1e8:.2f} 亿元")
    print(f"  主力净流入: {morning['main_net_inflow'].sum() / 1e8:.2f} 亿元")
    
    print(f"\n午盘 (13:00-15:00):")
    print(f"  成交量: {afternoon['volume'].sum():,} 手 ({afternoon['volume'].sum()/total_volume*100:.1f}%)")
    print(f"  成交额: {afternoon['turnover'].sum() / 1e8:.2f} 亿元")
    print(f"  主力净流入: {afternoon['main_net_inflow'].sum() / 1e8:.2f} 亿元")
    
    # 6. 关键时刻
    print("\n【6. 关键时刻】")
    print("-" * 80)
    
    # 最高价时刻
    max_price_idx = df['price'].idxmax()
    print(f"最高价时刻: {df.loc[max_price_idx, 'time']} ({df.loc[max_price_idx, 'price']:.2f})")
    
    # 最低价时刻
    min_price_idx = df['price'].idxmin()
    print(f"最低价时刻: {df.loc[min_price_idx, 'time']} ({df.loc[min_price_idx, 'price']:.2f})")
    
    # 最大成交量时刻
    max_vol_idx = df['volume'].idxmax()
    print(f"最大成交量时刻: {df.loc[max_vol_idx, 'time']} ({df.loc[max_vol_idx, 'volume']:,} 手)")
    
    # 最大主力净流入时刻
    max_inflow_idx = df['main_net_inflow'].idxmax()
    print(f"最大主力净流入时刻: {df.loc[max_inflow_idx, 'time']} ({df.loc[max_inflow_idx, 'main_net_inflow'] / 1e6:.2f} 百万元)")
    
    # 7. 数据预览
    print("\n【7. 数据预览】")
    print("-" * 80)
    print("前10条数据:")
    print(df.head(10).to_string(index=False))
    
    print("\n提示: 可以使用 matplotlib 绘制分时图和主力资金流向图")

if __name__ == "__main__":
    main()
