# -*- coding: utf-8 -*-
"""
异动个股数据示例
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaipanla_crawler import KaipanlaCrawler
import pandas as pd

def main():
    crawler = KaipanlaCrawler()
    
    print("=" * 80)
    print("异动个股数据示例")
    print("=" * 80)
    
    print("\n正在获取最新异动个股数据...")
    data = crawler.get_abnormal_stocks()
    
    # 1. 基本信息
    print("\n【1. 基本信息】")
    print("-" * 80)
    print(f"日期: {data['date']}")
    print(f"异动股票总数: {data['total_count']}")
    print(f"盘中异动: {len(data['intraday'])}只")
    print(f"收盘异动: {len(data['closed'])}只")
    print(f"涨跌监控: {len(data['monitor_list'])}只")
    print(f"五线回踩: {len(data['callback_list'])}只")
    
    # 2. 盘中异动股票
    if not data['intraday'].empty:
        print("\n【2. 盘中异动股票】")
        print("-" * 80)
        print(data['intraday'].to_string(index=False))
    
    # 3. 收盘异动股票
    if not data['closed'].empty:
        print("\n【3. 收盘异动股票】")
        print("-" * 80)
        print(data['closed'].to_string(index=False))
    
    # 4. 异动原因分析
    print("\n【4. 异动原因分析】")
    print("-" * 80)
    all_stocks = pd.concat([data['intraday'], data['closed']], ignore_index=True)
    
    if not all_stocks.empty:
        reason_counts = all_stocks['reason'].value_counts()
        for reason, count in reason_counts.items():
            print(f"{reason}: {count}只 ({count/len(all_stocks)*100:.1f}%)")
    
    # 5. 风险等级分类
    print("\n【5. 风险等级分类】")
    print("-" * 80)
    
    if not all_stocks.empty:
        # 高风险：偏离值>150%或连续天数>25天
        high_risk = all_stocks[(all_stocks['deviation'] > 150) | (all_stocks['days'] > 25)]
        print(f"高风险股票: {len(high_risk)}只")
        if not high_risk.empty:
            for _, row in high_risk.iterrows():
                print(f"  {row['stock_code']} {row['stock_name']}: 偏离{row['deviation']:.1f}%, 连续{row['days']}天")
        
        # 中风险：偏离值100-150%或连续天数15-25天
        medium_risk = all_stocks[
            ((all_stocks['deviation'] > 100) & (all_stocks['deviation'] <= 150)) |
            ((all_stocks['days'] > 15) & (all_stocks['days'] <= 25))
        ]
        medium_risk = medium_risk[~medium_risk.index.isin(high_risk.index)]
        print(f"\n中风险股票: {len(medium_risk)}只")
        if not medium_risk.empty:
            for _, row in medium_risk.iterrows():
                print(f"  {row['stock_code']} {row['stock_name']}: 偏离{row['deviation']:.1f}%, 连续{row['days']}天")
        
        # 低风险：其他
        low_risk = all_stocks[~all_stocks.index.isin(high_risk.index) & ~all_stocks.index.isin(medium_risk.index)]
        print(f"\n低风险股票: {len(low_risk)}只")
        if not low_risk.empty:
            for _, row in low_risk.iterrows():
                print(f"  {row['stock_code']} {row['stock_name']}: 偏离{row['deviation']:.1f}%, 连续{row['days']}天")
    
    # 6. 统计分析
    print("\n【6. 统计分析】")
    print("-" * 80)
    
    if not all_stocks.empty:
        print(f"连续天数:")
        print(f"  平均: {all_stocks['days'].mean():.1f}天")
        print(f"  最长: {all_stocks['days'].max()}天")
        print(f"  最短: {all_stocks['days'].min()}天")
        
        print(f"\n偏离值:")
        print(f"  平均: {all_stocks['deviation'].mean():.2f}%")
        print(f"  最大: {all_stocks['deviation'].max():.2f}%")
        print(f"  最小: {all_stocks['deviation'].min():.2f}%")
        
        if not data['closed'].empty:
            closed_with_change = data['closed'][data['closed']['change_pct'] != 0]
            if not closed_with_change.empty:
                print(f"\n收盘涨跌幅:")
                print(f"  平均: {closed_with_change['change_pct'].mean():.2f}%")
                print(f"  最大: {closed_with_change['change_pct'].max():.2f}%")
                print(f"  最小: {closed_with_change['change_pct'].min():.2f}%")
    
    # 7. 监控列表
    if data['monitor_list']:
        print("\n【7. 涨跌监控股票】")
        print("-" * 80)
        for stock in data['monitor_list']:
            print(f"{stock['stock_code']} {stock['stock_name']}")
    
    if data['callback_list']:
        print("\n【8. 五线回踩股票】")
        print("-" * 80)
        for stock in data['callback_list']:
            print(f"{stock['stock_code']} {stock['stock_name']}")
    
    print("\n提示: 异动股票风险较高，请谨慎操作！")

if __name__ == "__main__":
    main()
