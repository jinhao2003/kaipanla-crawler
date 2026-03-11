#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 MoodNumCount 接口 - 获取实时涨停家数、跌停家数及大盘数据
"""

import requests
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_mood_num_count():
    """测试获取实时涨跌停家数和大盘数据"""
    
    url = "https://apphwhq.longhuvip.com/w1/api/index.php"
    
    data = {
        "a": "MoodNumCount",
        "c": "MarketMood",
        "PhoneOSNew": "1",
        "DeviceID": "e78ba169-6c03-3faf-8e5e-a72f8411a8eb",
        "VerSion": "5.21.0.2",
        "apiv": "w42"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SHARK PRS-A0 Build/PQ3A.190605.01141736)",
        "Host": "apphwhq.longhuvip.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    
    print("=" * 60)
    print("测试 MoodNumCount 接口")
    print("=" * 60)
    
    try:
        response = requests.post(url, data=data, headers=headers, timeout=30, verify=False)
        response.raise_for_status()
        
        result = response.json()
        
        print("\n原始响应:")
        print(result)
        
        if result.get('errcode') == '0':
            print("\n✓ API调用成功")
            
            # 解析数据结构
            print("\n数据结构分析:")
            for key, value in result.items():
                print(f"  {key}: {type(value).__name__} = {value}")
            
        else:
            print(f"\n✗ API返回错误: {result.get('errcode')}")
            
    except Exception as e:
        print(f"\n✗ 请求失败: {e}")

if __name__ == "__main__":
    test_mood_num_count()
