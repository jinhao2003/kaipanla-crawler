#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 kaipanla_crawler.py 所有函数接口
生成测试结果报告
"""

import sys
import os
from datetime import datetime, timedelta
import json

# 设置环境变量避免编码问题
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 添加爬虫路径
sys.path.insert(0, r'D:\pythonProject2\量化交易1\kaipanla_crawler')

from kaipanla_crawler import KaipanlaCrawler, is_weekend, get_trading_dates

# 状态标记
OK = "[OK]"
FAIL = "[FAIL]"

def test_all_functions():
    """测试所有函数接口"""
    results = {
        "测试时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "测试日期": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "函数测试结果": []
    }

    # 获取测试日期（最近交易日）
    test_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    # 获取前5个交易日作为范围测试
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = test_date

    print(f"测试日期: {test_date}")
    print(f"测试区间: {start_date} ~ {end_date}")
    print("="*80)

    # 初始化爬虫
    crawler = KaipanlaCrawler()

    # ========== 工具函数测试 ==========
    print("\n[1. 测试工具函数]")

    # 1. is_weekend
    try:
        result = is_weekend(test_date)
        results["函数测试结果"].append({
            "函数名": "is_weekend",
            "描述": "判断是否为周末",
            "参数": f"date_str='{test_date}'",
            "状态": f"{OK} 成功",
            "返回值": str(result)
        })
        print(f"  {OK} is_weekend('{test_date}') = {result}")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "is_weekend",
            "描述": "判断是否为周末",
            "参数": f"date_str='{test_date}'",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} is_weekend 失败: {e}")

    # 2. get_trading_dates
    try:
        dates = get_trading_dates(start_date, end_date)
        results["函数测试结果"].append({
            "函数名": "get_trading_dates",
            "描述": "获取交易日列表",
            "参数": f"start='{start_date}', end='{end_date}'",
            "状态": f"{OK} 成功",
            "返回值": f"共 {len(dates)} 个交易日"
        })
        print(f"  {OK} get_trading_dates 获取到 {len(dates)} 个交易日")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_trading_dates",
            "描述": "获取交易日列表",
            "参数": f"start='{start_date}', end='{end_date}'",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_trading_dates 失败: {e}")

    # ========== 基础数据接口测试 ==========
    print("\n[2. 测试基础数据接口]")

    # 3. get_daily_data - 单日
    try:
        data = crawler.get_daily_data(end_date=test_date)
        results["函数测试结果"].append({
            "函数名": "get_daily_data (单日)",
            "描述": "获取单日交易数据",
            "参数": f"end_date='{test_date}'",
            "状态": f"{OK} 成功",
            "返回值": f"涨停数={data.get('涨停数', 'N/A')}, 跌停数={data.get('跌停数', 'N/A')}"
        })
        print(f"  {OK} get_daily_data(单日) 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_daily_data (单日)",
            "描述": "获取单日交易数据",
            "参数": f"end_date='{test_date}'",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_daily_data(单日) 失败: {e}")

    # 4. get_daily_data - 区间
    try:
        df = crawler.get_daily_data(start_date=start_date, end_date=end_date)
        row_count = len(df) if hasattr(df, '__len__') else 'N/A'
        results["函数测试结果"].append({
            "函数名": "get_daily_data (区间)",
            "描述": "获取日期范围交易数据",
            "参数": f"start='{start_date}', end='{end_date}'",
            "状态": f"{OK} 成功",
            "返回值": f"DataFrame 共 {row_count} 行"
        })
        print(f"  {OK} get_daily_data(区间) 成功，获取 {row_count} 条数据")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_daily_data (区间)",
            "描述": "获取日期范围交易数据",
            "参数": f"start='{start_date}', end='{end_date}'",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_daily_data(区间) 失败: {e}")

    # 5. get_new_high_data
    try:
        df = crawler.get_new_high_data(end_date=test_date)
        row_count = len(df) if hasattr(df, '__len__') else 'N/A'
        results["函数测试结果"].append({
            "函数名": "get_new_high_data",
            "描述": "获取百日新高数据",
            "参数": f"end_date='{test_date}'",
            "状态": f"{OK} 成功",
            "返回值": f"DataFrame 共 {row_count} 行"
        })
        print(f"  {OK} get_new_high_data 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_new_high_data",
            "描述": "获取百日新高数据",
            "参数": f"end_date='{test_date}'",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_new_high_data 失败: {e}")

    # ========== 市场情绪接口测试 ==========
    print("\n[3. 测试市场情绪接口]")

    # 6. get_market_sentiment
    try:
        data = crawler.get_market_sentiment(date=test_date)
        results["函数测试结果"].append({
            "函数名": "get_market_sentiment",
            "描述": "获取市场情绪数据",
            "参数": f"date='{test_date}'",
            "状态": f"{OK} 成功",
            "返回值": f"涨停{data.get('涨停数', 'N/A')}, 跌停{data.get('跌停数', 'N/A')}"
        })
        print(f"  {OK} get_market_sentiment 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_market_sentiment",
            "描述": "获取市场情绪数据",
            "参数": f"date='{test_date}'",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_market_sentiment 失败: {e}")

    # 7. get_market_index
    try:
        data = crawler.get_market_index(date=test_date)
        results["函数测试结果"].append({
            "函数名": "get_market_index",
            "描述": "获取大盘指数数据",
            "参数": f"date='{test_date}'",
            "状态": f"{OK} 成功",
            "返回值": f"上证指数={data.get('last_px', 'N/A')}"
        })
        print(f"  {OK} get_market_index 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_market_index",
            "描述": "获取大盘指数数据",
            "参数": f"date='{test_date}'",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_market_index 失败: {e}")

    # 8. get_limit_up_ladder
    try:
        data = crawler.get_limit_up_ladder(date=test_date)
        results["函数测试结果"].append({
            "函数名": "get_limit_up_ladder",
            "描述": "获取连板梯队数据",
            "参数": f"date='{test_date}'",
            "状态": f"{OK} 成功",
            "返回值": f"首板{data.get('首板数量', 'N/A')}, 2连板{data.get('2连板数量', 'N/A')}"
        })
        print(f"  {OK} get_limit_up_ladder 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_limit_up_ladder",
            "描述": "获取连板梯队数据",
            "参数": f"date='{test_date}'",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_limit_up_ladder 失败: {e}")

    # 9. get_sharp_withdrawal
    try:
        data = crawler.get_sharp_withdrawal(date=test_date)
        results["函数测试结果"].append({
            "函数名": "get_sharp_withdrawal",
            "描述": "获取大幅回撤数据",
            "参数": f"date='{test_date}'",
            "状态": f"{OK} 成功",
            "返回值": f"大幅回撤家数={data.get('大幅回撤家数', 'N/A')}"
        })
        print(f"  {OK} get_sharp_withdrawal 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_sharp_withdrawal",
            "描述": "获取大幅回撤数据",
            "参数": f"date='{test_date}'",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_sharp_withdrawal 失败: {e}")

    # ========== 板块数据接口测试 ==========
    print("\n[4. 测试板块数据接口]")

    # 10. get_sector_ranking
    try:
        df = crawler.get_sector_ranking(date=test_date, index=0)
        row_count = len(df) if hasattr(df, '__len__') else 'N/A'
        results["函数测试结果"].append({
            "函数名": "get_sector_ranking",
            "描述": "获取涨停原因板块排名",
            "参数": f"date='{test_date}', index=0",
            "状态": f"{OK} 成功",
            "返回值": f"DataFrame 共 {row_count} 行"
        })
        print(f"  {OK} get_sector_ranking 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_sector_ranking",
            "描述": "获取涨停原因板块排名",
            "参数": f"date='{test_date}', index=0",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_sector_ranking 失败: {e}")

    # 11. get_consecutive_limit_up
    try:
        df = crawler.get_consecutive_limit_up(date=test_date)
        row_count = len(df) if hasattr(df, '__len__') else 'N/A'
        results["函数测试结果"].append({
            "函数名": "get_consecutive_limit_up",
            "描述": "获取连板个股数据",
            "参数": f"date='{test_date}'",
            "状态": f"{OK} 成功",
            "返回值": f"DataFrame 共 {row_count} 行"
        })
        print(f"  {OK} get_consecutive_limit_up 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_consecutive_limit_up",
            "描述": "获取连板个股数据",
            "参数": f"date='{test_date}'",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_consecutive_limit_up 失败: {e}")

    # 12. get_sector_limit_up_ladder
    try:
        df = crawler.get_sector_limit_up_ladder(date=test_date)
        row_count = len(df) if hasattr(df, '__len__') else 'N/A'
        results["函数测试结果"].append({
            "函数名": "get_sector_limit_up_ladder",
            "描述": "获取板块涨停梯队",
            "参数": f"date='{test_date}'",
            "状态": f"{OK} 成功",
            "返回值": f"DataFrame 共 {row_count} 行"
        })
        print(f"  {OK} get_sector_limit_up_ladder 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_sector_limit_up_ladder",
            "描述": "获取板块涨停梯队",
            "参数": f"date='{test_date}'",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_sector_limit_up_ladder 失败: {e}")

    # 13. get_market_limit_up_ladder
    try:
        df = crawler.get_market_limit_up_ladder(date=test_date)
        row_count = len(df) if hasattr(df, '__len__') else 'N/A'
        results["函数测试结果"].append({
            "函数名": "get_market_limit_up_ladder",
            "描述": "获取市场涨停梯队",
            "参数": f"date='{test_date}'",
            "状态": f"{OK} 成功",
            "返回值": f"DataFrame 共 {row_count} 行"
        })
        print(f"  {OK} get_market_limit_up_ladder 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_market_limit_up_ladder",
            "描述": "获取市场涨停梯队",
            "参数": f"date='{test_date}'",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_market_limit_up_ladder 失败: {e}")

    # 14. get_sector_strength
    try:
        # 使用一个常见的板块代码测试
        data = crawler.get_sector_strength(sector_code="801900", date=test_date)
        results["函数测试结果"].append({
            "函数名": "get_sector_strength",
            "描述": "获取板块强度",
            "参数": f"sector_code='801900', date='{test_date}'",
            "状态": f"{OK} 成功",
            "返回值": f"强度={data.get('强度', 'N/A')}"
        })
        print(f"  {OK} get_sector_strength 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_sector_strength",
            "描述": "获取板块强度",
            "参数": f"sector_code='801900', date='{test_date}'",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_sector_strength 失败: {e}")

    # ========== 实时数据接口测试 ==========
    print("\n[5. 测试实时数据接口]")

    # 15. get_realtime_market_mood
    try:
        data = crawler.get_realtime_market_mood()
        results["函数测试结果"].append({
            "函数名": "get_realtime_market_mood",
            "描述": "获取实时市场情绪",
            "参数": "无",
            "状态": f"{OK} 成功",
            "返回值": f"涨停{data.get('涨停数', 'N/A')}, 跌停{data.get('跌停数', 'N/A')}"
        })
        print(f"  {OK} get_realtime_market_mood 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_realtime_market_mood",
            "描述": "获取实时市场情绪",
            "参数": "无",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_realtime_market_mood 失败: {e}")

    # 16. get_realtime_actual_limit_up_down
    try:
        data = crawler.get_realtime_actual_limit_up_down()
        results["函数测试结果"].append({
            "函数名": "get_realtime_actual_limit_up_down",
            "描述": "获取实时实际涨跌停",
            "参数": "无",
            "状态": f"{OK} 成功",
            "返回值": f"实际涨停{data.get('实际涨停', 'N/A')}, 实际跌停{data.get('实际跌停', 'N/A')}"
        })
        print(f"  {OK} get_realtime_actual_limit_up_down 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_realtime_actual_limit_up_down",
            "描述": "获取实时实际涨跌停",
            "参数": "无",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_realtime_actual_limit_up_down 失败: {e}")

    # 17. get_realtime_board_stocks
    try:
        df = crawler.get_realtime_board_stocks(board_type=1)
        row_count = len(df) if hasattr(df, '__len__') else 'N/A'
        results["函数测试结果"].append({
            "函数名": "get_realtime_board_stocks",
            "描述": "获取实时板块个股",
            "参数": "board_type=1 (首板)",
            "状态": f"{OK} 成功",
            "返回值": f"DataFrame 共 {row_count} 行"
        })
        print(f"  {OK} get_realtime_board_stocks 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_realtime_board_stocks",
            "描述": "获取实时板块个股",
            "参数": "board_type=1",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_realtime_board_stocks 失败: {e}")

    # 18. get_realtime_index_list
    try:
        data = crawler.get_realtime_index_list()
        results["函数测试结果"].append({
            "函数名": "get_realtime_index_list",
            "描述": "获取实时指数列表",
            "参数": "无",
            "状态": f"{OK} 成功",
            "返回值": f"获取到 {len(data)} 个指数"
        })
        print(f"  {OK} get_realtime_index_list 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_realtime_index_list",
            "描述": "获取实时指数列表",
            "参数": "无",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_realtime_index_list 失败: {e}")

    # 19. get_realtime_sharp_withdrawal
    try:
        df = crawler.get_realtime_sharp_withdrawal()
        row_count = len(df) if hasattr(df, '__len__') else 'N/A'
        results["函数测试结果"].append({
            "函数名": "get_realtime_sharp_withdrawal",
            "描述": "获取实时大幅回撤",
            "参数": "无",
            "状态": f"{OK} 成功",
            "返回值": f"DataFrame 共 {row_count} 行"
        })
        print(f"  {OK} get_realtime_sharp_withdrawal 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_realtime_sharp_withdrawal",
            "描述": "获取实时大幅回撤",
            "参数": "无",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_realtime_sharp_withdrawal 失败: {e}")

    # ========== 龙虎榜数据接口测试 ==========
    print("\n[6. 测试龙虎榜数据接口]")

    # 20. get_longhubang_stock_list
    try:
        df = crawler.get_longhubang_stock_list(date=test_date)
        row_count = len(df) if hasattr(df, '__len__') else 'N/A'
        results["函数测试结果"].append({
            "函数名": "get_longhubang_stock_list",
            "描述": "获取龙虎榜股票列表",
            "参数": f"date='{test_date}'",
            "状态": f"{OK} 成功",
            "返回值": f"DataFrame 共 {row_count} 行"
        })
        print(f"  {OK} get_longhubang_stock_list 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_longhubang_stock_list",
            "描述": "获取龙虎榜股票列表",
            "参数": f"date='{test_date}'",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_longhubang_stock_list 失败: {e}")

    # 21. get_longhubang_dataframe
    try:
        df = crawler.get_longhubang_dataframe(date=test_date)
        row_count = len(df) if hasattr(df, '__len__') else 'N/A'
        results["函数测试结果"].append({
            "函数名": "get_longhubang_dataframe",
            "描述": "获取完整龙虎榜数据",
            "参数": f"date='{test_date}'",
            "状态": f"{OK} 成功",
            "返回值": f"DataFrame 共 {row_count} 行"
        })
        print(f"  {OK} get_longhubang_dataframe 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_longhubang_dataframe",
            "描述": "获取完整龙虎榜数据",
            "参数": f"date='{test_date}'",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_longhubang_dataframe 失败: {e}")

    # ========== ETF数据接口测试 ==========
    print("\n[7. 测试ETF数据接口]")

    # 22. get_etf_ranking
    try:
        df = crawler.get_etf_ranking(date=test_date)
        row_count = len(df) if hasattr(df, '__len__') else 'N/A'
        results["函数测试结果"].append({
            "函数名": "get_etf_ranking",
            "描述": "获取ETF排名",
            "参数": f"date='{test_date}'",
            "状态": f"{OK} 成功",
            "返回值": f"DataFrame 共 {row_count} 行"
        })
        print(f"  {OK} get_etf_ranking 成功")
    except Exception as e:
        results["函数测试结果"].append({
            "函数名": "get_etf_ranking",
            "描述": "获取ETF排名",
            "参数": f"date='{test_date}'",
            "状态": f"{FAIL} 失败: {str(e)}",
            "返回值": "-"
        })
        print(f"  {FAIL} get_etf_ranking 失败: {e}")

    # ========== 统计 ==========
    print("\n" + "="*80)
    total = len(results["函数测试结果"])
    success = sum(1 for r in results["函数测试结果"] if OK in r["状态"])
    failed = total - success

    results["统计"] = {
        "总测试数": total,
        "成功": success,
        "失败": failed,
        "成功率": f"{success/total*100:.1f}%"
    }

    print(f"\n测试完成: 总计 {total} 个函数")
    print(f"  {OK} 成功: {success}")
    print(f"  {FAIL} 失败: {failed}")
    print(f"  成功率: {success/total*100:.1f}%")

    return results

if __name__ == "__main__":
    results = test_all_functions()

    # 保存JSON结果
    output_dir = r"D:\pythonProject2\量化交易1\kaipanla_crawler"
    json_path = os.path.join(output_dir, "test_results.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n详细结果已保存到: {json_path}")
