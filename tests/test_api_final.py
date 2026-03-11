# -*- coding: utf-8 -*-
"""
最终测试 - 带完整POST body
"""

import requests
import urllib3
import json
import uuid

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_final():
    """测试完整的POST请求"""
    url = "https://apphwhq.longhuvip.com/w1/api/index.php"
    
    params = {
        "apiv": "w42",
        "PhoneOSNew": "1",
        "VerSion": "5.21.0.2"
    }
    
    # POST body参数
    data = {
        "c": "Index",
        "a": "GetInfo",
        "View": "4,5,11",
        "DeviceID": str(uuid.uuid4())  # 生成随机设备ID
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; SHARK PRS-A0 Build/PQ3A.190605.01141736; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Safari/537.36;kaipanla 5.21.0.2",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Referer": "https://apppage.longhuvip.com/",
    }
    
    print("🚀 测试完整POST请求...")
    print(f"URL: {url}")
    print(f"URL参数: {params}")
    print(f"POST Body: {data}\n")
    
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
            data = response.json()
            print("✅ 请求成功！")
            print(f"响应键: {list(data.keys())}\n")
            
            # 打印完整数据
            print("=" * 60)
            print("完整响应数据:")
            print("=" * 60)
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            return data
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    result = test_final()
    if result and result.get("DaBanList"):
        print("\n" + "=" * 60)
        print("🎉 成功获取市场情绪数据！")
        print("=" * 60)
