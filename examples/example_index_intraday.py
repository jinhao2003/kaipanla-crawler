# -*- coding: utf-8 -*-
"""
指数分时功能示例

展示如何使用 get_index_intraday() 函数获取指数分时数据
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaipanla_crawler import KaipanlaCrawler
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def example_basic():
    """基本使用示例"""
    print("=" * 80)
    print("示例1: 获取上证指数分时")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_index_intraday("SH000001")
    
    print(f"\n日期: {data['date']}")
    print(f"指数代码: {data['index_code']}")
    print(f"昨收: {data['preclose']:.2f}")
    print(f"开盘: {data['open']:.2f}")
    print(f"最高: {data['high']:.2f}")
    print(f"最低: {data['low']:.2f}")
    print(f"收盘: {data['close']:.2f}")
    
    change = data['close'] - data['preclose']
    change_pct = (change / data['preclose']) * 100
    print(f"涨跌: {change:.2f}")
    print(f"涨跌幅: {change_pct:.2f}%")
    
    print(f"\n分时数据点数: {len(data['data'])}")
    print("\n前10条分时数据:")
    print(data['data'].head(10))

def example_analysis():
    """数据分析示例"""
    print("\n" + "=" * 80)
    print("示例2: 分时数据分析")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_index_intraday("SH000001")
    
    df = data['data']
    
    print("\n【价格统计】")
    print("-" * 80)
    print(f"最高价: {df['price'].max():.2f}")
    print(f"最低价: {df['price'].min():.2f}")
    print(f"平均价: {df['price'].mean():.2f}")
    print(f"振幅: {((df['price'].max() - df['price'].min()) / data['preclose'] * 100):.2f}%")
    
    print("\n【成交量统计】")
    print("-" * 80)
    print(f"总成交量: {df['volume'].sum():,}")
    print(f"平均每分钟成交量: {df['volume'].mean():.0f}")
    print(f"最大单分钟成交量: {df['volume'].max():,}")
    
    print("\n【涨跌统计】")
    print("-" * 80)
    up_count = len(df[df['flag'] == 1])
    down_count = len(df[df['flag'] == 0])
    print(f"上涨分钟数: {up_count}")
    print(f"下跌分钟数: {down_count}")
    print(f"上涨占比: {up_count / len(df) * 100:.1f}%")
    
    print("\n【价格与均价对比】")
    print("-" * 80)
    above_avg = len(df[df['price'] > df['avg_price']])
    below_avg = len(df[df['price'] < df['avg_price']])
    print(f"价格高于均价: {above_avg} 分钟 ({above_avg / len(df) * 100:.1f}%)")
    print(f"价格低于均价: {below_avg} 分钟 ({below_avg / len(df) * 100:.1f}%)")

def example_compare():
    """对比多个指数"""
    print("\n" + "=" * 80)
    print("示例3: 对比多个指数")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    
    indexes = [
        ("SH000001", "上证指数"),
        ("SZ399001", "深证成指"),
        ("SZ399006", "创业板指")
    ]
    
    print("\n指数对比:")
    print("-" * 80)
    print(f"{'指数名称':<10} {'昨收':>10} {'开盘':>10} {'收盘':>10} {'涨跌幅':>10}")
    print("-" * 80)
    
    for code, name in indexes:
        data = crawler.get_index_intraday(code)
        if len(data['data']) > 0:
            change_pct = ((data['close'] - data['preclose']) / data['preclose']) * 100
            print(f"{name:<10} {data['preclose']:>10.2f} {data['open']:>10.2f} {data['close']:>10.2f} {change_pct:>9.2f}%")

def example_plot():
    """绘制分时图"""
    print("\n" + "=" * 80)
    print("示例4: 绘制分时图")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_index_intraday("SH000001")
    
    df = data['data']
    
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    
    # 绘制价格和均价
    ax1.plot(df.index, df['price'], label='价格', linewidth=1.5)
    ax1.plot(df.index, df['avg_price'], label='均价', linewidth=1.5, linestyle='--')
    ax1.axhline(y=data['preclose'], color='gray', linestyle=':', label='昨收')
    ax1.set_ylabel('价格')
    ax1.set_title(f"{data['index_code']} 分时图 ({data['date']})")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 绘制成交量
    colors = ['red' if flag == 1 else 'green' for flag in df['flag']]
    ax2.bar(df.index, df['volume'], color=colors, alpha=0.6)
    ax2.set_ylabel('成交量')
    ax2.set_xlabel('时间点')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # 保存图表
    filename = f"index_intraday_{data['index_code']}_{data['date']}.png"
    plt.savefig(filename, dpi=100, bbox_inches='tight')
    print(f"\n图表已保存到: {filename}")
    
    # 显示图表（可选）
    # plt.show()

def example_save():
    """保存数据示例"""
    print("\n" + "=" * 80)
    print("示例5: 保存数据")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_index_intraday("SH000001")
    
    # 保存为CSV
    filename = f"index_intraday_{data['index_code']}_{data['date']}.csv"
    data['data'].to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n分时数据已保存到: {filename}")
    
    # 保存汇总信息
    summary = {
        "日期": data['date'],
        "指数代码": data['index_code'],
        "昨收": data['preclose'],
        "开盘": data['open'],
        "最高": data['high'],
        "最低": data['low'],
        "收盘": data['close'],
        "涨跌": data['close'] - data['preclose'],
        "涨跌幅(%)": ((data['close'] - data['preclose']) / data['preclose']) * 100
    }
    
    import json
    summary_filename = f"index_summary_{data['index_code']}_{data['date']}.json"
    with open(summary_filename, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"汇总信息已保存到: {summary_filename}")

if __name__ == "__main__":
    example_basic()
    example_analysis()
    example_compare()
    
    # 取消注释以运行其他示例
    # example_plot()  # 需要matplotlib
    # example_save()
    
    print("\n" + "=" * 80)
    print("✅ 所有示例运行完成！")
    print("=" * 80)
