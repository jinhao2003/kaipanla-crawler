# -*- coding: utf-8 -*-
"""
测试GET方法
"""

import requests
import urllib3
import json

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_get():
    """测试GET方法"""
    url = "https://apphwhq.longhuvip.com/w1/api/index.php"
    
    params = {
        "apiv": "w42",
        "PhoneOSNew": "1",
        "VerSion": "5.21.0.2"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; SHARK PRS-A0 Build/PQ3A.190605.01141736; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Safari/537.36;kaipanla 5.21.0.2",
        "Accept": "application/json, text/javascript, */*; q=0.01",
    }
    
    print("测试GET请求...")
    print(f"URL: {url}")
    print(f"参数: {params}\n")
    
    try:
        response = requests.get(
            url, 
            params=params,
            headers=headers,
            verify=False,
            proxies={'http': None, 'https': None},
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应长度: {len(response.text)} 字节")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        print(f"\n原始响应内容:")
        print(response.text[:1000])
        
        if response.text:
            try:
                data = response.json()
                print("\n✅ JSON解析成功！")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
                return data
            except:
                print("\n❌ 不是JSON格式")
        else:
            print("\n⚠️  响应为空")
            
    except Exception as e:
        print(f"\n❌ 请求异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_get()
