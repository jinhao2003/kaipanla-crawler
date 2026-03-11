# -*- coding: utf-8 -*-
"""
测试市场情绪数据获取
"""

from kaipanla_crawler import KaipanlaCrawler
import pandas as pd

def test_market_sentiment():
    """测试市场情绪数据获取"""
    print("=" * 60)
    print("开始测试市场情绪数据获取")
    print("=" * 60)
    
    # 创建爬虫实例
    crawler = KaipanlaCrawler()
    
    # 获取市场情绪数据
    print("\n正在获取市场情绪数据...")
    df = crawler.get_market_sentiment()
    
    if df.empty:
        print("❌ 获取失败：返回空数据")
        return False
    
    print("✅ 获取成功！")
    print(f"\n数据行数: {len(df)}")
    print(f"数据列数: {len(df.columns)}")
    
    print("\n" + "=" * 60)
    print("数据预览：")
    print("=" * 60)
    print(df.to_string())
    
    # 保存为CSV文件
    output_file = "market_sentiment.csv"
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"\n✅ 数据已保存到: {output_file}")
    
    return True

if __name__ == "__main__":
    try:
        success = test_market_sentiment()
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
