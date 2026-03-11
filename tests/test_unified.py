# -*- coding: utf-8 -*-
"""
测试统一接口
"""

import sys
for module in list(sys.modules.keys()):
    if 'kaipanla' in module:
        del sys.modules[module]

from kaipanla_crawler import KaipanlaCrawler

crawler = KaipanlaCrawler()

print("=" * 60)
print("测试1: 获取单日数据（返回Series）")
print("=" * 60)
series = crawler.get_daily_data("2026-01-16")
print(series)
print(f"\n数据类型: {type(series)}")

print("\n" + "=" * 60)
print("测试2: 获取日期范围数据（返回DataFrame）")
print("=" * 60)
df = crawler.get_daily_data("2026-01-16", "2026-01-14")
print(df)
print(f"\n数据类型: {type(df)}")
print(f"数据形状: {df.shape}")

# 保存为CSV
df.to_csv("daily_data_range.csv", index=False, encoding="utf-8-sig")
print("\n✅ 数据已保存到 daily_data_range.csv")
