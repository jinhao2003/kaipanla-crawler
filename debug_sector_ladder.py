#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试板块连板梯队API

查看API返回的原始数据结构
"""

import sys
sys.path.append('.')

import requests
import uuid
import json
from datetime import datetime

def debug_historical_api():
    """调试历史数据API"""
    print("=" * 80)
    print("调试历史板块连板梯队API")
    print("=" * 80)
    
    url = "https://apphis.longhuvip.com/w1/api/index.php"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SHARK PRS-A0 Build/PQ3A.190605.01141736)",
        "Host": "apphis.longhuvip.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    
    # 测试多个日期
    test_dates = ["2026-01-19", "2026-01-17", "2026-01-16", "2026-01-15"]
    
    for test_date in test_dates:
        print(f"\n测试日期: {test_date}")
        print("-" * 80)
        
        data = {
            "a": "GetYTFP_BKHX",
            "c": "FuPanLa",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "Date": test_date,
            "apiv": "w42"
        }
        
        try:
            response = requests.post(
                url,
                data=data,
                headers=headers,
                verify=False,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"状态码: {response.status_code}")
            print(f"errcode: {result.get('errcode', 'N/A')}")
            
            if result.get("list"):
                print(f"板块数量: {len(result['list'])}")
                print("\n原始数据结构（前2个板块）:")
                print(json.dumps(result['list'][:2], ensure_ascii=False, indent=2))
            else:
                print("无list字段或为空")
                print("\n完整响应:")
                print(json.dumps(result, ensure_ascii=False, indent=2))
            
            # 如果找到数据就停止
            if result.get("list") and len(result['list']) > 0:
                print(f"\n✅ 在 {test_date} 找到数据！")
                break
                
        except Exception as e:
            print(f"请求失败: {e}")


def debug_realtime_api():
    """调试实时数据API"""
    print("\n\n" + "=" * 80)
    print("调试实时板块连板梯队API")
    print("=" * 80)
    
    url = "https://apphwhq.longhuvip.com/w1/api/index.php"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SHARK PRS-A0 Build/PQ3A.190605.01141736)",
        "Host": "apphwhq.longhuvip.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    
    data = {
        "a": "GetYTFP_BKHX",
        "c": "FuPanLa",
        "PhoneOSNew": "1",
        "DeviceID": str(uuid.uuid4()),
        "VerSion": "5.21.0.2",
        "apiv": "w42"
    }
    
    try:
        response = requests.post(
            url,
            data=data,
            headers=headers,
            verify=False,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        
        print(f"状态码: {response.status_code}")
        print(f"errcode: {result.get('errcode', 'N/A')}")
        
        if result.get("list"):
            print(f"板块数量: {len(result['list'])}")
            print("\n原始数据结构（前2个板块）:")
            print(json.dumps(result['list'][:2], ensure_ascii=False, indent=2))
        else:
            print("无list字段或为空（可能是非交易时间）")
            print("\n完整响应:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
    except Exception as e:
        print(f"请求失败: {e}")


if __name__ == "__main__":
    # 调试历史API
    debug_historical_api()
    
    # 调试实时API
    debug_realtime_api()
