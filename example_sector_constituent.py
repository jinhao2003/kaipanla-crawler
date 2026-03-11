#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
板块成分股功能使用示例
"""

import sys
sys.path.insert(0, '.')

from kaipanla_crawler import KaipanlaCrawler

def example_1_get_core_stocks():
    """示例1：快速获取核心成分股"""
    print("=" * 100)
    print("示例1：快速获取核心成分股")
    print("=" * 100)
    
    crawler = KaipanlaCrawler()
    
    # 获取化工板块核心成分股（第一页）
    data = crawler.get_sector_constituent_stocks("801235", "2026-02-10")
    
    print(f"\n板块代码: {data['plate_id']}")
    print(f"日期: {data['date']}")
    print(f"返回股票数: {data['total_count']} 只")
    print(f"核心成分股代码数: {len(data['stock_codes'])} 只")
    
    print(f"\n核心成分股代码列表:")
    print(data['stock_codes'])
    
    print(f"\n涨幅前10只股票:")
    for i, stock in enumerate(data['stocks'][:10], 1):
        code = stock[0]
        name = stock[1]
        price = stock[5]
        change = stock[6]
        concept = stock[4]
        print(f"  {i}. {code} {name}: {price} ({change:+.2f}%) - {concept}")

def example_2_get_all_stocks():
    """示例2：获取板块所有相关股票"""
    print("\n" + "=" * 100)
    print("示例2：获取板块所有相关股票")
    print("=" * 100)
    
    crawler = KaipanlaCrawler()
    
    # 获取801632板块所有股票（较小的板块，速度快）
    print("\n正在获取801632板块所有股票...")
    data = crawler.get_sector_all_stocks("801632", "2026-02-10")
    
    print(f"\n板块代码: {data['plate_id']}")
    print(f"核心成分股: {data['core_count']} 只")
    print(f"API显示总数: {data['total_count_from_api']} 只")
    print(f"实际获取: {data['total_count']} 只")
    print(f"获取页数: {data['pages_fetched']} 页")
    
    # 统计涨跌分布
    up_count = sum(1 for s in data['all_stocks'] if s[6] > 0)
    down_count = sum(1 for s in data['all_stocks'] if s[6] < 0)
    flat_count = sum(1 for s in data['all_stocks'] if s[6] == 0)
    
    print(f"\n涨跌分布:")
    print(f"  上涨: {up_count} 只 ({up_count/data['total_count']*100:.1f}%)")
    print(f"  下跌: {down_count} 只 ({down_count/data['total_count']*100:.1f}%)")
    print(f"  平盘: {flat_count} 只 ({flat_count/data['total_count']*100:.1f}%)")

def example_3_find_limit_up():
    """示例3：找出板块涨停股票"""
    print("\n" + "=" * 100)
    print("示例3：找出板块涨停股票")
    print("=" * 100)
    
    crawler = KaipanlaCrawler()
    
    # 获取化工板块核心成分股
    data = crawler.get_sector_constituent_stocks("801235", "2026-02-10")
    
    # 筛选涨停股票
    limit_up_stocks = []
    for stock in data['stocks']:
        change_pct = stock[6]
        if change_pct >= 9.9:  # 涨停
            limit_up_stocks.append({
                'code': stock[0],
                'name': stock[1],
                'price': stock[5],
                'change': stock[6],
                'board': stock[23] if len(stock) > 23 else '',
                'leader': stock[24] if len(stock) > 24 else ''
            })
    
    print(f"\n化工板块涨停股票: {len(limit_up_stocks)} 只")
    for s in limit_up_stocks:
        board_info = f" {s['board']}" if s['board'] else ""
        leader_info = f" {s['leader']}" if s['leader'] else ""
        print(f"  {s['code']} {s['name']}: {s['change']:.2f}%{board_info}{leader_info}")

def example_4_compare_sectors():
    """示例4：对比多个板块"""
    print("\n" + "=" * 100)
    print("示例4：对比多个板块")
    print("=" * 100)
    
    crawler = KaipanlaCrawler()
    
    sectors = [
        ("801235", "化工"),
        ("801632", "801632"),
        ("801346", "电力设备"),
    ]
    
    print(f"\n{'板块代码':<10} {'板块名称':<15} {'核心成分股':<12} {'涨停数':<10} {'平均涨幅':<10}")
    print("-" * 70)
    
    for plate_id, plate_name in sectors:
        data = crawler.get_sector_constituent_stocks(plate_id, "2026-02-10")
        
        # 统计涨停数
        limit_up_count = sum(1 for s in data['stocks'] if s[6] >= 9.9)
        
        # 计算平均涨幅
        avg_change = sum(s[6] for s in data['stocks']) / len(data['stocks'])
        
        print(f"{plate_id:<10} {plate_name:<15} {len(data['stock_codes']):<12} {limit_up_count:<10} {avg_change:>9.2f}%")

def example_5_get_limited_pages():
    """示例5：只获取前几页（快速预览）"""
    print("\n" + "=" * 100)
    print("示例5：只获取前5页（快速预览）")
    print("=" * 100)
    
    crawler = KaipanlaCrawler()
    
    # 只获取化工板块前5页（150只股票）
    print("\n正在获取化工板块前5页...")
    data = crawler.get_sector_all_stocks("801235", "2026-02-10", max_pages=5)
    
    print(f"\n实际获取: {data['total_count']} 只")
    print(f"获取页数: {data['pages_fetched']} 页")
    print(f"API显示总数: {data['total_count_from_api']} 只")
    
    # 按涨跌幅排序
    sorted_stocks = sorted(data['all_stocks'], 
                           key=lambda x: x[6] if len(x) > 6 else 0, 
                           reverse=True)
    
    print(f"\n涨幅前10:")
    for i, stock in enumerate(sorted_stocks[:10], 1):
        code = stock[0]
        name = stock[1]
        price = stock[5]
        change = stock[6]
        print(f"  {i}. {code} {name}: {price} ({change:+.2f}%)")

if __name__ == "__main__":
    # 运行所有示例
    example_1_get_core_stocks()
    example_2_get_all_stocks()
    example_3_find_limit_up()
    example_4_compare_sectors()
    example_5_get_limited_pages()
    
    print("\n" + "=" * 100)
    print("所有示例运行完成！")
    print("=" * 100)
