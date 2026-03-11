#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 GetTrendIncremental 接口 - 获取昨日涨停表现、连板表现、破板表现
"""

import requests
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_trend_incremental():
    """测试获取昨日涨停表现数据"""
    
    url = "https://apphwhq.longhuvip.com/w1/api/index.php"
    
    # 测试不同的StockID
    stock_ids = [
        ("801900", "昨日涨停"),
        ("801901", "昨日连板"),
        ("801902", "昨日破板"),
    ]
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SHARK PRS-A0 Build/PQ3A.190605.01141736)",
        "Host": "apphwhq.longhuvip.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    
    print("=" * 60)
    print("测试 GetTrendIncremental 接口")
    print("=" * 60)
    
    for stock_id, name in stock_ids:
        print(f"\n【{name} - StockID: {stock_id}】")
        
        data = {
            "a": "GetTrendIncremental",
            "c": "ZhiShuL2Data",
            "PhoneOSNew": "1",
            "DeviceID": "e78ba169-6c03-3faf-8e5e-a72f8411a8eb",
            "VerSion": "5.21.0.2",
            "apiv": "w42",
            "StockID": stock_id,
            "Day": ""
        }
        
        try:
            response = requests.post(url, data=data, headers=headers, timeout=30, verify=False)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('errcode') == '0':
                print(f"✓ API调用成功")
                
                # 解析数据结构
                print("\n数据结构:")
                for key, value in result.items():
                    if key == 'list' and isinstance(value, list):
                        print(f"  {key}: list[{len(value)}]")
                        if value:
                            print(f"    示例元素: {value[0]}")
                    else:
                        print(f"  {key}: {type(value).__name__} = {value}")
                
            else:
                print(f"✗ API返回错误: {result.get('errcode')}")
                
        except Exception as e:
            print(f"✗ 请求失败: {e}")

if __name__ == "__main__":
    test_trend_incremental()
