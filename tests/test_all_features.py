# -*- coding: utf-8 -*-
"""
测试所有已实现的功能
"""

from kaipanla_crawler import KaipanlaCrawler
import pandas as pd

def test_all_features():
    """测试所有功能"""
    print("=" * 60)
    print("开盘啦爬虫 - 综合功能测试")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    target_date = "2026-01-16"
    
    # 1. 市场情绪数据
    print("\n" + "=" * 60)
    print("1. 市场情绪数据")
    print("=" * 60)
    df1 = crawler.get_market_sentiment(date=target_date)
    if not df1.empty:
        print("✅ 成功！")
        print(df1.T.to_string())
        df1.to_csv(f"market_sentiment_{target_date}.csv", index=False, encoding="utf-8-sig")
    else:
        print("❌ 失败")
    
    # 2. 大盘指数数据
    print("\n" + "=" * 60)
    print("2. 大盘指数数据")
    print("=" * 60)
    df2 = crawler.get_market_index(date=target_date)
    if not df2.empty:
        print("✅ 成功！")
        print(df2.to_string(index=False))
        df2.to_csv(f"market_index_{target_date}.csv", index=False, encoding="utf-8-sig")
    else:
        print("❌ 失败")
    
    # 3. 连板梯队数据
    print("\n" + "=" * 60)
    print("3. 连板梯队数据")
    print("=" * 60)
    df3 = crawler.get_limit_up_ladder(date=target_date)
    if not df3.empty:
        print("✅ 成功！")
        print(df3.T.to_string())
        df3.to_csv(f"limit_up_ladder_{target_date}.csv", index=False, encoding="utf-8-sig")
    else:
        print("❌ 失败")
    
    # 4. 大幅回撤股票
    print("\n" + "=" * 60)
    print("4. 大幅回撤股票")
    print("=" * 60)
    df4 = crawler.get_sharp_withdrawal(date=target_date)
    if not df4.empty:
        print("✅ 成功！")
        print(df4.to_string(index=False))
        df4.to_csv(f"sharp_withdrawal_{target_date}.csv", index=False, encoding="utf-8-sig")
    else:
        print("❌ 失败")
    
    # 汇总
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    
    results = {
        "市场情绪数据": not df1.empty,
        "大盘指数数据": not df2.empty,
        "连板梯队数据": not df3.empty,
        "大幅回撤股票": not df4.empty,
    }
    
    print("\n结果汇总:")
    for name, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        print(f"  {name}: {status}")
    
    success_count = sum(results.values())
    total_count = len(results)
    print(f"\n成功率: {success_count}/{total_count} ({success_count/total_count*100:.0f}%)")
    
    if success_count == total_count:
        print("\n🎉 所有功能测试通过！")
    
    return success_count == total_count


if __name__ == "__main__":
    try:
        test_all_features()
    except Exception as e:
        print(f"\n❌ 测试异常: {str(e)}")
        import traceback
        traceback.print_exc()
