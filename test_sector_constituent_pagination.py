#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试板块成分股接口 - 分页测试
"""

import sys
sys.path.insert(0, '.')

from kaipanla_crawler import KaipanlaCrawler
import requests
import uuid

def test_pagination():
    """测试分页获取所有成分股"""
    crawler = KaipanlaCrawler()
    
    plate_id = "801235"  # 化工板块
    date = "2026-02-10"
    
    print("=" * 100)
    print("测试：分页获取板块所有成分股")
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
                print(f"  请求失败: {result.get('errcode')}")
                break
            
            stocks = result.get("list", [])
            count = result.get("Count", 0)
            stock_codes = result.get("Stocks", [])
            
            print(f"  返回: {len(stocks)} 只股票, Count={count}, Stocks字段={len(stock_codes)}个代码")
            
            if not stocks:
                print(f"  没有更多数据，停止")
                break
            
            # 添加到总列表
            for stock in stocks:
                if len(stock) > 0:
                    code = stock[0]
                    if code not in all_codes_set:
                        all_stocks.append(stock)
                        all_codes_set.add(code)
            
            # 显示前3只
            if stocks:
                print(f"  前3只:")
                for i, stock in enumerate(stocks[:3], 1):
                    code = stock[0] if len(stock) > 0 else "N/A"
                    name = stock[1] if len(stock) > 1 else "N/A"
                    price = stock[5] if len(stock) > 5 else "N/A"
                    change = stock[6] if len(stock) > 6 else "N/A"
                    print(f"    {i}. {code} {name}: {price} ({change}%)")
            
            # 如果返回少于30只，说明是最后一页
            if len(stocks) < 30:
                print(f"  返回数量少于30，这是最后一页")
                break
            
            page += 1
            
            # 安全限制：最多请求10页
            if page >= 10:
                print(f"  已请求10页，停止")
                break
                
        except Exception as e:
            print(f"  请求异常: {e}")
            break
    
    print("\n" + "=" * 100)
    print("汇总结果")
    print("=" * 100)
    print(f"总共获取: {len(all_stocks)} 只不重复的股票")
    print(f"股票代码: {sorted(all_codes_set)[:20]}...")
    
    # 按涨跌幅排序显示前10
    print(f"\n涨幅前10:")
    sorted_stocks = sorted(all_stocks, key=lambda x: x[6] if len(x) > 6 else 0, reverse=True)
    for i, stock in enumerate(sorted_stocks[:10], 1):
        code = stock[0] if len(stock) > 0 else "N/A"
        name = stock[1] if len(stock) > 1 else "N/A"
        price = stock[5] if len(stock) > 5 else "N/A"
        change = stock[6] if len(stock) > 6 else "N/A"
        print(f"  {i}. {code} {name}: {price} ({change:+.2f}%)")

if __name__ == "__main__":
    test_pagination()
