#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试板块成分股接口 - 对比不同index参数
"""

import sys
sys.path.insert(0, '.')

from kaipanla_crawler import KaipanlaCrawler
import requests
import uuid

def test_with_different_index():
    """测试不同index参数的返回结果"""
    crawler = KaipanlaCrawler()
    
    plate_id = "801235"  # 化工板块
    date = "2026-02-10"
    
    print("=" * 100)
    print("测试：对比不同 Index 参数的返回结果")
    print("=" * 100)
    
    # 测试 Index=0
    print("\n" + "=" * 100)
    print("测试 1: Index=0 (第一页)")
    print("=" * 100)
    
    data_params_0 = {
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
        "Index": "0",  # 第一页
        "Date": date,
        "apiv": "w42",
        "Type": "6",
        "IsKZZType": "0",
        "UserID": "4315515",
        "PlateID": plate_id,
        "TSZB_Type": "0",
        "filterType": "0"
    }
    
    response_0 = requests.post(
        crawler.base_url,
        data=data_params_0,
        headers=crawler.headers,
        verify=False,
        proxies={'http': None, 'https': None},
        timeout=30
    )
    result_0 = response_0.json()
    
    stocks_0 = result_0.get("list", [])
    stock_codes_0 = result_0.get("Stocks", [])
    count_0 = result_0.get("Count", 0)
    
    print(f"\nIndex=0 返回结果:")
    print(f"  Count字段: {count_0}")
    print(f"  list长度: {len(stocks_0)}")
    print(f"  Stocks长度: {len(stock_codes_0)}")
    print(f"  股票代码列表: {stock_codes_0}")
    
    if stocks_0:
        print(f"\n  前5只股票:")
        for i, stock in enumerate(stocks_0[:5], 1):
            code = stock[0] if len(stock) > 0 else "N/A"
            name = stock[1] if len(stock) > 1 else "N/A"
            price = stock[5] if len(stock) > 5 else "N/A"
            change = stock[6] if len(stock) > 6 else "N/A"
            print(f"    {i}. {code} {name}: {price} ({change}%)")
    
    # 测试 Index=30
    print("\n" + "=" * 100)
    print("测试 2: Index=30 (第二页)")
    print("=" * 100)
    
    data_params_30 = data_params_0.copy()
    data_params_30["Index"] = "30"  # 第二页
    data_params_30["DeviceID"] = str(uuid.uuid4())
    
    response_30 = requests.post(
        crawler.base_url,
        data=data_params_30,
        headers=crawler.headers,
        verify=False,
        proxies={'http': None, 'https': None},
        timeout=30
    )
    result_30 = response_30.json()
    
    stocks_30 = result_30.get("list", [])
    stock_codes_30 = result_30.get("Stocks", [])
    count_30 = result_30.get("Count", 0)
    
    print(f"\nIndex=30 返回结果:")
    print(f"  Count字段: {count_30}")
    print(f"  list长度: {len(stocks_30)}")
    print(f"  Stocks长度: {len(stock_codes_30)}")
    print(f"  股票代码列表: {stock_codes_30}")
    
    if stocks_30:
        print(f"\n  前5只股票:")
        for i, stock in enumerate(stocks_30[:5], 1):
            code = stock[0] if len(stock) > 0 else "N/A"
            name = stock[1] if len(stock) > 1 else "N/A"
            price = stock[5] if len(stock) > 5 else "N/A"
            change = stock[6] if len(stock) > 6 else "N/A"
            print(f"    {i}. {code} {name}: {price} ({change}%)")
    
    # 对比分析
    print("\n" + "=" * 100)
    print("对比分析")
    print("=" * 100)
    
    print(f"\n1. Count字段对比:")
    print(f"   Index=0:  {count_0}")
    print(f"   Index=30: {count_30}")
    print(f"   是否相同: {count_0 == count_30}")
    
    print(f"\n2. 返回数据量对比:")
    print(f"   Index=0:  {len(stocks_0)} 只股票")
    print(f"   Index=30: {len(stocks_30)} 只股票")
    
    print(f"\n3. 股票代码对比:")
    if stock_codes_0 and stock_codes_30:
        # 检查是否有重复
        set_0 = set(stock_codes_0)
        set_30 = set(stock_codes_30)
        overlap = set_0 & set_30
        
        print(f"   Index=0 独有: {len(set_0 - set_30)} 只")
        print(f"   Index=30 独有: {len(set_30 - set_0)} 只")
        print(f"   重复: {len(overlap)} 只")
        
        if overlap:
            print(f"   重复的股票: {list(overlap)[:5]}...")
    
    print(f"\n4. 结论:")
    if count_0 == count_30 and count_0 > 30:
        print(f"   ✓ Count字段表示总数量: {count_0} 只")
        print(f"   ✓ Index参数用于分页，每页30只")
        print(f"   ✓ Index=0 返回第1-30只")
        print(f"   ✓ Index=30 返回第31-60只")
        print(f"   ✓ 需要循环请求获取所有成分股")
    elif len(stocks_0) < 30:
        print(f"   ✓ 该板块成分股少于30只，无需分页")
    else:
        print(f"   ? 需要进一步分析")
    
    # 测试 Index=60
    if count_0 > 60:
        print("\n" + "=" * 100)
        print("测试 3: Index=60 (第三页)")
        print("=" * 100)
        
        data_params_60 = data_params_0.copy()
        data_params_60["Index"] = "60"
        data_params_60["DeviceID"] = str(uuid.uuid4())
        
        response_60 = requests.post(
            crawler.base_url,
            data=data_params_60,
            headers=crawler.headers,
            verify=False,
            proxies={'http': None, 'https': None},
            timeout=30
        )
        result_60 = response_60.json()
        
        stocks_60 = result_60.get("list", [])
        print(f"\nIndex=60 返回结果:")
        print(f"  list长度: {len(stocks_60)}")
        
        if stocks_60:
            print(f"  前3只股票:")
            for i, stock in enumerate(stocks_60[:3], 1):
                code = stock[0] if len(stock) > 0 else "N/A"
                name = stock[1] if len(stock) > 1 else "N/A"
                print(f"    {i}. {code} {name}")

if __name__ == "__main__":
    test_with_different_index()
