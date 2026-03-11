# -*- coding: utf-8 -*-
"""
测试历史数据API接口
"""

import requests
import urllib3
import json
import uuid

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_historical_api():
    """测试历史数据接口"""
    print("=" * 60)
    print("测试历史数据API接口")
    print("=" * 60)
    
    url = "https://apphis.longhuvip.com/w1/api/index.php"
    
    # URL参数
    params = {
        "apiv": "w42",
        "PhoneOSNew": "1",
        "VerSion": "5.21.0.2"
    }
    
    # POST body参数
    data = {
        "a": "HisZhangFuDetail",
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
    
    print(f"\nURL: {url}")
    print(f"URL参数: {params}")
    print(f"POST Body: {data}")
    print(f"\n请求日期: {data['Day']}\n")
    
    try:
        response = requests.post(
            url, 
            params=params,
            data=data,
            headers=headers,
            verify=False,
            proxies={'http': None, 'https': None},
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        print(f"响应长度: {len(response.text)} 字节\n")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 请求成功！")
            print(f"响应键: {list(result.keys())}\n")
            
            # 打印完整数据
            print("=" * 60)
            print("完整响应数据:")
            print("=" * 60)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # 检查是否有日期字段
            if "Day" in result:
                print(f"\n✅ 返回日期: {result['Day']}")
                if result['Day'] == data['Day']:
                    print("✅ 日期匹配！此接口支持历史数据查询！")
                else:
                    print("⚠️  日期不匹配")
            
            return result
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return None

if __name__ == "__main__":
    result = test_historical_api()
    
    if result:
        print("\n" + "=" * 60)
        print("🎉 测试成功！")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ 测试失败！")
        print("=" * 60)
