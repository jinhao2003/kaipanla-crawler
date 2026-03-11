# -*- coding: utf-8 -*-
"""
测试大盘指数分时数据接口

测试 get_index_intraday() 方法
"""

from kaipanla_crawler import KaipanlaCrawler
import pandas as pd

def test_realtime_index_intraday():
    """测试获取实时大盘指数分时数据"""
    print("=" * 60)
    print("测试1: 获取上证指数实时分时数据")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 获取上证指数实时分时数据
    data = crawler.get_index_intraday("SH000001")
    
    if not data:
        print("❌ 获取数据失败")
        return False
    
    print(f"\n✓ 成功获取数据")
    print(f"指数代码: {data['index_code']}")
    print(f"指数名称: {data['index_name']}")
    print(f"日期: {data['date']}")
    print(f"昨收价: {data['preclose']:.2f}")
    print(f"开盘价: {data['open']:.2f}")
    print(f"最高价: {data['high']:.2f}")
    print(f"最低价: {data['low']:.2f}")
    print(f"当前价: {data['close']:.2f}")
    print(f"涨跌幅: {data['change_pct']:.2f}%")
    
    # 分析分时数据
    df = data['data']
    print(f"\n分时数据点数: {len(df)}")
    
    if len(df) > 0:
        print(f"\n前5条分时数据:")
        print(df.head())
        
        print(f"\n分时统计:")
        print(f"  最高涨幅: {df['pct_change'].max():.2f}%")
        print(f"  最低涨幅: {df['pct_change'].min():.2f}%")
        print(f"  振幅: {df['pct_change'].max() - df['pct_change'].min():.2f}%")
        
        # 识别关键变盘点
        min_idx = df['pct_change'].idxmin()
        max_idx = df['pct_change'].idxmax()
        
        print(f"\n关键变盘点:")
        print(f"  最低点: {df.loc[min_idx, 'time']}, 涨跌幅: {df.loc[min_idx, 'pct_change']:.2f}%")
        print(f"  最高点: {df.loc[max_idx, 'time']}, 涨跌幅: {df.loc[max_idx, 'pct_change']:.2f}%")
    
    return True


def test_historical_index_intraday():
    """测试获取历史大盘指数分时数据"""
    print("\n" + "=" * 60)
    print("测试2: 获取上证指数历史分时数据")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 获取历史分时数据
    date = "2026-01-20"
    data = crawler.get_index_intraday("SH000001", date)
    
    if not data:
        print(f"❌ 获取 {date} 数据失败")
        return False
    
    print(f"\n✓ 成功获取 {date} 数据")
    print(f"指数名称: {data['index_name']}")
    print(f"昨收价: {data['preclose']:.2f}")
    print(f"收盘价: {data['close']:.2f}")
    print(f"涨跌幅: {data['change_pct']:.2f}%")
    
    # 分析分时数据
    df = data['data']
    print(f"\n分时数据点数: {len(df)}")
    
    if len(df) > 0:
        print(f"\n分时统计:")
        print(f"  最高涨幅: {df['pct_change'].max():.2f}%")
        print(f"  最低涨幅: {df['pct_change'].min():.2f}%")
    
    return True


def test_multiple_indices():
    """测试获取多个指数的分时数据"""
    print("\n" + "=" * 60)
    print("测试3: 获取多个指数的实时分时数据")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    indices = {
        "SH000001": "上证指数",
        "SZ399001": "深证成指",
        "SZ399006": "创业板指"
    }
    
    for index_code, index_name in indices.items():
        print(f"\n获取 {index_name} ({index_code})...")
        data = crawler.get_index_intraday(index_code)
        
        if data:
            print(f"  ✓ 成功")
            print(f"  当前价: {data['close']:.2f}")
            print(f"  涨跌幅: {data['change_pct']:.2f}%")
            print(f"  分时数据点数: {len(data['data'])}")
        else:
            print(f"  ❌ 失败")
    
    return True


def test_resonance_point_detection():
    """测试识别共振点（用于盘面联动分析）"""
    print("\n" + "=" * 60)
    print("测试4: 识别大盘共振点")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 获取实时分时数据
    data = crawler.get_index_intraday("SH000001")
    
    if not data or len(data['data']) == 0:
        print("❌ 获取数据失败")
        return False
    
    df = data['data']
    
    # 识别急跌低点（涨跌幅最低点）
    min_idx = df['pct_change'].idxmin()
    min_point = df.loc[min_idx]
    
    print(f"\n急跌低点:")
    print(f"  时间: {min_point['time']}")
    print(f"  价格: {min_point['price']:.2f}")
    print(f"  涨跌幅: {min_point['pct_change']:.2f}%")
    
    # 识别V型反转点（低点后快速反弹）
    if min_idx < len(df) - 10:
        after_min = df.iloc[min_idx:min_idx+10]
        rebound = after_min['pct_change'].max() - min_point['pct_change']
        
        if rebound > 0.5:  # 反弹超过0.5%
            print(f"\n✓ 检测到V型反转:")
            print(f"  反弹幅度: {rebound:.2f}%")
            print(f"  反转时间: {min_point['time']} 之后")
    
    # 识别突破点（涨跌幅最高点）
    max_idx = df['pct_change'].idxmax()
    max_point = df.loc[max_idx]
    
    print(f"\n突破点:")
    print(f"  时间: {max_point['time']}")
    print(f"  价格: {max_point['price']:.2f}")
    print(f"  涨跌幅: {max_point['pct_change']:.2f}%")
    
    return True


if __name__ == "__main__":
    print("开始测试大盘指数分时数据接口...\n")
    
    # 运行所有测试
    tests = [
        test_realtime_index_intraday,
        test_historical_index_intraday,
        test_multiple_indices,
        test_resonance_point_detection
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("✓ 所有测试通过！")
    else:
        print(f"✗ {total - passed} 个测试失败")
