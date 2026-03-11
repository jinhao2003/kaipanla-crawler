#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
找到真正的结束位置
"""

import sys
sys.path.insert(0, '.')

from kaipanla_crawler import KaipanlaCrawler
import requests
import uuid

def test_find_real_end():
    """找到真正的数据结束位置"""
    crawler = KaipanlaCrawler()
    
    plate_id = "801235"  # 化工板块
    date = "2026-02-10"
    
    print("=" * 100)
    print("测试：找到真正的数据结束位置")
    print("=" * 100)
    
    # 测试不同的Index值
    test_indices = [0, 30, 690, 720, 750, 1380, 1410, 1440]
    
    for idx in test_indices:
        print(f"\n测试 Index={idx}")
        print("-" * 100)
        
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
            "Index": str(idx),
            "Date": date,
            "apiv": "w42",
            "Type": "6",
            "IsKZZType": "0",
            "UserID": "4315515",
            "PlateID": plate_id,
            "TSZB_Type": "0",
            "filterType": "0"
        }
        
        try:
            response = requests.post(
                crawler.base_url,
                data=data_params,
                headers=crawler.headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=30
            )
            result = response.json()
            
            count = result.get("Count", 0)
            stocks = result.get("list", [])
            
            print(f"Count: {count}, 返回股票数: {len(stocks)}")
            
            if stocks:
                first = stocks[0]
                code = first[0] if len(first) > 0 else "N/A"
                name = first[1] if len(first) > 1 else "N/A"
                print(f"第一只: {code} {name}")
            else:
                print("✓ 没有数据，这是结束位置")
                break
                
        except Exception as e:
            print(f"请求失败: {e}")
            break
    
    print("\n" + "=" * 100)
    print("结论")
    print("=" * 100)
    print("""
看起来 Count 字段不能直接用来计算总页数。

正确的方法是：
1. 循环请求，每次 Index += 30
2. 当返回的 list 为空时，停止
3. 或者当返回的股票数 < 30 时，说明是最后一页
""")

if __name__ == "__main__":
    test_find_real_end()
