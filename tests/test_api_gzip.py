# -*- coding: utf-8 -*-
"""
测试gzip压缩的响应
"""

import requests
import urllib3
import json
import gzip

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_with_gzip():
    """测试处理gzip响应"""
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
        "Accept-Encoding": "gzip, deflate",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Referer": "https://apppage.longhuvip.com/",
    }
    
    print("测试POST请求（处理gzip）...")
    print(f"URL: {url}")
    print(f"参数: {params}\n")
    
    try:
        response = requests.post(
            url, 
            params=params,
            headers=headers,
            verify=False,
            proxies={'http': None, 'https': None},
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        print(f"Content-Encoding: {response.headers.get('Content-Encoding')}")
        print(f"响应长度: {len(response.content)} 字节")
        print(f"解压后长度: {len(response.text)} 字节")
        
        if response.status_code == 200:
            # requests会自动解压gzip
            print(f"\n原始响应内容（前1000字符）:")
            print(response.text[:1000])
            
            try:
                data = response.json()
                print("\n✅ JSON解析成功！")
                print(f"响应键: {list(data.keys())}")
                
                # 打印完整数据
                print("\n完整响应数据:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                
                return data
            except Exception as e:
                print(f"\n❌ JSON解析失败: {e}")
                print(f"响应文本: {response.text}")
        else:
            print(f"\n❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"\n❌ 请求异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_with_gzip()
