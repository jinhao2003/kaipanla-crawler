# -*- coding: utf-8 -*-
"""
开盘啦APP数据爬虫包

使用方法：
    from kaipanla_crawler import KaipanlaCrawler
    
    crawler = KaipanlaCrawler()
    
    # 获取市场数据
    df = crawler.get_market_sentiment()
    
    # 获取板块资金数据（实时或历史）
    data = crawler.get_sector_capital_data("801235")  # 实时
    data = crawler.get_sector_capital_data("801235", date="2026-01-19")  # 历史
    
    # 获取N日板块强度排名
    df = crawler.get_sector_strength_ndays("2026-01-20", num_days=7)
    
    # 获取实时连板梯队指数
    index_data = crawler.get_realtime_limit_up_index()
    
    # 获取实时实际涨跌停数据
    limit_data = crawler.get_realtime_actual_limit_up_down()
    
    # 获取指定连板的股票列表（详细数据）
    stocks = crawler.get_realtime_board_stocks(board_type=1)  # 1=首板, 2=二板, 3=三板, 4=四板, 5=五板以上
    
    # 获取所有连板的股票列表
    all_boards = crawler.get_realtime_all_boards_stocks()
    
    # 获取指定连板的数量和列表（简洁接口）
    count, stocks = crawler.get_board_stocks_count_and_list(1)  # 1=首板
"""

from .kaipanla_crawler import KaipanlaCrawler, is_weekend, get_trading_dates

__all__ = [
    "KaipanlaCrawler",
    "is_weekend",
    "get_trading_dates",
]

__version__ = "1.3.0"  # 更新版本号，新增龙虎榜接口功能
