#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试板块竞价异动接口
"""

import sys
sys.path.insert(0, '.')

import requests
import uuid
import json

def test_realtime_bidding():
    """测试实时板块竞价异动"""
    print("=" * 100)
    print("测试：实时板块竞价异动")
    print("=" * 100)
    
    url = "https://apphwhq.longhuvip.com/w1/api/index.php"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; 23116PN5BC Build/PQ3A.190605.01141736)",
        "Host": "apphwhq.longhuvip.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    
    data = {
        "a": "GetBKJJ_W36",
        "c": "StockBidYiDong",
        "PhoneOSNew": "1",
        "DeviceID": str(uuid.uuid4()),
        "VerSion": "5.21.0.2",
        "Token": "0daffcf404348e2fb714795ba5bdff02",
        "apiv": "w42",
        "UserID": "4315515"
    }
    
    try:
        response = requests.post(
            url,
            data=data,
            headers=headers,
            verify=False,
            proxies={'http': None, 'https': None},
            timeout=30
        )
        result = response.json()
        
        print(f"\n返回结果:")
        print(f"日期: {result.get('Day', 'N/A')}")
        print(f"errcode: {result.get('errcode', 'N/A')}")
        
        # 分析三个列表
        list1 = result.get("List1", [])
        list2 = result.get("List2", [])
        list3 = result.get("List3", [])
        
        print(f"\nList1 (今日新增竞价异动): {len(list1)} 个板块")
        print(f"List2 (昨日爆发板块延续异动): {len(list2)} 个板块")
        print(f"List3 (其他异动板块): {len(list3)} 个板块")
        
        # 显示List1的前3个
        if list1:
            print(f"\nList1 前3个板块:")
            for i, sector in enumerate(list1[:3], 1):
                if len(sector) >= 6:
                    print(f"  {i}. {sector[0]} {sector[1]}")
                    print(f"     竞价爆量: {sector[2]}")
                    print(f"     异动金额: {sector[3]}")
                    print(f"     竞价板块强度: {sector[4]}")
                    print(f"     主力净额: {sector[5]}")
        
        # 显示List2的前3个
        if list2:
            print(f"\nList2 前3个板块:")
            for i, sector in enumerate(list2[:3], 1):
                if len(sector) >= 6:
                    print(f"  {i}. {sector[0]} {sector[1]}")
                    print(f"     竞价爆量: {sector[2]}")
                    print(f"     异动金额: {sector[3]}")
                    print(f"     竞价板块强度: {sector[4]}")
                    print(f"     主力净额: {sector[5]}")
        
        # 显示List3的前3个
        if list3:
            print(f"\nList3 前3个板块:")
            for i, sector in enumerate(list3[:3], 1):
                if len(sector) >= 6:
                    print(f"  {i}. {sector[0]} {sector[1]}")
                    print(f"     竞价爆量: {sector[2]}")
                    print(f"     异动金额: {sector[3]}")
                    print(f"     竞价板块强度: {sector[4]}")
                    print(f"     主力净额: {sector[5]}")
        
        # 分析字段数量
        if list1:
            print(f"\n字段数量分析:")
            print(f"  List1 第一个板块字段数: {len(list1[0])}")
            if len(list1[0]) > 6:
                print(f"  额外字段: {list1[0][6:]}")
        
        return result
        
    except Exception as e:
        print(f"请求失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_historical_bidding():
    """测试历史板块竞价异动"""
    print("\n" + "=" * 100)
    print("测试：历史板块竞价异动")
    print("=" * 100)
    
    url = "https://apphis.longhuvip.com/w1/api/index.php"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; 23116PN5BC Build/PQ3A.190605.01141736)",
        "Host": "apphis.longhuvip.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    
    data = {
        "a": "GetBKJJ_W36",
        "c": "StockBidYiDong",
        "PhoneOSNew": "1",
        "DeviceID": str(uuid.uuid4()),
        "VerSion": "5.21.0.2",
        "Token": "0daffcf404348e2fb714795ba5bdff02",
        "apiv": "w42",
        "UserID": "4315515",
        "Day": "2026-02-10"
    }
    
    try:
        response = requests.post(
            url,
            data=data,
            headers=headers,
            verify=False,
            proxies={'http': None, 'https': None},
            timeout=30
        )
        result = response.json()
        
        print(f"\n返回结果:")
        print(f"日期: {result.get('Day', 'N/A')}")
        print(f"errcode: {result.get('errcode', 'N/A')}")
        
        # 分析三个列表
        list1 = result.get("List1", [])
        list2 = result.get("List2", [])
        list3 = result.get("List3", [])
        
        print(f"\nList1 (今日新增竞价异动): {len(list1)} 个板块")
        print(f"List2 (昨日爆发板块延续异动): {len(list2)} 个板块")
        print(f"List3 (其他异动板块): {len(list3)} 个板块")
        
        # 显示List1的前3个
        if list1:
            print(f"\nList1 前3个板块:")
            for i, sector in enumerate(list1[:3], 1):
                if len(sector) >= 6:
                    print(f"  {i}. {sector[0]} {sector[1]}")
                    print(f"     竞价爆量: {sector[2]}")
                    print(f"     异动金额: {sector[3]}")
                    print(f"     竞价板块强度: {sector[4]}")
                    print(f"     主力净额: {sector[5]}")
        
        return result
        
    except Exception as e:
        print(f"请求失败: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # 测试实时接口
    realtime_result = test_realtime_bidding()
    
    # 测试历史接口
    historical_result = test_historical_bidding()
    
    # 对比
    print("\n" + "=" * 100)
    print("对比分析")
    print("=" * 100)
    
    if realtime_result and historical_result:
        print(f"\n实时接口日期: {realtime_result.get('Day')}")
        print(f"历史接口日期: {historical_result.get('Day')}")
        
        print(f"\n实时接口数据量:")
        print(f"  List1: {len(realtime_result.get('List1', []))} 个")
        print(f"  List2: {len(realtime_result.get('List2', []))} 个")
        print(f"  List3: {len(realtime_result.get('List3', []))} 个")
        
        print(f"\n历史接口数据量:")
        print(f"  List1: {len(historical_result.get('List1', []))} 个")
        print(f"  List2: {len(historical_result.get('List2', []))} 个")
        print(f"  List3: {len(historical_result.get('List3', []))} 个")
