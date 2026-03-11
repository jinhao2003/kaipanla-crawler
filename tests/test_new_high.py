# -*- coding: utf-8 -*-
"""
测试百日新高数据获取功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaipanla_crawler import KaipanlaCrawler

def test_single_day():
    """测试获取单日新高数据"""
    print("=" * 80)
    print("测试1: 获取单日新高数据")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_new_high_data("2026-01-16")
    
    print(f"\n日期: 2026-01-16")
    print(f"今日新增: {data}")
    print(f"数据类型: {type(data)}")
    
    # numpy.int64也是数值类型
    import numpy as np
    assert isinstance(data, (int, float, np.integer)), "单日数据应该返回数值"
    print("\n✅ 单日数据测试通过")

def test_date_range():
    """测试获取日期范围新高数据"""
    print("\n" + "=" * 80)
    print("测试2: 获取日期范围新高数据")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_new_high_data("2026-01-16", "2026-01-10")
    
    print(f"\n日期范围: 2026-01-10 到 2026-01-16")
    print(f"数据条数: {len(data)}")
    print("\n数据内容:")
    print(data)
    
    assert len(data) > 0, "应该返回多条数据"
    print("\n✅ 日期范围数据测试通过")

def test_recent_data():
    """测试获取最近一周的数据"""
    print("\n" + "=" * 80)
    print("测试3: 获取最近一周数据")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    data = crawler.get_new_high_data("2026-01-16", "2026-01-09")
    
    print(f"\n日期范围: 2026-01-09 到 2026-01-16")
    print("\n详细数据:")
    for date, value in data.items():
        print(f"  {date}: {value} 只新增")
    
    print(f"\n统计信息:")
    print(f"  平均新增: {data.mean():.1f}")
    print(f"  最大新增: {data.max()}")
    print(f"  最小新增: {data.min()}")
    
    print("\n✅ 最近一周数据测试通过")

if __name__ == "__main__":
    test_single_day()
    test_date_range()
    test_recent_data()
    
    print("\n" + "=" * 80)
    print("✅ 所有测试通过！")
    print("=" * 80)
