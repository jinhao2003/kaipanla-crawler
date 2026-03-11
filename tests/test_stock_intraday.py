# -*- coding: utf-8 -*-
"""
测试个股分时数据获取功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaipanla_crawler import KaipanlaCrawler

def test_basic():
    """测试基本功能"""
    print("=" * 80)
    print("测试1: 获取个股分时数据")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    
    # 测试股票: 002498 (汉缆股份)
    data = crawler.get_stock_intraday("002498", "2026-01-16")
    
    print(f"\n股票代码: {data['stock_code']}")
    print(f"日期: {data['date']}")
    print(f"主力净流入: {data['total_main_inflow']:,} 元")
    print(f"主力净流出: {data['total_main_outflow']:,} 元")
    print(f"主力净额: {data['total_main_inflow'] + data['total_main_outflow']:,} 元")
    
    df = data['data']
    print(f"\n分时数据条数: {len(df)}")
    print("\n前5条数据:")
    print(df.head())
    
    print("\n最后5条数据:")
    print(df.tail())
    
    assert len(df) > 0, "应该有分时数据"
    print("\n✅ 基本功能测试通过")

def test_data_analysis():
    """测试数据分析"""
    print("\n" + "=" * 80)
    print("测试2: 数据分析")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_stock_intraday("002498", "2026-01-16")
    
    df = data['data']
    
    # 价格统计
    print(f"\n价格统计:")
    print(f"  开盘价: {df['price'].iloc[0]:.2f}")
    print(f"  收盘价: {df['price'].iloc[-1]:.2f}")
    print(f"  最高价: {df['price'].max():.2f}")
    print(f"  最低价: {df['price'].min():.2f}")
    print(f"  平均价: {df['avg_price'].mean():.2f}")
    
    # 成交统计
    print(f"\n成交统计:")
    print(f"  总成交量: {df['volume'].sum():,} 手")
    print(f"  总成交额: {df['turnover'].sum() / 1e8:.2f} 亿元")
    print(f"  平均每分钟成交量: {df['volume'].mean():.0f} 手")
    
    # 主力资金统计
    print(f"\n主力资金统计:")
    print(f"  全天净流入: {data['total_main_inflow']:,} 元")
    print(f"  全天净流出: {data['total_main_outflow']:,} 元")
    print(f"  净额: {data['total_main_inflow'] + data['total_main_outflow']:,} 元")
    
    # 分钟级主力资金
    inflow_minutes = df[df['main_net_inflow'] > 0]
    outflow_minutes = df[df['main_net_inflow'] < 0]
    print(f"  净流入分钟数: {len(inflow_minutes)}")
    print(f"  净流出分钟数: {len(outflow_minutes)}")
    
    # Flag统计
    flag_counts = df['flag'].value_counts()
    print(f"\n价格标志统计:")
    print(f"  现价>=均价: {flag_counts.get(1, 0)} 分钟")
    print(f"  现价<均价: {flag_counts.get(0, 0)} 分钟")
    print(f"  涨停: {flag_counts.get(2, 0)} 分钟")
    
    print("\n✅ 数据分析测试通过")

def test_main_flow():
    """测试主力资金流向"""
    print("\n" + "=" * 80)
    print("测试3: 主力资金流向分析")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_stock_intraday("002498", "2026-01-16")
    
    df = data['data']
    
    # 找出主力净流入最大的时刻
    max_inflow_idx = df['main_net_inflow'].idxmax()
    max_inflow_time = df.loc[max_inflow_idx, 'time']
    max_inflow = df.loc[max_inflow_idx, 'main_net_inflow']
    
    print(f"\n最大净流入时刻:")
    print(f"  时间: {max_inflow_time}")
    print(f"  净流入: {max_inflow:,} 元")
    print(f"  价格: {df.loc[max_inflow_idx, 'price']:.2f}")
    
    # 找出主力净流出最大的时刻
    min_inflow_idx = df['main_net_inflow'].idxmin()
    min_inflow_time = df.loc[min_inflow_idx, 'time']
    min_inflow = df.loc[min_inflow_idx, 'main_net_inflow']
    
    print(f"\n最大净流出时刻:")
    print(f"  时间: {min_inflow_time}")
    print(f"  净流出: {min_inflow:,} 元")
    print(f"  价格: {df.loc[min_inflow_idx, 'price']:.2f}")
    
    # 早盘和午盘主力资金对比
    morning = df[df['time'] <= '11:30']
    afternoon = df[df['time'] >= '13:00']
    
    print(f"\n时段对比:")
    print(f"  早盘净流入: {morning['main_net_inflow'].sum():,} 元")
    print(f"  午盘净流入: {afternoon['main_net_inflow'].sum():,} 元")
    
    print("\n✅ 主力资金流向测试通过")

if __name__ == "__main__":
    test_basic()
    test_data_analysis()
    test_main_flow()
    
    print("\n" + "=" * 80)
    print("✅ 所有测试通过！")
    print("=" * 80)
