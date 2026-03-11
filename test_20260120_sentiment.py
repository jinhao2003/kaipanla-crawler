#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试2026年1月20日的情绪数据获取

测试内容：
1. 获取2026-01-20的完整交易数据
2. 获取2026-01-20的连板梯队数据
3. 获取2026-01-20的板块资金数据
4. 获取2026-01-20的板块强度数据
"""

from kaipanla_crawler import KaipanlaCrawler
from datetime import datetime


def test_daily_data():
    """测试1: 获取2026-01-20的完整交易数据"""
    print("=" * 60)
    print("测试1: 获取2026-01-20的完整交易数据")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    date = "2026-01-20"
    
    print(f"\n获取 {date} 的完整交易数据...\n")
    
    try:
        data = crawler.get_daily_data(date)
        
        if data is None or data.empty:
            print("✗ 获取数据失败")
            return False
        
        print("✓ 成功获取数据\n")
        print(f"日期: {data['日期']}")
        print(f"涨停数: {data['涨停数']}")
        print(f"跌停数: {data['跌停数']}")
        print(f"上涨家数: {data['上涨家数']}")
        print(f"下跌家数: {data['下跌家数']}")
        print(f"上证指数: {data['上证指数']}")
        print(f"涨跌幅: {data['涨跌幅']}")
        print(f"首板数量: {data['首板数量']}")
        print(f"2连板数量: {data['2连板数量']}")
        print(f"3连板数量: {data['3连板数量']}")
        print(f"4连板以上数量: {data['4连板以上数量']}")
        print(f"连板率: {data['连板率']}%")
        print(f"大幅回撤家数: {data['大幅回撤家数']}")
        
        return True
        
    except Exception as e:
        print(f"✗ 获取数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_consecutive_limit_up():
    """测试2: 获取2026-01-20的连板梯队数据"""
    print("\n" + "=" * 60)
    print("测试2: 获取2026-01-20的连板梯队数据")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    date = "2026-01-20"
    
    print(f"\n获取 {date} 的连板梯队数据...\n")
    
    try:
        data = crawler.get_consecutive_limit_up(date)
        
        if not data:
            print("✗ 获取数据失败")
            return False
        
        print("✓ 成功获取数据\n")
        print(f"日期: {data['date']}")
        print(f"最高板: {data['max_consecutive']}连板")
        print(f"最高板个股: {data['max_consecutive_stocks']}")
        print(f"最高板题材: {data['max_consecutive_concepts']}")
        
        print("\n连板梯队分布:")
        for consecutive, stocks in sorted(data['ladder'].items(), reverse=True):
            print(f"  {consecutive}连板: {len(stocks)}只")
            if len(stocks) <= 3:
                for stock in stocks:
                    print(f"    - {stock['股票名称']} ({stock['股票代码']})")
        
        return True
        
    except Exception as e:
        print(f"✗ 获取数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_market_limit_up_ladder():
    """测试3: 获取2026-01-20的全市场连板梯队"""
    print("\n" + "=" * 60)
    print("测试3: 获取2026-01-20的全市场连板梯队")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    date = "2026-01-20"
    
    print(f"\n获取 {date} 的全市场连板梯队...\n")
    
    try:
        data = crawler.get_market_limit_up_ladder(date)
        
        if not data:
            print("✗ 获取数据失败")
            return False
        
        print("✓ 成功获取数据\n")
        print(f"日期: {data['date']}")
        print(f"是否实时: {data['is_realtime']}")
        print(f"总涨停数: {data['statistics']['total_limit_up']}只")
        print(f"最高板: {data['statistics']['max_consecutive']}连板")
        
        print("\n连板分布:")
        for consecutive, count in sorted(data['statistics']['ladder_distribution'].items(), reverse=True):
            print(f"  {consecutive}连板: {count}只")
        
        if data['broken_stocks']:
            print(f"\n反包板: {len(data['broken_stocks'])}只")
            for stock in data['broken_stocks'][:3]:
                print(f"  - {stock['stock_name']} ({stock['consecutive_days']}连板)")
        
        return True
        
    except Exception as e:
        print(f"✗ 获取数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_sector_capital():
    """测试4: 获取2026-01-20的板块资金数据"""
    print("\n" + "=" * 60)
    print("测试4: 获取2026-01-20的板块资金数据")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    date = "2026-01-20"
    
    # 测试几个主要板块
    sectors = {
        "801235": "化工",
        "801346": "电力设备",
        "801225": "机械设备"
    }
    
    print(f"\n获取 {date} 的板块资金数据...\n")
    print(f"{'板块名称':<10} {'成交额(亿)':<12} {'涨跌幅(%)':<10} {'主力净额(亿)':<12}")
    print("-" * 50)
    
    success_count = 0
    for sector_code, sector_name in sectors.items():
        try:
            data = crawler.get_sector_capital_data(sector_code, date)
            
            if data:
                print(f"{sector_name:<10} "
                      f"{data['turnover'] / 100000000:<12.2f} "
                      f"{data['change_pct']:<10.2f} "
                      f"{data['main_net_inflow'] / 100000000:<12.2f}")
                success_count += 1
            else:
                print(f"{sector_name:<10} 获取失败")
                
        except Exception as e:
            print(f"{sector_name:<10} 错误: {e}")
    
    print(f"\n成功率: {success_count}/{len(sectors)}")
    return success_count > 0


def test_sector_ranking():
    """测试5: 获取2026-01-20的板块排名数据"""
    print("\n" + "=" * 60)
    print("测试5: 获取2026-01-20的板块排名数据")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    date = "2026-01-20"
    
    print(f"\n获取 {date} 的板块排名数据...\n")
    
    try:
        data = crawler.get_sector_ranking(date)
        
        if not data or not data.get('sectors'):
            print("✗ 获取数据失败")
            return False
        
        print("✓ 成功获取数据\n")
        
        # 显示市场概况
        summary = data['summary']
        print("市场概况:")
        print(f"  日期: {summary['日期']}")
        print(f"  上涨家数: {summary['上涨家数']}")
        print(f"  下跌家数: {summary['下跌家数']}")
        print(f"  涨停数: {summary['涨停数']}")
        print(f"  跌停数: {summary['跌停数']}")
        print(f"  涨跌比: {summary['涨跌比']}")
        
        # 显示前5个板块
        print("\n前5个板块:")
        for i, sector in enumerate(data['sectors'][:5], 1):
            print(f"{i}. {sector['sector_name']}: {sector['stock_count']}只涨停")
        
        return True
        
    except Exception as e:
        print(f"✗ 获取数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_new_high_data():
    """测试6: 获取2026-01-20的百日新高数据"""
    print("\n" + "=" * 60)
    print("测试6: 获取2026-01-20的百日新高数据")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    date = "2026-01-20"
    
    print(f"\n获取 {date} 的百日新高数据...\n")
    
    try:
        new_high_count = crawler.get_new_high_data(date)
        
        if new_high_count is None:
            print("✗ 获取数据失败")
            return False
        
        print("✓ 成功获取数据\n")
        print(f"今日新增百日新高: {new_high_count}只")
        
        return True
        
    except Exception as e:
        print(f"✗ 获取数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def calculate_sentiment_indicators():
    """计算情绪指标"""
    print("\n" + "=" * 60)
    print("计算情绪指标")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    date = "2026-01-20"
    
    print(f"\n基于 {date} 的数据计算情绪指标...\n")
    
    try:
        # 获取完整数据
        daily_data = crawler.get_daily_data(date)
        new_high = crawler.get_new_high_data(date)
        
        if daily_data is None or daily_data.empty or new_high is None:
            print("✗ 数据不完整")
            return False
        
        # 计算三条情绪指标线
        # 1. 大盘系数 = 上涨家数 / 20
        market_coefficient = daily_data['上涨家数'] / 20.0
        
        # 2. 超短情绪 = 涨停数 + (新增百日新高 / 2) + (昨日涨停表现 * 10)
        # 注意：这里缺少"昨日涨停表现"数据，暂时用0代替
        ultra_short_sentiment = daily_data['涨停数'] + (new_high / 2.0) + 0
        
        # 3. 亏钱效应 = (炸板率 * 100) + (跌停数 + 大幅回撤家数) * 2
        # 注意：这里缺少"炸板率"数据，暂时用0代替
        loss_effect = 0 + (daily_data['跌停数'] + daily_data['大幅回撤家数']) * 2.0
        
        print("✓ 情绪指标计算完成\n")
        print(f"【三条情绪指标线】")
        print(f"1. 大盘系数: {market_coefficient:.2f}")
        print(f"   计算公式: 上涨家数({daily_data['上涨家数']}) / 20 = {market_coefficient:.2f}")
        
        print(f"\n2. 超短情绪: {ultra_short_sentiment:.2f}")
        print(f"   计算公式: 涨停数({daily_data['涨停数']}) + 新增百日新高({new_high})/2 + 昨日涨停表现*10")
        print(f"   注意: 昨日涨停表现数据暂缺")
        
        print(f"\n3. 亏钱效应: {loss_effect:.2f}")
        print(f"   计算公式: 炸板率*100 + (跌停数({daily_data['跌停数']}) + 大幅回撤({daily_data['大幅回撤家数']}))*2")
        print(f"   注意: 炸板率数据暂缺")
        
        print(f"\n【市场细节】")
        print(f"涨停数: {daily_data['涨停数']}")
        print(f"跌停数: {daily_data['跌停数']}")
        print(f"连板率: {daily_data['连板率']}%")
        print(f"首板: {daily_data['首板数量']}只")
        print(f"2连板: {daily_data['2连板数量']}只")
        print(f"3连板: {daily_data['3连板数量']}只")
        print(f"4连板以上: {daily_data['4连板以上数量']}只")
        
        return True
        
    except Exception as e:
        print(f"✗ 计算失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("开始测试2026年1月20日的情绪数据获取\n")
    
    tests = [
        ("获取完整交易数据", test_daily_data),
        ("获取连板梯队数据", test_consecutive_limit_up),
        ("获取全市场连板梯队", test_market_limit_up_ladder),
        ("获取板块资金数据", test_sector_capital),
        ("获取板块排名数据", test_sector_ranking),
        ("获取百日新高数据", test_new_high_data),
        ("计算情绪指标", calculate_sentiment_indicators),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ 测试失败: {e}")
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
    
    if passed == total:
        print("\n🎉 所有测试通过！2026年1月20日的情绪数据可以正常获取！")
    else:
        print(f"\n⚠️  部分测试失败，请检查失败的项目")
