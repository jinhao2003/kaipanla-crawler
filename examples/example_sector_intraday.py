# -*- coding: utf-8 -*-
"""
板块分时数据示例
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaipanla_crawler import KaipanlaCrawler
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def main():
    crawler = KaipanlaCrawler()
    
    print("=" * 80)
    print("板块分时数据示例")
    print("=" * 80)
    
    # 获取半导体板块分时数据
    sector_code = "801346"  # 半导体板块
    date = "2026-01-16"
    
    print(f"\n正在获取板块 {sector_code} 在 {date} 的分时数据...")
    data = crawler.get_sector_intraday(sector_code, date)
    
    # 1. 基本信息
    print("\n【1. 基本信息】")
    print("-" * 80)
    print(f"板块代码: {data['sector_code']}")
    print(f"日期: {data['date']}")
    print(f"开盘价: {data['open']:.2f}")
    print(f"收盘价: {data['close']:.2f}")
    print(f"最高价: {data['high']:.2f}")
    print(f"最低价: {data['low']:.2f}")
    print(f"昨收价: {data['preclose']:.2f}")
    
    change = data['close'] - data['preclose']
    change_pct = (change / data['preclose']) * 100
    print(f"涨跌额: {change:+.2f}")
    print(f"涨跌幅: {change_pct:+.2f}%")
    
    # 2. 成交统计
    df = data['data']
    print("\n【2. 成交统计】")
    print("-" * 80)
    print(f"总成交量: {df['volume'].sum():,} 手")
    print(f"总成交额: {df['turnover'].sum() / 1e8:.2f} 亿元")
    print(f"平均每分钟成交量: {df['volume'].mean():.0f} 手")
    print(f"平均每分钟成交额: {df['turnover'].mean() / 1e6:.2f} 百万元")
    
    # 3. 涨跌统计
    print("\n【3. 涨跌统计】")
    print("-" * 80)
    trend_counts = df['trend'].value_counts()
    up_count = trend_counts.get(1, 0)
    down_count = trend_counts.get(0, 0)
    flat_count = trend_counts.get(2, 0)
    
    print(f"上涨分钟数: {up_count} ({up_count/len(df)*100:.1f}%)")
    print(f"下跌分钟数: {down_count} ({down_count/len(df)*100:.1f}%)")
    print(f"平盘分钟数: {flat_count} ({flat_count/len(df)*100:.1f}%)")
    
    # 4. 时间段分析
    print("\n【4. 时间段分析】")
    print("-" * 80)
    
    # 早盘
    morning = df[df['time'] <= '11:30']
    morning_vol = morning['volume'].sum()
    morning_amt = morning['turnover'].sum()
    
    # 午盘
    afternoon = df[df['time'] >= '13:00']
    afternoon_vol = afternoon['volume'].sum()
    afternoon_amt = afternoon['turnover'].sum()
    
    total_vol = df['volume'].sum()
    total_amt = df['turnover'].sum()
    
    print(f"早盘 (09:30-11:30):")
    print(f"  成交量: {morning_vol:,} 手 ({morning_vol/total_vol*100:.1f}%)")
    print(f"  成交额: {morning_amt/1e8:.2f} 亿元 ({morning_amt/total_amt*100:.1f}%)")
    
    print(f"\n午盘 (13:00-15:00):")
    print(f"  成交量: {afternoon_vol:,} 手 ({afternoon_vol/total_vol*100:.1f}%)")
    print(f"  成交额: {afternoon_amt/1e8:.2f} 亿元 ({afternoon_amt/total_amt*100:.1f}%)")
    
    # 5. 关键时刻
    print("\n【5. 关键时刻】")
    print("-" * 80)
    
    # 最高价时刻
    max_price_idx = df['price'].idxmax()
    max_price_time = df.loc[max_price_idx, 'time']
    max_price = df.loc[max_price_idx, 'price']
    print(f"最高价时刻: {max_price_time} ({max_price:.2f})")
    
    # 最低价时刻
    min_price_idx = df['price'].idxmin()
    min_price_time = df.loc[min_price_idx, 'time']
    min_price = df.loc[min_price_idx, 'price']
    print(f"最低价时刻: {min_price_time} ({min_price:.2f})")
    
    # 最大成交量时刻
    max_vol_idx = df['volume'].idxmax()
    max_vol_time = df.loc[max_vol_idx, 'time']
    max_vol = df.loc[max_vol_idx, 'volume']
    print(f"最大成交量时刻: {max_vol_time} ({max_vol:,} 手)")
    
    # 6. 数据预览
    print("\n【6. 数据预览】")
    print("-" * 80)
    print("前10条数据:")
    print(df.head(10).to_string(index=False))
    
    print("\n提示: 可以使用 matplotlib 绘制分时图")
    print("示例: df.plot(x='time', y='price')")

if __name__ == "__main__":
    main()
