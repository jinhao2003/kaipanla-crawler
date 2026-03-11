# -*- coding: utf-8 -*-
"""
测试数据对齐问题
"""

import requests
import uuid
import json

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

result = response.json()

print(f"\n返回状态: {result.get('errcode')}")
print(f"日期: {result.get('date')}")

# 查看第一个板块的第一只股票
if result.get('list'):
    first_sector = result['list'][0]
    print(f"\n第一个板块: {first_sector.get('ZSName')}")
    
    if first_sector.get('StockList'):
        first_stock = first_sector['StockList'][0]
        print(f"\n第一只股票数据（共{len(first_stock)}个字段）:")
        for i, value in enumerate(first_stock):
            print(f"  索引{i}: {value} (类型: {type(value).__name__})")
        
        # 保存完整数据到文件
        with open('raw_sector_data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("\n完整数据已保存到: raw_sector_data.json")
