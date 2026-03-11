#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 Index=693 的返回结果
"""

import sys
sys.path.insert(0, '.')

from kaipanla_crawler import KaipanlaCrawler
import requests
import uuid

def test_index_693():
    """测试 Index=693"""
    crawler = KaipanlaCrawler()
    
    plate_id = "801235"  # 化工板块
    date = "2026-02-10"
    
    print("=" * 100)
    print("测试：Index=693 的返回结果")
    print("=" * 100)
    
    test_indices = [0, 30, 60, 90, 693]
    
    for idx in test_indices:
        print(f"\n{'=' * 100}")
        print(f"测试 Index={idx}")
        print('=' * 100)
        
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
            
            errcode = result.get("errcode", "unknown")
            stocks = result.get("list", [])
            count = result.get("Count", 0)
            stock_codes = result.get("Stocks", [])
            
            print(f"\n返回结果:")
            print(f"  errcode: {errcode}")
            print(f"  Count字段: {count}")
            print(f"  list长度: {len(stocks)}")
            print(f"  Stocks字段长度: {len(stock_codes)}")
            
            if stock_codes:
                print(f"  Stocks前10个: {stock_codes[:10]}")
            
            if stocks:
                print(f"\n  前5只股票:")
                for i, stock in enumerate(stocks[:5], 1):
                    code = stock[0] if len(stock) > 0 else "N/A"
                    name = stock[1] if len(stock) > 1 else "N/A"
                    price = stock[5] if len(stock) > 5 else "N/A"
                    change = stock[6] if len(stock) > 6 else "N/A"
                    print(f"    {i}. {code} {name}: {price} ({change}%)")
            else:
                print(f"  ⚠️ 没有返回股票数据")
            
            # 检查其他关键字段
            other_keys = [k for k in result.keys() if k not in ['errcode', 'list', 'Count', 'Stocks']]
            if other_keys:
                print(f"\n  其他字段: {other_keys[:10]}")
                
        except Exception as e:
            print(f"  ❌ 请求异常: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_index_693()
