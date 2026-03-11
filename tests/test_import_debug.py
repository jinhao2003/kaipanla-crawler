# -*- coding: utf-8 -*-
"""
调试导入问题
"""

import requests
import urllib3
import uuid

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("步骤1: 导入配置")
try:
    from kaipanla_config import (
        BASE_URL, DEFAULT_HEADERS, API_ENDPOINTS,
        AUTH_TOKEN, USERNAME, PASSWORD, REQUEST_PARAMS_TEMPLATE
    )
    print(f"✅ 配置导入成功")
    print(f"BASE_URL: {BASE_URL}")
    print(f"Headers keys: {list(DEFAULT_HEADERS.keys())}")
except Exception as e:
    print(f"❌ 配置导入失败: {e}")
    import traceback
    traceback.print_exc()

print("\n步骤2: 使用配置发送请求")
try:
    endpoint = API_ENDPOINTS.get("market_sentiment")
    config = REQUEST_PARAMS_TEMPLATE.get("market_sentiment", {})
    url_params = config.get("url_params", {}).copy()
    post_data = config.get("post_data", {}).copy()
    post_data["DeviceID"] = str(uuid.uuid4())
    
    url = f"{BASE_URL}{endpoint}"
    
    print(f"URL: {url}")
    print(f"URL参数: {url_params}")
    print(f"POST数据: {post_data}")
    print(f"Headers: {DEFAULT_HEADERS}")
    
    response = requests.post(
        url, 
        params=url_params,
        data=post_data,
        headers=DEFAULT_HEADERS,
        verify=False,
        proxies={'http': None, 'https': None},
        timeout=30
    )
    
    print(f"\n✅ 请求成功! 状态码: {response.status_code}")
    print(f"响应键: {list(response.json().keys())}")
    
except Exception as e:
    print(f"\n❌ 请求失败: {e}")
    import traceback
    traceback.print_exc()
