# -*- coding: utf-8 -*-
"""
测试板块分时数据获取功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaipanla_crawler import KaipanlaCrawler

def test_basic():
    """测试基本功能"""
    print("=" * 80)
    print("测试1: 获取板块分时数据")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    
    # 测试板块代码: 801346 (半导体)
    data = crawler.get_sector_intraday("801346", "2026-01-16")
    
    print(f"\n板块代码: {data['sector_code']}")
    print(f"日期: {data['date']}")
    print(f"开盘价: {data['open']}")
    print(f"收盘价: {data['close']}")
    print(f"最高价: {data['high']}")
    print(f"最低价: {data['low']}")
    print(f"昨收价: {data['preclose']}")
    print(f"涨跌幅: {((data['close'] - data['preclose']) / data['preclose'] * 100):.2f}%")
    
    print(f"\n分时数据条数: {len(data['data'])}")
    print("\n前5条数据:")
    print(data['data'].head())
    
    print("\n最后5条数据:")
    print(data['data'].tail())
    
    assert len(data['data']) > 0, "应该有分时数据"
    print("\n✅ 基本功能测试通过")

def test_data_analysis():
    """测试数据分析"""
    print("\n" + "=" * 80)
    print("测试2: 数据分析")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_sector_intraday("801346", "2026-01-16")
    
    df = data['data']
    
    # 统计分析
    print(f"\n价格统计:")
    print(f"  平均价: {df['price'].mean():.2f}")
    print(f"  最高价: {df['price'].max():.2f}")
    print(f"  最低价: {df['price'].min():.2f}")
    
    print(f"\n成交量统计:")
    print(f"  总成交量: {df['volume'].sum():,}")
    print(f"  平均每分钟成交量: {df['volume'].mean():.0f}")
    print(f"  最大单分钟成交量: {df['volume'].max():,}")
    
    print(f"\n成交额统计:")
    print(f"  总成交额: {df['turnover'].sum():,.0f} 元")
    print(f"  平均每分钟成交额: {df['turnover'].mean():,.0f} 元")
    
    # 涨跌统计
    trend_counts = df['trend'].value_counts()
    print(f"\n涨跌统计:")
    print(f"  上涨分钟数: {trend_counts.get(1, 0)}")
    print(f"  下跌分钟数: {trend_counts.get(0, 0)}")
    print(f"  平盘分钟数: {trend_counts.get(2, 0)}")
    
    print("\n✅ 数据分析测试通过")

def test_time_periods():
    """测试时间段分析"""
    print("\n" + "=" * 80)
    print("测试3: 时间段分析")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_sector_intraday("801346", "2026-01-16")
    
    df = data['data']
    
    # 早盘 (09:30-11:30)
    morning = df[df['time'] <= '11:30']
    print(f"\n早盘 (09:30-11:30):")
    print(f"  成交量: {morning['volume'].sum():,}")
    print(f"  成交额: {morning['turnover'].sum():,.0f} 元")
    print(f"  价格变化: {morning['price'].iloc[0]:.2f} → {morning['price'].iloc[-1]:.2f}")
    
    # 午盘 (13:00-15:00)
    afternoon = df[df['time'] >= '13:00']
    print(f"\n午盘 (13:00-15:00):")
    print(f"  成交量: {afternoon['volume'].sum():,}")
    print(f"  成交额: {afternoon['turnover'].sum():,.0f} 元")
    print(f"  价格变化: {afternoon['price'].iloc[0]:.2f} → {afternoon['price'].iloc[-1]:.2f}")
    
    print("\n✅ 时间段分析测试通过")

if __name__ == "__main__":
    test_basic()
    test_data_analysis()
    test_time_periods()
    
    print("\n" + "=" * 80)
    print("✅ 所有测试通过！")
    print("=" * 80)
