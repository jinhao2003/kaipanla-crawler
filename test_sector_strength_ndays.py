#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试N日板块强度排名功能

测试内容：
1. 获取7日板块强度数据
2. 分析板块热度趋势
3. 查看特定板块的每日涨停数
4. 数据格式验证
"""

from kaipanla_crawler import KaipanlaCrawler
from datetime import datetime
import pandas as pd


def test_7days_sector_strength():
    """测试1: 获取7日板块强度数据"""
    print("=" * 60)
    print("测试1: 获取7日板块强度数据")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    end_date = "2026-01-20"
    num_days = 7
    
    print(f"\n获取截至 {end_date} 的最近 {num_days} 个交易日板块强度数据...\n")
    
    df = crawler.get_sector_strength_ndays(end_date, num_days=num_days)
    
    if df.empty:
        print("❌ 获取数据失败")
        return False
    
    print(f"\n✓ 成功获取数据")
    print(f"数据行数: {len(df)}")
    print(f"交易日数: {df['日期'].nunique()}")
    print(f"板块数: {df['板块名称'].nunique()}")
    
    print("\n数据预览（前10行）:")
    print(df.head(10))
    
    return True


def test_sector_trend_analysis():
    """测试2: 分析板块热度趋势"""
    print("\n" + "=" * 60)
    print("测试2: 分析板块热度趋势")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    end_date = "2026-01-20"
    num_days = 7
    
    print(f"\n获取数据并分析板块热度...\n")
    
    df = crawler.get_sector_strength_ndays(end_date, num_days=num_days)
    
    if df.empty:
        print("❌ 获取数据失败")
        return False
    
    # 计算每个板块的总涨停数
    sector_trend = df.groupby('板块名称')['涨停数'].sum().sort_values(ascending=False)
    
    print(f"✓ {num_days}日最强板块 TOP 10:\n")
    print(f"{'排名':<6} {'板块名称':<15} {'总涨停数':<10}")
    print("-" * 40)
    for i, (sector_name, total_count) in enumerate(sector_trend.head(10).items(), 1):
        print(f"{i:<6} {sector_name:<15} {total_count:<10}")
    
    # 计算每个板块的平均涨停数
    sector_avg = df.groupby('板块名称')['涨停数'].mean().sort_values(ascending=False)
    
    print(f"\n✓ {num_days}日平均涨停数最高板块 TOP 10:\n")
    print(f"{'排名':<6} {'板块名称':<15} {'平均涨停数':<10}")
    print("-" * 40)
    for i, (sector_name, avg_count) in enumerate(sector_avg.head(10).items(), 1):
        print(f"{i:<6} {sector_name:<15} {avg_count:<10.2f}")
    
    return True


def test_specific_sector_daily_data():
    """测试3: 查看特定板块的每日涨停数"""
    print("\n" + "=" * 60)
    print("测试3: 查看特定板块的每日涨停数")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    end_date = "2026-01-20"
    num_days = 7
    
    df = crawler.get_sector_strength_ndays(end_date, num_days=num_days)
    
    if df.empty:
        print("❌ 获取数据失败")
        return False
    
    # 选择涨停数最多的板块
    sector_trend = df.groupby('板块名称')['涨停数'].sum().sort_values(ascending=False)
    if sector_trend.empty:
        print("❌ 没有板块数据")
        return False
    
    top_sector = sector_trend.index[0]
    
    print(f"\n查看板块 [{top_sector}] 的每日涨停数:\n")
    
    sector_data = df[df['板块名称'] == top_sector].sort_values('日期')
    
    print(f"{'日期':<12} {'涨停数':<10} {'涨停股票':<50}")
    print("-" * 80)
    for _, row in sector_data.iterrows():
        stocks = row['涨停股票'][:50] + "..." if len(row['涨停股票']) > 50 else row['涨停股票']
        print(f"{row['日期']:<12} {row['涨停数']:<10} {stocks:<50}")
    
    print(f"\n总涨停数: {sector_data['涨停数'].sum()}")
    print(f"平均涨停数: {sector_data['涨停数'].mean():.2f}")
    print(f"最高涨停数: {sector_data['涨停数'].max()}")
    print(f"最低涨停数: {sector_data['涨停数'].min()}")
    
    return True


def test_sector_comparison():
    """测试4: 对比多个板块的强度变化"""
    print("\n" + "=" * 60)
    print("测试4: 对比多个板块的强度变化")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    end_date = "2026-01-20"
    num_days = 7
    
    df = crawler.get_sector_strength_ndays(end_date, num_days=num_days)
    
    if df.empty:
        print("❌ 获取数据失败")
        return False
    
    # 选择前3个最强板块
    sector_trend = df.groupby('板块名称')['涨停数'].sum().sort_values(ascending=False)
    top_sectors = sector_trend.head(3).index.tolist()
    
    print(f"\n对比前3个最强板块的每日涨停数:\n")
    
    # 创建透视表
    pivot_df = df[df['板块名称'].isin(top_sectors)].pivot_table(
        index='日期',
        columns='板块名称',
        values='涨停数',
        fill_value=0
    )
    
    print(pivot_df)
    
    print("\n各板块总涨停数:")
    for sector in top_sectors:
        total = df[df['板块名称'] == sector]['涨停数'].sum()
        print(f"  {sector}: {total}")
    
    return True


def test_data_validation():
    """测试5: 数据格式验证"""
    print("\n" + "=" * 60)
    print("测试5: 数据格式验证")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    end_date = "2026-01-20"
    num_days = 7
    
    df = crawler.get_sector_strength_ndays(end_date, num_days=num_days)
    
    if df.empty:
        print("❌ 获取数据失败")
        return False
    
    # 验证必需列
    required_columns = ['日期', '板块代码', '板块名称', '涨停数', '涨停股票']
    
    print("\n验证数据列...")
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"❌ 缺失列: {missing_columns}")
        return False
    
    print("✓ 所有必需列完整")
    
    # 验证数据类型
    print("\n验证数据类型...")
    if not pd.api.types.is_integer_dtype(df['涨停数']):
        print(f"❌ '涨停数' 列应为整数类型")
        return False
    
    print("✓ 数据类型正确")
    
    # 验证数值范围
    print("\n验证数值范围...")
    if (df['涨停数'] < 0).any():
        print(f"❌ 涨停数不应为负数")
        return False
    
    print("✓ 数值范围合理")
    
    # 验证日期格式
    print("\n验证日期格式...")
    try:
        pd.to_datetime(df['日期'])
        print("✓ 日期格式正确")
    except:
        print("❌ 日期格式错误")
        return False
    
    return True


def test_custom_days():
    """测试6: 自定义天数"""
    print("\n" + "=" * 60)
    print("测试6: 自定义天数")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    end_date = "2026-01-20"
    
    # 测试不同天数
    test_days = [3, 5, 10]
    
    for num_days in test_days:
        print(f"\n获取 {num_days} 日数据...")
        df = crawler.get_sector_strength_ndays(end_date, num_days=num_days)
        
        if df.empty:
            print(f"  ❌ 获取 {num_days} 日数据失败")
            continue
        
        actual_days = df['日期'].nunique()
        print(f"  ✓ 成功获取 {actual_days} 个交易日数据")
        print(f"  数据行数: {len(df)}")
    
    return True


if __name__ == "__main__":
    print("开始测试N日板块强度排名功能\n")
    
    tests = [
        ("获取7日板块强度数据", test_7days_sector_strength),
        ("分析板块热度趋势", test_sector_trend_analysis),
        ("查看特定板块的每日涨停数", test_specific_sector_daily_data),
        ("对比多个板块的强度变化", test_sector_comparison),
        ("数据格式验证", test_data_validation),
        ("自定义天数", test_custom_days),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # 输出测试总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\n通过率: {passed}/{total} ({passed/total*100:.1f}%)")
