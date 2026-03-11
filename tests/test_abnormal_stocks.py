# -*- coding: utf-8 -*-
"""
测试异动个股数据获取功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaipanla_crawler import KaipanlaCrawler

def test_basic():
    """测试基本功能"""
    print("=" * 80)
    print("测试1: 获取异动个股数据")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_abnormal_stocks()
    
    print(f"\n日期: {data['date']}")
    print(f"异动股票总数: {data['total_count']}")
    print(f"时间戳: {data['timestamp']}")
    
    print(f"\n盘中异动股票数: {len(data['intraday'])}")
    if not data['intraday'].empty:
        print("\n盘中异动股票:")
        print(data['intraday'].to_string(index=False))
    
    print(f"\n收盘异动股票数: {len(data['closed'])}")
    if not data['closed'].empty:
        print("\n收盘异动股票:")
        print(data['closed'].to_string(index=False))
    
    print(f"\n涨跌监控股票数: {len(data['monitor_list'])}")
    if data['monitor_list']:
        print("涨跌监控股票:")
        for stock in data['monitor_list']:
            print(f"  {stock['stock_code']} {stock['stock_name']}")
    
    print(f"\n五线回踩股票数: {len(data['callback_list'])}")
    if data['callback_list']:
        print("五线回踩股票:")
        for stock in data['callback_list']:
            print(f"  {stock['stock_code']} {stock['stock_name']}")
    
    print("\n✅ 基本功能测试通过")

def test_data_analysis():
    """测试数据分析"""
    print("\n" + "=" * 80)
    print("测试2: 数据分析")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_abnormal_stocks()
    
    # 合并盘中和收盘数据
    import pandas as pd
    all_stocks = pd.concat([data['intraday'], data['closed']], ignore_index=True)
    
    if not all_stocks.empty:
        print(f"\n总异动股票数: {len(all_stocks)}")
        
        # 异动原因统计
        print("\n异动原因统计:")
        reason_counts = all_stocks['reason'].value_counts()
        for reason, count in reason_counts.items():
            print(f"  {reason}: {count}只")
        
        # 连续天数统计
        print("\n连续天数统计:")
        print(f"  平均连续天数: {all_stocks['days'].mean():.1f}天")
        print(f"  最长连续天数: {all_stocks['days'].max()}天")
        print(f"  最短连续天数: {all_stocks['days'].min()}天")
        
        # 偏离值统计
        print("\n偏离值统计:")
        print(f"  平均偏离值: {all_stocks['deviation'].mean():.2f}%")
        print(f"  最大偏离值: {all_stocks['deviation'].max():.2f}%")
        print(f"  最小偏离值: {all_stocks['deviation'].min():.2f}%")
        
        # 涨跌幅统计（仅收盘数据有）
        if not data['closed'].empty:
            closed_with_change = data['closed'][data['closed']['change_pct'] != 0]
            if not closed_with_change.empty:
                print("\n收盘涨跌幅统计:")
                print(f"  平均涨跌幅: {closed_with_change['change_pct'].mean():.2f}%")
                print(f"  最大涨幅: {closed_with_change['change_pct'].max():.2f}%")
                print(f"  最大跌幅: {closed_with_change['change_pct'].min():.2f}%")
    
    print("\n✅ 数据分析测试通过")

def test_high_risk_stocks():
    """测试高风险股票筛选"""
    print("\n" + "=" * 80)
    print("测试3: 高风险股票筛选")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_abnormal_stocks()
    
    # 合并数据
    import pandas as pd
    all_stocks = pd.concat([data['intraday'], data['closed']], ignore_index=True)
    
    if not all_stocks.empty:
        # 筛选高偏离值股票（偏离值>100%）
        high_deviation = all_stocks[all_stocks['deviation'] > 100]
        print(f"\n高偏离值股票（>100%）: {len(high_deviation)}只")
        if not high_deviation.empty:
            print(high_deviation[['stock_code', 'stock_name', 'deviation', 'days']].to_string(index=False))
        
        # 筛选长期异动股票（连续天数>20天）
        long_term = all_stocks[all_stocks['days'] > 20]
        print(f"\n长期异动股票（>20天）: {len(long_term)}只")
        if not long_term.empty:
            print(long_term[['stock_code', 'stock_name', 'days', 'deviation']].to_string(index=False))
    
    print("\n✅ 高风险股票筛选测试通过")

if __name__ == "__main__":
    test_basic()
    test_data_analysis()
    test_high_risk_stocks()
    
    print("\n" + "=" * 80)
    print("✅ 所有测试通过！")
    print("=" * 80)
