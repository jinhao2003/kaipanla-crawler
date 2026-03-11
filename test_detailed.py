#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细测试 kaipanla_crawler.py 所有接口
- 测试实时接口
- N/A 视为失败
- 详细展示数据结构
"""

import sys
import os
import json
from datetime import datetime, timedelta
import pandas as pd

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.path.insert(0, r'D:\pythonProject2\量化交易1\kaipanla_crawler')

from kaipanla_crawler import KaipanlaCrawler, is_weekend, get_trading_dates

# 检查值是否为有效数据
def is_valid_value(value):
    """检查值是否有效（不是N/A，不是空，不是0）"""
    if value is None:
        return False
    if isinstance(value, str):
        if value in ['N/A', 'None', '', 'null', 'nan']:
            return False
        if 'Name' in value and 'dtype' in value:  # pandas Series字符串
            return False
    if isinstance(value, (int, float)):
        if value == 0 or pd.isna(value):
            return False
    if isinstance(value, pd.DataFrame):
        return len(value) > 0
    if isinstance(value, pd.Series):
        return len(value) > 0 and not all(pd.isna(value))
    if isinstance(value, dict):
        return len(value) > 0
    if isinstance(value, list):
        return len(value) > 0
    return True

# 格式化数据用于展示
def format_data_for_display(data, max_rows=5):
    """格式化数据用于展示"""
    if isinstance(data, pd.DataFrame):
        if len(data) == 0:
            return "空DataFrame"
        columns = list(data.columns)
        preview = data.head(max_rows).to_string()
        return f"列名: {columns}\n数据预览 ({min(max_rows, len(data))}行/{len(data)}行):\n{preview}"
    elif isinstance(data, pd.Series):
        if len(data) == 0:
            return "空Series"
        preview = data.head(max_rows).to_string()
        return f"数据预览 ({min(max_rows, len(data))}行/{len(data)}行):\n{preview}"
    elif isinstance(data, dict):
        result = []
        for k, v in list(data.items())[:20]:  # 最多显示20个键
            if isinstance(v, (pd.DataFrame, pd.Series)):
                result.append(f"  {k}: DataFrame/Series ({len(v)} 行)")
            elif isinstance(v, list):
                result.append(f"  {k}: list ({len(v)} 项)")
            elif isinstance(v, dict):
                result.append(f"  {k}: dict ({len(v)} 键)")
            else:
                result.append(f"  {k}: {v}")
        return "\n".join(result)
    elif isinstance(data, list):
        if len(data) == 0:
            return "空列表"
        result = [f"列表 ({len(data)} 项):"]
        for i, item in enumerate(data[:max_rows]):
            if isinstance(item, dict):
                result.append(f"  [{i}]: {item}")
            else:
                result.append(f"  [{i}]: {item}")
        return "\n".join(result)
    else:
        return str(data)

def run_detailed_test():
    """运行详细测试"""
    results = {
        "测试时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "测试说明": "N/A或空值视为失败，详细展示数据结构",
        "测试结果": []
    }

    test_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    print(f"="*80)
    print(f"详细接口测试")
    print(f"测试日期: {test_date}")
    print(f"="*80)

    crawler = KaipanlaCrawler()

    # ========== 1. 工具函数 ==========
    print("\n" + "="*80)
    print("【1. 工具函数测试】")
    print("="*80)

    # 1.1 is_weekend
    print("\n[1.1] is_weekend() - 判断是否为周末")
    print("-"*60)
    try:
        result = is_weekend(test_date)
        is_valid = isinstance(result, bool)
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"状态: {status}")
        print(f"参数: date_str='{test_date}'")
        print(f"返回: {result}")
        print(f"说明: {'是周末' if result else '不是周末'}")
        results["测试结果"].append({
            "函数": "is_weekend",
            "分类": "工具函数",
            "状态": "成功" if is_valid else "失败",
            "返回值": str(result)
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "is_weekend",
            "分类": "工具函数",
            "状态": "失败",
            "错误": str(e)
        })

    # 1.2 get_trading_dates
    print("\n[1.2] get_trading_dates() - 获取交易日列表")
    print("-"*60)
    try:
        dates = get_trading_dates(start_date, test_date)
        is_valid = len(dates) > 0
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"状态: {status}")
        print(f"参数: start='{start_date}', end='{test_date}'")
        print(f"返回: 共 {len(dates)} 个交易日")
        print(f"交易日列表: {dates}")
        results["测试结果"].append({
            "函数": "get_trading_dates",
            "分类": "工具函数",
            "状态": "成功" if is_valid else "失败",
            "交易日数量": len(dates)
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_trading_dates",
            "分类": "工具函数",
            "状态": "失败",
            "错误": str(e)
        })

    # ========== 2. 历史数据接口 ==========
    print("\n" + "="*80)
    print("【2. 历史数据接口测试】")
    print("="*80)

    # 2.1 get_daily_data 单日
    print("\n[2.1] get_daily_data() - 获取单日交易数据")
    print("-"*60)
    try:
        data = crawler.get_daily_data(end_date=test_date)
        print(f"返回类型: {type(data).__name__}")
        print(f"数据结构:\n{format_data_for_display(data)}")

        # 检查关键字段
        key_fields = ['涨停数', '跌停数', '上涨家数', '下跌家数']
        valid_fields = [f for f in key_fields if is_valid_value(data.get(f))]
        is_valid = len(valid_fields) >= 2  # 至少2个有效字段

        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")
        print(f"有效字段: {valid_fields}")

        results["测试结果"].append({
            "函数": "get_daily_data(单日)",
            "分类": "历史数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "Series",
            "涨停数": str(data.get('涨停数', 'N/A')),
            "跌停数": str(data.get('跌停数', 'N/A'))
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_daily_data(单日)",
            "分类": "历史数据",
            "状态": "失败",
            "错误": str(e)
        })

    # 2.2 get_daily_data 区间
    print("\n[2.2] get_daily_data() - 获取区间交易数据")
    print("-"*60)
    try:
        df = crawler.get_daily_data(start_date=start_date, end_date=test_date)
        print(f"返回类型: {type(df).__name__}")
        print(f"数据结构:\n{format_data_for_display(df)}")

        is_valid = len(df) > 0 and '涨停数' in df.columns
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")

        results["测试结果"].append({
            "函数": "get_daily_data(区间)",
            "分类": "历史数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "DataFrame",
            "行数": len(df),
            "列数": len(df.columns) if len(df) > 0 else 0
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_daily_data(区间)",
            "分类": "历史数据",
            "状态": "失败",
            "错误": str(e)
        })

    # 2.3 get_market_sentiment
    print("\n[2.3] get_market_sentiment() - 获取市场情绪数据")
    print("-"*60)
    try:
        df = crawler.get_market_sentiment(date=test_date)
        print(f"返回类型: {type(df).__name__}")
        print(f"数据结构:\n{format_data_for_display(df)}")

        is_valid = len(df) > 0 and '涨停数' in df.columns and df['涨停数'].iloc[0] > 0
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")

        results["测试结果"].append({
            "函数": "get_market_sentiment",
            "分类": "历史数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "DataFrame",
            "涨停数": int(df['涨停数'].iloc[0]) if len(df) > 0 and '涨停数' in df.columns else 'N/A'
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_market_sentiment",
            "分类": "历史数据",
            "状态": "失败",
            "错误": str(e)
        })

    # 2.4 get_market_index
    print("\n[2.4] get_market_index() - 获取大盘指数数据")
    print("-"*60)
    try:
        df = crawler.get_market_index(date=test_date)
        print(f"返回类型: {type(df).__name__}")
        print(f"数据结构:\n{format_data_for_display(df)}")

        is_valid = len(df) > 0 and '最新价' in df.columns
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")

        results["测试结果"].append({
            "函数": "get_market_index",
            "分类": "历史数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "DataFrame",
            "指数数量": len(df)
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_market_index",
            "分类": "历史数据",
            "状态": "失败",
            "错误": str(e)
        })

    # 2.5 get_limit_up_ladder
    print("\n[2.5] get_limit_up_ladder() - 获取连板梯队数据")
    print("-"*60)
    try:
        df = crawler.get_limit_up_ladder(date=test_date)
        print(f"返回类型: {type(df).__name__}")
        print(f"数据结构:\n{format_data_for_display(df)}")

        is_valid = len(df) > 0
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")

        results["测试结果"].append({
            "函数": "get_limit_up_ladder",
            "分类": "历史数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "DataFrame",
            "行数": len(df)
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_limit_up_ladder",
            "分类": "历史数据",
            "状态": "失败",
            "错误": str(e)
        })

    # 2.6 get_sharp_withdrawal
    print("\n[2.6] get_sharp_withdrawal() - 获取大幅回撤数据")
    print("-"*60)
    try:
        df = crawler.get_sharp_withdrawal(date=test_date)
        print(f"返回类型: {type(df).__name__}")
        print(f"数据结构:\n{format_data_for_display(df)}")

        is_valid = len(df) > 0
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")

        results["测试结果"].append({
            "函数": "get_sharp_withdrawal",
            "分类": "历史数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "DataFrame",
            "行数": len(df)
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_sharp_withdrawal",
            "分类": "历史数据",
            "状态": "失败",
            "错误": str(e)
        })

    # ========== 3. 板块数据接口 ==========
    print("\n" + "="*80)
    print("【3. 板块数据接口测试】")
    print("="*80)

    # 3.1 get_sector_ranking
    print("\n[3.1] get_sector_ranking() - 获取涨停原因板块排名")
    print("-"*60)
    try:
        df = crawler.get_sector_ranking(date=test_date, index=0)
        print(f"返回类型: {type(df).__name__}")
        print(f"数据结构:\n{format_data_for_display(df)}")

        is_valid = len(df) > 0
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")

        results["测试结果"].append({
            "函数": "get_sector_ranking",
            "分类": "板块数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "DataFrame",
            "行数": len(df)
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_sector_ranking",
            "分类": "板块数据",
            "状态": "失败",
            "错误": str(e)
        })

    # 3.2 get_consecutive_limit_up
    print("\n[3.2] get_consecutive_limit_up() - 获取连板个股数据")
    print("-"*60)
    try:
        df = crawler.get_consecutive_limit_up(date=test_date)
        print(f"返回类型: {type(df).__name__}")
        print(f"数据结构:\n{format_data_for_display(df)}")

        is_valid = len(df) > 0
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")

        results["测试结果"].append({
            "函数": "get_consecutive_limit_up",
            "分类": "板块数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "DataFrame",
            "行数": len(df)
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_consecutive_limit_up",
            "分类": "板块数据",
            "状态": "失败",
            "错误": str(e)
        })

    # 3.3 get_sector_strength
    print("\n[3.3] get_sector_strength() - 获取板块强度")
    print("-"*60)
    try:
        data = crawler.get_sector_strength(sector_code="801900", date=test_date)
        print(f"返回类型: {type(data).__name__}")
        print(f"数据结构:\n{format_data_for_display(data)}")

        is_valid = isinstance(data, dict) and len(data) > 0 and is_valid_value(data.get('强度'))
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")

        results["测试结果"].append({
            "函数": "get_sector_strength",
            "分类": "板块数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "dict",
            "强度": data.get('强度', 'N/A') if isinstance(data, dict) else 'N/A'
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_sector_strength",
            "分类": "板块数据",
            "状态": "失败",
            "错误": str(e)
        })

    # ========== 4. 实时数据接口 ==========
    print("\n" + "="*80)
    print("【4. 实时数据接口测试】")
    print("="*80)

    # 4.1 get_realtime_market_mood
    print("\n[4.1] get_realtime_market_mood() - 获取实时市场情绪")
    print("-"*60)
    try:
        data = crawler.get_realtime_market_mood()
        print(f"返回类型: {type(data).__name__}")
        print(f"数据结构:\n{format_data_for_display(data)}")

        is_valid = isinstance(data, dict) and len(data) > 0 and is_valid_value(data.get('涨停家数'))
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")

        results["测试结果"].append({
            "函数": "get_realtime_market_mood",
            "分类": "实时数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "dict",
            "涨停家数": data.get('涨停家数', 'N/A') if isinstance(data, dict) else 'N/A',
            "跌停家数": data.get('跌停家数', 'N/A') if isinstance(data, dict) else 'N/A'
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_realtime_market_mood",
            "分类": "实时数据",
            "状态": "失败",
            "错误": str(e)
        })

    # 4.2 get_realtime_actual_limit_up_down
    print("\n[4.2] get_realtime_actual_limit_up_down() - 获取实时实际涨跌停")
    print("-"*60)
    try:
        data = crawler.get_realtime_actual_limit_up_down()
        print(f"返回类型: {type(data).__name__}")
        print(f"数据结构:\n{format_data_for_display(data)}")

        is_valid = isinstance(data, dict) and len(data) > 0 and is_valid_value(data.get('actual_limit_up'))
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")

        results["测试结果"].append({
            "函数": "get_realtime_actual_limit_up_down",
            "分类": "实时数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "dict",
            "实际涨停": data.get('actual_limit_up', 'N/A') if isinstance(data, dict) else 'N/A'
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_realtime_actual_limit_up_down",
            "分类": "实时数据",
            "状态": "失败",
            "错误": str(e)
        })

    # 4.3 get_realtime_board_stocks
    print("\n[4.3] get_realtime_board_stocks() - 获取实时板块个股")
    print("-"*60)
    try:
        df = crawler.get_realtime_board_stocks(board_type=1)
        print(f"返回类型: {type(df).__name__}")
        print(f"数据结构:\n{format_data_for_display(df)}")

        is_valid = len(df) > 0
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")

        results["测试结果"].append({
            "函数": "get_realtime_board_stocks",
            "分类": "实时数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "DataFrame",
            "行数": len(df)
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_realtime_board_stocks",
            "分类": "实时数据",
            "状态": "失败",
            "错误": str(e)
        })

    # 4.4 get_realtime_index_list
    print("\n[4.4] get_realtime_index_list() - 获取实时指数列表")
    print("-"*60)
    try:
        data = crawler.get_realtime_index_list()
        print(f"返回类型: {type(data).__name__}")
        print(f"数据结构:\n{format_data_for_display(data)}")

        is_valid = isinstance(data, dict) and 'indexes' in data and len(data['indexes']) > 0
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")

        results["测试结果"].append({
            "函数": "get_realtime_index_list",
            "分类": "实时数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "dict",
            "指数数量": len(data.get('indexes', [])) if isinstance(data, dict) else 0
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_realtime_index_list",
            "分类": "实时数据",
            "状态": "失败",
            "错误": str(e)
        })

    # 4.5 get_realtime_sharp_withdrawal
    print("\n[4.5] get_realtime_sharp_withdrawal() - 获取实时大幅回撤")
    print("-"*60)
    try:
        df = crawler.get_realtime_sharp_withdrawal()
        print(f"返回类型: {type(df).__name__}")
        print(f"数据结构:\n{format_data_for_display(df)}")

        is_valid = len(df) > 0
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")

        results["测试结果"].append({
            "函数": "get_realtime_sharp_withdrawal",
            "分类": "实时数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "DataFrame",
            "行数": len(df)
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_realtime_sharp_withdrawal",
            "分类": "实时数据",
            "状态": "失败",
            "错误": str(e)
        })

    # 4.6 get_realtime_index_trend
    print("\n[4.6] get_realtime_index_trend() - 获取实时指数趋势")
    print("-"*60)
    try:
        data = crawler.get_realtime_index_trend(stock_id="801900")
        print(f"返回类型: {type(data).__name__}")
        print(f"数据结构:\n{format_data_for_display(data)}")

        is_valid = isinstance(data, dict) and len(data) > 0 and is_valid_value(data.get('change_pct'))
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")

        results["测试结果"].append({
            "函数": "get_realtime_index_trend",
            "分类": "实时数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "dict",
            "涨跌幅": data.get('change_pct', 'N/A') if isinstance(data, dict) else 'N/A'
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_realtime_index_trend",
            "分类": "实时数据",
            "状态": "失败",
            "错误": str(e)
        })

    # ========== 5. 龙虎榜数据接口 ==========
    print("\n" + "="*80)
    print("【5. 龙虎榜数据接口测试】")
    print("="*80)

    # 5.1 get_longhubang_stock_list
    print("\n[5.1] get_longhubang_stock_list() - 获取龙虎榜股票列表")
    print("-"*60)
    try:
        df = crawler.get_longhubang_stock_list(date=test_date)
        print(f"返回类型: {type(df).__name__}")
        print(f"数据结构:\n{format_data_for_display(df)}")

        is_valid = len(df) > 0
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")

        results["测试结果"].append({
            "函数": "get_longhubang_stock_list",
            "分类": "龙虎榜数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "DataFrame",
            "行数": len(df)
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_longhubang_stock_list",
            "分类": "龙虎榜数据",
            "状态": "失败",
            "错误": str(e)
        })

    # 5.2 get_longhubang_dataframe
    print("\n[5.2] get_longhubang_dataframe() - 获取完整龙虎榜数据")
    print("-"*60)
    try:
        df = crawler.get_longhubang_dataframe(date=test_date)
        print(f"返回类型: {type(df).__name__}")
        print(f"数据结构:\n{format_data_for_display(df)}")

        is_valid = len(df) > 0
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")

        results["测试结果"].append({
            "函数": "get_longhubang_dataframe",
            "分类": "龙虎榜数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "DataFrame",
            "行数": len(df)
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_longhubang_dataframe",
            "分类": "龙虎榜数据",
            "状态": "失败",
            "错误": str(e)
        })

    # ========== 6. ETF数据接口 ==========
    print("\n" + "="*80)
    print("【6. ETF数据接口测试】")
    print("="*80)

    # 6.1 get_etf_ranking
    print("\n[6.1] get_etf_ranking() - 获取ETF排名")
    print("-"*60)
    try:
        df = crawler.get_etf_ranking(date=test_date)
        print(f"返回类型: {type(df).__name__}")
        print(f"数据结构:\n{format_data_for_display(df)}")

        is_valid = len(df) > 0
        status = "✅ 成功" if is_valid else "❌ 失败(数据无效)"
        print(f"\n状态: {status}")

        results["测试结果"].append({
            "函数": "get_etf_ranking",
            "分类": "ETF数据",
            "状态": "成功" if is_valid else "失败",
            "数据类型": "DataFrame",
            "行数": len(df)
        })
    except Exception as e:
        print(f"状态: ❌ 失败")
        print(f"错误: {e}")
        results["测试结果"].append({
            "函数": "get_etf_ranking",
            "分类": "ETF数据",
            "状态": "失败",
            "错误": str(e)
        })

    # ========== 统计 ==========
    print("\n" + "="*80)
    print("【测试统计】")
    print("="*80)

    total = len(results["测试结果"])
    success = sum(1 for r in results["测试结果"] if r["状态"] == "成功")
    failed = total - success

    print(f"\n总计: {total} 个接口")
    print(f"✅ 成功: {success}")
    print(f"❌ 失败: {failed}")
    print(f"成功率: {success/total*100:.1f}%")

    # 按分类统计
    categories = {}
    for r in results["测试结果"]:
        cat = r["分类"]
        if cat not in categories:
            categories[cat] = {"total": 0, "success": 0}
        categories[cat]["total"] += 1
        if r["状态"] == "成功":
            categories[cat]["success"] += 1

    print("\n按分类统计:")
    for cat, stats in categories.items():
        print(f"  {cat}: {stats['success']}/{stats['total']} 成功")

    results["统计"] = {
        "总计": total,
        "成功": success,
        "失败": failed,
        "成功率": f"{success/total*100:.1f}%",
        "分类统计": categories
    }

    return results

if __name__ == "__main__":
    results = run_detailed_test()

    # 保存结果
    output_dir = r"D:\pythonProject2\量化交易1\kaipanla_crawler"
    json_path = os.path.join(output_dir, "detailed_test_results.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n详细结果已保存到: {json_path}")
