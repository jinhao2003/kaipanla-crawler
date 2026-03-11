# -*- coding: utf-8 -*-
"""
测试完整的连板梯队数据
"""

import sys
for module in list(sys.modules.keys()):
    if 'kaipanla' in module:
        del sys.modules[module]

from kaipanla_crawler import KaipanlaCrawler

crawler = KaipanlaCrawler()
df = crawler.get_limit_up_ladder("2026-01-16")

print("=" * 60)
print("连板梯队数据（涨停表现）")
print("=" * 60)
print(df.T)

print("\n" + "=" * 60)
print("数据说明：")
print("=" * 60)
print(f"一板: {df['一板'].iloc[0]}")
print(f"二板: {df['二板'].iloc[0]}")
print(f"三板: {df['三板'].iloc[0]}")
print(f"高度板: {df['高度板'].iloc[0]}")
print(f"连板率: {df['连板率(%)'].iloc[0]}%")
print(f"今日涨停破板率: {df['今日涨停破板率(%)'].iloc[0]}%")
print(f"昨日涨停今表现: {df['昨日涨停今表现(%)'].iloc[0]}%")
print(f"昨日连板今表现: {df['昨日连板今表现(%)'].iloc[0]}%")
print(f"昨日破板今表现: {df['昨日破板今表现(%)'].iloc[0]}%")
print(f"市场评价: {df['市场评价'].iloc[0]}")
