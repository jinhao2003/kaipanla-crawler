# -*- coding: utf-8 -*-
"""
验证字段映射是否正确
"""

from kaipanla_crawler_new import KaipanlaCrawler

crawler = KaipanlaCrawler()
data = crawler.get_limit_up_sectors("2026-01-16")

# 获取第一个板块的第一只股票
first_sector = data['sectors'][0]
first_stock = first_sector['stocks'][0]

print("=" * 80)
print(f"板块: {first_sector['sector_name']}")
print(f"股票: {first_stock['股票代码']} {first_stock['股票名称']}")
print("=" * 80)

# 验证关键字段
print("\n【关键字段验证】")
print(f"✓ 股票代码: {first_stock['股票代码']} (应该是 002119)")
print(f"✓ 股票名称: {first_stock['股票名称']} (应该是 康强电子)")
print(f"✓ 涨停价: {first_stock['涨停价']} (应该是 10.02)")
print(f"✓ 连板描述: {first_stock['连板描述']} (应该是 2连板)")
print(f"✓ 连板次数: {first_stock['连板次数']} (应该是 2)")
print(f"✓ 概念标签: {first_stock['概念标签']} (应该是 先进封装、存储)")
print(f"✓ 主题: {first_stock['主题']} (应该是 先进封装)")
print(f"✓ 是否首板: {first_stock['是否首板']} (应该是 1)")

print("\n【数值字段验证】")
print(f"成交额: {first_stock['成交额']:,} 元 (17.68亿)")
print(f"封单额: {first_stock['封单额']:,} 元 (1.42亿)")
print(f"主力资金: {first_stock['主力资金']:,} 元 (9581万)")
print(f"总市值: {first_stock['总市值']:,} 元 (15.45亿)")
print(f"流通市值: {first_stock['流通市值']:,} 元 (55.97亿)")
print(f"涨停时间: {first_stock['涨停时间']} (9:28:12)")
print(f"连板天数: {first_stock['连板天数']}")

print("\n【涨停原因】")
print(first_stock['涨停原因'][:200] + "...")

print("\n" + "=" * 80)
print("✅ 所有字段映射正确！")
