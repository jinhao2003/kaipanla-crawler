#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试ETF榜单接口
"""

import sys
sys.path.insert(0, '.')

import requests
import uuid

def test_realtime_etf():
    """测试实时ETF榜单"""
    print("=" * 100)
    print("测试：实时ETF榜单")
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
        "Order": "1",
        "a": "ETFStockRanking",
        "st": "30",
        "c": "NewStockRanking",
        "Filtration": "0",
        "PhoneOSNew": "1",
        "DeviceID": str(uuid.uuid4()),
        "VerSion": "5.21.0.2",
        "Token": "0daffcf404348e2fb714795ba5bdff02",
        "Index": "0",
        "PidType": "0",
        "apiv": "w42",
        "Type": "1",
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
        print(f"errcode: {result.get('errcode', 'N/A')}")
        
        etf_list = result.get("list", [])
        count = result.get("Count", 0)
        
        print(f"Count: {count}")
        print(f"返回ETF数量: {len(etf_list)}")
        
        if etf_list:
            print(f"\n前5个ETF:")
            for i, etf in enumerate(etf_list[:5], 1):
                if len(etf) >= 4:
                    print(f"  {i}. {etf[0]} {etf[1]}: {etf[2]} ({etf[3]:+.2f}%)")
            
            # 分析第一个ETF的字段
            first_etf = etf_list[0]
            print(f"\n第一个ETF字段分析:")
            print(f"  字段数量: {len(first_etf)}")
            
            field_names = [
                "ETF代码", "ETF名称", "价格", "涨幅(%)", "成交额",
                "量比", "昨日增减金额", "昨日增减份额", "昨日增减比例(%)", "一周收益(%)",
                "一月收益(%)", "三个月收益(%)", "半年收益(%)", "总市值", "未知14",
                "未知15", "未知16", "未知17", "未知18", "今年以来涨幅", "未知20"
            ]
            
            print(f"\n字段详情:")
            for idx, value in enumerate(first_etf):
                field_name = field_names[idx] if idx < len(field_names) else f"未知{idx}"
                print(f"  [{idx}] {field_name}: {value}")
        
        return result
        
    except Exception as e:
        print(f"请求失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_historical_etf():
    """测试历史ETF榜单"""
    print("\n" + "=" * 100)
    print("测试：历史ETF榜单")
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
        "Order": "1",
        "a": "ETFStockRanking",
        "st": "30",
        "c": "NewStockRanking",
        "Filtration": "0",
        "PhoneOSNew": "1",
        "DeviceID": str(uuid.uuid4()),
        "VerSion": "5.21.0.2",
        "Token": "0daffcf404348e2fb714795ba5bdff02",
        "Index": "0",
        "PidType": "0",
        "Date": "2026-02-09",
        "apiv": "w42",
        "Type": "1",
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
        print(f"errcode: {result.get('errcode', 'N/A')}")
        
        etf_list = result.get("list", [])
        count = result.get("Count", 0)
        
        print(f"Count: {count}")
        print(f"返回ETF数量: {len(etf_list)}")
        
        if etf_list:
            print(f"\n前5个ETF:")
            for i, etf in enumerate(etf_list[:5], 1):
                if len(etf) >= 4:
                    print(f"  {i}. {etf[0]} {etf[1]}: {etf[2]} ({etf[3]:+.2f}%)")
        
        return result
        
    except Exception as e:
        print(f"请求失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_pagination():
    """测试分页"""
    print("\n" + "=" * 100)
    print("测试：ETF榜单分页")
    print("=" * 100)
    
    url = "https://apphwhq.longhuvip.com/w1/api/index.php"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; 23116PN5BC Build/PQ3A.190605.01141736)",
        "Host": "apphwhq.longhuvip.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    
    all_etfs = []
    page = 0
    
    while page < 5:  # 最多测试5页
        index = page * 30
        print(f"\n请求第 {page + 1} 页 (Index={index})...")
        
        data = {
            "Order": "1",
            "a": "ETFStockRanking",
            "st": "30",
            "c": "NewStockRanking",
            "Filtration": "0",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "Token": "0daffcf404348e2fb714795ba5bdff02",
            "Index": str(index),
            "PidType": "0",
            "apiv": "w42",
            "Type": "1",
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
            
            etf_list = result.get("list", [])
            count = result.get("Count", 0)
            
            print(f"  Count={count}, 返回={len(etf_list)}个ETF")
            
            if not etf_list:
                print(f"  没有更多数据，停止")
                break
            
            all_etfs.extend(etf_list)
            
            # 显示前3个
            if etf_list:
                print(f"  前3个:")
                for i, etf in enumerate(etf_list[:3], 1):
                    if len(etf) >= 4:
                        print(f"    {i}. {etf[0]} {etf[1]}: {etf[3]:+.2f}%")
            
            # 如果返回少于30个，说明是最后一页
            if len(etf_list) < 30:
                print(f"  返回数量 < 30，这是最后一页")
                break
            
            page += 1
            
        except Exception as e:
            print(f"  请求失败: {e}")
            break
    
    print(f"\n总共获取: {len(all_etfs)} 个ETF")

if __name__ == "__main__":
    # 测试实时接口
    realtime_result = test_realtime_etf()
    
    # 测试历史接口
    historical_result = test_historical_etf()
    
    # 测试分页
    test_pagination()
