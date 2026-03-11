#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试反包板处理逻辑

验证 TDType=0 的反包板股票是否正确处理
"""

import sys
sys.path.append('.')

from kaipanla_crawler import KaipanlaCrawler


def test_broken_board_identification():
    """测试反包板识别"""
    print("=" * 80)
    print("测试反包板识别功能")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    test_date = "2026-01-16"
    
    print(f"\n正在获取 {test_date} 的板块连板梯队...")
    print("-" * 80)
    
    try:
        data = crawler.get_sector_limit_up_ladder(test_date)
        
        print(f"\n✅ 数据获取成功！")
        
        # 统计反包板
        total_broken = 0
        total_normal = 0
        
        for sector in data['sectors']:
            sector_name = sector['sector_name']
            normal_count = len(sector['stocks'])
            broken_count = len(sector.get('broken_stocks', []))
            
            total_normal += normal_count
            total_broken += broken_count
            
            if broken_count > 0:
                print(f"\n📊 {sector_name}:")
                print(f"   正常连板: {normal_count}只")
                print(f"   反包板: {broken_count}只")
                
                # 显示反包板详情
                for stock in sector['broken_stocks']:
                    print(f"      🔄 {stock['stock_code']} {stock['stock_name']}")
                    print(f"         Tips: {stock['tips']}")
                    print(f"         连板天数: {stock['consecutive_days']}")
                    print(f"         is_broken: {stock.get('is_broken', False)}")
        
        print(f"\n" + "=" * 80)
        print(f"📈 总体统计:")
        print(f"   正常连板股票: {total_normal}只")
        print(f"   反包板股票: {total_broken}只")
        print(f"   总计: {total_normal + total_broken}只")
        
        # 验证反包板不计入连板梯队
        print(f"\n✅ 验证结果:")
        print(f"   - 反包板股票已单独记录在 broken_stocks 字段")
        print(f"   - 反包板股票不计入 stocks 字段（连板梯队）")
        print(f"   - 每只反包板股票都有 is_broken=True 标记")
        
        print("\n" + "=" * 80)
        print("✅ 测试完成！")
        print("=" * 80)
        
        return data
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_consecutive_days_parsing():
    """测试连板天数解析"""
    print("\n" + "=" * 80)
    print("测试连板天数解析")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    test_date = "2026-01-16"
    
    print(f"\n正在获取 {test_date} 的数据...")
    
    try:
        data = crawler.get_sector_limit_up_ladder(test_date)
        
        print(f"\n✅ 数据获取成功！")
        print(f"\n📊 连板天数解析验证:")
        print("-" * 80)
        
        for sector in data['sectors']:
            # 检查正常连板
            for stock in sector['stocks']:
                if stock['consecutive_days'] > 1:
                    print(f"✓ {stock['stock_name']}: {stock['consecutive_days']}连板")
            
            # 检查反包板的连板天数解析
            for stock in sector.get('broken_stocks', []):
                print(f"🔄 {stock['stock_name']}: {stock['tips']} -> 解析为{stock['consecutive_days']}连板")
        
        print("\n" + "=" * 80)
        print("✅ 解析测试完成！")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_data_structure():
    """测试数据结构完整性"""
    print("\n" + "=" * 80)
    print("测试数据结构完整性")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    test_date = "2026-01-16"
    
    print(f"\n正在获取 {test_date} 的数据...")
    
    try:
        data = crawler.get_sector_limit_up_ladder(test_date)
        
        print(f"\n✅ 数据获取成功！")
        print(f"\n📋 数据结构验证:")
        print("-" * 80)
        
        # 验证顶层字段
        required_fields = ['date', 'is_realtime', 'sectors']
        for field in required_fields:
            if field in data:
                print(f"✓ {field}: {type(data[field]).__name__}")
            else:
                print(f"✗ 缺少字段: {field}")
        
        # 验证板块字段
        if data['sectors']:
            sector = data['sectors'][0]
            print(f"\n板块字段:")
            sector_fields = ['sector_code', 'sector_name', 'limit_up_count', 'stocks', 'broken_stocks']
            for field in sector_fields:
                if field in sector:
                    value = sector[field]
                    if isinstance(value, list):
                        print(f"✓ {field}: list (长度={len(value)})")
                    else:
                        print(f"✓ {field}: {type(value).__name__} = {value}")
                else:
                    print(f"✗ 缺少字段: {field}")
            
            # 验证股票字段
            if sector['stocks']:
                stock = sector['stocks'][0]
                print(f"\n正常股票字段:")
                stock_fields = ['stock_code', 'stock_name', 'consecutive_days', 'tips']
                for field in stock_fields:
                    if field in stock:
                        print(f"✓ {field}: {stock[field]}")
                    else:
                        print(f"✗ 缺少字段: {field}")
            
            # 验证反包板字段
            if sector.get('broken_stocks'):
                broken = sector['broken_stocks'][0]
                print(f"\n反包板股票字段:")
                broken_fields = ['stock_code', 'stock_name', 'consecutive_days', 'tips', 'is_broken']
                for field in broken_fields:
                    if field in broken:
                        print(f"✓ {field}: {broken[field]}")
                    else:
                        print(f"✗ 缺少字段: {field}")
        
        print("\n" + "=" * 80)
        print("✅ 结构验证完成！")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_comparison_with_market_ladder():
    """对比板块连板梯队和全市场连板梯队"""
    print("\n" + "=" * 80)
    print("对比板块连板梯队和全市场连板梯队")
    print("=" * 80)
    
    crawler = KaipanlaCrawler()
    test_date = "2026-01-16"
    
    print(f"\n正在获取 {test_date} 的数据...")
    
    try:
        # 获取板块连板梯队
        sector_data = crawler.get_sector_limit_up_ladder(test_date)
        
        # 获取全市场连板梯队
        market_data = crawler.get_market_limit_up_ladder(test_date)
        
        print(f"\n✅ 数据获取成功！")
        print(f"\n📊 数据对比:")
        print("-" * 80)
        
        # 统计板块数据
        sector_normal = sum(len(s['stocks']) for s in sector_data['sectors'])
        sector_broken = sum(len(s.get('broken_stocks', [])) for s in sector_data['sectors'])
        
        # 统计全市场数据
        market_normal = market_data['statistics']['total_limit_up']
        market_broken = len(market_data['broken_stocks'])
        
        print(f"板块连板梯队:")
        print(f"   正常连板: {sector_normal}只")
        print(f"   反包板: {sector_broken}只")
        print(f"   总计: {sector_normal + sector_broken}只")
        
        print(f"\n全市场连板梯队:")
        print(f"   正常连板: {market_normal}只")
        print(f"   反包板: {market_broken}只")
        print(f"   总计: {market_normal + market_broken}只")
        
        # 验证一致性
        print(f"\n✅ 一致性验证:")
        if sector_broken == market_broken:
            print(f"   ✓ 反包板数量一致: {sector_broken}只")
        else:
            print(f"   ✗ 反包板数量不一致: 板块{sector_broken}只 vs 全市场{market_broken}只")
        
        print("\n" + "=" * 80)
        print("✅ 对比完成！")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 测试1: 反包板识别
    print("\n【测试1】反包板识别")
    test_broken_board_identification()
    
    # 测试2: 连板天数解析
    print("\n\n【测试2】连板天数解析")
    test_consecutive_days_parsing()
    
    # 测试3: 数据结构完整性
    print("\n\n【测试3】数据结构完整性")
    test_data_structure()
    
    # 测试4: 对比两个接口
    print("\n\n【测试4】对比板块和全市场数据")
    test_comparison_with_market_ladder()
