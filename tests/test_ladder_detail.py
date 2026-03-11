# -*- coding: utf-8 -*-
"""
测试连板梯队详细数据
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
    "a": "ZhangTingExpression",
    "c": "HisHomeDingPan",
    "PhoneOSNew": "1",
    "DeviceID": str(uuid.uuid4()),
    "VerSion": "5.21.0.2",
    "apiv": "w42",
    "Day": "2026-01-16"
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
print("完整响应数据:")
print(json.dumps(result, indent=2, ensure_ascii=False))

print("\n\ninfo数组内容:")
info = result.get("info", [])
for i, value in enumerate(info):
    print(f"info[{i}] = {value}")
