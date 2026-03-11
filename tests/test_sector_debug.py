# -*- coding: utf-8 -*-
"""
调试板块数据
"""

from kaipanla_crawler import KaipanlaCrawler

crawler = KaipanlaCrawler()
data = crawler.get_sector_ranking("2026-01-16")

print("返回数据类型:", type(data))
print("\n数据内容:")
print(data)
