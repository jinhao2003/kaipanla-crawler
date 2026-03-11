#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试全市场连板梯队API
"""

import requests
import json
import uuid

# API配置
base_url = "https://apphis.longhuvip.com/w1/api/index.php"
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SHARK PRS-A0 Build/PQ3A.190605.01141736)",
    "Host": "apphis.longhuvip.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
}

# 请求参数
data = {
    "a": "GetYTFP_SCTD",
    "c": "FuPanLa",
    "PhoneOSNew": "1",
    "DeviceID": str(uuid.uuid4()),
    "VerSion": "5.21.0.2",
    "Date": "2026-01-16",
    "apiv": "w42"
}

print("=" * 80)
print("调试全市场连板梯队API")
print("=" * 80)
print(f"\nAPI地址: {base_url}")
print(f"请求参数: {data}")
print("\n发送请求...")

try:
    response = requests.post(
        base_url,
        data=data,
        headers=headers,
        verify=False,
        proxies={'http': None, 'https': None},
        timeout=60
    )
    
    print(f"响应状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    
    result = response.json()
    
    print("\n" + "=" * 80)
    print("API响应内容:")
    print("=" * 80)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 分析响应结构
    print("\n" + "=" * 80)
    print("响应结构分析:")
    print("=" * 80)
    
    print(f"errcode: {result.get('errcode')}")
    print(f"errmsg: {result.get('errmsg')}")
    print(f"Date: {result.get('Date')}")
    
    if 'TD' in result:
        td_list = result['TD']
        print(f"\nTD字段类型: {type(td_list)}")
        print(f"TD字段长度: {len(td_list)}")
        
        if td_list:
            print(f"\n第一个TD组:")
            print(json.dumps(td_list[0], indent=2, ensure_ascii=False))
    else:
        print("\n⚠️ 响应中没有TD字段")
    
    # 列出所有顶层字段
    print(f"\n所有顶层字段: {list(result.keys())}")
    
except Exception as e:
    print(f"\n❌ 请求失败: {e}")
    import traceback
    traceback.print_exc()
