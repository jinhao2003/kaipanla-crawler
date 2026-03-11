#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
详细核对板块成分股字段映射
"""

import sys
sys.path.insert(0, '.')

from kaipanla_crawler import KaipanlaCrawler
import requests
import uuid

def test_field_mapping():
    """测试字段映射"""
    crawler = KaipanlaCrawler()
    
    plate_id = "801235"  # 化工板块
    date = "2026-02-10"
    
    print("=" * 120)
    print("测试：详细核对板块成分股字段映射")
    print("=" * 120)
    
    # 请求数据
    data_params = {
        "Order": "1",
        "TSZB": "0",
        "a": "ZhiShuStockList_W8",
        "st": "30",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "old": "1",
        "DeviceID": str(uuid.uuid4()),
        "VerSion": "5.21.0.2",
        "IsZZ": "0",
        "Token": "0daffcf404348e2fb714795ba5bdff02",
        "Index": "0",
        "Date": date,
        "apiv": "w42",
        "Type": "6",
        "IsKZZType": "0",
        "UserID": "4315515",
        "PlateID": plate_id,
        "TSZB_Type": "0",
        "filterType": "0"
    }
    
    response = requests.post(
        crawler.base_url,
        data=data_params,
        headers=crawler.headers,
        verify=False,
        proxies={'http': None, 'https': None},
        timeout=30
    )
    result = response.json()
    
    stocks = result.get("list", [])
    
    if not stocks:
        print("没有获取到数据")
        return
    
    # 取第一只股票详细分析
    first_stock = stocks[0]
    
    print(f"\n第一只股票原始数据:")
    print(f"数组长度: {len(first_stock)}")
    print(f"股票代码: {first_stock[0]}")
    print(f"股票名称: {first_stock[1]}")
    
    # 根据你提供的字段说明，创建完整的字段映射
    field_mapping = {
        0: "股票代码",
        1: "股票名称",
        2: "未知2",
        3: "未知3",
        4: "所属板块（多个以顿号分割）",
        5: "价格",
        6: "涨幅（%）",
        7: "成交额",
        8: "实际换手（%）",
        9: "未知9",
        10: "实际流通市值",
        11: "主力买",
        12: "主力卖",
        13: "主力净额",
        14: "买成占比（%）",
        15: "卖成占比（%）",
        16: "净成占比（%）",
        17: "买流占比（%）",
        18: "卖流占比（%）",
        19: "净流占比（%）",
        20: "区间涨幅（%）",
        21: "量比",
        22: "未知22",
        23: "连板天数（如10天7板）",
        24: "板块地位（龙一、龙二...）",
        25: "换手率",
        26: "未知26",
        27: "未知27",
        28: "收盘封单",
        29: "最大封单",
        30: "未知30",
        31: "未知31",
        32: "未知32",
        33: "振幅（%）",
        34: "未知34",
        35: "未知35",
        36: "未知36",
        37: "总市值",
        38: "流通市值",
        39: "未知39",
        40: "领涨次数",
        41: "未知41",
        42: "第四季度机构增仓",
        43: "未知43",
        44: "2025年预测净利润",
        45: "2026年预测净利润",
        46: "未知46",
        47: "2025年动态预测PE",
        48: "2026年动态预测PE",
        49: "日期（如2022-03-31）",
        50: "300w以上大单净额",
        51: "未知51",
        52: "2027年动态预测PE",
        53: "市净率（PB）",
        54: "涨幅",
        55: "未知55",
        56: "价格",
        57: "涨幅",
        58: "人气值",
        59: "排名变化",
        60: "PE（动）",
        61: "PETTM",
        62: "PE（静）",
    }
    
    print(f"\n详细字段映射（共 {len(first_stock)} 个字段）:")
    print("-" * 120)
    print(f"{'索引':<5} {'字段名':<35} {'值':<50} {'类型':<15}")
    print("-" * 120)
    
    for i, value in enumerate(first_stock):
        field_name = field_mapping.get(i, f"未知{i}")
        value_str = str(value)[:47] + "..." if len(str(value)) > 50 else str(value)
        value_type = type(value).__name__
        print(f"{i:<5} {field_name:<35} {value_str:<50} {value_type:<15}")
    
    # 显示前5只股票的关键字段对比
    print("\n" + "=" * 120)
    print("前5只股票关键字段对比")
    print("=" * 120)
    print(f"{'代码':<10} {'名称':<12} {'价格':<8} {'涨幅%':<8} {'成交额':<12} {'换手%':<8} {'连板':<12} {'地位':<8}")
    print("-" * 120)
    
    for stock in stocks[:5]:
        code = stock[0]
        name = stock[1]
        price = stock[5]
        change = stock[6]
        turnover = stock[7]
        turnover_rate = stock[8]
        board = stock[23] if len(stock) > 23 else ""
        leader = stock[24] if len(stock) > 24 else ""
        
        print(f"{code:<10} {name:<12} {price:<8} {change:<8.2f} {turnover:<12} {turnover_rate:<8.2f} {board:<12} {leader:<8}")

def compare_two_interfaces():
    """对比两个接口的参数差异"""
    print("\n" + "=" * 120)
    print("对比两个接口的参数差异")
    print("=" * 120)
    
    # 第一个接口（你提供的）
    interface1 = {
        "Order": "1",
        "TSZB": "0",
        "a": "ZhiShuStockList_W8",
        "st": "30",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "old": "1",
        "DeviceID": "e78ba169-6c03-3faf-8e5e-a72f8411a8eb",
        "VerSion": "5.21.0.2",
        "IsZZ": "0",
        "Token": "0daffcf404348e2fb714795ba5bdff02",
        "Index": "0",
        "Date": "2026-02-10",
        "apiv": "w42",
        "Type": "6",
        "IsKZZType": "0",
        "UserID": "4315515",
        "PlateID": "801235",
        "TSZB_Type": "0",
        "filterType": "0"
    }
    
    # 第二个接口（我们使用的）
    interface2 = {
        "Order": "1",
        "TSZB": "0",
        "a": "ZhiShuStockList_W8",
        "st": "30",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "old": "1",
        "DeviceID": "e78ba169-6c03-3faf-8e5e-a72f8411a8eb",
        "VerSion": "5.21.0.2",
        "IsZZ": "0",
        "Token": "0daffcf404348e2fb714795ba5bdff02",
        "Index": "0",
        "Date": "2026-02-10",
        "apiv": "w42",
        "Type": "6",
        "IsKZZType": "0",
        "UserID": "4315515",
        "PlateID": "801235",
        "TSZB_Type": "0",
        "filterType": "0"
    }
    
    print("\n参数对比:")
    print(f"{'参数名':<20} {'接口1':<40} {'接口2':<40} {'是否相同':<10}")
    print("-" * 120)
    
    all_keys = set(interface1.keys()) | set(interface2.keys())
    
    for key in sorted(all_keys):
        val1 = interface1.get(key, "缺失")
        val2 = interface2.get(key, "缺失")
        same = "✓" if val1 == val2 else "✗"
        print(f"{key:<20} {str(val1):<40} {str(val2):<40} {same:<10}")
    
    print("\n结论:")
    if interface1 == interface2:
        print("  ✓ 两个接口的参数完全相同")
    else:
        print("  ✗ 两个接口的参数有差异")
        diff_keys = [k for k in all_keys if interface1.get(k) != interface2.get(k)]
        print(f"  差异参数: {diff_keys}")

if __name__ == "__main__":
    test_field_mapping()
    compare_two_interfaces()
