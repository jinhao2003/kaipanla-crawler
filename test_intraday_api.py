# -*- coding: utf-8 -*-
"""
测试分时数据API接口
"""

import requests
import uuid
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_sector_intraday_api():
    """测试板块分时API"""
    print("=" * 80)
    print("测试板块分时API")
    print("=" * 80)
    
    # 历史数据URL
    base_url = "https://apphis.longhuvip.com/w1/api/index.php"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SHARK PRS-A0 Build/PQ3A.190605.01141736)",
        "Host": "apphis.longhuvip.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    
    # 测试不同的API参数
    test_cases = [
        {
            "name": "GetTrend - ZhiShuL2Data",
            "data": {
                "a": "GetTrend",
                "c": "ZhiShuL2Data",
                "PhoneOSNew": "1",
                "DeviceID": str(uuid.uuid4()),
                "VerSion": "5.21.0.2",
                "apiv": "w42",
                "StockID": "801346",
                "Day": "2026-01-16"
            }
        },
        {
            "name": "GetTrendIncremental - ZhiShuL2Data",
            "data": {
                "a": "GetTrendIncremental",
                "c": "ZhiShuL2Data",
                "PhoneOSNew": "1",
                "DeviceID": str(uuid.uuid4()),
                "VerSion": "5.21.0.2",
                "apiv": "w42",
                "StockID": "801346",
                "Day": "2026-01-16",
                "Time": "15:00"
            }
        },
        {
            "name": "GetZsReal - StockL2History",
            "data": {
                "a": "GetZsReal",
                "c": "StockL2History",
                "PhoneOSNew": "1",
                "DeviceID": str(uuid.uuid4()),
                "VerSion": "5.21.0.2",
                "apiv": "w42",
                "Day": "2026-01-16"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n测试: {test_case['name']}")
        print("-" * 80)
        
        try:
            response = requests.post(
                base_url,
                data=test_case['data'],
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=60
            )
            
            print(f"状态码: {response.status_code}")
            print(f"响应长度: {len(response.text)} 字节")
            print(f"响应前200字符: {response.text[:200]}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"JSON解析成功")
                    print(f"errcode: {result.get('errcode', 'N/A')}")
                    print(f"返回字段: {list(result.keys())}")
                    
                    # 如果有trend字段，显示前几条
                    if 'trend' in result:
                        trend = result['trend']
                        print(f"trend数据条数: {len(trend)}")
                        if len(trend) > 0:
                            print(f"第一条数据: {trend[0]}")
                            print(f"最后一条数据: {trend[-1]}")
                    
                except Exception as e:
                    print(f"JSON解析失败: {e}")
            
        except Exception as e:
            print(f"请求失败: {e}")
        
        print()

def test_stock_intraday_api():
    """测试个股分时API"""
    print("=" * 80)
    print("测试个股分时API")
    print("=" * 80)
    
    base_url = "https://apphis.longhuvip.com/w1/api/index.php"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SHARK PRS-A0 Build/PQ3A.190605.01141736)",
        "Host": "apphis.longhuvip.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    
    test_cases = [
        {
            "name": "GetTrend - StockL2Data",
            "data": {
                "a": "GetTrend",
                "c": "StockL2Data",
                "PhoneOSNew": "1",
                "DeviceID": str(uuid.uuid4()),
                "VerSion": "5.21.0.2",
                "apiv": "w42",
                "StockID": "002498",
                "Day": "2026-01-16"
            }
        },
        {
            "name": "GetTrendIncremental - StockL2Data",
            "data": {
                "a": "GetTrendIncremental",
                "c": "StockL2Data",
                "PhoneOSNew": "1",
                "DeviceID": str(uuid.uuid4()),
                "VerSion": "5.21.0.2",
                "apiv": "w42",
                "StockID": "002498",
                "Day": "2026-01-16",
                "Time": "15:00"
            }
        },
        {
            "name": "GetTrendIncremental - StockL2Data (历史，无Time)",
            "data": {
                "a": "GetTrendIncremental",
                "c": "StockL2Data",
                "PhoneOSNew": "1",
                "DeviceID": str(uuid.uuid4()),
                "VerSion": "5.21.0.2",
                "apiv": "w42",
                "StockID": "002498",
                "Day": "2026-01-16"
            }
        },
        {
            "name": "GetStockTrend - StockL2Data",
            "data": {
                "a": "GetStockTrend",
                "c": "StockL2Data",
                "PhoneOSNew": "1",
                "DeviceID": str(uuid.uuid4()),
                "VerSion": "5.21.0.2",
                "apiv": "w42",
                "StockID": "002498",
                "Day": "2026-01-16"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n测试: {test_case['name']}")
        print("-" * 80)
        
        try:
            response = requests.post(
                base_url,
                data=test_case['data'],
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=60
            )
            
            print(f"状态码: {response.status_code}")
            print(f"响应长度: {len(response.text)} 字节")
            print(f"响应前200字符: {response.text[:200]}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"JSON解析成功")
                    print(f"errcode: {result.get('errcode', 'N/A')}")
                    print(f"返回字段: {list(result.keys())}")
                    
                    # 如果有trend字段，显示前几条
                    if 'trend' in result:
                        trend = result['trend']
                        print(f"trend数据条数: {len(trend)}")
                        if len(trend) > 0:
                            print(f"第一条数据: {trend[0]}")
                            print(f"最后一条数据: {trend[-1]}")
                    
                except Exception as e:
                    print(f"JSON解析失败: {e}")
            
        except Exception as e:
            print(f"请求失败: {e}")
        
        print()

if __name__ == "__main__":
    test_sector_intraday_api()
    test_stock_intraday_api()
