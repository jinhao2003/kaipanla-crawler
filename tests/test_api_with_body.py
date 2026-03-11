# -*- coding: utf-8 -*-
"""
测试带POST body的API请求
"""

import requests
import urllib3
import json

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_api_with_body():
    """测试带POST body的API"""
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
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Referer": "https://apppage.longhuvip.com/",
    }
    
    # 尝试不同的POST body
    test_bodies = [
        {},  # 空body
        {"date": "2026-01-19"},  # 带日期
        {"type": "market"},  # 带类型
    ]
    
    for i, body in enumerate(test_bodies, 1):
        print(f"\n{'='*60}")
        print(f"测试 {i}: POST body = {body}")
        print('='*60)
        
        try:
            response = requests.post(
                url, 
                params=params,
                data=body,
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=30
            )
            
            print(f"状态码: {response.status_code}")
            print(f"响应内容: {response.text[:500]}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("✅ 请求成功！")
                    print(f"响应键: {list(data.keys())}")
                    
                    # 检查是否有数据
                    if data.get("DaBanList") or data.get("list") or data.get("List"):
                        print("\n🎉 找到数据！")
                        print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
                        return data
                    else:
                        print("⚠️  响应为空")
                        print(json.dumps(data, indent=2, ensure_ascii=False))
                except:
                    print("❌ 响应不是JSON格式")
                    print(f"原始响应: {response.text}")
            else:
                print(f"❌ 请求失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 请求异常: {str(e)}")
    
    return None

if __name__ == "__main__":
    test_api_with_body()
