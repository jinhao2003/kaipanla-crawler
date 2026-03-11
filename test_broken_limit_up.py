"""测试获取历史炸板股数据"""
from kaipanla_crawler import KaipanlaCrawler
import json

# 创建爬虫实例
crawler = KaipanlaCrawler()

# 测试日期
test_date = "2026-02-13"

print(f"测试获取 {test_date} 的炸板股数据...")
print("=" * 80)

# 先测试原始API响应
import requests
import uuid

device_id = str(uuid.uuid4())
data = {
    "Order": "1",
    "a": "HisDaBanList",
    "st": "30",
    "c": "HisHomeDingPan",
    "PhoneOSNew": "1",
    "DeviceID": device_id,
    "VerSion": "5.21.0.2",
    "Index": "0",
    "Is_st": "1",
    "PidType": "2",
    "apiv": "w42",
    "Type": "4",
    "FilterMotherboard": "0",
    "Filter": "0",
    "FilterTIB": "0",
    "Day": test_date,
    "FilterGem": "0"
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; 23116PN5BC Build/PQ3A.190605.01141736)",
    "Host": "apphis.longhuvip.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
}

print("\n发送原始API请求...")
response = requests.post(
    "https://apphis.longhuvip.com/w1/api/index.php",
    data=data,
    headers=headers,
    verify=False,
    timeout=60
)

print(f"状态码: {response.status_code}")
result = response.json()
print(f"\n原始响应（前1000字符）:")
print(json.dumps(result, ensure_ascii=False, indent=2)[:1000])

# 获取炸板股数据
broken_stocks = crawler.get_historical_broken_limit_up(test_date)

if broken_stocks:
    print(f"\n✅ 成功获取 {len(broken_stocks)} 只炸板股\n")
    
    # 显示前5只
    print("前5只炸板股详情:")
    print("-" * 80)
    for i, stock in enumerate(broken_stocks[:5], 1):
        print(f"\n{i}. {stock['stock_code']} {stock['stock_name']}")
        print(f"   涨幅: {stock['change_pct']:.2f}%")
        print(f"   昨日连板: {stock['yesterday_consecutive']}板 ({stock['yesterday_consecutive_text']})")
        print(f"   板块: {stock['sector']}")
        print(f"   换手率: {stock['turnover_rate']:.2f}%")
        print(f"   成交额: {stock['turnover_amount']:.0f}万元")
        print(f"   主力净额: {stock['main_capital_net']:.0f}万元")
        
        # 转换时间戳为可读格式
        if stock['limit_up_time'] > 0:
            from datetime import datetime
            limit_time = datetime.fromtimestamp(stock['limit_up_time'])
            open_time = datetime.fromtimestamp(stock['open_time']) if stock['open_time'] > 0 else None
            print(f"   涨停时间: {limit_time.strftime('%H:%M:%S')}")
            if open_time:
                print(f"   开板时间: {open_time.strftime('%H:%M:%S')}")
    
    # 保存完整数据到JSON文件
    output_file = f"broken_limit_up_{test_date.replace('-', '')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(broken_stocks, f, ensure_ascii=False, indent=2)
    
    print(f"\n完整数据已保存到: {output_file}")
    
else:
    print("\n✗ 未获取到炸板股数据（可能当天没有炸板股）")

print("\n" + "=" * 80)
