# -*- coding: utf-8 -*-
"""
直接测试板块函数
"""

import requests
import uuid

sector_base_url = "https://apphwhq.longhuvip.com/w1/api/index.php"
sector_headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SHARK PRS-A0 Build/PQ3A.190605.01141736)",
    "Host": "apphwhq.longhuvip.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
}

date = "2026-01-16"
data = {
    "a": "GetPlateInfo_w38",
    "st": "100",
    "c": "DailyLimitResumption",
    "PhoneOSNew": "1",
    "DeviceID": str(uuid.uuid4()),
    "VerSion": "5.21.0.2",
    "Index": "0",
    "apiv": "w42"
}

print("发送请求...")
response = requests.post(
    sector_base_url,
    data=data,
    headers=sector_headers,
    verify=False,
    timeout=30
)

print(f"状态码: {response.status_code}")
result = response.json()

print(f"\nerrcode: {result.get('errcode')}")
print(f"date: {result.get('date')}")
print(f"\nnums: {result.get('nums')}")
print(f"\n板块数量: {len(result.get('list', []))}")

if result.get('list'):
    first_sector = result['list'][0]
    print(f"\n第一个板块:")
    print(f"  代码: {first_sector.get('ZSCode')}")
    print(f"  名称: {first_sector.get('ZSName')}")
    print(f"  股票数: {first_sector.get('num')}")
    print(f"  股票列表长度: {len(first_sector.get('StockList', []))}")
    
    if first_sector.get('StockList'):
        first_stock = first_sector['StockList'][0]
        print(f"\n  第一只股票数据长度: {len(first_stock)}")
        print(f"  股票代码: {first_stock[0]}")
        print(f"  股票名称: {first_stock[1]}")
