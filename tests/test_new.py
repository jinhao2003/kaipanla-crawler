# -*- coding: utf-8 -*-
"""
全新测试 - 2026-01-16数据
"""

import sys
import os

# 强制重新加载
for module in list(sys.modules.keys()):
    if 'kaipanla' in module:
        del sys.modules[module]

# 导入爬虫
from kaipanla_crawler import KaipanlaCrawler

def main():
    print("=" * 60)
    print("开盘啦爬虫 - 2026-01-16数据获取")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    date = "2026-01-16"
    
    # 1. 涨跌统计数据
    print("\n【1. 涨跌统计数据】")
    print("-" * 60)
    df1 = crawler.get_market_sentiment(date)
    if not df1.empty:
        print(f"✅ 成功获取 {len(df1)} 行数据")
        print(df1.T)
        df1.to_csv(f"1_market_sentiment_{date}.csv", index=False, encoding="utf-8-sig")
    else:
        print("❌ 获取失败")
    
    # 2. 大盘指数数据
    print("\n【2. 大盘指数数据】")
    print("-" * 60)
    df2 = crawler.get_market_index(date)
    if not df2.empty:
        print(f"✅ 成功获取 {len(df2)} 行数据")
        print(df2)
        df2.to_csv(f"2_market_index_{date}.csv", index=False, encoding="utf-8-sig")
    else:
        print("❌ 获取失败")
    
    # 3. 连板梯队数据
    print("\n【3. 连板梯队数据】")
    print("-" * 60)
    df3 = crawler.get_limit_up_ladder(date)
    if not df3.empty:
        print(f"✅ 成功获取 {len(df3)} 行数据")
        print(df3.T)
        df3.to_csv(f"3_limit_up_ladder_{date}.csv", index=False, encoding="utf-8-sig")
    else:
        print("❌ 获取失败")
    
    # 4. 大幅回撤股票
    print("\n【4. 大幅回撤股票】")
    print("-" * 60)
    df4 = crawler.get_sharp_withdrawal(date)
    if not df4.empty:
        print(f"✅ 成功获取 {len(df4)} 行数据")
        print(df4)
        df4.to_csv(f"4_sharp_withdrawal_{date}.csv", index=False, encoding="utf-8-sig")
    else:
        print("❌ 获取失败")
    
    # 汇总
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    
    success_count = sum([not df1.empty, not df2.empty, not df3.empty, not df4.empty])
    print(f"\n成功: {success_count}/4")
    
    if success_count == 4:
        print("\n🎉 所有数据获取成功！CSV文件已保存。")


if __name__ == "__main__":
    main()
