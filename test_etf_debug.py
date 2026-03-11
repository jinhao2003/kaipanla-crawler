#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试ETF榜单接口
"""

import sys
sys.path.insert(0, '.')

import requests
import uuid
import json

def test_etf_debug():
    """调试ETF接口"""
    print("=" * 100)
    print("调试：ETF榜单接口")
    print("=" * 100)
    
    url = "https://apphwhq.longhuvip.com/w1/api/index.php"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; 23116PN5BC Build/PQ3A.190605.01141736)",
        "Host": "apphwhq.longhuvip.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    
    data = {
        "Order": "1",
        "a": "ETFStockRanking",
        "st": "30",
        "c": "NewStockRanking",
        "Filtration": "0",
        "PhoneOSNew": "1",
        "DeviceID": str(uuid.uuid4()),
        "VerSion": "5.21.0.2",
        "Token": "0daffcf404348e2fb714795ba5bdff02",
        "Index": "0",
        "PidType": "0",
        "apiv": "w42",
        "Type": "1",
        "UserID": "4315515"
    }
    
    try:
        response = requests.post(
            url,
            data=data,
            headers=headers,
            verify=False,
            proxies={'http': None, 'https': None},
            timeout=30
        )
        result = response.json()
        
        print(f"\n完整返回结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"请求失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_etf_debug()
