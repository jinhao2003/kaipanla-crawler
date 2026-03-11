# -*- coding: utf-8 -*-
"""
测试涨停原因板块爬虫功能
"""

from kaipanla_crawler import KaipanlaCrawler
import json

def test_sector_ranking():
    """测试板块排名功能"""
    crawler = KaipanlaCrawler()
    
    # 获取2026-01-16的板块数据
    print("=" * 80)
    print("测试涨停原因板块数据获取")
    print("=" * 80)
    
    data = crawler.get_sector_ranking("2026-01-16")
    
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
            if stock['涨停原因']:
                # 只显示前100个字符
                reason = stock['涨停原因'][:100] + "..." if len(stock['涨停原因']) > 100 else stock['涨停原因']
                print(f"      原因: {reason}")
        
        if len(sector['stocks']) > 3:
            print(f"   ... 还有 {len(sector['stocks']) - 3} 只股票")
    
    # 保存完整数据到JSON文件
    output_file = "sector_ranking_2026-01-16.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n完整数据已保存到: {output_file}")
    
    return data


def test_specific_sector():
    """测试特定板块的详细信息"""
    crawler = KaipanlaCrawler()
    data = crawler.get_sector_ranking("2026-01-16")
    
    print("\n" + "=" * 80)
    print("【芯片板块详细信息】")
    print("=" * 80)
    
    # 查找芯片板块
    chip_sector = None
    for sector in data['sectors']:
        if '芯片' in sector['sector_name']:
            chip_sector = sector
            break
    
    if chip_sector:
        print(f"\n板块名称: {chip_sector['sector_name']}")
        print(f"涨停股票数: {chip_sector['stock_count']}")
        print("\n涨停股票列表:")
        print("-" * 80)
        
        for i, stock in enumerate(chip_sector['stocks'], 1):
            print(f"\n{i}. {stock['股票代码']} {stock['股票名称']}")
            print(f"   涨停价: {stock['涨停价']}")
            print(f"   {stock['连板描述']} (连板{stock['连板次数']}次)")
            print(f"   成交额: {stock['成交额']:,}")
            print(f"   总市值: {stock['总市值']:,}")
            print(f"   概念标签: {stock['概念标签']}")
            print(f"   主题: {stock['主题']}")
            print(f"   涨停原因: {stock['涨停原因'][:200]}...")
    else:
        print("未找到芯片板块")


if __name__ == "__main__":
    # 测试基本功能
    test_sector_ranking()
    
    # 测试特定板块
    test_specific_sector()
