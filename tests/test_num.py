# -*- coding: utf-8 -*-
"""
测试获取大幅回撤的num
"""

import sys
for module in list(sys.modules.keys()):
    if 'kaipanla' in module:
        del sys.modules[module]

from kaipanla_crawler import KaipanlaCrawler

crawler = KaipanlaCrawler()
df = crawler.get_sharp_withdrawal("2026-01-16")

print("大幅回撤股票数据:")
print(df)

if not df.empty:
    print(f"\n总数: {df['总数'].iloc[0]}")
    print(f"返回的股票数: {len(df)}")
