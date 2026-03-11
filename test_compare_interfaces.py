#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
对比两个接口的差异，特别是竞价数据
"""

import sys
sys.path.insert(0, '.')

import requests
import uuid

def test_interface_with_plate_803023():
    """测试PlateID=803023的接口（你提供的新接口）"""
    print("=" * 120)
    print("测试：PlateID=803023 接口（包含竞价数据）")
    print("=" * 120)
    
    url = "https://apphis.longhuvip.com/w1/api/index.php"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; 23116PN5BC Build/PQ3A.190605.01141736)",
        "Host": "apphis.longhuvip.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    
    data = {
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
        "Date": "2026-02-10",
        "apiv": "w42",
        "Type": "6",
        "IsKZZType": "0",
        "UserID": "4315515",
        "PlateID": "803023",  # 新的板块ID
        "TSZB_Type": "0",
        "filterType": "0"
    }
    
    try:
        response = requests.post(
            url,
            data=data,
            headers=headers,
            verify=False,
            proxies={'http': None, 'https': None},
            timeout=30
        )
        result = response.json()
        
        stocks = result.get("list", [])
        
        if not stocks:
            print("没有获取到数据")
            return None
        
        print(f"\n返回结果:")
        print(f"errcode: {result.get('errcode')}")
        print(f"Count: {result.get('Count')}")
        print(f"股票数量: {len(stocks)}")
        
        # 分析第一只股票
        first_stock = stocks[0]
        print(f"\n第一只股票:")
        print(f"数组长度: {len(first_stock)}")
        print(f"股票代码: {first_stock[0]}")
        print(f"股票名称: {first_stock[1]}")
        
        # 重点查看竞价相关字段（索引34-36）
        print(f"\n竞价相关字段:")
        print(f"  [34] 竞价量比: {first_stock[34] if len(first_stock) > 34 else 'N/A'}")
        print(f"  [35] 竞价金额: {first_stock[35] if len(first_stock) > 35 else 'N/A'}")
        print(f"  [36] 竞价涨幅: {first_stock[36] if len(first_stock) > 36 else 'N/A'}")
        
        return first_stock
        
    except Exception as e:
        print(f"请求失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_interface_with_plate_801235():
    """测试PlateID=801235的接口（之前的化工板块）"""
    print("\n" + "=" * 120)
    print("测试：PlateID=801235 接口（化工板块）")
    print("=" * 120)
    
    url = "https://apphis.longhuvip.com/w1/api/index.php"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; 23116PN5BC Build/PQ3A.190605.01141736)",
        "Host": "apphis.longhuvip.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    
    data = {
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
        "Date": "2026-02-10",
        "apiv": "w42",
        "Type": "6",
        "IsKZZType": "0",
        "UserID": "4315515",
        "PlateID": "801235",  # 化工板块
        "TSZB_Type": "0",
        "filterType": "0"
    }
    
    try:
        response = requests.post(
            url,
            data=data,
            headers=headers,
            verify=False,
            proxies={'http': None, 'https': None},
            timeout=30
        )
        result = response.json()
        
        stocks = result.get("list", [])
        
        if not stocks:
            print("没有获取到数据")
            return None
        
        print(f"\n返回结果:")
        print(f"errcode: {result.get('errcode')}")
        print(f"Count: {result.get('Count')}")
        print(f"股票数量: {len(stocks)}")
        
        # 分析第一只股票
        first_stock = stocks[0]
        print(f"\n第一只股票:")
        print(f"数组长度: {len(first_stock)}")
        print(f"股票代码: {first_stock[0]}")
        print(f"股票名称: {first_stock[1]}")
        
        # 重点查看竞价相关字段（索引34-36）
        print(f"\n竞价相关字段:")
        print(f"  [34] 竞价量比: {first_stock[34] if len(first_stock) > 34 else 'N/A'}")
        print(f"  [35] 竞价金额: {first_stock[35] if len(first_stock) > 35 else 'N/A'}")
        print(f"  [36] 竞价涨幅: {first_stock[36] if len(first_stock) > 36 else 'N/A'}")
        
        return first_stock
        
    except Exception as e:
        print(f"请求失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def compare_fields(stock1, stock2):
    """对比两个接口返回的字段"""
    print("\n" + "=" * 120)
    print("字段对比分析")
    print("=" * 120)
    
    if not stock1 or not stock2:
        print("无法对比，数据不完整")
        return
    
    print(f"\nPlateID=803023 字段数: {len(stock1)}")
    print(f"PlateID=801235 字段数: {len(stock2)}")
    
    # 对比竞价相关字段
    print(f"\n竞价字段对比:")
    print(f"{'字段':<20} {'803023':<30} {'801235':<30}")
    print("-" * 120)
    
    fields_to_compare = [
        (34, "竞价量比"),
        (35, "竞价金额"),
        (36, "竞价涨幅"),
    ]
    
    for idx, name in fields_to_compare:
        val1 = stock1[idx] if len(stock1) > idx else "N/A"
        val2 = stock2[idx] if len(stock2) > idx else "N/A"
        print(f"{name:<20} {str(val1):<30} {str(val2):<30}")
    
    # 对比其他关键字段
    print(f"\n其他关键字段对比:")
    print(f"{'字段':<20} {'803023':<30} {'801235':<30}")
    print("-" * 120)
    
    other_fields = [
        (0, "股票代码"),
        (1, "股票名称"),
        (5, "价格"),
        (6, "涨幅"),
        (7, "成交额"),
        (23, "连板天数"),
        (24, "板块地位"),
    ]
    
    for idx, name in other_fields:
        val1 = stock1[idx] if len(stock1) > idx else "N/A"
        val2 = stock2[idx] if len(stock2) > idx else "N/A"
        print(f"{name:<20} {str(val1):<30} {str(val2):<30}")
    
    # 详细对比所有字段
    print(f"\n详细字段对比（前40个字段）:")
    print(f"{'索引':<5} {'字段名':<25} {'803023':<30} {'801235':<30} {'是否相同':<10}")
    print("-" * 120)
    
    field_names = [
        "股票代码", "股票名称", "未知2", "未知3", "所属板块",
        "价格", "涨幅", "成交额", "实际换手", "未知9",
        "实际流通市值", "主力买", "主力卖", "主力净额", "买成占比",
        "卖成占比", "净成占比", "买流占比", "卖流占比", "净流占比",
        "区间涨幅", "量比", "未知22", "连板天数", "板块地位",
        "换手率", "未知26", "未知27", "收盘封单", "最大封单",
        "未知30", "未知31", "未知32", "振幅", "竞价量比",
        "竞价金额", "竞价涨幅", "总市值", "流通市值", "未知39"
    ]
    
    max_len = min(len(stock1), len(stock2), 40)
    
    for i in range(max_len):
        field_name = field_names[i] if i < len(field_names) else f"未知{i}"
        val1 = str(stock1[i])[:27] + "..." if len(str(stock1[i])) > 30 else str(stock1[i])
        val2 = str(stock2[i])[:27] + "..." if len(str(stock2[i])) > 30 else str(stock2[i])
        same = "✓" if stock1[i] == stock2[i] else "✗"
        
        print(f"{i:<5} {field_name:<25} {val1:<30} {val2:<30} {same:<10}")

if __name__ == "__main__":
    # 测试两个接口
    stock_803023 = test_interface_with_plate_803023()
    stock_801235 = test_interface_with_plate_801235()
    
    # 对比字段
    compare_fields(stock_803023, stock_801235)
    
    # 结论
    print("\n" + "=" * 120)
    print("结论")
    print("=" * 120)
    print("""
1. 接口参数完全相同，只是 PlateID 不同
2. 返回的数据结构相同
3. 关键差异在于索引34-36的竞价相关字段：
   - [34] 竞价量比
   - [35] 竞价金额
   - [36] 竞价涨幅
4. 这些竞价字段在不同板块可能有不同的值
5. 建议更新字段映射文档，补充竞价相关字段说明
""")
