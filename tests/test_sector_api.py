# -*- coding: utf-8 -*-
"""
测试板块API
"""

import requests
import urllib3
import json
import uuid

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://apphis.longhuvip.com/w1/api/index.php"

params = {
    "apiv": "w42",
    "PhoneOSNew": "1",
    "VerSion": "5.21.0.2"
}

data = {
    "Order": "1",
    "a": "RealRankingInfo",
    "st": "30",
    "c": "ZhiShuRanking",
    "PhoneOSNew": "1",
    "DeviceID": str(uuid.uuid4()),
    "VerSion": "5.21.0.2",
    "Index": "0",
    "Date": "2026-01-16",
    "apiv": "w42",
    "Type": "1",
    "ZSType": "7"
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SHARK PRS-A0 Build/PQ3A.190605.01141736)",
    "Host": "apphis.longhuvip.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
}

response = requests.post(
    url, 
    params=params,
    data=data,
    headers=headers,
    verify=False,
    proxies={'http': None, 'https': None},
    timeout=30
)

result = response.json()

print("=" * 60)
print("板块数据API响应")
print("=" * 60)

# 打印第一个板块的详细数据
if result.get("list"):
    first_sector = result["list"][0]
    print(f"\n第一个板块: {first_sector[1]}")
    print(f"板块代码: {first_sector[0]}")
    print(f"\n数据数组长度: {len(first_sector)}")
    print("\n数组内容:")
    for i, value in enumerate(first_sector):
        print(f"  [{i}] = {value}")

# 打印第二个板块对比
if len(result.get("list", [])) > 1:
    second_sector = result["list"][1]
    print(f"\n\n第二个板块: {second_sector[1]}")
    print(f"板块代码: {second_sector[0]}")
    print("\n数组内容:")
    for i, value in enumerate(second_sector):
        print(f"  [{i}] = {value}")

print("\n\n其他字段:")
print(f"Count: {result.get('Count')}")
print(f"Day: {result.get('Day')}")
print(f"Title: {result.get('Title')}")
