#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试如何计算总页数
"""

import sys
sys.path.insert(0, '.')

from kaipanla_crawler import KaipanlaCrawler
import requests
import uuid
import math

def test_calculate_pages():
    """测试计算总页数的方法"""
    crawler = KaipanlaCrawler()
    
    plate_id = "801235"  # 化工板块
    date = "2026-02-10"
    
    print("=" * 100)
    print("测试：如何计算总页数")
    print("=" * 100)
    
    # 第一步：请求第一页，获取核心成分股数量
    print("\n第一步：请求第一页 (Index=0)")
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
    result_page1 = response.json()
    
    count_page1 = result_page1.get("Count", 0)
    stocks_page1 = result_page1.get("list", [])
    stock_codes = result_page1.get("Stocks", [])
    
    print(f"Count字段: {count_page1}")
    print(f"返回股票数: {len(stocks_page1)}")
    print(f"Stocks字段: {len(stock_codes)} 个核心成分股代码")
    
    # 第二步：请求第二页，获取总数
    print("\n第二步：请求第二页 (Index=30)")
    print("-" * 100)
    
    data_params["Index"] = "30"
    data_params["DeviceID"] = str(uuid.uuid4())
    
    response = requests.post(
        crawler.base_url,
        data=data_params,
        headers=crawler.headers,
        verify=False,
        proxies={'http': None, 'https': None},
        timeout=30
    )
    result_page2 = response.json()
    
    count_page2 = result_page2.get("Count", 0)
    stocks_page2 = result_page2.get("list", [])
    
    print(f"Count字段: {count_page2}")
    print(f"返回股票数: {len(stocks_page2)}")
    
    # 第三步：计算总页数
    print("\n第三步：计算总页数")
    print("-" * 100)
    
    total_stocks = count_page2 if count_page2 > count_page1 else count_page1
    page_size = 30
    total_pages = math.ceil(total_stocks / page_size)
    
    print(f"总股票数: {total_stocks}")
    print(f"每页数量: {page_size}")
    print(f"计算总页数: {total_pages} 页")
    print(f"计算公式: math.ceil({total_stocks} / {page_size}) = {total_pages}")
    
    # 第四步：验证最后一页
    print("\n第四步：验证最后一页")
    print("-" * 100)
    
    # 计算最后一页的Index
    last_page_index = (total_pages - 1) * page_size
    print(f"最后一页Index: {last_page_index}")
    
    data_params["Index"] = str(last_page_index)
    data_params["DeviceID"] = str(uuid.uuid4())
    
    response = requests.post(
        crawler.base_url,
        data=data_params,
        headers=crawler.headers,
        verify=False,
        proxies={'http': None, 'https': None},
        timeout=30
    )
    result_last = response.json()
    
    stocks_last = result_last.get("list", [])
    print(f"最后一页返回股票数: {len(stocks_last)}")
    
    if stocks_last:
        print(f"最后一页前3只:")
        for i, stock in enumerate(stocks_last[:3], 1):
            code = stock[0] if len(stock) > 0 else "N/A"
            name = stock[1] if len(stock) > 1 else "N/A"
            print(f"  {i}. {code} {name}")
    
    # 第五步：验证下一页是否为空
    print("\n第五步：验证下一页是否为空")
    print("-" * 100)
    
    next_page_index = total_pages * page_size
    print(f"下一页Index: {next_page_index}")
    
    data_params["Index"] = str(next_page_index)
    data_params["DeviceID"] = str(uuid.uuid4())
    
    response = requests.post(
        crawler.base_url,
        data=data_params,
        headers=crawler.headers,
        verify=False,
        proxies={'http': None, 'https': None},
        timeout=30
    )
    result_next = response.json()
    
    stocks_next = result_next.get("list", [])
    print(f"下一页返回股票数: {len(stocks_next)}")
    
    if len(stocks_next) == 0:
        print("✓ 验证成功：下一页为空，说明总页数计算正确")
    else:
        print(f"⚠️ 下一页还有数据，实际总数可能更多")
    
    # 总结
    print("\n" + "=" * 100)
    print("总结")
    print("=" * 100)
    print(f"""
计算总页数的方法：

1. 请求第一页 (Index=0)，获取 Count 字段 = {count_page1}（核心成分股数量）
2. 请求第二页 (Index=30)，获取 Count 字段 = {count_page2}（所有相关股票总数）
3. 取较大的 Count 值作为总数 = {total_stocks}
4. 计算总页数 = math.ceil({total_stocks} / 30) = {total_pages} 页
5. 最后一页 Index = ({total_pages} - 1) × 30 = {last_page_index}

注意：
- 如果只需要核心成分股，使用第一页的 Stocks 字段即可（{len(stock_codes)} 只）
- 如果需要所有相关股票，需要分页获取（约 {total_pages} 页，{total_stocks} 只）
""")

if __name__ == "__main__":
    test_calculate_pages()
