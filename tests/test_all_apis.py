# -*- coding: utf-8 -*-
"""
测试所有API接口
"""

import requests
import urllib3
import json
import uuid

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_api(name, data_params):
    """测试单个API"""
    print("\n" + "=" * 60)
    print(f"测试: {name}")
    print("=" * 60)
    
    url = "https://apphis.longhuvip.com/w1/api/index.php"
    
    params = {
        "apiv": "w42",
        "PhoneOSNew": "1",
        "VerSion": "5.21.0.2"
    }
    
    data = {
        "PhoneOSNew": "1",
        "DeviceID": str(uuid.uuid4()),
        "VerSion": "5.21.0.2",
        "apiv": "w42",
        "Day": "2026-01-16"
    }
    data.update(data_params)
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SHARK PRS-A0 Build/PQ3A.190605.01141736)",
        "Host": "apphis.longhuvip.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    
    print(f"POST参数: {data_params}")
    
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
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功！响应键: {list(result.keys())}")
            print(f"\n响应数据（前2000字符）:")
            print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])
            return result
        else:
            print(f"❌ 失败: {response.status_code}")
            print(f"响应: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
    
    return None


def main():
    """测试所有接口"""
    print("=" * 60)
    print("开盘啦API接口测试")
    print("=" * 60)
    
    # 1. 涨跌统计及相关数据
    api1 = test_api(
        "涨跌统计及相关数据",
        {"a": "HisZhangFuDetail", "c": "HisHomeDingPan"}
    )
    
    # 2. 大盘数据
    api2 = test_api(
        "大盘数据",
        {"a": "GetZsReal", "c": "StockL2History"}
    )
    
    # 3. 连板梯队数据
    api3 = test_api(
        "连板梯队数据",
        {"a": "ZhangTingExpression", "c": "HisHomeDingPan"}
    )
    
    # 4. 大幅回撤家数
    api4 = test_api(
        "大幅回撤家数",
        {"a": "SharpWithdrawal", "c": "HisHomeDingPan"}
    )
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    
    # 统计结果
    results = {
        "涨跌统计": api1 is not None,
        "大盘数据": api2 is not None,
        "连板梯队": api3 is not None,
        "大幅回撤": api4 is not None,
    }
    
    print("\n结果汇总:")
    for name, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        print(f"  {name}: {status}")


if __name__ == "__main__":
    main()
