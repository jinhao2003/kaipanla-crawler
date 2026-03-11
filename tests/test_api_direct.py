# -*- coding: utf-8 -*-
"""
直接测试API连接
"""

import requests
import urllib3
import json

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_api():
    """直接测试API"""
    url = "https://apphwhq.longhuvip.com/w1/api/index.php"
    
    params = {
        "apiv": "w42",
        "PhoneOSNew": "1",
        "VerSion": "5.21.0.2"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; SHARK PRS-A0 Build/PQ3A.190605.01141736; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Safari/537.36;kaipanla 5.21.0.2",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
    }
    
    print("测试URL:", url)
    print("参数:", params)
    print("\n发送请求...")
    
    try:
        # 禁用代理和SSL验证
        response = requests.post(
            url, 
            params=params,
            headers=headers,
            verify=False,
            proxies={'http': None, 'https': None},
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应长度: {len(response.text)} 字节")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ 请求成功！")
            print("\n响应数据结构:")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
            return data
        else:
            print(f"\n❌ 请求失败: {response.status_code}")
            print(response.text[:500])
            return None
            
    except Exception as e:
        print(f"\n❌ 请求异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_api()
