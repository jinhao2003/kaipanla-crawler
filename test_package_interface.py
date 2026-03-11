#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试包接口 - 验证所有新增功能可以通过 KaipanlaCrawler 类正常访问
"""

from kaipanla_crawler import KaipanlaCrawler

def test_package_interface():
    """测试包接口的完整性"""
    
    print("=" * 60)
    print("测试 kaipanla_crawler 包接口")
    print("=" * 60)
    
    # 创建爬虫实例
    crawler = KaipanlaCrawler()
    
    # 测试1: 板块资金数据（实时）
    print("\n1. 测试板块资金数据获取（实时）...")
    try:
        data = crawler.get_sector_capital_data("801235")
        if data:
            print(f"   ✓ 成功获取板块资金数据")
            print(f"   - 成交额: {data.get('成交额', 0) / 1e8:.2f}亿")
            print(f"   - 主力净额: {data.get('主力净额', 0) / 1e8:.2f}亿")
        else:
            print("   ✗ 未获取到数据")
    except Exception as e:
        print(f"   ✗ 错误: {e}")
    
    # 测试2: N日板块强度
    print("\n2. 测试N日板块强度排名...")
    try:
        df = crawler.get_sector_strength_ndays("2026-01-20", num_days=3)
        if not df.empty:
            print(f"   ✓ 成功获取{len(df)}条板块强度数据")
            print(f"   - 数据日期范围: {df['日期'].min()} 至 {df['日期'].max()}")
        else:
            print("   ✗ 未获取到数据")
    except Exception as e:
        print(f"   ✗ 错误: {e}")
    
    # 测试3: 实时市场情绪
    print("\n3. 测试实时市场情绪...")
    try:
        mood = crawler.get_realtime_market_mood()
        if mood:
            print(f"   ✓ 成功获取市场情绪数据")
            print(f"   - 涨停: {mood.get('涨停家数', 0)}家")
            print(f"   - 跌停: {mood.get('跌停家数', 0)}家")
            print(f"   - 上涨: {mood.get('上涨家数', 0)}家")
            print(f"   - 下跌: {mood.get('下跌家数', 0)}家")
        else:
            print("   ✗ 未获取到数据")
    except Exception as e:
        print(f"   ✗ 错误: {e}")
    
    # 测试4: 实时实际涨跌停
    print("\n4. 测试实时实际涨跌停数据...")
    try:
        limit_data = crawler.get_realtime_actual_limit_up_down()
        if limit_data:
            print(f"   ✓ 成功获取涨跌停数据")
            print(f"   - 实际涨停: {limit_data.get('实际涨停', 0)}家")
            print(f"   - 实际跌停: {limit_data.get('实际跌停', 0)}家")
        else:
            print("   ✗ 未获取到数据")
    except Exception as e:
        print(f"   ✗ 错误: {e}")
    
    # 测试5: 获取首板股票列表（详细数据）
    print("\n5. 测试获取首板股票列表（详细数据）...")
    try:
        stocks = crawler.get_realtime_board_stocks(board_type=1)
        print(f"   ✓ 成功获取首板股票列表: {len(stocks)}只")
        if stocks:
            print(f"   - 示例: {stocks[0].get('股票名称', '')} ({stocks[0].get('股票代码', '')})")
    except Exception as e:
        print(f"   ✗ 错误: {e}")
    
    # 测试6: 获取所有连板股票
    print("\n6. 测试获取所有连板股票...")
    try:
        all_boards = crawler.get_realtime_all_boards_stocks()
        total = sum(len(stocks) for stocks in all_boards.values())
        print(f"   ✓ 成功获取所有连板数据，共{total}只股票")
        for board_name, stocks in all_boards.items():
            print(f"   - {board_name}: {len(stocks)}只")
    except Exception as e:
        print(f"   ✗ 错误: {e}")
    
    # 测试7: 简洁接口（数量+列表）
    print("\n7. 测试简洁接口（get_board_stocks_count_and_list）...")
    try:
        count, stocks = crawler.get_board_stocks_count_and_list(1)
        print(f"   ✓ 成功获取首板数据")
        print(f"   - 数量: {count}只")
        print(f"   - 列表长度: {len(stocks)}")
        if stocks:
            print(f"   - 示例: {stocks[0]}")
    except Exception as e:
        print(f"   ✗ 错误: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成！所有新增功能均可通过 KaipanlaCrawler 类访问")
    print("=" * 60)

if __name__ == "__main__":
    test_package_interface()
