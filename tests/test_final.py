# -*- coding: utf-8 -*-
"""
最终测试 - 2026-01-16数据
"""

# 强制重新导入
import sys
if 'kaipanla_crawler' in sys.modules:
    del sys.modules['kaipanla_crawler']

from kaipanla_crawler import KaipanlaCrawler

def main():
    print("=" * 60)
    print("开盘啦爬虫 - 2026-01-16数据获取测试")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    date = "2026-01-16"
    
    # 1. 市场情绪
    print("\n1. 市场情绪数据")
    print("-" * 60)
    df1 = crawler.get_market_sentiment(date)
    print(f"✅ 获取 {len(df1)} 行数据")
    print(df1.T)
    
    # 2. 大盘指数
    print("\n2. 大盘指数数据")
    print("-" * 60)
    df2 = crawler.get_market_index(date)
    print(f"✅ 获取 {len(df2)} 行数据")
    print(df2)
    
    # 3. 连板梯队
    print("\n3. 连板梯队数据")
    print("-" * 60)
    df3 = crawler.get_limit_up_ladder(date)
    print(f"✅ 获取 {len(df3)} 行数据")
    print(df3.T)
    
    # 4. 大幅回撤
    print("\n4. 大幅回撤股票")
    print("-" * 60)
    df4 = crawler.get_sharp_withdrawal(date)
    print(f"✅ 获取 {len(df4)} 行数据")
    print(df4)
    
    print("\n" + "=" * 60)
    print("🎉 所有数据获取成功！")
    print("=" * 60)


if __name__ == "__main__":
    main()
