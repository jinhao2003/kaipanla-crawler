# -*- coding: utf-8 -*-
"""
测试涨停原因板块爬虫功能
"""

from kaipanla_crawler_new import KaipanlaCrawler
import json

def test_limit_up_sectors():
    """测试涨停原因板块功能"""
    crawler = KaipanlaCrawler()
    
    print("=" * 80)
    print("测试涨停原因板块数据获取")
    print("=" * 80)
    
    data = crawler.get_limit_up_sectors("2026-01-16")
    
    # 打印市场概况
    print("\n【市场概况】")
    print("-" * 80)
    for key, value in data['summary'].items():
        print(f"{key}: {value}")
    
    # 打印板块信息
    print(f"\n【板块列表】共 {len(data['sectors'])} 个板块")
    print("-" * 80)
    
    for i, sector in enumerate(data['sectors'], 1):
        print(f"\n{i}. {sector['sector_name']} (代码: {sector['sector_code']})")
        print(f"   涨停股票数: {sector['stock_count']}")
        
        # 打印前3只涨停股票
        for j, stock in enumerate(sector['stocks'][:3], 1):
            print(f"   {j}) {stock['股票代码']} {stock['股票名称']}")
            print(f"      涨停价: {stock['涨停价']}, {stock['连板描述']}")
            print(f"      概念: {stock['概念标签']}")
            print(f"      主题: {stock['主题']}")
            if stock['涨停原因'] and isinstance(stock['涨停原因'], str):
                # 只显示前100个字符
                reason = stock['涨停原因'][:100] + "..." if len(stock['涨停原因']) > 100 else stock['涨停原因']
                print(f"      原因: {reason}")
        
        if len(sector['stocks']) > 3:
            print(f"   ... 还有 {len(sector['stocks']) - 3} 只股票")
    
    # 保存完整数据到JSON文件
    output_file = "limit_up_sectors_2026-01-16.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n完整数据已保存到: {output_file}")
    
    return data


if __name__ == "__main__":
    test_limit_up_sectors()
