#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试API响应数据结构

测试 DailyLimitPerformance API 返回的数据格式
"""

import requests
import json
import uuid


def test_daily_limit_performance_api():
    """测试 DailyLimitPerformance API"""
    print("=" * 60)
    print("测试 DailyLimitPerformance API (PidType=2, 二板)")
    print("=" * 60)
    
    url = "https://apphwhq.longhuvip.com/w1/api/index.php"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SHARK PRS-A0 Build/PQ3A.190605.01141736)",
        "Host": "apphwhq.longhuvip.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    
    data = {
        "Order": "0",
        "a": "DailyLimitPerformance",
        "st": "2000",
        "c": "HomeDingPan",
        "PhoneOSNew": "1",
        "DeviceID": str(uuid.uuid4()),
        "VerSion": "5.21.0.2",
        "Index": "0",
        "PidType": "2",  # 2表示二板
        "apiv": "w42",
        "Type": "4"
    }
    
    print("\n发送请求...")
    print(f"URL: {url}")
    print(f"参数: {data}")
    
    try:
        response = requests.post(
            url,
            data=data,
            headers=headers,
            verify=False,
            proxies={'http': None, 'https': None},
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        
        print("\n✓ 请求成功\n")
        
        # 显示响应的基本信息
        print("=" * 60)
        print("响应数据结构")
        print("=" * 60)
        
        print(f"\nerrcode: {result.get('errcode', 'N/A')}")
        
        # 显示所有顶层键
        print(f"\n顶层键: {list(result.keys())}")
        
        # 如果有list字段，显示其结构
        if 'list' in result:
            stock_list = result['list']
            print(f"\nlist字段: 包含 {len(stock_list)} 条数据")
            
            if stock_list:
                print("\n第一条数据的键:")
                first_item = stock_list[0]
                if isinstance(first_item, dict):
                    for key, value in first_item.items():
                        print(f"  {key}: {type(value).__name__} = {value}")
                elif isinstance(first_item, list):
                    print(f"  数组格式，长度: {len(first_item)}")
                    print(f"  内容: {first_item}")
                
                # 显示前3条数据
                print(f"\n前3条数据:")
                for i, item in enumerate(stock_list[:3], 1):
                    print(f"\n  [{i}] {item}")
        
        # 显示完整的JSON（格式化）
        print("\n" + "=" * 60)
        print("完整JSON响应（格式化）")
        print("=" * 60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        return result
        
    except Exception as e:
        print(f"\n✗ 请求失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_all_board_types():
    """测试所有连板类型的API"""
    print("\n" + "=" * 60)
    print("测试所有连板类型的API")
    print("=" * 60)
    
    url = "https://apphwhq.longhuvip.com/w1/api/index.php"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SHARK PRS-A0 Build/PQ3A.190605.01141736)",
        "Host": "apphwhq.longhuvip.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    
    board_types = {
        1: "首板",
        2: "二板",
        3: "三板",
        4: "四板",
        5: "五板及以上"
    }
    
    results = {}
    
    for board_type, board_name in board_types.items():
        print(f"\n测试 {board_name} (PidType={board_type})...")
        
        data = {
            "Order": "0",
            "a": "DailyLimitPerformance",
            "st": "2000",
            "c": "HomeDingPan",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "Index": "0",
            "PidType": str(board_type),
            "apiv": "w42",
            "Type": "4"
        }
        
        try:
            response = requests.post(
                url,
                data=data,
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            
            errcode = result.get('errcode', 'N/A')
            stock_count = len(result.get('list', []))
            
            print(f"  errcode: {errcode}")
            print(f"  股票数量: {stock_count}")
            
            if stock_count > 0:
                print(f"  前3只股票:")
                for i, stock in enumerate(result['list'][:3], 1):
                    if isinstance(stock, dict):
                        stock_name = stock.get('StockName', 'N/A')
                        stock_code = stock.get('StockID', 'N/A')
                        print(f"    {i}. {stock_name} ({stock_code})")
                    elif isinstance(stock, list) and len(stock) > 1:
                        print(f"    {i}. {stock[1]} ({stock[0]})")
            
            results[board_type] = result
            
        except Exception as e:
            print(f"  ✗ 请求失败: {e}")
            results[board_type] = None
    
    return results


def analyze_data_structure(result):
    """分析数据结构"""
    print("\n" + "=" * 60)
    print("数据结构分析")
    print("=" * 60)
    
    if not result:
        print("无数据")
        return
    
    stock_list = result.get('list', [])
    
    if not stock_list:
        print("股票列表为空")
        return
    
    first_stock = stock_list[0]
    
    print(f"\n数据类型: {type(first_stock).__name__}")
    
    if isinstance(first_stock, dict):
        print("\n字典格式，字段列表:")
        for key in first_stock.keys():
            print(f"  - {key}")
    
    elif isinstance(first_stock, list):
        print(f"\n数组格式，长度: {len(first_stock)}")
        print("\n索引对应的可能含义:")
        if len(first_stock) > 0:
            print(f"  [0]: {first_stock[0]} (可能是股票代码)")
        if len(first_stock) > 1:
            print(f"  [1]: {first_stock[1]} (可能是股票名称)")
        if len(first_stock) > 2:
            print(f"  [2]: {first_stock[2]}")
        if len(first_stock) > 3:
            print(f"  [3]: {first_stock[3]}")
        if len(first_stock) > 4:
            print(f"  [4]: {first_stock[4]}")
        
        print(f"\n完整数据: {first_stock}")


if __name__ == "__main__":
    print("开始测试 DailyLimitPerformance API\n")
    
    # 测试1: 详细测试二板API
    result = test_daily_limit_performance_api()
    
    if result:
        analyze_data_structure(result)
    
    # 测试2: 测试所有连板类型
    all_results = test_all_board_types()
    
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    print("\n各连板类型的数据量:")
    for board_type, result in all_results.items():
        board_names = {1: "首板", 2: "二板", 3: "三板", 4: "四板", 5: "五板及以上"}
        if result:
            count = len(result.get('list', []))
            print(f"  {board_names[board_type]}: {count}只")
        else:
            print(f"  {board_names[board_type]}: 获取失败")
