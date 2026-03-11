# -*- coding: utf-8 -*-
"""
测试板块数据获取功能
"""

import sys
for module in list(sys.modules.keys()):
    if 'kaipanla' in module:
        del sys.modules[module]

from kaipanla_crawler import KaipanlaCrawler

crawler = KaipanlaCrawler()

print("=" * 60)
print("测试板块排行数据获取")
print("=" * 60)

# 获取2026-01-16的板块数据
df = crawler.get_sector_ranking("2026-01-16", limit=10)

print(f"\n✅ 成功获取 {len(df)} 个板块数据")
print("\n前5个板块:")
print(df.head())

print("\n\n详细数据（前3个板块）:")
for i in range(min(3, len(df))):
    print(f"\n【{i+1}. {df.iloc[i]['板块名称']}】")
    print(f"  板块代码: {df.iloc[i]['板块代码']}")
    print(f"  强度: {df.iloc[i]['强度']}")
    print(f"  涨跌幅: {df.iloc[i]['涨跌幅(%)']}%")
    print(f"  成交额: {df.iloc[i]['成交额(元)']:,.0f} 元")
    print(f"  主力净流入: {df.iloc[i]['主力净流入(元)']:,.0f} 元")
    print(f"  机构增仓: {df.iloc[i]['机构增仓(元)']:,.0f} 元")

# 保存为CSV
df.to_csv("sector_ranking_2026-01-16.csv", index=False, encoding="utf-8-sig")
print("\n✅ 数据已保存到 sector_ranking_2026-01-16.csv")
