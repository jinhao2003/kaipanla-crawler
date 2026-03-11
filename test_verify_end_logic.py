#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证结束逻辑：当返回数量 < 30 时停止
"""

import sys
sys.path.insert(0, '.')

from kaipanla_crawler import KaipanlaCrawler
import requests
import uuid

def test_plate(plate_id, plate_name, date="2026-02-10"):
    """测试指定板块"""
    crawler = KaipanlaCrawler()
    
    print("=" * 100)
    print(f"测试板块: {plate_id} ({plate_name})")
    print("=" * 100)
    
    all_stocks = []
    all_codes_set = set()
    page = 0
    
    while True:
        index = page * 30
        print(f"\n请求第 {page + 1} 页 (Index={index})...")
        
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
            "Index": str(index),
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
            
            if result.get("errcode") != "0":
                print(f"  ❌ 请求失败: {result.get('errcode')}")
                break
            
            stocks = result.get("list", [])
            count = result.get("Count", 0)
            stock_codes = result.get("Stocks", [])
            
            print(f"  Count={count}, 返回={len(stocks)}只", end="")
            
            if page == 0 and stock_codes:
                print(f", Stocks字段={len(stock_codes)}个代码")
            else:
                print()
            
            if not stocks:
                print(f"  ✓ 没有数据，停止")
                break
            
            # 显示前3只
            if len(stocks) <= 5:
                print(f"  股票:")
                for i, stock in enumerate(stocks, 1):
                    code = stock[0] if len(stock) > 0 else "N/A"
                    name = stock[1] if len(stock) > 1 else "N/A"
                    print(f"    {i}. {code} {name}")
            else:
                print(f"  前3只:")
                for i, stock in enumerate(stocks[:3], 1):
                    code = stock[0] if len(stock) > 0 else "N/A"
                    name = stock[1] if len(stock) > 1 else "N/A"
                    print(f"    {i}. {code} {name}")
            
            # 添加到总列表（去重）
            for stock in stocks:
                if len(stock) > 0:
                    code = stock[0]
                    if code not in all_codes_set:
                        all_stocks.append(stock)
                        all_codes_set.add(code)
            
            # 如果返回少于30只，说明是最后一页
            if len(stocks) < 30:
                print(f"  ✓ 返回数量 < 30，这是最后一页，停止")
                break
            
            page += 1
            
            # 安全限制
            if page >= 50:
                print(f"  ⚠️ 已请求50页，停止")
                break
                
        except Exception as e:
            print(f"  ❌ 请求异常: {e}")
            break
    
    print(f"\n{'=' * 100}")
    print(f"汇总结果")
    print(f"{'=' * 100}")
    print(f"总共获取: {len(all_stocks)} 只不重复的股票")
    print(f"获取页数: {page + 1} 页")
    
    return len(all_stocks), page + 1

if __name__ == "__main__":
    date = "2026-02-10"
    
    # 测试多个板块
    test_plates = [
        ("801235", "化工"),
        ("801632", "801632板块"),
        ("801346", "电力设备"),
    ]
    
    results = []
    for plate_id, plate_name in test_plates:
        total, pages = test_plate(plate_id, plate_name, date)
        results.append((plate_id, plate_name, total, pages))
        print("\n" + "=" * 100)
        print()
    
    # 总结
    print("\n" + "=" * 100)
    print("所有板块测试结果汇总")
    print("=" * 100)
    for plate_id, plate_name, total, pages in results:
        print(f"{plate_id} ({plate_name}): {total} 只股票, {pages} 页")
