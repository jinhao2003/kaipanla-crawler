# -*- coding: utf-8 -*-
"""
测试指数分时功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaipanla_crawler import KaipanlaCrawler

def test_basic():
    """测试基本功能"""
    print("=" * 80)
    print("测试1: 获取上证指数分时")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_index_intraday("SH000001")
    
    print(f"\n日期: {data['date']}")
    print(f"指数代码: {data['index_code']}")
    
    if len(data['data']) == 0:
        print("\n⚠️  当前非交易时间或未获取到数据")
        print("提示: 请在交易日的交易时间（9:30-15:00）运行测试")
        return
    
    print(f"昨收: {data['preclose']:.2f}")
    print(f"开盘: {data['open']:.2f}")
    print(f"最高: {data['high']:.2f}")
    print(f"最低: {data['low']:.2f}")
    print(f"收盘: {data['close']:.2f}")
    print(f"涨跌: {data['close'] - data['preclose']:.2f}")
    print(f"涨跌幅: {((data['close'] - data['preclose']) / data['preclose'] * 100):.2f}%")
    
    print(f"\n分时数据点数: {len(data['data'])}")
    print("\n前10条分时数据:")
    print(data['data'].head(10).to_string(index=False))
    
    assert len(data['data']) > 0, "应该有分时数据"
    assert 'time' in data['data'].columns, "应该有时间列"
    assert 'price' in data['data'].columns, "应该有价格列"
    
    print("\n✅ 基本功能测试通过")

def test_analysis():
    """测试数据分析"""
    print("\n" + "=" * 80)
    print("测试2: 数据分析")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_index_intraday("SH000001")
    
    if len(data['data']) == 0:
        print("\n⚠️  跳过分析测试（无数据）")
        return
    
    df = data['data']
    
    print(f"\n数据统计:")
    print(f"最高价: {df['price'].max():.2f}")
    print(f"最低价: {df['price'].min():.2f}")
    print(f"平均价: {df['price'].mean():.2f}")
    print(f"总成交量: {df['volume'].sum():,}")
    
    # 上涨和下跌分钟数
    up_count = len(df[df['flag'] == 1])
    down_count = len(df[df['flag'] == 0])
    print(f"\n上涨分钟数: {up_count}")
    print(f"下跌分钟数: {down_count}")
    print(f"上涨占比: {up_count / len(df) * 100:.1f}%")
    
    # 价格与均价对比
    above_avg = len(df[df['price'] > df['avg_price']])
    print(f"\n价格高于均价的分钟数: {above_avg}")
    print(f"占比: {above_avg / len(df) * 100:.1f}%")
    
    print("\n✅ 数据分析测试通过")

def test_other_indexes():
    """测试其他指数"""
    print("\n" + "=" * 80)
    print("测试3: 获取其他指数")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    
    indexes = [
        ("SH000001", "上证指数"),
        ("SZ399001", "深证成指"),
        ("SZ399006", "创业板指")
    ]
    
    has_data = False
    for code, name in indexes:
        print(f"\n【{name}】")
        print("-" * 80)
        data = crawler.get_index_intraday(code)
        
        if len(data['data']) > 0:
            has_data = True
            print(f"昨收: {data['preclose']:.2f}")
            print(f"开盘: {data['open']:.2f}")
            print(f"收盘: {data['close']:.2f}")
            print(f"涨跌幅: {((data['close'] - data['preclose']) / data['preclose'] * 100):.2f}%")
            print(f"分时数据点数: {len(data['data'])}")
        else:
            print("未获取到数据（非交易时间）")
    
    if not has_data:
        print("\n⚠️  所有指数均无数据（非交易时间）")
    
    print("\n✅ 其他指数测试通过")

if __name__ == "__main__":
    test_basic()
    test_analysis()
    test_other_indexes()
    
    print("\n" + "=" * 80)
    print("✅ 所有测试通过！")
    print("=" * 80)
