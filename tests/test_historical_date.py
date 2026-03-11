# -*- coding: utf-8 -*-
"""
测试获取历史日期数据
"""

from kaipanla_crawler import KaipanlaCrawler
import pandas as pd

def test_historical_date():
    """测试获取2026年1月16日的数据"""
    print("=" * 60)
    print("测试获取2026年1月16日的市场情绪数据")
    print("=" * 60)
    
    # 创建爬虫实例
    crawler = KaipanlaCrawler()
    
    # 获取指定日期的数据
    target_date = "2026-01-16"
    print(f"\n正在获取 {target_date} 的数据...")
    df = crawler.get_market_sentiment(date=target_date)
    
    if df.empty:
        print("❌ 获取失败：返回空数据")
        print("\n注意：API可能只返回实时数据，不支持历史日期查询")
        return False
    
    print("✅ 获取成功！")
    print(f"\n数据行数: {len(df)}")
    print(f"数据列数: {len(df.columns)}")
    
    print("\n" + "=" * 60)
    print("数据预览：")
    print("=" * 60)
    
    # 转置显示，更易读
    print(df.T.to_string())
    
    # 检查返回的日期
    returned_date = df["日期"].iloc[0]
    print(f"\n请求日期: {target_date}")
    print(f"返回日期: {returned_date}")
    
    if returned_date == target_date:
        print("✅ 日期匹配！API支持历史数据查询")
    else:
        print("⚠️  日期不匹配！API可能只返回当前实时数据")
    
    # 保存为CSV文件
    output_file = f"market_sentiment_{target_date}.csv"
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"\n✅ 数据已保存到: {output_file}")
    
    return True

if __name__ == "__main__":
    try:
        success = test_historical_date()
        if success:
            print("\n" + "=" * 60)
            print("✅ 测试完成！")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ 测试失败！")
            print("=" * 60)
    except Exception as e:
        print(f"\n❌ 测试异常: {str(e)}")
        import traceback
        traceback.print_exc()
