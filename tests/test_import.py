# -*- coding: utf-8 -*-
"""
测试导入
"""

import sys
import importlib

# 强制重新加载模块
if 'kaipanla_crawler' in sys.modules:
    del sys.modules['kaipanla_crawler']

from kaipanla_crawler import KaipanlaCrawler

crawler = KaipanlaCrawler()

# 检查方法是否存在
methods = [m for m in dir(crawler) if not m.startswith('_')]
print("可用方法:")
for method in methods:
    print(f"  - {method}")

# 测试get_market_index
if hasattr(crawler, 'get_market_index'):
    print("\n✅ get_market_index 方法存在")
    df = crawler.get_market_index("2026-01-16")
    print(f"返回数据行数: {len(df)}")
else:
    print("\n❌ get_market_index 方法不存在")
