#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 get_yesterday_performance() 函数
"""

import sys
sys.path.insert(0, '.')

from kaipanla_crawler import KaipanlaCrawler

def test_yesterday_performance():
    """测试获取昨日表现数据"""
    
    print("=" * 60)
    print("测试 get_yesterday_performance() 函数")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    # 测试三种类型
    types = [
        ("limit_up", "昨日涨停表现"),
        ("consecutive", "昨日连板表现"),
        ("broken", "昨日破板表现")
    ]
    
    for perf_type, name in types:
        print(f"\n【{name}】")
        data = crawler.get_yesterday_performance(perf_type)
        
        if data:
            print(f"✓ 成功获取数据")
            print(f"  代码: {data['code']}")
            print(f"  日期: {data['day']}")
            print(f"  昨收: {data['preclose_px']:.2f}")
            print(f"  开盘: {data['begin_px']:.2f}")
            print(f"  最高: {data['hprice']:.2f}")
            print(f"  最低: {data['lprice']:.2f}")
            
            if data['trend']:
                current_price = data['trend'][-1][1]
                change = ((current_price - data['preclose_px']) / data['preclose_px']) * 100
                print(f"  现价: {current_price:.2f}")
                print(f"  涨跌幅: {change:+.2f}%")
                print(f"  分时点数: {len(data['trend'])}个")
        else:
            print(f"✗ 未获取到数据")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_yesterday_performance()
