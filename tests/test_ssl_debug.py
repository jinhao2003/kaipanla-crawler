# -*- coding: utf-8 -*-
"""
调试SSL问题
"""

import requests
import urllib3
import uuid

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_direct():
    """直接调用 - 和test_api_final.py一样"""
    print("=" * 60)
    print("测试1: 直接调用（test_api_final.py方式）")
    print("=" * 60)
    
    url = "https://apphwhq.longhuvip.com/w1/api/index.php"
    
    params = {
        "apiv": "w42",
        "PhoneOSNew": "1",
        "VerSion": "5.21.0.2"
    }
    
    data = {
        "c": "Index",
        "a": "GetInfo",
        "View": "4,5,11",
        "DeviceID": str(uuid.uuid4())
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
        
        print(f"✅ 成功! 状态码: {response.status_code}")
        print(f"响应键: {list(response.json().keys())}")
        return True
    except Exception as e:
        print(f"❌ 失败: {str(e)}")
        return False


def test_with_class():
    """通过类调用 - 模拟爬虫方式"""
    print("\n" + "=" * 60)
    print("测试2: 通过类调用（爬虫方式）")
    print("=" * 60)
    
    from kaipanla_crawler import KaipanlaCrawler
    
    try:
        crawler = KaipanlaCrawler()
        df = crawler.get_market_sentiment()
        
        if not df.empty:
            print(f"✅ 成功! 获取到 {len(df)} 行数据")
            return True
        else:
            print("❌ 失败: 返回空数据")
            return False
    except Exception as e:
        print(f"❌ 失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    result1 = test_direct()
    result2 = test_with_class()
    
    print("\n" + "=" * 60)
    print("测试结果:")
    print("=" * 60)
    print(f"直接调用: {'✅ 成功' if result1 else '❌ 失败'}")
    print(f"类调用: {'✅ 成功' if result2 else '❌ 失败'}")
