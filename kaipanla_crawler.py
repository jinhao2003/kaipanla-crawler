# -*- coding: utf-8 -*-
"""
开盘啦APP数据爬虫

主要功能：
- get_daily_data(end_date, start_date=None): 获取指定日期范围的交易数据
  - 只传end_date: 返回单日Series
  - 传start_date和end_date: 返回日期范围DataFrame
- get_new_high_data(end_date, start_date=None): 获取百日新高数据
- get_sector_intraday(sector_code, date=None): 获取板块分时数据
- get_stock_intraday(stock_code, date=None): 获取个股分时数据
- get_abnormal_stocks(): 获取异动个股数据（实时）

- get_sector_ranking(date, index): 获取涨停原因板块数据
- get_sector_strength(sector_code, date=None): 获取板块强度数据（直接返回强度值，支持历史数据）
- get_multiple_sectors_strength(sector_codes, date=None): 批量获取多个板块的强度数据
- get_sector_strength_history(sector_code, start_date, end_date): 获取板块强度历史数据（指定日期范围）
- get_sector_strength_dataframe(sector_code, start_date, end_date): 获取板块强度历史数据并返回DataFrame格式
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import uuid
import urllib3
import time  # 添加time模块用于sleep延迟

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def is_weekend(date_str):
    """
    判断给定日期是否为周末
    
    Args:
        date_str: 日期字符串，格式YYYY-MM-DD
        
    Returns:
        bool: True表示是周末，False表示不是周末
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        # weekday(): 0=周一, 1=周二, ..., 5=周六, 6=周日
        return date_obj.weekday() >= 5  # 5=周六, 6=周日
    except:
        return False


def get_trading_dates(start_date, end_date):
    """
    获取指定日期范围内的所有交易日（排除周末）
    
    Args:
        start_date: 开始日期，格式YYYY-MM-DD
        end_date: 结束日期，格式YYYY-MM-DD
        
    Returns:
        list: 交易日列表
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    if start > end:
        start, end = end, start
    
    trading_dates = []
    current = start
    
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        # 排除周末
        if not is_weekend(date_str):
            trading_dates.append(date_str)
        current += timedelta(days=1)
    
    return trading_dates


class KaipanlaCrawler:
    """开盘啦数据爬虫"""
    
    def __init__(self):
        self.base_url = "https://apphis.longhuvip.com/w1/api/index.php"
        self.sector_base_url = "https://apphwhq.longhuvip.com/w1/api/index.php"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SHARK PRS-A0 Build/PQ3A.190605.01141736)",
            "Host": "apphis.longhuvip.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        self.sector_headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SHARK PRS-A0 Build/PQ3A.190605.01141736)",
            "Host": "apphwhq.longhuvip.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
    
    def _request(self, data_params, date, timeout=None):
        """发送POST请求
        
        Args:
            data_params: 请求参数
            date: 日期
            timeout: 超时时间（秒），默认1600秒
        """
        params = {"apiv": "w42", "PhoneOSNew": "1", "VerSion": "5.21.0.2"}
        data = {
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "apiv": "w42",
            "Day": date
        }
        data.update(data_params)
        
        try:
            response = requests.post(
                self.base_url,
                params=params,
                data=data,
                headers=self.headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout  # 使用参数化的超时时间
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"请求失败 ({date}): {e}")
            return {}
    
    def _get_single_day_data(self, date):
        """
        获取单日完整数据
        
        Returns:
            dict: 包含所有字段的字典
        """
        # 1. 获取涨跌统计数据
        result1 = self._request({"a": "HisZhangFuDetail", "c": "HisHomeDingPan"}, date)
        info1 = result1.get("info", {}) if result1 else {}
        
        # 2. 获取大盘指数数据
        result2 = self._request({"a": "GetZsReal", "c": "StockL2History"}, date)
        stock_list = result2.get("StockList", []) if result2 else []
        
        # 提取上证指数数据
        sh_index = None
        for stock in stock_list:
            if stock.get("StockID") == "SH000001":
                sh_index = stock
                break
        
        # 3. 获取连板梯队数据
        result3 = self._request({"a": "ZhangTingExpression", "c": "HisHomeDingPan"}, date)
        info3 = result3.get("info", []) if result3 else []
        
        # 4. 获取大幅回撤数据
        result4 = self._request({"a": "SharpWithdrawal", "c": "HisHomeDingPan"}, date)
        withdrawal_num = result4.get("num", 0) if result4 else 0
        
        # 整合数据
        data = {
            "日期": result1.get("date", date) if result1 else date,
            "涨停数": int(info1.get("ZT", 0)),
            "实际涨停": int(info1.get("SJZT", 0)),
            "跌停数": int(info1.get("DT", 0)),
            "实际跌停": int(info1.get("SJDT", 0)),
            "上涨家数": int(info1.get("SZJS", 0)),
            "下跌家数": int(info1.get("XDJS", 0)),
            "平盘家数": int(info1.get("0", 0)),
            "上证指数": float(sh_index.get("last_px", 0)) if sh_index else 0,
            "最新价": float(sh_index.get("last_px", 0)) if sh_index else 0,
            "涨跌幅": sh_index.get("increase_rate", "") if sh_index else "",
            "成交额": int(sh_index.get("turnover", 0)) if sh_index else 0,
            "首板数量": info3[0] if len(info3) > 0 else 0,
            "2连板数量": info3[1] if len(info3) > 1 else 0,
            "3连板数量": info3[2] if len(info3) > 2 else 0,
            "4连板以上数量": info3[3] if len(info3) > 3 else 0,
            "连板率": round(info3[4], 2) if len(info3) > 4 else 0,
            "大幅回撤家数": withdrawal_num,
        }
        
        return data
    
    def get_daily_data(self, end_date, start_date=None):
        """
        获取交易日数据
        
        Args:
            end_date: 结束日期，格式YYYY-MM-DD
            start_date: 起始日期，格式YYYY-MM-DD，可选
            
        Returns:
            - 只传end_date: 返回Series（单日数据）
            - 传start_date和end_date: 返回DataFrame（日期范围数据）
        
        示例:
            # 获取单日数据
            data = crawler.get_daily_data("2026-01-16")
            
            # 获取日期范围数据
            df = crawler.get_daily_data("2026-01-16", "2026-01-10")
        """
        # 只传结束日期，返回单日Series
        if start_date is None:
            data = self._get_single_day_data(end_date)
            return pd.Series(data)
        
        # 传了起始和结束日期，返回DataFrame
        # 使用新的交易日判断函数，排除周末
        date_list = get_trading_dates(start_date, end_date)
        
        print(f"日期范围: {start_date} 到 {end_date}")
        print(f"交易日数量: {len(date_list)} 天（已排除周末）")
        
        # 获取每日数据
        records = []
        for date in date_list:
            print(f"正在获取 {date} 的数据...")
            data = self._get_single_day_data(date)
            records.append(data)
        
        df = pd.DataFrame(records)
        
        # 过滤掉没有数据的日期（节假日）
        df = df[df["涨停数"] > 0]
        
        return df
    
    def get_new_high_data(self, end_date, start_date=None, timeout=None):
        """
        获取百日新高数据
        
        Args:
            end_date: 结束日期，格式YYYY-MM-DD
            start_date: 起始日期，格式YYYY-MM-DD，可选
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            pd.Series: 索引为日期，值为今日新增新高数量
            
        示例:
            crawler = KaipanlaCrawler()
            # 获取单日数据
            data = crawler.get_new_high_data("2026-01-16")
            print(data)  # 2026-01-16    127
            
            # 获取日期范围数据
            data = crawler.get_new_high_data("2026-01-16", "2026-01-10")
            print(data)
        """
        # 构造请求参数
        data = {
            "a": "GetDayNewHigh_W28",
            "st": "360",
            "c": "StockNewHigh",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "Index": "0",
            "GroupID": "ALL",
            "apiv": "w42",
            "Type": "0_0_0_0_0"
        }
        
        try:
            response = requests.post(
                self.base_url,
                data=data,
                headers=self.headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result or result.get("errcode") != "0":
                print(f"获取新高数据失败: {result.get('errcode', 'unknown error')}")
                return pd.Series()
            
            # 解析x字段中的数据
            x_data = result.get("x", [])
            if not x_data:
                return pd.Series()
            
            # 解析所有日期数据
            dates = []
            new_highs = []
            
            for item in x_data:
                # 格式: "20260116_478_127_0"
                parts = item.split("_")
                if len(parts) >= 3:
                    date_str = parts[0]  # "20260116"
                    # total_count = int(parts[1])  # 478 (新高数量)
                    new_count = int(parts[2])  # 127 (今日新增)
                    
                    # 转换日期格式: 20260116 -> 2026-01-16
                    formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                    dates.append(formatted_date)
                    new_highs.append(new_count)
            
            # 创建Series
            series = pd.Series(new_highs, index=dates)
            series.index.name = "日期"
            series.name = "今日新增"
            
            # 如果只传了结束日期，返回单个值
            if start_date is None:
                if end_date in series.index:
                    return series[end_date]
                else:
                    print(f"警告: 未找到日期 {end_date} 的数据")
                    return pd.Series()
            
            # 如果传了起始和结束日期，返回范围数据
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            
            if start > end:
                start, end = end, start
            
            # 筛选日期范围
            mask = (pd.to_datetime(series.index) >= start) & (pd.to_datetime(series.index) <= end)
            return series[mask]
            
        except Exception as e:
            print(f"请求新高数据失败: {e}")
            return pd.Series()
    
    # ========== 保留原有的单独接口（向后兼容）==========
    
    def get_market_sentiment(self, date=None):
        """获取涨跌统计数据"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        result = self._request({"a": "HisZhangFuDetail", "c": "HisHomeDingPan"}, date)
        if not result:
            return pd.DataFrame()
        info = result.get("info", {})
        return pd.DataFrame({
            "日期": [result.get("date", date)],
            "涨停数": [int(info.get("ZT", 0))],
            "实际涨停": [int(info.get("SJZT", 0))],
            "跌停数": [int(info.get("DT", 0))],
            "实际跌停": [int(info.get("SJDT", 0))],
            "上涨家数": [int(info.get("SZJS", 0))],
            "下跌家数": [int(info.get("XDJS", 0))],
            "平盘家数": [int(info.get("0", 0))]
        })
    
    def get_market_index(self, date=None):
        """获取大盘指数数据"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        result = self._request({"a": "GetZsReal", "c": "StockL2History"}, date)
        if not result:
            return pd.DataFrame()
        return pd.DataFrame([{
            "日期": date,
            "指数代码": s.get("StockID", ""),
            "指数名称": s.get("prod_name", ""),
            "最新价": float(s.get("last_px", 0)),
            "涨跌额": float(s.get("increase_amount", 0)),
            "涨跌幅": s.get("increase_rate", ""),
            "成交额(元)": int(s.get("turnover", 0))
        } for s in result.get("StockList", [])])
    
    def get_limit_up_ladder(self, date=None):
        """获取连板梯队数据"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        result = self._request({"a": "ZhangTingExpression", "c": "HisHomeDingPan"}, date)
        if not result:
            return pd.DataFrame()
        info = result.get("info", [])
        if len(info) < 12:
            return pd.DataFrame()
        return pd.DataFrame({
            "日期": [date],
            "一板": [info[0]],
            "二板": [info[1]],
            "三板": [info[2]],
            "高度板": [info[3]],
            "连板率(%)": [round(info[4], 2)],
            "昨日首板今日上涨数": [info[5]],
            "昨日首板今日下跌数": [info[6]],
            "今日涨停破板率(%)": [round(info[7], 2)],
            "昨日涨停今表现(%)": [round(info[8], 2)],
            "昨日连板今表现(%)": [round(info[9], 2)],
            "昨日破板今表现(%)": [round(info[10], 2)],
            "市场评价": [info[11]]
        })
    
    def get_sharp_withdrawal(self, date=None):
        """获取大幅回撤股票数据"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        result = self._request({"a": "SharpWithdrawal", "c": "HisHomeDingPan"}, date)
        if not result:
            return pd.DataFrame()
        total_num = result.get("num", 0)
        return pd.DataFrame([{
            "日期": result.get("date", date),
            "股票代码": i[0],
            "股票名称": i[1],
            "当日涨跌幅(%)": round(i[2], 2),
            "回撤幅度(%)": round(i[3], 2),
            "最新价": round(i[4], 2),
            "总数": total_num
        } for i in result.get("info", []) if len(i) >= 5])
    

    def get_sector_ranking(self, date=None, index=0, timeout=None):
        """
        获取涨停原因板块数据
        
        Args:
            date: 日期，格式YYYY-MM-DD，默认为当前日期
            index: 分页索引，默认0（第一页）
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            dict: 包含板块统计和详细列表的字典
                - summary: 市场概况（涨停数、跌停数等）
                - sectors: 板块列表，每个板块包含：
                    - sector_code: 板块代码
                    - sector_name: 板块名称
                    - stocks: 该板块涨停股票列表
                    - stock_count: 涨停股票数量
        
        示例:
            crawler = KaipanlaCrawler()
            data = crawler.get_sector_ranking("2026-01-16")
            
            # 访问市场概况
            print(data['summary'])
            
            # 遍历板块
            for sector in data['sectors']:
                print(f"板块: {sector['sector_name']}, 涨停数: {sector['stock_count']}")
                for stock in sector['stocks']:
                    print(f"  {stock['股票代码']} {stock['股票名称']}")
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 构造请求参数
        data = {
            "a": "GetPlateInfo_w38",
            "st": "100",
            "c": "DailyLimitResumption",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "Index": str(index),
            "apiv": "w42",
            "Day": date  # 添加日期参数
        }
        
        try:
            response = requests.post(
                self.sector_base_url,
                data=data,
                headers=self.sector_headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result or result.get("errcode") != "0":
                print(f"获取板块数据失败: {result.get('errcode', 'unknown error')}")
                return {"summary": {}, "sectors": []}
            
            # 解析市场概况
            nums = result.get("nums", {})
            summary = {
                "日期": result.get("date", date),
                "上涨家数": nums.get("SZJS", 0),
                "下跌家数": nums.get("XDJS", 0),
                "涨停数": nums.get("ZT", 0),
                "跌停数": nums.get("DT", 0),
                "涨跌比": round(nums.get("ZBL", 0), 2),
                "昨日涨跌比": round(nums.get("yestRase", 0), 2)
            }
            
            # 解析板块列表
            sectors = []
            for sector_data in result.get("list", []):
                sector_info = {
                    "sector_code": sector_data.get("ZSCode", ""),
                    "sector_name": sector_data.get("ZSName", ""),
                    "stock_count": sector_data.get("num", 0),
                    "stocks": []
                }
                
                # 解析该板块的涨停股票
                # 原始数据数组结构（基于实际API返回）:
                # [0]股票代码, [1]股票名称, [2]?, [3]?, [4]涨停价,
                # [5]?, [6]未知(可能是时间戳), [7]?, [8]流通市值(元), [9]连板天数,
                # [10]连板次数, [11]概念标签, [12]封单额(元), [13]主力资金(元),
                # [14]首次封板时间(小时.分钟比例), [15]总市值(元), [16]涨停原因, [17]主题, [18]是否首板
                # 注意: 该API不提供个股成交额数据
                for stock in sector_data.get("StockList", []):
                    if len(stock) >= 19:  # 确保数据完整
                        # 转换封板时间格式
                        # API返回格式: 小时.分钟比例，如 20.41 表示 20:24
                        seal_time_raw = stock[14] if stock[14] else ""
                        seal_time = ""
                        if seal_time_raw:
                            try:
                                # 尝试解析为时间格式
                                hour = int(seal_time_raw)
                                minute_decimal = seal_time_raw - hour
                                minute = int(round(minute_decimal * 60))

                                # 处理分钟进位
                                if minute >= 60:
                                    hour += minute // 60
                                    minute = minute % 60

                                # 只接受有效的小时范围 (0-23)
                                if 0 <= hour <= 23:
                                    seal_time = f"{hour:02d}:{minute:02d}:00"
                                else:
                                    # 超出范围的时间，可能是数据错误
                                    seal_time = str(seal_time_raw)
                            except:
                                seal_time = str(seal_time_raw)

                        stock_info = {
                            "股票代码": stock[0],
                            "股票名称": stock[1],
                            "涨停价": round(stock[4], 2) if stock[4] else 0,
                            "成交额": 0,  # 该API不提供个股成交额，需要从其他数据源获取
                            "流通市值": stock[8] if stock[8] else 0,  # 流通市值（元）
                            "连板天数": stock[9],
                            "连板次数": stock[10],
                            "概念标签": stock[11],
                            "封单额": stock[12] if stock[12] else 0,  # 封单额（元）
                            "主力资金": stock[13] if stock[13] else 0,  # 主力资金净额（元）
                            "首次封板时间": seal_time,  # 首次封板时间（已格式化）
                            "总市值": stock[15] if stock[15] else 0,  # 总市值（元）
                            "涨停原因": stock[16] if stock[16] else "",
                            "主题": stock[17] if stock[17] else "",
                            "是否首板": stock[18] if len(stock) > 18 else 0,
                            # 兼容旧字段名
                            "涨停时间": seal_time,  # 等同于首次封板时间
                        }
                        sector_info["stocks"].append(stock_info)
                
                sectors.append(sector_info)
            
            return {
                "summary": summary,
                "sectors": sectors
            }
            
        except Exception as e:
            print(f"请求板块数据失败 ({date}): {e}")
            return {"summary": {}, "sectors": []}
    
    def get_consecutive_limit_up(self, date=None, timeout=None):
        """
        获取指定日期的连板梯队情况
        
        Args:
            date: 日期，格式YYYY-MM-DD，默认为当前日期
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            dict: 包含连板梯队信息
                - date: 日期
                - max_consecutive: 最高连板高度
                - max_consecutive_stocks: 最高连板个股名称（多个用/分隔）
                - max_consecutive_concepts: 最高连板个股题材（多个用/分隔）
                - ladder: 连板梯队详细数据
                    - 2: 二连板股票列表
                    - 3: 三连板股票列表
                    - 4: 四连板股票列表
                    - ...
        
        示例:
            crawler = KaipanlaCrawler()
            data = crawler.get_consecutive_limit_up("2026-01-19")
            print(f"最高板: {data['max_consecutive']}连板")
            print(f"最高板个股: {data['max_consecutive_stocks']}")
            print(f"最高板题材: {data['max_consecutive_concepts']}")
            print(f"连板梯队: {data['ladder']}")
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 存储所有连板数据
        ladder_data = {}
        max_consecutive = 0
        max_stocks = []
        
        # 从高到低尝试获取连板数据（最多尝试到20连板）
        for pid_type in range(20, 1, -1):
            data = {
                "Order": "0",
                "a": "DailyLimitPerformance",
                "st": "2000",
                "c": "HisHomeDingPan",
                "PhoneOSNew": "1",
                "DeviceID": str(uuid.uuid4()),
                "VerSion": "5.21.0.2",
                "Index": "0",
                "PidType": str(pid_type),
                "apiv": "w42",
                "Type": "4",
                "Day": date
            }
            
            try:
                response = requests.post(
                    self.base_url,
                    data=data,
                    headers=self.headers,
                    verify=False,
                    proxies={'http': None, 'https': None},
                    timeout=timeout
                )
                response.raise_for_status()
                result = response.json()
                
                if result and result.get("errcode") == "0":
                    info = result.get("info", [])
                    if info and len(info) > 0 and len(info[0]) > 0:
                        # 有数据，说明存在这个连板高度
                        stock_list = info[0]
                        
                        # 解析股票信息
                        stocks = []
                        for stock_data in stock_list:
                            if len(stock_data) >= 13:
                                stock_info = {
                                    "股票代码": stock_data[0],
                                    "股票名称": stock_data[1],
                                    "连板天数": stock_data[9] if len(stock_data) > 9 else pid_type,
                                    "题材": stock_data[5] if len(stock_data) > 5 else "",
                                    "概念": stock_data[12] if len(stock_data) > 12 else ""
                                }
                                stocks.append(stock_info)
                        
                        if stocks:
                            ladder_data[pid_type] = stocks
                            
                            # 更新最高连板
                            if pid_type > max_consecutive:
                                max_consecutive = pid_type
                                max_stocks = stocks
            
            except Exception as e:
                # 忽略错误，继续尝试下一个连板高度
                continue
        
        # 如果没有找到任何连板数据，返回空结果
        if max_consecutive == 0:
            return {
                "date": date,
                "max_consecutive": 0,
                "max_consecutive_stocks": "",
                "max_consecutive_concepts": "",
                "ladder": {}
            }
        
        # 提取最高板个股名称和题材
        stock_names = []
        stock_concepts_list = []  # 每只股票的概念列表
        
        for stock in max_stocks:
            stock_names.append(stock["股票名称"])
            
            # 合并题材和概念
            all_concepts = []
            if stock["题材"]:
                # 按"、"或"/"分割
                concepts = [c.strip() for c in stock["题材"].replace("/", "、").split("、") if c.strip()]
                all_concepts.extend(concepts)
            if stock["概念"]:
                # 按"、"或"/"分割
                concepts = [c.strip() for c in stock["概念"].replace("/", "、").split("、") if c.strip()]
                all_concepts.extend(concepts)
            
            # 去重但保持顺序
            unique_concepts = []
            seen = set()
            for c in all_concepts:
                if c not in seen:
                    unique_concepts.append(c)
                    seen.add(c)
            
            # 使用"、"分隔同一个股的多个题材
            stock_concept = "、".join(unique_concepts) if unique_concepts else ""
            stock_concepts_list.append(stock_concept)
        
        # 使用"/"分隔不同个股
        max_consecutive_stocks = "/".join(stock_names)
        # 使用"/"分隔不同个股的概念
        max_consecutive_concepts = "/".join([c for c in stock_concepts_list if c])
        
        return {
            "date": date,
            "max_consecutive": max_consecutive,
            "max_consecutive_stocks": max_consecutive_stocks,
            "max_consecutive_concepts": max_consecutive_concepts,
            "ladder": ladder_data
        }
    
    def get_sector_limit_up_ladder(self, date=None, timeout=None):
        """
        获取板块连板梯队（历史或实时）
        
        Args:
            date: 日期，格式YYYY-MM-DD，默认为None（获取实时数据）
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            dict: 包含板块连板梯队信息
                - date: 日期
                - is_realtime: 是否为实时数据
                - sectors: 板块列表，每个板块包含：
                    - sector_name: 板块名称
                    - limit_up_count: 涨停数
                    - stocks: 涨停股票列表
                        - stock_code: 股票代码
                        - stock_name: 股票名称
                        - consecutive_days: 连板天数
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取历史数据
            data = crawler.get_sector_limit_up_ladder("2026-01-16")
            
            # 获取实时数据
            data = crawler.get_sector_limit_up_ladder()
            
            # 遍历板块
            for sector in data['sectors']:
                print(f"{sector['sector_name']}: {sector['limit_up_count']}只涨停")
                for stock in sector['stocks']:
                    print(f"  {stock['stock_code']} {stock['stock_name']} {stock['consecutive_days']}连板")
        """
        is_realtime = date is None
        
        if is_realtime:
            # 获取实时数据
            url = self.sector_base_url
            headers = self.sector_headers
            data_params = {
                "a": "GetYTFP_BKHX",
                "c": "FuPanLa",
                "PhoneOSNew": "1",
                "DeviceID": str(uuid.uuid4()),
                "VerSion": "5.21.0.2",
                "apiv": "w42"
            }
            display_date = datetime.now().strftime("%Y-%m-%d")
        else:
            # 获取历史数据
            url = self.base_url
            headers = self.headers
            data_params = {
                "a": "GetYTFP_BKHX",
                "c": "FuPanLa",
                "PhoneOSNew": "1",
                "DeviceID": str(uuid.uuid4()),
                "VerSion": "5.21.0.2",
                "Date": date,
                "apiv": "w42"
            }
            display_date = date
        
        try:
            response = requests.post(
                url,
                data=data_params,
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result or result.get("errcode") != "0":
                print(f"获取板块连板梯队失败: {result.get('errcode', 'unknown error')}")
                return {
                    "date": display_date,
                    "is_realtime": is_realtime,
                    "sectors": []
                }
            
            # 解析板块数据（注意：字段名是大写的List）
            sectors = []
            sector_list = result.get("List", [])
            
            for sector_data in sector_list:
                sector_name = sector_data.get("ZSName", "")
                sector_code = sector_data.get("ZSCode", "")
                td_list = sector_data.get("TD", [])
                
                # 解析股票列表
                stocks = []
                broken_stocks = []  # 反包板股票（TDType=0）
                
                for td_group in td_list:
                    td_type = td_group.get("TDType", "1")
                    stock_list = td_group.get("Stock", [])
                    
                    # TDType说明：
                    # 0: 反包板（记录但不计入连板梯队）
                    # 1: 首板
                    # 2: 2连板
                    # 3: 3连板
                    # 9: 打开高度标注
                    # ...
                    
                    for stock_data in stock_list:
                        stock_code = stock_data.get("StockID", "")
                        stock_name = stock_data.get("StockName", "")
                        tips = stock_data.get("Tips", "")
                        
                        # 处理TDType=0（反包板）
                        if td_type == "0":
                            # 反包板：从Tips中解析连板天数
                            consecutive_days = 0
                            if tips:
                                import re
                                match = re.search(r'(\d+)天(\d+)板', tips)
                                if match:
                                    consecutive_days = int(match.group(2))
                            
                            stock_info = {
                                "stock_code": stock_code,
                                "stock_name": stock_name,
                                "consecutive_days": consecutive_days,
                                "tips": tips,
                                "is_broken": True  # 标记为反包板
                            }
                            broken_stocks.append(stock_info)
                        
                        # 处理TDType=9（打开高度标注）
                        elif td_type == "9":
                            stock_info = {
                                "stock_code": stock_code,
                                "stock_name": stock_name,
                                "consecutive_days": 0,
                                "tips": tips,
                                "is_height_mark": True  # 标记为打开高度
                            }
                            stocks.append(stock_info)
                        
                        # 处理正常连板（TDType=1,2,3...）
                        else:
                            try:
                                consecutive_days = int(td_type)
                            except:
                                consecutive_days = 1
                            
                            stock_info = {
                                "stock_code": stock_code,
                                "stock_name": stock_name,
                                "consecutive_days": consecutive_days,
                                "tips": tips
                            }
                            stocks.append(stock_info)
                
                if stocks or broken_stocks:  # 只添加有涨停股票的板块
                    sector_info = {
                        "sector_code": sector_code,
                        "sector_name": sector_name,
                        "limit_up_count": int(sector_data.get("Count", len(stocks))),
                        "stocks": stocks,  # 正常连板股票
                        "broken_stocks": broken_stocks  # 反包板股票（不计入连板梯队）
                    }
                    sectors.append(sector_info)
            
            return {
                "date": result.get("Date", display_date),
                "is_realtime": is_realtime,
                "sectors": sectors
            }
            
        except Exception as e:
            print(f"请求板块连板梯队失败 ({display_date}): {e}")
            import traceback
            traceback.print_exc()
            return {
                "date": display_date,
                "is_realtime": is_realtime,
                "sectors": []
            }
    
    def get_market_limit_up_ladder(self, date=None, timeout=None):
        """
        获取全市场连板梯队（历史或实时）
        
        Args:
            date: 日期，格式YYYY-MM-DD，默认为None（获取实时数据）
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            dict: 包含全市场连板梯队信息
                - date: 日期
                - is_realtime: 是否为实时数据
                - ladder: 连板梯队数据
                    - 1: 首板股票列表
                    - 2: 2连板股票列表
                    - 3: 3连板股票列表
                    - ...
                - broken_stocks: 反包板股票列表
                - height_marks: 打开高度标注股票列表
                - statistics: 统计信息
                    - total_limit_up: 总涨停数
                    - max_consecutive: 最高连板
                    - ladder_distribution: 连板分布
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取历史数据
            data = crawler.get_market_limit_up_ladder("2026-01-16")
            
            # 获取实时数据
            data = crawler.get_market_limit_up_ladder()
            
            print(f"日期: {data['date']}")
            print(f"数据类型: {'实时' if data['is_realtime'] else '历史'}")
            print(f"总涨停数: {data['statistics']['total_limit_up']}")
            print(f"最高连板: {data['statistics']['max_consecutive']}")
            
            # 遍历连板梯队
            for consecutive, stocks in sorted(data['ladder'].items(), reverse=True):
                print(f"{consecutive}连板: {len(stocks)}只")
                for stock in stocks[:5]:  # 显示前5只
                    print(f"  {stock['stock_code']} {stock['stock_name']}")
        """
        is_realtime = date is None
        
        if is_realtime:
            # 获取实时数据
            url = self.sector_base_url
            headers = self.sector_headers
            data_params = {
                "a": "GetYTFP_SCTD",
                "c": "FuPanLa",
                "PhoneOSNew": "1",
                "DeviceID": str(uuid.uuid4()),
                "VerSion": "5.21.0.2",
                "apiv": "w42"
            }
            display_date = datetime.now().strftime("%Y-%m-%d")
        else:
            # 获取历史数据
            url = self.base_url
            headers = self.headers
            data_params = {
                "a": "GetYTFP_SCTD",
                "c": "FuPanLa",
                "PhoneOSNew": "1",
                "DeviceID": str(uuid.uuid4()),
                "VerSion": "5.21.0.2",
                "Date": date,
                "apiv": "w42"
            }
            display_date = date
        
        try:
            response = requests.post(
                url,
                data=data_params,
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result or result.get("errcode") != "0":
                print(f"获取全市场连板梯队失败: {result.get('errcode', 'unknown error')}")
                return {
                    "date": display_date,
                    "is_realtime": is_realtime,
                    "ladder": {},
                    "broken_stocks": [],
                    "height_marks": [],
                    "statistics": {
                        "total_limit_up": 0,
                        "max_consecutive": 0,
                        "ladder_distribution": {}
                    }
                }
            
            # 解析连板梯队数据
            ladder = {}
            broken_stocks = []
            height_marks = []
            list_data = result.get("List", [])
            
            for group in list_data:
                tip = group.get("Tip", "1")
                stock_list = group.get("Stocks", [])
                
                for stock_data in stock_list:
                    stock_code = stock_data.get("StockID", "")
                    stock_name = stock_data.get("Name", "")
                    tips = stock_data.get("Tips", "")
                    
                    # 处理Tip=0（反包板）
                    if tip == "0":
                        consecutive_days = 0
                        if tips:
                            import re
                            match = re.search(r'(\d+)天(\d+)板', tips)
                            if match:
                                consecutive_days = int(match.group(2))
                        
                        stock_info = {
                            "stock_code": stock_code,
                            "stock_name": stock_name,
                            "consecutive_days": consecutive_days,
                            "tips": tips,
                            "is_broken": True
                        }
                        broken_stocks.append(stock_info)
                    
                    # 处理Tip=9（打开高度标注）
                    elif tip == "9":
                        stock_info = {
                            "stock_code": stock_code,
                            "stock_name": stock_name,
                            "consecutive_days": 0,
                            "tips": tips,
                            "is_height_mark": True
                        }
                        height_marks.append(stock_info)
                    
                    # 处理正常连板
                    else:
                        try:
                            consecutive_days = int(tip)
                        except:
                            consecutive_days = 1
                        
                        stock_info = {
                            "stock_code": stock_code,
                            "stock_name": stock_name,
                            "consecutive_days": consecutive_days,
                            "tips": tips
                        }
                        
                        # 添加到对应的连板梯队
                        if consecutive_days not in ladder:
                            ladder[consecutive_days] = []
                        ladder[consecutive_days].append(stock_info)
            
            # 计算统计信息
            total_limit_up = sum(len(stocks) for stocks in ladder.values())
            max_consecutive = max(ladder.keys()) if ladder else 0
            ladder_distribution = {k: len(v) for k, v in ladder.items()}
            
            return {
                "date": result.get("Date", display_date),
                "is_realtime": is_realtime,
                "ladder": ladder,
                "broken_stocks": broken_stocks,
                "height_marks": height_marks,
                "statistics": {
                    "total_limit_up": total_limit_up,
                    "max_consecutive": max_consecutive,
                    "ladder_distribution": ladder_distribution
                }
            }
            
        except Exception as e:
            print(f"请求全市场连板梯队失败 ({display_date}): {e}")
            import traceback
            traceback.print_exc()
            return {
                "date": display_date,
                "is_realtime": is_realtime,
                "ladder": {},
                "broken_stocks": [],
                "height_marks": [],
                "statistics": {
                    "total_limit_up": 0,
                    "max_consecutive": 0,
                    "ladder_distribution": {}
                }
            }
    
    def get_historical_broken_limit_up(self, date, timeout=None):
        """
        获取历史炸板股数据（曾涨停但未封住的个股）
        
        Args:
            date: 日期，格式YYYY-MM-DD
            timeout: 超时时间（秒）
            
        Returns:
            list: 炸板股列表，每个元素包含：
                - stock_code: 股票代码
                - stock_name: 股票名称
                - change_pct: 涨幅
                - limit_up_time: 涨停时间（时间戳）
                - open_time: 开板时间（时间戳）
                - yesterday_consecutive: 昨日连板高度
                - yesterday_consecutive_text: 昨日连板高度文字描述
                - sector: 所属板块
                - main_capital_net: 主力净额
                - turnover_amount: 成交额
                - turnover_rate: 换手率
                - actual_circulation: 实际流通
        """
        try:
            # 生成设备ID
            device_id = str(uuid.uuid4())
            
            # 构建请求参数
            data = {
                "Order": "1",
                "a": "HisDaBanList",
                "st": "30",
                "c": "HisHomeDingPan",
                "PhoneOSNew": "1",
                "DeviceID": device_id,
                "VerSion": "5.21.0.2",
                "Index": "0",
                "Is_st": "1",
                "PidType": "2",
                "apiv": "w42",
                "Type": "4",
                "FilterMotherboard": "0",
                "Filter": "0",
                "FilterTIB": "0",
                "Day": date,
                "FilterGem": "0"
            }
            
            # 发送请求
            response = requests.post(
                self.base_url,
                data=data,
                headers=self.headers,
                verify=False,
                timeout=timeout or 60
            )
            
            if response.status_code != 200:
                print(f"请求失败，状态码: {response.status_code}")
                return []
            
            result = response.json()
            
            # 解析返回数据 - 数据在"list"字段中
            broken_stocks = []
            stock_list = result.get("list", [])
            
            for stock_data in stock_list:
                # 数据格式：
                # [0]股票代码, [1]股票名称, [2]?, [3]?, [4]涨幅, [5]?, 
                # [6]涨停时间, [7]开板时间, [8]?, [9]昨日连板文字, 
                # [10]昨日连板高度, [11]板块, [12]主力净额, [13]成交额, 
                # [14]换手率, [15]实际流通, [16]?, ...
                
                if len(stock_data) < 16:
                    continue
                
                broken_stock = {
                    "stock_code": stock_data[0],
                    "stock_name": stock_data[1],
                    "change_pct": float(stock_data[4]) if stock_data[4] else 0.0,
                    "limit_up_time": int(stock_data[6]) if stock_data[6] else 0,
                    "open_time": int(stock_data[7]) if stock_data[7] else 0,
                    "yesterday_consecutive_text": stock_data[9] if stock_data[9] else "",
                    "yesterday_consecutive": int(stock_data[10]) if stock_data[10] else 0,
                    "sector": stock_data[11] if stock_data[11] else "",
                    "main_capital_net": float(stock_data[12]) if stock_data[12] else 0.0,
                    "turnover_amount": float(stock_data[13]) if stock_data[13] else 0.0,
                    "turnover_rate": float(stock_data[14]) if stock_data[14] else 0.0,
                    "actual_circulation": stock_data[15] if stock_data[15] else ""
                }
                
                broken_stocks.append(broken_stock)
            
            print(f"成功获取 {len(broken_stocks)} 只炸板股 ({date})")
            return broken_stocks
            
        except Exception as e:
            print(f"获取历史炸板股失败 ({date}): {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_sector_capital_data(self, sector_code, date=None, timeout=None):
        """
        获取板块资金成交额数据
        
        Args:
            sector_code: 板块代码，如 "801235"（化工）
            date: 日期，格式YYYY-MM-DD，默认为空（获取实时数据）
            timeout: 超时时间（秒），默认60秒
            
        Returns:
            dict: 包含板块资金数据
                - sector_code: 板块代码
                - date: 日期
                - turnover: 成交额（元）
                - change_pct: 涨跌幅（%）
                - market_cap: 市值（亿元）
                - main_net_inflow: 主力净额（元）
                - main_sell: 主卖（元）
                - net_amount: 净额（元）
                - up_count: 上涨家数
                - down_count: 下跌家数
                - flat_count: 平盘家数
                - circulating_market_cap: 流通市值（元）
                - total_market_cap: 总市值（元）
                - turnover_rate: 换手率（%）
                - main_net_inflow_pct: 主力净占比（%）
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取化工板块实时数据
            data = crawler.get_sector_capital_data("801235")
            print(f"成交额: {data['turnover'] / 100000000:.2f}亿")
            print(f"主力净额: {data['main_net_inflow'] / 100000000:.2f}亿")
            
            # 获取指定日期数据
            data = crawler.get_sector_capital_data("801235", "2026-01-20")
        """
        # 根据是否传入日期，选择不同的API地址和headers
        if date:
            # 历史数据：使用 apphis.longhuvip.com
            url = self.base_url
            headers = self.headers
        else:
            # 实时数据：使用 apphwhq.longhuvip.com
            url = self.sector_base_url
            headers = self.sector_headers
        
        # 构造请求参数
        data_params = {
            "a": "GetPanKou",
            "c": "ZhiShuL2Data",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "apiv": "w42",
            "StockID": sector_code,
            "Day": date if date else ""
        }
        
        try:
            response = requests.post(
                url,
                data=data_params,
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result or result.get("errcode") != "0":
                print(f"获取板块资金数据失败: {result.get('errcode', 'unknown error')}")
                return {}
            
            # 解析pankou数据
            # 实时数据pankou数组格式（12个元素）：
            # [成交额, 涨跌幅, 市值, 主力净额, 主卖, 净额, 上涨, 下跌, 平盘, 流通市值, 总市值, 换手率]
            # 
            # 历史数据pankou数组格式（11个元素）：
            # [成交额, 涨跌幅, 市值, 主力净额, 主卖, 净额, 上涨, 下跌, 平盘, 流通市值, 总市值]
            # 注意：历史数据没有换手率字段
            pankou = result.get("pankou", [])
            
            if len(pankou) < 11:
                print(f"板块数据格式不完整: {pankou}")
                return {}
            
            # 解析数据
            capital_data = {
                "sector_code": result.get("code", sector_code),
                "date": date if date else datetime.now().strftime("%Y-%m-%d"),
                "turnover": float(pankou[0]) if pankou[0] else 0,  # 成交额（元）
                "change_pct": float(pankou[1]) if pankou[1] else 0,  # 涨跌幅（%）
                "market_cap": float(pankou[2]) if pankou[2] else 0,  # 市值（亿元）
                "main_net_inflow": float(pankou[3]) if pankou[3] else 0,  # 主力净额（元）
                "main_sell": float(pankou[4]) if pankou[4] else 0,  # 主卖（元）
                "net_amount": float(pankou[5]) if pankou[5] else 0,  # 净额（元）
                "up_count": int(pankou[6]) if pankou[6] else 0,  # 上涨家数
                "down_count": int(pankou[7]) if pankou[7] else 0,  # 下跌家数
                "flat_count": int(pankou[8]) if pankou[8] else 0,  # 平盘家数
                "circulating_market_cap": float(pankou[9]) if pankou[9] else 0,  # 流通市值（元）
                "total_market_cap": float(pankou[10]) if pankou[10] else 0,  # 总市值（元）
                "turnover_rate": float(pankou[11]) if len(pankou) > 11 and pankou[11] else 0,  # 换手率（%）- 历史数据可能没有
            }
            
            # 计算主力净占比
            if capital_data["turnover"] > 0:
                capital_data["main_net_inflow_pct"] = (capital_data["main_net_inflow"] / capital_data["turnover"]) * 100
            else:
                capital_data["main_net_inflow_pct"] = 0
            
            return capital_data
            
        except Exception as e:
            print(f"请求板块资金数据失败 ({sector_code}): {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def get_sector_strength_ndays(self, end_date, num_days=7, timeout=None):
        """
        获取N日板块强度排名数据
        
        Args:
            end_date: 结束日期，格式YYYY-MM-DD
            num_days: 获取天数，默认7天
            timeout: 超时时间（秒），默认60秒
            
        Returns:
            pd.DataFrame: 包含N日板块强度数据
                - 日期: 交易日期
                - 板块代码: 板块代码
                - 板块名称: 板块名称
                - 涨停数: 该板块涨停股票数量
                - 涨停股票: 涨停股票列表（股票代码）
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取最近7日板块强度
            df = crawler.get_sector_strength_ndays("2026-01-20", num_days=7)
            
            # 分析板块热度趋势
            sector_trend = df.groupby('板块名称')['涨停数'].sum().sort_values(ascending=False)
            print("7日最强板块:")
            print(sector_trend.head(10))
            
            # 查看特定板块的每日涨停数
            sector_name = "化工"
            sector_data = df[df['板块名称'] == sector_name]
            print(f"\n{sector_name}板块每日涨停数:")
            print(sector_data[['日期', '涨停数']])
        """
        # 生成日期列表（向前推算num_days个交易日）
        end = datetime.strptime(end_date, "%Y-%m-%d")
        dates = []
        current = end
        
        # 简单向前推算，实际交易日会在请求时过滤
        for i in range(num_days * 2):  # 多推算一些天数以确保有足够的交易日
            date_str = current.strftime("%Y-%m-%d")
            dates.append(date_str)
            current -= timedelta(days=1)
            if len(dates) >= num_days * 2:
                break
        
        all_data = []
        trading_days_count = 0
        
        print(f"开始获取{num_days}日板块强度数据...")
        
        for date in dates:
            if trading_days_count >= num_days:
                break
            
            try:
                # 获取该日期的板块排名数据
                sector_data = self.get_sector_ranking(date, timeout=timeout)
                
                if not sector_data or not sector_data.get("sectors"):
                    # 可能是非交易日，跳过
                    continue
                
                trading_days_count += 1
                print(f"  获取 {date} 数据... ({trading_days_count}/{num_days})")
                
                # 解析每个板块的数据
                for sector in sector_data["sectors"]:
                    sector_name = sector.get("sector_name", "")
                    sector_code = sector.get("sector_code", "")
                    stock_count = sector.get("stock_count", 0)
                    
                    # 提取涨停股票代码列表
                    stock_codes = [stock.get("股票代码", "") for stock in sector.get("stocks", [])]
                    
                    row = {
                        "日期": date,
                        "板块代码": sector_code,
                        "板块名称": sector_name,
                        "涨停数": stock_count,
                        "涨停股票": ",".join(stock_codes)
                    }
                    all_data.append(row)
                
            except Exception as e:
                print(f"  获取 {date} 数据失败: {e}")
                continue
        
        if not all_data:
            print("未获取到任何板块数据")
            return pd.DataFrame()
        
        df = pd.DataFrame(all_data)
        print(f"[OK] 成功获取 {trading_days_count} 个交易日的板块数据")
        
        return df
    
    def get_realtime_market_mood(self, timeout=None):
        """
        获取实时市场情绪数据（涨停家数、跌停家数、上涨下跌家数及大盘数据）
        
        Args:
            timeout: 超时时间（秒），默认60秒
            
        Returns:
            dict: 包含市场情绪数据
                - 上涨家数: 上涨股票数量
                - 下跌家数: 下跌股票数量
                - 涨停家数: 涨停股票数量
                - 跌停家数: 跌停股票数量
                - 全市场流通量: 全市场流通量
                - 前日流通量: 前一交易日流通量
                - 涨跌比: 上涨家数/下跌家数
                - 市场颜色: 1=红色(上涨), 0=绿色(下跌)
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取实时市场情绪
            mood = crawler.get_realtime_market_mood()
            print(f"涨停: {mood['涨停家数']}家")
            print(f"跌停: {mood['跌停家数']}家")
            print(f"上涨: {mood['上涨家数']}家")
            print(f"下跌: {mood['下跌家数']}家")
            print(f"涨跌比: {mood['涨跌比']}")
        """
        # 构造请求参数
        data_params = {
            "a": "MoodNumCount",
            "c": "MarketMood",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "apiv": "w42"
        }
        
        try:
            response = requests.post(
                self.sector_base_url,
                data=data_params,
                headers=self.sector_headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result or result.get("errcode") != "0":
                print(f"获取实时市场情绪失败: {result.get('errcode', 'unknown error')}")
                return {}
            
            # 解析数据
            list_data = result.get("list", {})
            
            mood_data = {
                "上涨家数": int(list_data.get("SZJS", 0)),
                "下跌家数": int(list_data.get("XDJS", 0)),
                "涨停家数": int(list_data.get("ZTJS", 0)),
                "跌停家数": int(list_data.get("DTJS", 0)),
                "全市场流通量": int(list_data.get("qscln", 0)),
                "前日流通量": int(list_data.get("q_zrcs", 0)),
                "涨跌比": float(list_data.get("bl", 0)),
                "市场颜色": int(list_data.get("color", 0))
            }
            
            return mood_data
            
        except Exception as e:
            print(f"请求实时市场情绪失败: {e}")
            import traceback
            traceback.prprint_exc()
            return {}
            print(f"请求实时连板梯队指数失败: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def get_realtime_actual_limit_up_down(self, timeout=None):
        """
        获取实时实际涨跌停数据
        
        Args:
            timeout: 超时时间（秒），默认60秒
            
        Returns:
            dict: 包含实际涨跌停数据
                - actual_limit_up: 实际涨停数
                - actual_limit_down: 实际跌停数
                - limit_up: 涨停数（包含一字板）
                - limit_down: 跌停数（包含一字板）
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取实时实际涨跌停数据
            data = crawler.get_realtime_actual_limit_up_down()
            print(f"实际涨停: {data['actual_limit_up']}只")
            print(f"实际跌停: {data['actual_limit_down']}只")
        """
        # 构造请求参数
        data_params = {
            "a": "MarketStockZDNum",
            "c": "HomeDingPan",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "apiv": "w42"
        }
        
        try:
            response = requests.post(
                self.sector_base_url,
                data=data_params,
                headers=self.sector_headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result or result.get("errcode") != "0":
                print(f"获取实时实际涨跌停数据失败: {result.get('errcode', 'unknown error')}")
                return {}
            
            # 解析数据
            limit_data = {
                "actual_limit_up": int(result.get("actual_limit_up", 0)),
                "actual_limit_down": int(result.get("actual_limit_down", 0)),
                "limit_up": int(result.get("limit_up", 0)),
                "limit_down": int(result.get("limit_down", 0)),
            }
            
            return limit_data
            
        except Exception as e:
            print(f"请求实时实际涨跌停数据失败: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def get_realtime_board_stocks(self, board_type=1, timeout=None):
        """
        获取实时指定连板的股票列表
        
        Args:
            board_type: 连板类型
                1: 首板
                2: 二板
                3: 三板
                4: 四板
                5: 五板及以上
            timeout: 超时时间（秒），默认60秒
            
        Returns:
            list: 股票列表，每个股票包含：
                - stock_code: 股票代码
                - stock_name: 股票名称
                - board_type: 连板类型
                - limit_up_reason: 涨停原因
                - turnover: 成交额
                - circulating_market_cap: 流通市值
                - total_market_cap: 总市值
                - main_net_inflow: 主力净额
                - seal_amount: 封单额
                - concepts: 概念标签
                - amplitude: 振幅
                - consecutive_days: 连板天数
                - sector_code: 板块代码
                - limit_up_price: 涨停价
                - limit_up_pct: 涨停幅度
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取首板股票
            first_board = crawler.get_realtime_board_stocks(board_type=1)
            print(f"首板股票: {len(first_board)}只")
            
            # 获取二板股票
            second_board = crawler.get_realtime_board_stocks(board_type=2)
            print(f"二板股票: {len(second_board)}只")
        """
        # 构造请求参数
        data_params = {
            "Order": "0",
            "a": "DailyLimitPerformance",
            "st": "2000",
            "c": "HomeDingPan",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "Index": "0",
            "PidType": str(board_type),
            "apiv": "w42",
            "Type": "4"
        }
        
        try:
            response = requests.post(
                self.sector_base_url,
                data=data_params,
                headers=self.sector_headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result or result.get("errcode") != "0":
                print(f"获取实时{board_type}板股票失败: {result.get('errcode', 'unknown error')}")
                return []
            
            # 解析股票列表
            # 数据结构: result['info'][0] 是股票数组列表
            stocks = []
            info = result.get("info", [])
            
            if not info or len(info) < 1:
                return []
            
            stock_list = info[0] if isinstance(info[0], list) else []
            
            for stock_data in stock_list:
                if not isinstance(stock_data, list) or len(stock_data) < 23:
                    continue
                
                stock_info = {
                    "stock_code": stock_data[0],
                    "stock_name": stock_data[1],
                    "board_type": board_type,
                    "timestamp": stock_data[4],
                    "limit_up_reason": stock_data[5],
                    "turnover": stock_data[6],
                    "circulating_market_cap": stock_data[7],
                    "main_buy": stock_data[8],
                    "main_sell": stock_data[9],
                    "main_net_inflow": stock_data[10],
                    "seal_amount": stock_data[11],
                    "concepts": stock_data[12],
                    "total_market_cap": stock_data[13],
                    "amplitude": stock_data[14],
                    "consecutive_days": stock_data[15],
                    "change_pct": stock_data[17] if len(stock_data) > 17 else 0,
                    "sector_code": stock_data[19] if len(stock_data) > 19 else "",
                    "sector_limit_up_count": stock_data[20] if len(stock_data) > 20 else 0,
                    "limit_up_price": stock_data[21] if len(stock_data) > 21 else 0,
                    "limit_up_pct": stock_data[22] if len(stock_data) > 22 else 0,
                }
                stocks.append(stock_info)
            
            return stocks
            
        except Exception as e:
            print(f"请求实时{board_type}板股票失败: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_realtime_all_boards_stocks(self, timeout=None):
        """
        获取实时所有连板的股票列表（首板到五板以上）
        
        Args:
            timeout: 超时时间（秒），默认60秒
            
        Returns:
            dict: 包含各连板的股票列表
                - first_board: 首板股票列表
                - second_board: 二板股票列表
                - third_board: 三板股票列表
                - fourth_board: 四板股票列表
                - fifth_board_plus: 五板及以上股票列表
                - statistics: 统计信息
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取所有连板股票
            data = crawler.get_realtime_all_boards_stocks()
            
            print(f"首板: {len(data['first_board'])}只")
            print(f"二板: {len(data['second_board'])}只")
            print(f"三板: {len(data['third_board'])}只")
            print(f"四板: {len(data['fourth_board'])}只")
            print(f"五板以上: {len(data['fifth_board_plus'])}只")
        """
        board_names = {
            1: "first_board",
            2: "second_board",
            3: "third_board",
            4: "fourth_board",
            5: "fifth_board_plus"
        }
        
        all_boards = {}
        total_stocks = 0
        
        print("获取实时所有连板股票...")
        
        for board_type, board_name in board_names.items():
            print(f"  获取{board_type}板股票...")
            stocks = self.get_realtime_board_stocks(board_type, timeout)
            all_boards[board_name] = stocks
            total_stocks += len(stocks)
        
        # 统计信息
        all_boards["statistics"] = {
            "total_stocks": total_stocks,
            "first_board_count": len(all_boards["first_board"]),
            "second_board_count": len(all_boards["second_board"]),
            "third_board_count": len(all_boards["third_board"]),
            "fourth_board_count": len(all_boards["fourth_board"]),
            "fifth_board_plus_count": len(all_boards["fifth_board_plus"]),
        }
        
        # 计算连板率
        if total_stocks > 0:
            consecutive = total_stocks - len(all_boards["first_board"])
            all_boards["statistics"]["consecutive_rate"] = (consecutive / total_stocks) * 100
        else:
            all_boards["statistics"]["consecutive_rate"] = 0
        
        print(f"[OK] 成功获取 {total_stocks} 只涨停股票")
        
        return all_boards
    
    def get_board_stocks_count_and_list(self, board_type, timeout=None):
        """
        获取指定连板的个股数量和个股列表
        
        Args:
            board_type: 连板类型
                1: 首板
                2: 二板
                3: 三板
                4: 四板
                5: 五板及以上（最高板）
            timeout: 超时时间（秒），默认60秒
            
        Returns:
            tuple: (个股数量, 个股列表)
                - count: int, 该连板的个股数量
                - stocks: list, 个股列表，每个股票包含详细信息
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取首板数量和列表
            count, stocks = crawler.get_board_stocks_count_and_list(1)
            print(f"首板: {count}只")
            for stock in stocks:
                print(f"  {stock['stock_name']} ({stock['stock_code']})")
            
            # 获取二板数量和列表
            count, stocks = crawler.get_board_stocks_count_and_list(2)
            print(f"二板: {count}只")
            
            # 获取最高板数量和列表
            count, stocks = crawler.get_board_stocks_count_and_list(5)
            print(f"最高板: {count}只")
        """
        # 获取该连板的股票列表
        stocks = self.get_realtime_board_stocks(board_type, timeout)
        
        # 返回数量和列表
        count = len(stocks)
        
        return count, stocks
    
    def get_realtime_index_trend(self, stock_id="801900", time="15:00", timeout=None):
        """
        获取实时指数趋势数据（昨日涨停今日表现、昨日断板今日表现等）
        
        Args:
            stock_id: 指数代码
                - 801900: 昨日涨停今日表现
                - 801903: 昨日断板今日表现
                - 其他指数代码
            time: 时间点，格式"HH:MM"，默认"15:00"（收盘）
            timeout: 超时时间（秒），默认60秒
            
        Returns:
            dict: 包含指数趋势数据
                - stock_id: 指数代码
                - date: 日期
                - time: 时间
                - value: 指数值
                - change_pct: 涨跌幅 (%)
                - intraday_data: 分时数据列表
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取昨日涨停今日表现
            data = crawler.get_realtime_index_trend(stock_id="801900")
            print(f"昨日涨停今表现: {data['value']}")
            
            # 获取昨日断板今日表现
            data = crawler.get_realtime_index_trend(stock_id="801903")
            print(f"昨日断板今表现: {data['value']}")
        """
        # 构造请求参数
        data_params = {
            "a": "GetTrendIncremental",
            "apiv": "w42",
            "c": "ZhiShuL2Data",
            "StockID": stock_id,
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "Time": time,
            "Day": ""
        }
        
        try:
            response = requests.post(
                self.sector_base_url,
                data=data_params,
                headers=self.sector_headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result or result.get("errcode") != "0":
                print(f"获取实时指数趋势失败: {result.get('errcode', 'unknown error')}")
                return {}
            
            # 解析数据
            # 计算涨跌幅: (收盘价 - 昨收价) / 昨收价 * 100
            trend_data = result.get("trend", [])
            preclose_px = result.get("preclose_px", 0)
            
            if trend_data and len(trend_data) > 0:
                close_price = trend_data[0][1]  # 收盘价
                change_pct = (close_price - preclose_px) / preclose_px * 100 if preclose_px != 0 else 0
            else:
                change_pct = 0
            
            # 返回格式可能包含分时数据
            return {
                "stock_id": stock_id,
                "date": result.get("day", ""),
                "time": time,
                "value": change_pct,  # 使用计算后的涨跌幅
                "change_pct": change_pct,
                "intraday_data": result.get("trend", []),
                "raw_data": result
            }
            
        except Exception as e:
            print(f"请求实时指数趋势失败: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def get_realtime_index_list(self, stock_ids=None, timeout=None):
        """
        获取实时指数列表数据（批量获取多个指数）
        
        Args:
            stock_ids: 指数代码列表，默认获取主要指数
                - SH000001: 上证指数
                - SZ399001: 深证成指
                - SZ399006: 创业板指
                - SH000688: 科创50
            timeout: 超时时间（秒），默认60秒
            
        Returns:
            dict: 包含各指数数据
                - indexes: 指数列表
                    - stock_id: 指数代码
                    - name: 指数名称
                    - value: 最新值
                    - change_pct: 涨跌幅 (%)
                    - change_amount: 涨跌额
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取主要指数
            data = crawler.get_realtime_index_list()
            for index in data['indexes']:
                print(f"{index['name']}: {index['change_pct']:.2f}%")
        """
        if stock_ids is None:
            stock_ids = ["SH000001", "SZ399001", "SZ399006", "SH000688"]
        
        # 构造请求参数
        stock_id_list = ",".join(stock_ids)
        data_params = {
            "a": "RefreshStockList",
            "c": "UserSelectStock",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "Token": "",  # 可能需要token，但测试时可以为空
            "apiv": "w42",
            "StockIDList": stock_id_list,
            "UserID": ""
        }
        
        try:
            response = requests.post(
                self.sector_base_url,
                data=data_params,
                headers=self.sector_headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result or result.get("errcode") != "0":
                print(f"获取实时指数列表失败: {result.get('errcode', 'unknown error')}")
                return {}
            
            # 解析数据
            indexes = []
            stock_list = result.get("StockList", [])
            
            for stock in stock_list:
                index_data = {
                    "stock_id": stock.get("StockID", ""),
                    "name": stock.get("prod_name", ""),
                    "value": float(stock.get("last_px", 0)),
                    "change_pct": float(stock.get("increase_rate", "0").replace("%", "")),
                    "change_amount": float(stock.get("increase_amount", 0)),
                    "turnover": int(stock.get("turnover", 0))
                }
                indexes.append(index_data)
            
            return {
                "indexes": indexes,
                "raw_data": result
            }
            
        except Exception as e:
            print(f"请求实时指数列表失败: {e}")
            import traceback
            traceback.print_exc()
            return {}

    def get_realtime_sharp_withdrawal(self, timeout=None):
        """
        获取实时大幅回撤股票数据
        
        Args:
            timeout: 超时时间（秒），默认60秒
            
        Returns:
            dict: 包含大幅回撤数据
                - date: 日期
                - count: 大幅回撤股票数量
                - stocks: 股票列表，每个股票包含：
                    - stock_code: 股票代码
                    - stock_name: 股票名称
                    - board_type: 连板类型
                    - tag: 标签（如"游资"）
                    - latest_price: 最新价
                    - change_pct: 涨跌幅 (%)
                    - pullback_pct: 回撤幅度 (%)
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取实时大幅回撤数据
            data = crawler.get_realtime_sharp_withdrawal()
            print(f"日期: {data['date']}")
            print(f"大幅回撤: {data['count']}只")
            
            for stock in data['stocks']:
                print(f"{stock['stock_name']}: 回撤{stock['pullback_pct']:.2f}%")
        """
        # 构造请求参数
        data_params = {
            "Order": "0",
            "a": "SharpWithdrawalList",
            "st": "20",
            "c": "HomeDingPan",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "Index": "0",
            "apiv": "w42",
            "Type": "5"
        }
        
        try:
            response = requests.post(
                self.sector_base_url,
                data=data_params,
                headers=self.sector_headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result or result.get("errcode") != "0":
                print(f"获取实时大幅回撤数据失败: {result.get('errcode', 'unknown error')}")
                return {}
            
            # 解析数据
            # info 格式: [["股票代码", "股票名称", 连板类型, "标签", 最新价, 涨跌幅, 回撤幅度], ...]
            # 示例: [["002201","九鼎新材",1,"游资",12.6,-15.6062,-9.61]]
            info = result.get("info", [])
            count = result.get("num", 0)
            date_str = result.get("date", "")
            
            stocks = []
            for stock_data in info:
                if len(stock_data) >= 7:
                    stock_info = {
                        "stock_code": stock_data[0],
                        "stock_name": stock_data[1],
                        "board_type": stock_data[2],
                        "tag": stock_data[3],
                        "latest_price": float(stock_data[4]),
                        "change_pct": float(stock_data[5]),
                        "pullback_pct": float(stock_data[6])
                    }
                    stocks.append(stock_info)
            
            return {
                "date": date_str,
                "count": count,
                "stocks": stocks,
                "raw_data": result
            }
            
        except Exception as e:
            print(f"请求实时大幅回撤数据失败: {e}")
            import traceback
            traceback.print_exc()
            return {}
            data = crawler.get_realtime_rise_fall_analysis()
            print(f"日期: {data['date']}")
            print(f"涨停: {data['limit_up_count']}只")
            print(f"跌停: {data['limit_down_count']}只")
            print(f"炸板率: {data['blown_limit_up_rate']:.2f}%")
            print(f"昨日涨停今表现: {data['yesterday_limit_up_performance']:.2f}%")

    def get_realtime_rise_fall_analysis(self, timeout=None):
        """
        获取实时涨跌分析数据

        Args:
            timeout: 超时时间（秒），默认60秒

        Returns:
            dict: 包含涨跌分析数据
                - date: 日期
                - limit_up_count: 涨停数
                - limit_down_count: 跌停数
                - blown_limit_up_count: 炸板数
                - broken_limit_up_count: 破板数
                - blown_limit_up_rate: 炸板率 (%)
                - yesterday_limit_up_performance: 昨日涨停今表现 (%)
                - yesterday_broken_performance: 昨日断板今日表现 (%)
                - raw_data: 原始数据

        示例:
            crawler = KaipanlaCrawler()

            # 获取实时涨跌分析
            data = crawler.get_realtime_rise_fall_analysis()
            print(f"日期: {data['date']}")
            print(f"涨停: {data['limit_up_count']}只")
            print(f"跌停: {data['limit_down_count']}只")
            print(f"炸板率: {data['blown_limit_up_rate']:.2f}%")
            print(f"昨日涨停今表现: {data['yesterday_limit_up_performance']:.2f}%")
        """
        # 构造请求参数
        data_params = {
            "a": "RiseFallAnalysis",
            "st": "250",
            "c": "HisHomeDingPan",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "Index": "0",
            "apiv": "w42"
        }
        
        try:
            response = requests.post(
                self.base_url,
                data=data_params,
                headers=self.headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result or result.get("errcode") != "0":
                print(f"获取实时涨跌分析失败: {result.get('errcode', 'unknown error')}")
                return {}
            
            # 解析数据
            # info 格式: [[涨停数, 跌停数, 破板数, 炸板数, 炸板率, 昨日涨停今表现, 日期], ...]
            # 示例: [[78,4,72,8,24.2718,25,"2026-01-21"],[53,16,48,5,22.0588,15,"2026-01-20"]]
            info = result.get("info", [])
            
            if not info or len(info) < 1:
                print("未获取到涨跌分析数据")
                return {}
            
            # 取第一条数据（最新日期）
            latest = info[0]
            
            if len(latest) < 7:
                print(f"数据格式不完整: {latest}")
                return {}
            
            # 解析字段
            limit_up_count = int(latest[0])  # 涨停数
            limit_down_count = int(latest[1])  # 跌停数
            broken_limit_up_count = int(latest[2])  # 破板数
            blown_limit_up_count = int(latest[3])  # 炸板数
            blown_limit_up_rate = float(latest[4])  # 炸板率 (%)
            # yesterday_limit_up_performance = float(latest[5])  # 昨日涨停今表现 (%) - 这个值不准确
            date_str = latest[6]  # 日期
            
            # 使用正确的接口获取昨日涨停今表现 (801900)
            zt_data = self.get_realtime_index_trend(stock_id="801900", time="15:00", timeout=timeout)
            yesterday_limit_up_performance = zt_data.get("change_pct", 0.0) if zt_data else 0.0
            
            # 使用正确的接口获取昨日断板今日表现 (801903)
            pb_data = self.get_realtime_index_trend(stock_id="801903", time="15:00", timeout=timeout)
            yesterday_broken_performance = pb_data.get("change_pct", 0.0) if pb_data else 0.0
            
            return {
                "date": date_str,
                "limit_up_count": limit_up_count,
                "limit_down_count": limit_down_count,
                "blown_limit_up_count": blown_limit_up_count,
                "broken_limit_up_count": broken_limit_up_count,
                "blown_limit_up_rate": blown_limit_up_rate,
                "yesterday_limit_up_performance": yesterday_limit_up_performance,
                "yesterday_broken_performance": yesterday_broken_performance,
                "raw_data": info
            }
            
        except Exception as e:
            print(f"请求实时涨跌分析失败: {e}")
            import traceback
            traceback.print_exc()
            return {}
    

    def get_sector_intraday(self, sector_code, date=None, timeout=300):
        """
        获取板块分时数据
        
        Args:
            sector_code: 板块代码，如 "801346"（半导体）
            date: 日期，格式YYYY-MM-DD，默认为None（获取实时数据）
            timeout: 超时时间（秒），默认60秒
            
        Returns:
            dict: 包含板块分时数据
                - sector_code: 板块代码
                - date: 日期
                - open: 开盘价
                - close: 收盘价
                - high: 最高价
                - low: 最低价
                - preclose: 昨收价
                - data: DataFrame，包含分时数据
                    - time: 时间（HH:MM格式）
                    - price: 价格
                    - volume: 成交量（手）
                    - turnover: 成交额（元）
                    - trend: 涨跌趋势（1=上涨, 0=下跌, 2=平盘）
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取历史分时数据
            data = crawler.get_sector_intraday("801346", "2026-01-16")
            print(f"板块: {data['sector_code']}")
            print(f"收盘价: {data['close']}")
            print(f"涨跌幅: {((data['close'] - data['preclose']) / data['preclose'] * 100):.2f}%")
            
            # 分析分时数据
            df = data['data']
            print(f"总成交量: {df['volume'].sum():,} 手")
        """
        is_realtime = date is None
        
        if is_realtime:
            # 实时数据
            url = self.sector_base_url
            headers = self.sector_headers
            display_date = datetime.now().strftime("%Y-%m-%d")
        else:
            # 历史数据
            url = self.base_url
            headers = self.headers
            display_date = date
        
        # 构造请求参数
        data_params = {
            "a": "GetTrendIncremental",  # 修正：使用正确的API方法
            "c": "ZhiShuL2Data",
            "PhoneOSNew": "1",
            "DeviceID": "e78ba169-6c03-3faf-8e5e-a72f8411a8eb",  # 使用固定的DeviceID
            "VerSion": "5.21.0.2",
            "apiv": "w42",
            "StockID": sector_code,
            "Day": date if date else ""
        }
        
        try:
            # 添加请求延迟，防止达到速率限制
            time.sleep(0.5)  # 500毫秒延迟
            
            response = requests.post(
                url,
                data=data_params,
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            
            # 检查响应内容是否为空或无效
            if not response.text.strip():
                print(f"请求板块分时数据失败 ({sector_code}): 响应内容为空")
                return {}
            
            try:
                result = response.json()
            except (ValueError, requests.exceptions.JSONDecodeError) as json_error:
                print(f"请求板块分时数据失败 ({sector_code}): JSON解析错误 - {json_error}")
                print(f"响应内容: {response.text[:200]}...")  # 显示前200个字符
                return {}
            
            if not result or result.get("errcode") != "0":
                error_code = result.get('errcode', 'unknown error') if result else 'empty response'
                print(f"获取板块分时数据失败: {error_code}")
                return {}
            
            # 解析基本信息
            # trend 数组格式: [时间, 价格, 成交量, 成交额, 涨跌趋势]
            # 示例: ["09:31", 1234.56, 12345, 123456789, 1]
            trend_data = result.get("trend", [])
            
            if not trend_data:
                print(f"未获取到板块 {sector_code} 的分时数据")
                return {}
            
            # 解析分时数据
            records = []
            for item in trend_data:
                if len(item) >= 5:
                    record = {
                        "time": item[0],
                        "price": float(item[1]),
                        "volume": int(item[2]),
                        "turnover": float(item[3]),
                        "trend": int(item[4])  # 1=上涨, 0=下跌, 2=平盘
                    }
                    records.append(record)
            
            df = pd.DataFrame(records)
            
            # 计算开高低收
            if len(df) > 0:
                open_price = df['price'].iloc[0]
                close_price = df['price'].iloc[-1]
                high_price = df['price'].max()
                low_price = df['price'].min()
            else:
                open_price = close_price = high_price = low_price = 0
            
            # 获取昨收价（从result中获取，如果没有则用开盘价估算）
            preclose = float(result.get("preclose", open_price))
            
            return {
                "sector_code": sector_code,
                "date": result.get("date", display_date),
                "open": open_price,
                "close": close_price,
                "high": high_price,
                "low": low_price,
                "preclose": preclose,
                "data": df
            }
            
        except Exception as e:
            print(f"请求板块分时数据失败 ({sector_code}): {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def get_sector_volume_turnover(self, sector_code, date=None, timeout=300):
        """
        获取板块分时成交量和成交额数据
        
        Args:
            sector_code: 板块代码，如 "803023"（AI应用）
            date: 日期，格式YYYY-MM-DD，默认为None（获取实时数据）
            timeout: 超时时间（秒），默认300秒
            
        Returns:
            dict: 包含板块分时成交量/成交额数据
                - sector_code: 板块代码
                - date: 日期
                - data: DataFrame，包含分时数据
                    - time: 时间（HH:MM格式）
                    - volume: 成交量（可能单位为手或股）
                    - turnover: 成交额（元）
                    - unknown: 未知字段
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取实时数据
            data = crawler.get_sector_volume_turnover("803023")
            print(f"板块: {data['sector_code']}")
            df = data['data']
            print(f"总成交额: {df['turnover'].sum() / 1e8:.2f} 亿")
            
            # 获取历史数据
            data = crawler.get_sector_volume_turnover("803023", "2026-02-06")
            print(f"历史成交额: {data['data']['turnover'].sum() / 1e8:.2f} 亿")
        """
        is_realtime = date is None
        
        if is_realtime:
            # 实时数据
            url = self.sector_base_url
            headers = self.sector_headers
            display_date = datetime.now().strftime("%Y-%m-%d")
        else:
            # 历史数据
            url = self.base_url
            headers = self.headers
            display_date = date
        
        # 构造请求参数
        data_params = {
            "a": "GetVolTurIncremental",
            "c": "ZhiShuL2Data",
            "PhoneOSNew": "1",
            "DeviceID": "e78ba169-6c03-3faf-8e5e-a72f8411a8eb",
            "VerSion": "5.21.0.2",
            "apiv": "w42",
            "StockID": sector_code,
            "Day": date if date else ""
        }
        
        try:
            # 添加请求延迟，防止达到速率限制
            time.sleep(0.5)  # 500毫秒延迟
            
            response = requests.post(
                url,
                data=data_params,
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            
            # 检查响应内容是否为空或无效
            if not response.text.strip():
                print(f"请求板块成交量/成交额数据失败 ({sector_code}): 响应内容为空")
                return {}
            
            try:
                result = response.json()
            except (ValueError, requests.exceptions.JSONDecodeError) as json_error:
                print(f"请求板块成交量/成交额数据失败 ({sector_code}): JSON解析错误 - {json_error}")
                print(f"响应内容: {response.text[:200]}...")
                return {}
            
            if not result or result.get("errcode") != "0":
                error_code = result.get('errcode', 'unknown error') if result else 'empty response'
                print(f"获取板块成交量/成交额数据失败: {error_code}")
                return {}
            
            # 解析数据
            # volumeturnover 数组格式: [时间, 成交量(?), 成交额, 未知字段]
            # 示例: ["09:30", 2677717, 4343603936, 2]
            volume_turnover_data = result.get("volumeturnover", [])
            
            if not volume_turnover_data:
                print(f"未获取到板块 {sector_code} 的成交量/成交额数据")
                return {}
            
            # 解析分时数据
            records = []
            for item in volume_turnover_data:
                if len(item) >= 3:
                    record = {
                        "time": item[0],
                        "volume": int(item[1]) if item[1] else 0,  # 可能是成交量
                        "turnover": float(item[2]) if item[2] else 0.0,  # 成交额（元）
                        "unknown": int(item[3]) if len(item) > 3 and item[3] else 0  # 未知字段
                    }
                    records.append(record)
            
            df = pd.DataFrame(records)
            
            return {
                "sector_code": result.get("code", sector_code),
                "date": result.get("day", display_date),
                "data": df
            }
            
        except Exception as e:
            print(f"请求板块成交量/成交额数据失败 ({sector_code}): {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def get_stock_intraday(self, stock_code, date=None, timeout=300):
        """
        获取个股分时数据
        
        Args:
            stock_code: 股票代码，如 "002498"
            date: 日期，格式YYYY-MM-DD，默认为None（获取实时数据）
            timeout: 超时时间（秒），默认60秒
            
        Returns:
            dict: 包含个股分时数据
                - stock_code: 股票代码
                - date: 日期
                - total_main_inflow: 主力净流入总额（元）
                - total_main_outflow: 主力净流出总额（元）
                - data: DataFrame，包含分时数据
                    - time: 时间（HH:MM格式）
                    - price: 价格
                    - avg_price: 均价
                    - volume: 成交量（手）
                    - turnover: 成交额（元）
                    - main_net_inflow: 主力净流入（元）
                    - flag: 价格标志（1=现价>=均价, 0=现价<均价, 2=涨停）
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取历史分时数据
            data = crawler.get_stock_intraday("002498", "2026-01-16")
            print(f"股票: {data['stock_code']}")
            print(f"主力净额: {(data['total_main_inflow'] + data['total_main_outflow']) / 1e8:.2f} 亿")
            
            # 分析分时数据
            df = data['data']
            print(f"总成交量: {df['volume'].sum():,} 手")
            print(f"总成交额: {df['turnover'].sum() / 1e8:.2f} 亿")
        """
        is_realtime = date is None
        
        if is_realtime:
            # 实时数据
            url = self.sector_base_url
            headers = self.sector_headers
            display_date = datetime.now().strftime("%Y-%m-%d")
        else:
            # 历史数据
            url = self.base_url
            headers = self.headers
            display_date = date
        
        # 判断是否为大盘指数
        is_index = stock_code.startswith('SH') and stock_code.endswith('1') or stock_code.startswith('SZ') and '399' in stock_code
        
        # 构造请求参数
        if is_index:
            if is_realtime:
                # 大盘指数实时数据使用特殊的API
                data_params = {
                    "a": "GetZstrend",
                    "apiv": "w42",
                    "c": "StockL2Data",
                    "StockID": stock_code,
                    "PhoneOSNew": "1",
                    "UserID": "0",
                    "DeviceID": "e78ba169-6c03-3faf-8e5e-a72f8411a8eb",
                    "VerSion": "5.21.0.2",
                    "Token": "0"
                }
            else:
                # 大盘指数历史数据使用历史API
                url = "https://apphis.longhuvip.com/w1/api/index.php"
                headers = self.headers
                data_params = {
                    "a": "GetStockTrend",
                    "c": "StockL2History",
                    "PhoneOSNew": "1",
                    "DeviceID": "e78ba169-6c03-3faf-8e5e-a72f8411a8eb",
                    "VerSion": "5.21.0.2",
                    "Token": "0",
                    "apiv": "w42",
                    "StockID": stock_code,
                    "UserID": "0",
                    "Day": date.replace('-', '')  # 格式化日期为YYYYMMDD
                }
        else:
            # 个股数据使用历史API（实时和历史都用同一个接口）
            url = "https://apphis.longhuvip.com/w1/api/index.php"
            headers = self.headers
            data_params = {
                "a": "GetStockTrend",
                "apiv": "w42",
                "c": "StockL2History",
                "StockID": stock_code,
                "PhoneOSNew": "1",
                "UserID": "0",
                "DeviceID": "e78ba169-6c03-3faf-8e5e-a72f8411a8eb",
                "VerSion": "5.21.0.2",
                "Token": "0"
            }
            if date:
                data_params["Day"] = date.replace('-', '')  # 格式化日期为YYYYMMDD
        
        try:
            # 添加请求延迟，防止达到速率限制
            time.sleep(0.5)  # 500毫秒延迟
            
            response = requests.post(
                url,
                data=data_params,
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            
            # 检查响应内容是否为空或无效
            if not response.text.strip():
                print(f"请求个股分时数据失败 ({stock_code}): 响应内容为空")
                return {}
            
            try:
                result = response.json()
            except (ValueError, requests.exceptions.JSONDecodeError) as json_error:
                print(f"请求个股分时数据失败 ({stock_code}): JSON解析错误 - {json_error}")
                print(f"响应内容: {response.text[:200]}...")  # 显示前200个字符
                return {}
            
            if not result or result.get("errcode") != "0":
                error_code = result.get('errcode', 'unknown error') if result else 'empty response'
                print(f"获取个股分时数据失败: {error_code}")
                return {}
            
            # 解析分时数据
            trend_data = result.get("trend", [])
            
            if not trend_data:
                print(f"未获取到股票 {stock_code} 的分时数据")
                return {}
            
            # 解析分时数据
            records = []
            
            if is_index:
                # 大盘指数数据格式: [时间, 价格, 均价, 成交量, flag]
                # 示例: ["09:30", 4040.3, 4049.196, 6773713, 1]
                for item in trend_data:
                    if len(item) >= 5:
                        record = {
                            "time": item[0],
                            "price": float(item[1]),
                            "avg_price": float(item[2]),
                            "volume": int(item[3]),
                            "turnover": 0.0,  # 大盘指数没有成交额
                            "main_net_inflow": 0.0,  # 大盘指数没有主力净流入
                            "flag": int(item[4])
                        }
                        records.append(record)
            else:
                # 个股数据格式（历史和实时）:
                # 历史: [时间, 价格, 均价, 成交量, flag] - 5个字段，无主力净流入
                # 实时: [时间, 价格, 均价, 成交量, 成交额, 主力净流入, flag] - 7个字段
                for item in trend_data:
                    if len(item) >= 7:
                        # 实时数据格式（7个字段）
                        record = {
                            "time": item[0],
                            "price": float(item[1]),
                            "avg_price": float(item[2]),
                            "volume": int(item[3]),
                            "turnover": float(item[4]),
                            "main_net_inflow": float(item[5]),
                            "flag": int(item[6])
                        }
                        records.append(record)
                    elif len(item) >= 5:
                        # 历史数据格式（5个字段，无主力净流入）
                        record = {
                            "time": item[0],
                            "price": float(item[1]),
                            "avg_price": float(item[2]),
                            "volume": int(item[3]),
                            "turnover": 0.0,  # 历史数据没有分时成交额
                            "main_net_inflow": 0.0,  # 历史数据没有主力净流入
                            "flag": int(item[4])
                        }
                        records.append(record)
            
            df = pd.DataFrame(records)
            
            # 计算主力资金总额（仅对个股有效）
            if is_index:
                total_main_inflow = 0.0
                total_main_outflow = 0.0
            else:
                # 检查是否有主力净流入列且有非零数据
                if 'main_net_inflow' in df.columns and not df.empty:
                    # 确保main_net_inflow列存在且有数据
                    main_inflow_data = df['main_net_inflow'].fillna(0)  # 填充NaN为0
                    # 检查是否所有值都为0（历史数据的情况）
                    if main_inflow_data.abs().sum() > 0:
                        total_main_inflow = main_inflow_data[main_inflow_data > 0].sum()
                        total_main_outflow = main_inflow_data[main_inflow_data < 0].sum()
                    else:
                        # 历史数据没有主力净流入
                        total_main_inflow = 0.0
                        total_main_outflow = 0.0
                else:
                    # 如果没有主力净流入数据，设为0
                    total_main_inflow = 0.0
                    total_main_outflow = 0.0
            
            return {
                "stock_code": stock_code,
                "date": result.get("day", display_date),
                "total_turnover": result.get("total_turnover", 0),  # 添加总成交额
                "preclose_px": result.get("preclose_px", 0),  # 昨收价
                "begin_px": result.get("begin_px", 0),  # 开盘价
                "lprice": result.get("lprice", 0),  # 最低价
                "hprice": result.get("hprice", 0),  # 最高价
                "px_change_rate": result.get("px_change_rate", 0),  # 涨跌幅
                "total_main_inflow": total_main_inflow,
                "total_main_outflow": total_main_outflow,
                "data": df
            }
            
        except Exception as e:
            print(f"请求个股分时数据失败 ({stock_code}): {e}")
            import traceback
            traceback.print_exc()
            return {}

    def get_stock_big_order_intraday(self, stock_code, date=None, timeout=300):
        """
        获取个股大单净额分时数据（支持历史数据）
        
        Args:
            stock_code: 股票代码，如 "688223"
            date: 日期，格式YYYY-MM-DD，默认为None（获取实时数据）
            timeout: 超时时间（秒），默认300秒
            
        Returns:
            dict: 包含大单净额分时数据
                - stock_code: 股票代码
                - date: 日期
                - big_order_buy_total: 大单买入总额
                - big_order_sell_total: 大单卖出总额
                - big_order_net_total: 大单净额总计
                - data: DataFrame，包含大单净额分时数据
                    - time: 时间（HH:MM格式）
                    - unknown1: 未知字段1
                    - big_order_net: 大单净额
                    - intraday_buy: 分时买入
                    - intraday_sell: 分时卖出
                    - buy_orders: 买单数
                    - sell_orders: 卖单数
                    - unknown2-7: 其他未知字段
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取历史大单净额数据
            data = crawler.get_stock_big_order_intraday("688223", "2026-02-04")
            print(f"股票: {data['stock_code']}")
            print(f"大单买入总额: {data['big_order_buy_total']:,.0f}")
            print(f"大单卖出总额: {data['big_order_sell_total']:,.0f}")
            print(f"大单净额总计: {data['big_order_net_total']:,.0f}")
            
            # 分析分时大单净额数据
            df = data['data']
            print(f"分时大单净额汇总: {df['big_order_net'].sum():,.0f}")
        """
        is_realtime = date is None
        
        if is_realtime:
            # 实时数据 - 使用新的实时大单接口
            url = self.sector_base_url
            headers = self.sector_headers
            display_date = datetime.now().strftime("%Y-%m-%d")
            
            # 构造请求参数（实时数据）
            data_params = {
                "a": "GetMainMonitor_Trend_w30",
                "c": "StockL2Data",
                "PhoneOSNew": "1",
                "DeviceID": "e78ba169-6c03-3faf-8e5e-a72f8411a8eb",
                "VerSion": "5.21.0.2",
                "Token": "0daffcf404348e2fb714795ba5bdff02",
                "Money": "2",
                "apiv": "w42",
                "StockID": stock_code,
                "UserID": "4315515",
                "IsBS": "0"
            }
        else:
            # 历史数据 - 使用新的历史大单接口
            url = "https://apphis.longhuvip.com/w1/api/index.php"
            headers = self.headers
            display_date = date
            
            # 构造请求参数（历史数据）
            data_params = {
                "a": "GetMainMonitor_Trend_w30",
                "c": "StockL2History",
                "PhoneOSNew": "1",
                "DeviceID": "e78ba169-6c03-3faf-8e5e-a72f8411a8eb",
                "VerSion": "5.21.0.2",
                "Token": "0daffcf404348e2fb714795ba5bdff02",
                "Date": date,
                "Money": "0",
                "apiv": "w42",
                "StockID": stock_code,
                "UserID": "4315515",
                "IsBS": "0"
            }
        
        try:
            # 添加请求延迟，防止达到速率限制
            time.sleep(0.5)  # 500毫秒延迟
            
            response = requests.post(
                url,
                data=data_params,
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            
            # 检查响应内容是否为空或无效
            if not response.text.strip():
                print(f"请求大单净额数据失败 ({stock_code}): 响应内容为空")
                return {}
            
            try:
                result = response.json()
            except (ValueError, requests.exceptions.JSONDecodeError) as json_error:
                print(f"请求大单净额数据失败 ({stock_code}): JSON解析错误 - {json_error}")
                print(f"响应内容: {response.text[:200]}...")
                return {}
            
            if not result or result.get("errcode") != "0":
                error_code = result.get('errcode', 'unknown error') if result else 'empty response'
                print(f"获取大单净额数据失败: {error_code}")
                return {}
            
            # 解析大单净额数据
            trend_data = result.get("trend", [])
            
            if not trend_data:
                print(f"未获取到股票 {stock_code} 的大单净额数据")
                return {}
            
            # 获取大单买卖总额（仅历史数据有）
            big_order_buy_total = 0
            big_order_sell_total = 0
            big_order_net_total = 0
            
            if not is_realtime:
                # 历史数据包含ZJB（大单买）和ZJS（大单卖）字段
                big_order_buy_total = result.get("ZJB", 0)  # 大单买
                big_order_sell_total = result.get("ZJS", 0)  # 大单卖（通常为负数）
                big_order_net_total = big_order_buy_total + big_order_sell_total  # 净额
            
            # 解析分时大单净额数据
            records = []
            
            # 实时和历史数据格式相同
            # 数据格式: [时间, 未知1, 净额, 分时买, 分时卖, 买单, 卖单, 未知2-7...]
            # 示例: ["09:30", 156, -466657, 32769873, -33236530, 61, 65, 4668985, 4735275, 14206167, 18563706, 23892817, 9343713]
            for item in trend_data:
                if len(item) >= 13:
                    record = {
                        "time": item[0],
                        "unknown1": item[1],
                        "big_order_net": float(item[2]),  # 大单净额
                        "intraday_buy": float(item[3]),   # 分时买入
                        "intraday_sell": float(item[4]),  # 分时卖出
                        "buy_orders": int(item[5]),       # 买单数
                        "sell_orders": int(item[6]),      # 卖单数
                        "unknown2": item[7],
                        "unknown3": item[8],
                        "unknown4": item[9],
                        "unknown5": item[10],
                        "unknown6": item[11],
                        "unknown7": item[12]
                    }
                    records.append(record)
            
            df = pd.DataFrame(records)
            
            return {
                "stock_code": stock_code,
                "date": result.get("date", display_date),
                "big_order_buy_total": big_order_buy_total,
                "big_order_sell_total": big_order_sell_total,
                "big_order_net_total": big_order_net_total,
                "data": df
            }
            
        except Exception as e:
            print(f"请求大单净额数据失败 ({stock_code}): {e}")
            import traceback
            traceback.print_exc()
            return {}

    def get_index_intraday(self, index_code="SH000001", date=None, timeout=300):
        """
        获取大盘指数分时数据
        
        Args:
            index_code: 指数代码，默认"SH000001"（上证指数）
                       其他常用指数：
                       - SH000001: 上证指数
                       - SZ399001: 深证成指
                       - SZ399006: 创业板指
                       - SH000300: 沪深300
            date: 日期，格式YYYY-MM-DD，默认为None（获取实时数据）
            timeout: 超时时间（秒），默认60秒
            
        Returns:
            dict: 包含指数分时数据
                - index_code: 指数代码
                - index_name: 指数名称
                - date: 日期
                - open: 开盘价
                - close: 收盘价
                - high: 最高价
                - low: 最低价
                - preclose: 昨收价
                - change_pct: 涨跌幅（%）
                - data: DataFrame，包含分时数据
                    - time: 时间（HH:MM格式）
                    - timestamp: 时间戳（datetime对象）
                    - price: 价格
                    - pct_change: 涨跌幅（相对昨收，%）
                    - volume: 成交量（手）
                    - turnover: 成交额（元）
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取上证指数实时分时数据
            data = crawler.get_index_intraday("SH000001")
            print(f"指数: {data['index_name']}")
            print(f"当前价: {data['close']:.2f}")
            print(f"涨跌幅: {data['change_pct']:.2f}%")
            
            # 获取历史分时数据
            data = crawler.get_index_intraday("SH000001", "2026-01-20")
            
            # 分析分时数据
            df = data['data']
            print(f"最高涨幅: {df['pct_change'].max():.2f}%")
            print(f"最低涨幅: {df['pct_change'].min():.2f}%")
            
            # 识别关键变盘点
            # 找到最低点
            min_idx = df['pct_change'].idxmin()
            print(f"最低点时间: {df.loc[min_idx, 'time']}, 涨跌幅: {df.loc[min_idx, 'pct_change']:.2f}%")
        """
        is_realtime = date is None
        
        if is_realtime:
            # 实时数据：使用 apphwhq.longhuvip.com
            url = self.sector_base_url
            headers = self.sector_headers
            display_date = datetime.now().strftime("%Y-%m-%d")
            
            # 构造请求参数（实时数据）
            data_params = {
                "a": "GetStockTrendIncremental",
                "c": "StockL2Data",
                "PhoneOSNew": "1",
                "DeviceID": "e78ba169-6c03-3faf-8e5e-a72f8411a8eb",
                "VerSion": "5.21.0.2",
                "Token": "0daffcf404348e2fb714795ba5bdff02",
                "apiv": "w42",
                "Type": "1",
                "StockID": index_code,
                "UserID": "4315515"
            }
        else:
            # 历史数据：使用 apphis.longhuvip.com
            url = self.base_url
            headers = self.headers
            display_date = date
            
            # 构造请求参数（历史数据）
            data_params = {
                "a": "GetStockTrend",
                "apiv": "w42",
                "c": "StockL2History",
                "StockID": index_code,
                "PhoneOSNew": "1",
                "UserID": "4315515",
                "DeviceID": "e78ba169-6c03-3faf-8e5e-a72f8411a8eb",
                "VerSion": "5.21.0.2",
                "Token": "0daffcf404348e2fb714795ba5bdff02",
                "Day": date.replace('-', '')  # 格式化日期为YYYYMMDD
            }
        
        try:
            response = requests.post(
                url,
                data=data_params,
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result or result.get("errcode") != "0":
                print(f"获取指数分时数据失败: {result.get('errcode', 'unknown error')}")
                return {}
            
            # 解析基本信息
            index_name = result.get("name", "")
            preclose = float(result.get("preclose", 0))
            
            # 解析分时数据
            # 实时和历史数据格式相同
            # trend 数组格式: [时间, 分时白线(价格), 分时黄线(均价), 成交量, 趋势]
            # 示例: ["09:30", 4103.54, 4107.079, 6521790, 1]
            trend_data = result.get("trend", [])
            
            if not trend_data:
                print(f"未获取到指数 {index_code} 的分时数据")
                return {}
            
            # 如果preclose为0，使用开盘价作为参考
            if preclose == 0 and len(trend_data) > 0:
                first_price = float(trend_data[0][1])
                # 尝试从前一天的收盘价推算（假设开盘价与昨收价接近）
                # 或者直接使用开盘价作为基准
                preclose = first_price
                print(f"警告: API未返回昨收价，使用开盘价 {preclose:.2f} 作为参考")
            
            # 解析分时数据
            records = []
            for item in trend_data:
                if len(item) >= 5:
                    price = float(item[1])  # 分时白线（价格）
                    avg_price = float(item[2])  # 分时黄线（均价）
                    
                    # 计算涨跌幅（相对昨收）
                    pct_change = ((price - preclose) / preclose * 100) if preclose > 0 else 0
                    
                    # 构造时间戳
                    time_str = item[0]
                    try:
                        timestamp = datetime.strptime(f"{display_date} {time_str}", "%Y-%m-%d %H:%M")
                    except:
                        timestamp = None
                    
                    record = {
                        "time": time_str,
                        "timestamp": timestamp,
                        "price": price,
                        "avg_price": avg_price,
                        "pct_change": pct_change,
                        "volume": int(item[3]) if len(item) > 3 else 0,
                        "trend": int(item[4]) if len(item) > 4 else 0  # 趋势标志
                    }
                    records.append(record)
            
            df = pd.DataFrame(records)
            
            # 计算开高低收
            if len(df) > 0:
                open_price = df['price'].iloc[0]
                close_price = df['price'].iloc[-1]
                high_price = df['price'].max()
                low_price = df['price'].min()
                change_pct = ((close_price - preclose) / preclose * 100) if preclose > 0 else 0
            else:
                open_price = close_price = high_price = low_price = 0
                change_pct = 0
            
            return {
                "index_code": index_code,
                "index_name": index_name,
                "date": result.get("date", display_date),
                "open": open_price,
                "close": close_price,
                "high": high_price,
                "low": low_price,
                "preclose": preclose,
                "change_pct": change_pct,
                "data": df
            }
            
        except Exception as e:
            print(f"请求指数分时数据失败 ({index_code}): {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def get_plate_news(self, plate_id: str, index: int = 0, page_size: int = 30, timeout: int = 1600):
        """获取指定板块的最新要闻
        
        Args:
            plate_id: 板块代码，如 "801070"（化工）
            index: 分页索引，默认0（第一页）
            page_size: 每页数量，默认30条
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            dict: 包含板块要闻列表
                - plate_id: 板块代码
                - news_list: 要闻列表，每条包含：
                    - id: 新闻ID
                    - title: 标题
                    - content: 内容
                    - time: 发布时间（时间戳）
                    - datetime: 发布时间（datetime对象）
                    - type: 类型（1=快讯，2=新闻）
                - total_count: 总数量
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取化工板块要闻
            news = crawler.get_plate_news("801070")
            
            # 遍历要闻
            for item in news['news_list']:
                print(f"[{item['datetime']}] {item['content'][:50]}...")
            
            # 获取第二页
            news_page2 = crawler.get_plate_news("801070", index=30)
        """
        # 构造请求参数
        data_params = {
            "a": "GetPlateNewsList",
            "st": str(page_size),
            "c": "APPComplexData",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "Index": str(index),
            "apiv": "w42",
            "PlateID": plate_id
        }
        
        # 使用专门的要闻API地址
        url = "https://apparticle.longhuvip.com/w1/api/index.php"
        
        # 使用专门的headers
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; 23116PN5BC Build/PQ3A.190605.01141736)",
            "Host": "apparticle.longhuvip.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        
        try:
            response = requests.post(
                url,
                data=data_params,
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result or result.get("errcode") != "0":
                print(f"获取板块要闻失败: {result.get('errcode', 'unknown error')}")
                return {
                    "plate_id": plate_id,
                    "news_list": [],
                    "total_count": 0
                }
            
            # 解析要闻列表
            news_list = []
            raw_list = result.get("List", [])
            
            for item in raw_list:
                news_id = item.get("ID", "")
                title = item.get("Title", "")
                content = item.get("Content", "")
                time_timestamp = int(item.get("Time", 0))
                news_type = int(item.get("Type", 1))  # 1=快讯，2=新闻
                
                # 转换时间戳为datetime对象
                try:
                    news_datetime = datetime.fromtimestamp(time_timestamp)
                except:
                    news_datetime = None
                
                news_item = {
                    "id": news_id,
                    "title": title,
                    "content": content,
                    "time": time_timestamp,
                    "datetime": news_datetime,
                    "type": news_type,
                    "type_name": "快讯" if news_type == 1 else "新闻"
                }
                
                news_list.append(news_item)
            
            return {
                "plate_id": plate_id,
                "news_list": news_list,
                "total_count": len(news_list)
            }
            
        except Exception as e:
            print(f"请求板块要闻失败 ({plate_id}): {e}")
            import traceback
            traceback.print_exc()
            return {
                "plate_id": plate_id,
                "news_list": [],
                "total_count": 0
            }
    
    def get_plate_news_dataframe(self, plate_id: str, max_pages: int = 3, page_size: int = 30, timeout: int = 1600):
        """获取指定板块的最新要闻（返回DataFrame格式）
        
        Args:
            plate_id: 板块代码
            max_pages: 最大页数，默认3页
            page_size: 每页数量，默认30条
            timeout: 超时时间（秒）
            
        Returns:
            pd.DataFrame: 包含要闻数据的DataFrame
                - id: 新闻ID
                - title: 标题
                - content: 内容
                - datetime: 发布时间
                - type_name: 类型名称
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取化工板块要闻（最多3页，共90条）
            df = crawler.get_plate_news_dataframe("801070", max_pages=3)
            
            # 查看最新10条
            print(df.head(10))
            
            # 筛选快讯
            flash_news = df[df['type_name'] == '快讯']
        """
        all_news = []
        
        for page in range(max_pages):
            index = page * page_size
            print(f"获取第 {page + 1}/{max_pages} 页...")
            
            result = self.get_plate_news(
                plate_id=plate_id,
                index=index,
                page_size=page_size,
                timeout=timeout
            )
            
            news_list = result.get("news_list", [])
            
            if not news_list:
                print(f"第 {page + 1} 页无数据，停止获取")
                break
            
            all_news.extend(news_list)
            print(f"  获取到 {len(news_list)} 条要闻")
        
        if not all_news:
            return pd.DataFrame()
        
        # 转换为DataFrame
        df = pd.DataFrame(all_news)
        
        # 选择需要的列
        columns = ['id', 'title', 'content', 'datetime', 'type_name']
        df = df[columns]

        # 按时间降序排列
        df = df.sort_values('datetime', ascending=False).reset_index(drop=True)

        print(f"\n[OK] 共获取 {len(df)} 条板块要闻")

        return df

    def get_ths_hot_rank(self, headless=True, wait_time=5, timeout=300, max_rank=50):
        """获取同花顺热榜个股数据

        Args:
            headless: 是否使用无头模式（不显示浏览器窗口）
            wait_time: 页面加载后等待时间（秒）
            timeout: 操作超时时间（秒）
            max_rank: 最大获取排名数，默认50

        Returns:
            pd.Series: index为排名，values为个股名字
        """
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException, NoSuchElementException

        url = "https://eq.10jqka.com.cn/frontend/thsTopRank/index.html#/"

        # 配置ChromeChrome选项
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        driver = None
        try:
            # 初始化浏览器
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(timeout)

            print(f"Accessing THS hot rank page...")
            driver.get(url)

            # 等待页面加载
            print(f"Waiting for page load ({wait_time} seconds)...")
            import time
            time.sleep(wait_time)

            result = {}
            success_count = 0

            # 循环获取指定数量的数据
            for rank in range(1, max_rank + 1):
                try:
                    # 构造XPath - 根据用户提供的结构
                    # 排名: div[1]/div/div[N]/div[1]/div[1]/div
                    # 名字: div[1]/div/div[N]/div[1]/div[2]/span

                    rank_xpath = f'/html/body/div[1]/div/div[3]/div/div[1]/div/div[2]/div[1]/div/div[{rank}]/div[1]/div[1]/div'
                    name_xpath = f'/html/body/div[1]/div/div[3]/div/div[1]/div/div[2]/div[1]/div/div[{rank}]/div[1]/div[2]/span'

                    # 获取排名
                    rank_element = driver.find_element(By.XPATH, rank_xpath)
                    rank_value = rank_element.text.strip()

                    # 获取名字
                    name_element = driver.find_element(By.XPATH, name_xpath)
                    name_value = name_element.text.strip()

                    # 使用排名作为key，名字作为value
                    result[rank] = name_value
                    success_count += 1

                except (NoSuchElementException, Exception) as e:
                    print(f"  Failed to get rank {rank}: {str(e)}")
                    continue

            # 关闭浏览器
            driver.quit()

            if not result:
                print("No data retrieved")
                return pd.Series()

            # 转换为Series，index为排名
            series = pd.Series(result)
            series.index.name = 'Rank'
            series.name = 'Stock Name'

            print(f"\nTotal retrieved: {len(series)} items")
            return series

        except Exception as e:
            print(f"Crawling failed: {str(e)}")
            if driver:
                driver.quit()
            return pd.Series()

    def get_plate_news(self, plate_id: str, index: int = 0, page_size: int = 30, timeout: int = 1600):
        """获取指定板块的最新要闻
        
        Args:
            plate_id: 板块代码，如 "801070"（化工）
            index: 分页索引，默认0（第一页）
            page_size: 每页数量，默认30条
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            dict: 包含板块要闻列表
                - plate_id: 板块代码
                - news_list: 要闻列表，每条包含：
                    - id: 新闻ID
                    - title: 标题
                    - content: 内容
                    - time: 发布时间（时间戳）
                    - datetime: 发布时间（datetime对象）
                    - type: 类型（1=快讯，2=新闻）
                - total_count: 总数量
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取化工板块要闻
            news = crawler.get_plate_news("801070")
            
            # 遍历要闻
            for item in news['news_list']:
                print(f"[{item['datetime']}] {item['content'][:50]}...")
            
            # 获取第二页
            news_page2 = crawler.get_plate_news("801070", index=30)
        """
        # 构造请求参数
        data_params = {
            "a": "GetPlateNewsList",
            "st": str(page_size),
            "c": "APPComplexData",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "Index": str(index),
            "apiv": "w42",
            "PlateID": plate_id
        }
        
        # 使用专门的要闻API地址
        url = "https://apparticle.longhuvip.com/w1/api/index.php"
        
        # 使用sector_headers（与板块相关的接口使用相同的headers）
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; 23116PN5BC Build/PQ3A.190605.01141736)",
            "Host": "apparticle.longhuvip.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        
        try:
            response = requests.post(
                url,
                data=data_params,
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result or result.get("errcode") != "0":
                print(f"获取板块要闻失败: {result.get('errcode', 'unknown error')}")
                return {
                    "plate_id": plate_id,
                    "news_list": [],
                    "total_count": 0
                }
            
            # 解析要闻列表
            news_list = []
            raw_list = result.get("List", [])
            
            for item in raw_list:
                news_id = item.get("ID", "")
                title = item.get("Title", "")
                content = item.get("Content", "")
                time_timestamp = int(item.get("Time", 0))
                news_type = int(item.get("Type", 1))  # 1=快讯，2=新闻
                
                # 转换时间戳为datetime对象
                try:
                    news_datetime = datetime.fromtimestamp(time_timestamp)
                except:
                    news_datetime = None
                
                news_item = {
                    "id": news_id,
                    "title": title,
                    "content": content,
                    "time": time_timestamp,
                    "datetime": news_datetime,
                    "type": news_type,
                    "type_name": "快讯" if news_type == 1 else "新闻"
                }
                
                news_list.append(news_item)
            
            return {
                "plate_id": plate_id,
                "news_list": news_list,
                "total_count": len(news_list)
            }
            
        except Exception as e:
            print(f"请求板块要闻失败 ({plate_id}): {e}")
            import traceback
            traceback.print_exc()
            return {
                "plate_id": plate_id,
                "news_list": [],
                "total_count": 0
            }
    
    def get_plate_news_dataframe(self, plate_id: str, max_pages: int = 3, page_size: int = 30, timeout: int = 1600):
        """获取指定板块的最新要闻（返回DataFrame格式）
        
        Args:
            plate_id: 板块代码
            max_pages: 最大页数，默认3页
            page_size: 每页数量，默认30条
            timeout: 超时时间（秒）
            
        Returns:
            pd.DataFrame: 包含要闻数据的DataFrame
                - id: 新闻ID
                - title: 标题
                - content: 内容
                - datetime: 发布时间
                - type_name: 类型名称
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取化工板块要闻（最多3页，共90条）
            df = crawler.get_plate_news_dataframe("801070", max_pages=3)
            
            # 查看最新10条
            print(df.head(10))
            
            # 筛选快讯
            flash_news = df[df['type_name'] == '快讯']
        """
        all_news = []
        
        for page in range(max_pages):
            index = page * page_size
            print(f"获取第 {page + 1}/{max_pages} 页...")
            
            result = self.get_plate_news(
                plate_id=plate_id,
                index=index,
                page_size=page_size,
                timeout=timeout
            )
            
            news_list = result.get("news_list", [])
            
            if not news_list:
                print(f"第 {page + 1} 页无数据，停止获取")
                break
            
            all_news.extend(news_list)
            print(f"  获取到 {len(news_list)} 条要闻")
        
        if not all_news:
            return pd.DataFrame()
        
        # 转换为DataFrame
        df = pd.DataFrame(all_news)
        
        # 选择需要的列
        columns = ['id', 'title', 'content', 'datetime', 'type_name']
        df = df[columns]
        
        # 按时间降序排列
        df = df.sort_values('datetime', ascending=False).reset_index(drop=True)
        
        print(f"\n[OK] 共获取 {len(df)} 条板块要闻")
        
        return df

    def get_sector_strength(self, sector_code, date=None, timeout=1600):
        """
        获取板块强度数据（直接返回强度值）
        
        Args:
            sector_code: 板块代码，如 '801235'（化工）、'801159'（机器人概念）
            date: 日期，格式YYYY-MM-DD，默认为当前日期
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            dict: 包含板块强度数据
                - sector_code: 板块代码
                - strength: 板块强度值（直接从API获取，无需计算）
                - date: 数据日期
                - time: 数据时间戳
                - raw_data: 原始API返回的List数据
                - success: 是否成功获取
                - error: 错误信息（如果有）
                - is_historical: 是否为历史数据
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取化工板块当前强度
            result = crawler.get_sector_strength("801235")
            if result['success']:
                print(f"化工板块强度: {result['strength']}")
            
            # 获取机器人概念板块历史强度
            result = crawler.get_sector_strength("801159", "2026-02-05")
            if result['success']:
                print(f"机器人概念板块强度: {result['strength']}")
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 判断是否为历史数据（非当日数据使用历史API）
        today = datetime.now().strftime("%Y-%m-%d")
        is_historical = (date != today)
        
        # 根据是否为历史数据选择不同的API端点
        if is_historical:
            # 历史数据使用 apphis.longhuvip.com
            api_url = "https://apphis.longhuvip.com/w1/api/index.php"
            api_headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; 23116PN5BC Build/PQ3A.190605.01141736)",
                "Host": "apphis.longhuvip.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
            }
        else:
            # 当日数据使用 apphwhq.longhuvip.com
            api_url = self.sector_base_url
            api_headers = self.sector_headers
        
        # 构造请求参数
        data = {
            "a": "GetPlate_Info_QJ",
            "c": "ZhiShuRanking",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "Date": date,
            "apiv": "w42",
            "PlateID": sector_code
        }
        
        try:
            response = requests.post(
                api_url,
                data=data,
                headers=api_headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result or result.get("errcode") != "0":
                error_msg = f"获取板块强度失败: {result.get('errcode', 'unknown error')}"
                print(error_msg)
                return {
                    "sector_code": sector_code,
                    "strength": None,
                    "date": date,
                    "time": None,
                    "raw_data": None,
                    "success": False,
                    "error": error_msg,
                    "is_historical": is_historical
                }
            
            # 解析数据
            list_data = result.get("List", [])
            time_data = result.get("Time", 0)
            actual_date = result.get("Date", date)
            min_day = result.get("MinDay", "")
            
            if len(list_data) < 2:
                error_msg = "API返回数据格式不正确，List长度不足"
                print(error_msg)
                return {
                    "sector_code": sector_code,
                    "strength": None,
                    "date": actual_date,
                    "time": time_data,
                    "raw_data": list_data,
                    "success": False,
                    "error": error_msg,
                    "is_historical": is_historical
                }
            
            # 强度值在List的第二个位置（索引1）
            strength_value = list_data[1]
            
            return {
                "sector_code": sector_code,
                "strength": strength_value,
                "date": actual_date,
                "time": time_data,
                "raw_data": list_data,
                "success": True,
                "error": None,
                "is_historical": is_historical,
                "min_day": min_day
            }
            
        except Exception as e:
            error_msg = f"请求板块强度失败 ({sector_code}, {date}): {e}"
            print(error_msg)
            return {
                "sector_code": sector_code,
                "strength": None,
                "date": date,
                "time": None,
                "raw_data": None,
                "success": False,
                "error": error_msg,
                "is_historical": is_historical
            }
    
    def get_multiple_sectors_strength(self, sector_codes, date=None, timeout=1600):
        """
        批量获取多个板块的强度数据
        
        Args:
            sector_codes: 板块代码列表，如 ['801235', '801159']
            date: 日期，格式YYYY-MM-DD，默认为当前日期
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            dict: 以板块代码为key的强度数据字典
                {
                    '801235': {
                        'sector_code': '801235',
                        'strength': 5208,
                        'date': '2026-02-06',
                        'success': True,
                        ...
                    },
                    '801159': {
                        'sector_code': '801159', 
                        'strength': 5334,
                        'date': '2026-02-06',
                        'success': True,
                        ...
                    }
                }
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 批量获取多个板块强度
            sector_codes = ['801235', '801159']  # 化工、机器人概念
            results = crawler.get_multiple_sectors_strength(sector_codes)
            
            for code, data in results.items():
                if data['success']:
                    print(f"板块 {code} 强度: {data['strength']}")
                else:
                    print(f"板块 {code} 获取失败: {data['error']}")
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        results = {}
        
        print(f"开始批量获取 {len(sector_codes)} 个板块的强度数据...")
        
        for i, sector_code in enumerate(sector_codes, 1):
            print(f"  获取板块 {sector_code} ({i}/{len(sector_codes)})...")
            
            result = self.get_sector_strength(sector_code, date, timeout)
            results[sector_code] = result
            
            if result['success']:
                print(f"    [OK] 强度: {result['strength']}")
            else:
                print(f"    [ERROR] 失败: {result['error']}")
        
        success_count = sum(1 for r in results.values() if r['success'])
        print(f"[OK] 批量获取完成: {success_count}/{len(sector_codes)} 个板块成功")
        
        return results
    
    def get_sector_strength_history(self, sector_code, start_date, end_date, timeout=1600):
        """
        获取板块强度历史数据（指定日期范围）
        
        Args:
            sector_code: 板块代码，如 '801235'（化工）、'801159'（机器人概念）
            start_date: 开始日期，格式YYYY-MM-DD
            end_date: 结束日期，格式YYYY-MM-DD
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            dict: 包含历史强度数据
                - sector_code: 板块代码
                - date_range: 日期范围 [start_date, end_date]
                - history_data: 历史数据列表，每项包含：
                    - date: 日期
                    - strength: 强度值
                    - raw_data: 原始数据
                - success_count: 成功获取的数据条数
                - total_count: 总请求数据条数
                - success: 是否有成功获取的数据
                - errors: 错误信息列表
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取化工板块最近5天的强度历史
            result = crawler.get_sector_strength_history(
                "801235", "2026-02-01", "2026-02-06"
            )
            
            if result['success']:
                print(f"成功获取 {result['success_count']} 天数据")
                for data in result['history_data']:
                    print(f"{data['date']}: {data['strength']}")
        """
        from datetime import datetime, timedelta
        
        # 解析日期
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError as e:
            return {
                "sector_code": sector_code,
                "date_range": [start_date, end_date],
                "history_data": [],
                "success_count": 0,
                "total_count": 0,
                "success": False,
                "errors": [f"日期格式错误: {e}"]
            }
        
        if start > end:
            return {
                "sector_code": sector_code,
                "date_range": [start_date, end_date],
                "history_data": [],
                "success_count": 0,
                "total_count": 0,
                "success": False,
                "errors": ["开始日期不能晚于结束日期"]
            }
        
        # 生成日期列表
        date_list = []
        current = start
        while current <= end:
            date_list.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)
        
        print(f"开始获取板块 {sector_code} 的历史强度数据...")
        print(f"日期范围: {start_date} 到 {end_date} ({len(date_list)} 天)")
        
        history_data = []
        errors = []
        
        for i, date in enumerate(date_list, 1):
            print(f"  获取 {date} 数据... ({i}/{len(date_list)})")
            
            result = self.get_sector_strength(sector_code, date, timeout)
            
            if result['success']:
                history_data.append({
                    "date": result['date'],
                    "strength": result['strength'],
                    "raw_data": result['raw_data'],
                    "time": result['time'],
                    "is_historical": result.get('is_historical', True)
                })
                print(f"    [OK] 强度: {result['strength']}")
            else:
                errors.append(f"{date}: {result['error']}")
                print(f"    [ERROR] 失败: {result['error']}")
        
        success_count = len(history_data)
        total_count = len(date_list)
        
        print(f"[OK] 历史数据获取完成: {success_count}/{total_count} 天成功")
        
        return {
            "sector_code": sector_code,
            "date_range": [start_date, end_date],
            "history_data": history_data,
            "success_count": success_count,
            "total_count": total_count,
            "success": success_count > 0,
            "errors": errors
        }
    
    def get_sector_strength_dataframe(self, sector_code, start_date, end_date, timeout=1600):
        """
        获取板块强度历史数据并返回DataFrame格式
        
        Args:
            sector_code: 板块代码
            start_date: 开始日期，格式YYYY-MM-DD
            end_date: 结束日期，格式YYYY-MM-DD
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            pd.DataFrame: 包含历史强度数据的DataFrame
                - date: 日期
                - sector_code: 板块代码
                - strength: 强度值
                - time: 时间戳
                - is_historical: 是否为历史数据
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取化工板块强度DataFrame
            df = crawler.get_sector_strength_dataframe(
                "801235", "2026-02-01", "2026-02-06"
            )
            
            if not df.empty:
                print(df)
                # 可以进行数据分析
                print(f"平均强度: {df['strength'].mean():.2f}")
                print(f"最大强度: {df['strength'].max()}")
        """
        # 获取历史数据
        result = self.get_sector_strength_history(sector_code, start_date, end_date, timeout)
        
        if not result['success'] or not result['history_data']:
            print(f"未获取到有效的历史数据")
            return pd.DataFrame()
        
        # 转换为DataFrame
        data_list = []
        for item in result['history_data']:
            data_list.append({
                'date': item['date'],
                'sector_code': sector_code,
                'strength': item['strength'],
                'time': item['time'],
                'is_historical': item.get('is_historical', True)
            })
        
        df = pd.DataFrame(data_list)
        
        # 按日期排序
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)
        
        print(f"[OK] 成功创建DataFrame: {len(df)} 条记录")
        
        return df

    def get_longhubang_stock_list(self, date=None, index=0, page_size=500, timeout=1600):
        """
        获取龙虎榜上榜个股列表（当日或历史）
        
        Args:
            date: 日期，格式YYYY-MM-DD，默认为None（获取当日数据）
            index: 分页索引，默认0（第一页）
            page_size: 每页数量，默认500条
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            dict: 包含龙虎榜上榜个股列表
                - date: 日期
                - user_type: 用户类型
                - stocks: 股票列表，每只股票包含：
                    - stock_code: 股票代码
                    - stock_name: 股票名称
                    - change_pct: 涨跌幅
                    - reason_type: 上榜原因类型
                    - buy_amount: 买入金额
                    - join_num: 上榜营业部数量
                    - turnover: 成交额
                    - circulating_market_cap: 流通市值
                    - amplitude: 振幅
                    - turnover_ratio: 换手率
                    - total_market_cap: 总市值
                - total_count: 总数量
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取当日龙虎榜
            result = crawler.get_longhubang_stock_list()
            
            # 获取历史龙虎榜
            result = crawler.get_longhubang_stock_list("2026-02-05")
            
            # 遍历上榜个股
            for stock in result['stocks']:
                print(f"{stock['stock_name']} ({stock['stock_code']}): {stock['change_pct']}")
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 构造请求参数
        url = "https://applhb.longhuvip.com/w1/api/index.php"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; 23116PN5BC Build/PQ3A.190605.01141736)",
            "Host": "applhb.longhuvip.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        
        data_params = {
            "a": "GetStockList",
            "st": str(page_size),
            "c": "LongHuBang",
            "PhoneOSNew": "1",
            "DeviceID": "e78ba169-6c03-3faf-8e5e-a72f8411a8eb",
            "VerSion": "5.21.0.2",
            "Token": "0daffcf404348e2fb714795ba5bdff02",
            "Time": date,
            "Index": str(index),
            "apiv": "w42",
            "Type": "2",
            "UserID": "4315515"
        }
        
        try:
            response = requests.post(
                url,
                data=data_params,
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result:
                print(f"获取龙虎榜列表失败: 响应为空")
                return {
                    "date": date,
                    "user_type": 0,
                    "stocks": [],
                    "total_count": 0
                }
            
            # 解析股票列表
            stocks = []
            stock_list = result.get("list", [])
            
            for stock_data in stock_list:
                stock_info = {
                    "stock_code": stock_data.get("ID", ""),
                    "stock_name": stock_data.get("Name", ""),
                    "change_pct": stock_data.get("IncreaseAmount", ""),
                    "reason_type": stock_data.get("D3", ""),
                    "buy_amount": float(stock_data.get("BuyIn", 0)),  # 改为float
                    "join_num": int(stock_data.get("JoinNum", 0)),
                    "turnover": int(stock_data.get("Turnover", 0)),
                    "circulating_market_cap": int(stock_data.get("CircPrice", 0)),
                    "amplitude": stock_data.get("Amplitude", ""),
                    "turnover_ratio": stock_data.get("TurnoverRatio", ""),
                    "total_market_cap": int(stock_data.get("Capitalization", 0))
                }
                stocks.append(stock_info)
            
            return {
                "date": result.get("Time", date),
                "user_type": result.get("UserType", 0),
                "stocks": stocks,
                "total_count": len(stocks)
            }
            
        except Exception as e:
            print(f"请求龙虎榜列表失败 ({date}): {e}")
            import traceback
            traceback.print_exc()
            return {
                "date": date,
                "user_type": 0,
                "stocks": [],
                "total_count": 0
            }
    
    def get_longhubang_stock_detail(self, stock_code, date=None, timeout=1600):
        """
        获取指定个股的龙虎榜详细数据（当日或历史）
        
        Args:
            stock_code: 股票代码，如 "002342"
            date: 日期，格式YYYY-MM-DD，默认为None（获取当日数据，16:30之后有效）
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            dict: 包含个股龙虎榜详细数据
                - stock_code: 股票代码
                - stock_name: 股票名称
                - date: 日期
                - current_price: 当前价
                - change_pct: 涨跌幅
                - turnover_ratio: 换手率
                - circulating_shares: 流通股本（亿股）
                - net_buy_amount: 净买入金额
                - turnover: 成交额
                - more_turnover: 更多成交额
                - on_list_count: 上榜次数
                - on_list_start: 首次上榜
                - on_time_list: 历史上榜日期列表
                - buy_sell_data: 买卖数据列表，每条包含：
                    - buy_list: 买入营业部列表
                        - seat_id: 席位ID
                        - seat_name: 席位名称
                        - buy_amount: 买入金额
                        - sell_amount: 卖出金额
                        - rank: 排名
                        - group_id: 分组ID
                        - group_icon: 分组标签（如"量化抢筹"）
                    - sell_list: 卖出营业部列表
                    - up_reason: 上榜原因
                    - buy_total: 买入总额
                    - sell_total: 卖出总额
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取当日龙虎榜详情（16:30之后有效）
            result = crawler.get_longhubang_stock_detail("002342")
            
            # 获取历史龙虎榜详情
            result = crawler.get_longhubang_stock_detail("002342", "2026-02-06")
            
            # 查看买入营业部
            for data in result['buy_sell_data']:
                print(f"上榜原因: {data['up_reason']}")
                for seat in data['buy_list']:
                    print(f"  买入: {seat['seat_name']}, 金额: {seat['buy_amount']:,}")
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 构造请求参数
        url = "https://applhb.longhuvip.com/w1/api/index.php"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Linux; Android 9; 23116PN5BC Build/PQ3A.190605.01141736; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36;kaipanla 5.21.0.2",
            "Host": "applhb.longhuvip.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        
        data_params = {
            "c": "Stock",
            "a": "GetNewOneStockInfo",
            "Type": "0",
            "Time": date,
            "StockID": stock_code,
            "UserID": "4315515",
            "Token": "0daffcf404348e2fb714795ba5bdff02",
            "DeviceID": "e78ba169-6c03-3faf-8e5e-a72f8411a8eb"
        }
        
        # 添加apiv参数到URL
        url_with_params = f"{url}?apiv=w42&PhoneOSNew=1&VerSion=5.21.0.2"
        
        try:
            response = requests.post(
                url_with_params,
                data=data_params,
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if not result or result.get("errcode") != "0":
                error_code = result.get('errcode', 'unknown error') if result else 'empty response'
                print(f"获取龙虎榜详情失败: {error_code}")
                return {}
            
            # 解析基本信息
            stock_name = result.get("Name", "")
            current_price = result.get("CurPrice", "")
            change_pct = result.get("QuoteChange", "")
            turnover_ratio = result.get("TurnoverRatio", "")
            circulating_shares = result.get("Circulation", "")
            net_buy_amount = int(result.get("BuyIn", 0))
            turnover = int(result.get("Turnover", 0))
            more_turnover = int(result.get("MoreTurnover", 0))
            on_list_count = int(result.get("ToBusinessCount", 0))
            on_list_start = int(result.get("lbStart", 0))
            on_time_list = result.get("OnTimeList", [])
            
            # 解析买卖数据
            buy_sell_data = []
            list_data = result.get("List", [])
            
            for item in list_data:
                # 解析买入列表
                buy_list = []
                for buy_seat in item.get("BuyList", []):
                    seat_info = {
                        "seat_id": buy_seat.get("ID", ""),
                        "seat_name": buy_seat.get("Name", ""),
                        "buy_amount": int(buy_seat.get("Buy", 0)),
                        "sell_amount": int(buy_seat.get("Sell", 0)),
                        "rank": int(buy_seat.get("PX", 0)),
                        "group_id": buy_seat.get("GroupID", ""),
                        "group_icon": buy_seat.get("GroupIcon", [])
                    }
                    buy_list.append(seat_info)
                
                # 解析卖出列表
                sell_list = []
                for sell_seat in item.get("SellList", []):
                    seat_info = {
                        "seat_id": sell_seat.get("ID", ""),
                        "seat_name": sell_seat.get("Name", ""),
                        "buy_amount": int(sell_seat.get("Buy", 0)),
                        "sell_amount": int(sell_seat.get("Sell", 0)),
                        "rank": int(sell_seat.get("PX", 0)),
                        "group_id": sell_seat.get("GroupID", ""),
                        "group_icon": sell_seat.get("GroupIcon", [])
                    }
                    sell_list.append(seat_info)
                
                buy_sell_info = {
                    "buy_list": buy_list,
                    "sell_list": sell_list,
                    "up_reason": item.get("UpReason", []),
                    "buy_total": int(item.get("BuyTotal", 0)),
                    "sell_total": int(item.get("SellTotal", 0))
                }
                buy_sell_data.append(buy_sell_info)
            
            return {
                "stock_code": stock_code,
                "stock_name": stock_name,
                "date": result.get("Time", date),
                "current_price": current_price,
                "change_pct": change_pct,
                "turnover_ratio": turnover_ratio,
                "circulating_shares": circulating_shares,
                "net_buy_amount": net_buy_amount,
                "turnover": turnover,
                "more_turnover": more_turnover,
                "on_list_count": on_list_count,
                "on_list_start": on_list_start,
                "on_time_list": on_time_list,
                "buy_sell_data": buy_sell_data
            }
            
        except Exception as e:
            print(f"请求龙虎榜详情失败 ({stock_code}, {date}): {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def get_longhubang_dataframe(self, date=None, timeout=1600):
        """
        获取龙虎榜上榜个股列表并返回DataFrame格式
        
        Args:
            date: 日期，格式YYYY-MM-DD，默认为None（获取当日数据）
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            pd.DataFrame: 包含龙虎榜上榜个股数据的DataFrame
                - stock_code: 股票代码
                - stock_name: 股票名称
                - change_pct: 涨跌幅
                - reason_type: 上榜原因类型
                - buy_amount: 买入金额
                - join_num: 上榜营业部数量
                - turnover: 成交额
                - circulating_market_cap: 流通市值
                - amplitude: 振幅
                - turnover_ratio: 换手率
                - total_market_cap: 总市值
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取当日龙虎榜DataFrame
            df = crawler.get_longhubang_dataframe()
            
            # 获取历史龙虎榜DataFrame
            df = crawler.get_longhubang_dataframe("2026-02-05")
            
            # 分析数据
            print(f"上榜个股数量: {len(df)}")
            print(f"平均换手率: {df['turnover_ratio'].astype(float).mean():.2f}%")
        """
        result = self.get_longhubang_stock_list(date, timeout=timeout)
        
        if not result or not result.get("stocks"):
            print(f"未获取到龙虎榜数据")
            return pd.DataFrame()
        
        # 转换为DataFrame
        df = pd.DataFrame(result["stocks"])
        
        print(f"[OK] 成功获取 {len(df)} 只龙虎榜上榜个股")
        
        return df

    def get_sector_constituent_stocks(self, plate_id, date=None, order=1, timeout=1600):
        """
        获取板块核心成分股列表（仅第一页，30只）
        
        注意：
        - 此函数只返回第一页的30只股票
        - Stocks字段包含该板块的所有核心成分股代码（通常30-50只）
        - 如需获取所有相关股票，请使用 get_sector_all_stocks()
        
        Args:
            plate_id: 板块代码，如 "801235"（化工）
            date: 日期，格式YYYY-MM-DD，默认为None（获取当日数据）
            order: 排序方式，默认1
                1: 涨幅排序
                其他值待测试
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            dict: 包含板块成分股信息
                - date: 日期
                - plate_id: 板块代码
                - stocks: 成分股列表（第一页30只，每只股票包含详细信息）
                - total_count: 返回的股票数量（30只）
                - stock_codes: 核心成分股代码列表（通常30-50只）
        
        股票数据字段（list格式，索引说明）:
            [0]: 股票代码
            [1]: 股票名称
            [4]: 概念标签
            [5]: 最新价
            [6]: 涨跌幅
            [7]: 成交额
            [8]: 换手率
            [10]: 流通市值
            [23]: 连板描述（如"2连板"、"首板"）
            [24]: 龙头标记（如"龙一"、"龙二"）
            ... 更多字段见返回数据
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取化工板块核心成分股（第一页）
            data = crawler.get_sector_constituent_stocks("801235", "2026-02-10")
            
            print(f"板块: {data['plate_id']}")
            print(f"返回股票数: {data['total_count']}")
            print(f"核心成分股代码: {data['stock_codes']}")  # 所有核心成分股代码
            
            # 遍历返回的股票
            for stock in data['stocks']:
                code = stock[0]
                name = stock[1]
                price = stock[5]
                change_pct = stock[6]
                print(f"{code} {name}: {price} ({change_pct:+.2f}%)")
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 构造请求参数
        data_params = {
            "Order": str(order),
            "TSZB": "0",
            "a": "ZhiShuStockList_W8",
            "st": "30",
            "c": "ZhiShuRanking",
            "PhoneOSNew": "1",
            "old": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "IsZZ": "0",
            "Token": "0daffcf404348e2fb714795ba5bdff02",
            "Index": "0",
            "Date": date,
            "apiv": "w42",
            "Type": "6",
            "IsKZZType": "0",
            "UserID": "4315515",
            "PlateID": plate_id,
            "TSZB_Type": "0",
            "filterType": "0"
        }
        
        try:
            response = requests.post(
                self.base_url,
                data=data_params,
                headers=self.headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("errcode") != "0":
                print(f"获取板块成分股失败: {result.get('errcode', 'unknown error')}")
                return {
                    "date": date,
                    "plate_id": plate_id,
                    "stocks": [],
                    "total_count": 0,
                    "stock_codes": []
                }
            
            # 解析成分股数据
            stocks = result.get("list", [])
            stock_codes = result.get("Stocks", [])
            
            return {
                "date": date,
                "plate_id": plate_id,
                "stocks": stocks,
                "total_count": len(stocks),
                "stock_codes": stock_codes
            }
            
        except Exception as e:
            print(f"请求板块成分股失败 ({plate_id}, {date}): {e}")
            import traceback
            traceback.print_exc()
            return {
                "date": date,
                "plate_id": plate_id,
                "stocks": [],
                "total_count": 0,
                "stock_codes": []
            }

    def get_sector_all_stocks(self, plate_id, date=None, order=1, max_pages=None, timeout=1600):
        """
        获取板块所有相关股票（分页获取完整列表）
        
        注意：
        - 第一页(Index=0)返回核心成分股（30只），Stocks字段包含所有核心成分股代码（30-50只）
        - 第二页开始Count字段显示所有相关股票总数
        - 当返回数量 < 30 时，说明是最后一页
        - 自动分页获取所有股票并去重
        
        Args:
            plate_id: 板块代码，如 "801235"（化工）
            date: 日期，格式YYYY-MM-DD，默认为None（获取当日数据）
            order: 排序方式，默认1（涨幅排序）
            max_pages: 最大请求页数，默认None（获取所有页，直到返回数量<30）
                      建议设置上限避免请求过多，如 max_pages=50
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            dict: 包含板块所有相关股票信息
                - date: 日期
                - plate_id: 板块代码
                - core_stock_codes: 核心成分股代码列表（来自第一页的Stocks字段）
                - core_count: 核心成分股数量（第一页的Count）
                - all_stocks: 所有相关股票列表（分页获取，去重）
                - total_count: 实际获取的股票总数
                - total_count_from_api: API返回的总数（第二页的Count）
                - pages_fetched: 实际获取的页数
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取化工板块所有相关股票
            data = crawler.get_sector_all_stocks("801235", "2026-02-10")
            
            print(f"核心成分股: {data['core_count']} 只")
            print(f"API显示总数: {data['total_count_from_api']} 只")
            print(f"实际获取: {data['total_count']} 只")
            print(f"获取页数: {data['pages_fetched']} 页")
            
            # 只获取前5页（150只股票）
            data = crawler.get_sector_all_stocks("801235", "2026-02-10", max_pages=5)
            
            # 按涨跌幅排序
            sorted_stocks = sorted(data['all_stocks'], 
                                   key=lambda x: x[6] if len(x) > 6 else 0, 
                                   reverse=True)
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        all_stocks = []
        all_codes_set = set()
        core_stock_codes = []
        core_count = 0
        total_count_from_api = 0
        page = 0
        
        while True:
            # 检查是否达到最大页数
            if max_pages is not None and page >= max_pages:
                break
            
            index = page * 30
            
            # 构造请求参数
            data_params = {
                "Order": str(order),
                "TSZB": "0",
                "a": "ZhiShuStockList_W8",
                "st": "30",
                "c": "ZhiShuRanking",
                "PhoneOSNew": "1",
                "old": "1",
                "DeviceID": str(uuid.uuid4()),
                "VerSion": "5.21.0.2",
                "IsZZ": "0",
                "Token": "0daffcf404348e2fb714795ba5bdff02",
                "Index": str(index),
                "Date": date,
                "apiv": "w42",
                "Type": "6",
                "IsKZZType": "0",
                "UserID": "4315515",
                "PlateID": plate_id,
                "TSZB_Type": "0",
                "filterType": "0"
            }
            
            try:
                response = requests.post(
                    self.base_url,
                    data=data_params,
                    headers=self.headers,
                    verify=False,
                    proxies={'http': None, 'https': None},
                    timeout=timeout
                )
                response.raise_for_status()
                result = response.json()
                
                if result.get("errcode") != "0":
                    print(f"获取板块股票失败 (Index={index}): {result.get('errcode', 'unknown error')}")
                    break
                
                stocks = result.get("list", [])
                count = result.get("Count", 0)
                
                # 第一页获取核心成分股代码
                if page == 0:
                    core_stock_codes = result.get("Stocks", [])
                    core_count = count
                elif page == 1:
                    # 第二页获取总数
                    total_count_from_api = count
                
                # 如果没有数据，停止
                if not stocks:
                    break
                
                # 添加到总列表（去重）
                for stock in stocks:
                    if len(stock) > 0:
                        code = stock[0]
                        if code not in all_codes_set:
                            all_stocks.append(stock)
                            all_codes_set.add(code)
                
                # 如果返回少于30只，说明是最后一页
                if len(stocks) < 30:
                    break
                
                page += 1
                
                # 添加延迟避免请求过快
                if page > 0 and page % 10 == 0:
                    time.sleep(0.5)
                
            except Exception as e:
                print(f"请求板块股票失败 ({plate_id}, Index={index}): {e}")
                break
        
        return {
            "date": date,
            "plate_id": plate_id,
            "core_stock_codes": core_stock_codes,
            "core_count": core_count,
            "all_stocks": all_stocks,
            "total_count": len(all_stocks),
            "total_count_from_api": total_count_from_api if total_count_from_api > 0 else core_count,
            "pages_fetched": page + 1
        }

    def get_sector_bidding_anomaly(self, date=None, timeout=1600):
        """
        获取板块竞价异动数据
        
        Args:
            date: 日期，格式YYYY-MM-DD，默认为None（获取实时数据）
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            dict: 包含板块竞价异动信息
                - date: 日期
                - is_realtime: 是否为实时数据
                - list1: 今日新增竞价异动板块列表
                - list2: 昨日爆发板块延续异动列表
                - list3: 其他异动板块列表
                - total_count: 总异动板块数量
        
        板块数据字段（list格式，索引说明）:
            [0]: 板块代码
            [1]: 板块名称
            [2]: 竞价爆量
            [3]: 异动金额（元）
            [4]: 竞价板块强度
            [5]: 主力净额（元）
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取实时竞价异动
            data = crawler.get_sector_bidding_anomaly()
            
            # 获取历史竞价异动
            data = crawler.get_sector_bidding_anomaly("2026-02-10")
            
            print(f"日期: {data['date']}")
            print(f"今日新增: {len(data['list1'])} 个板块")
            print(f"昨日延续: {len(data['list2'])} 个板块")
            print(f"其他异动: {len(data['list3'])} 个板块")
            
            # 遍历今日新增异动板块
            for sector in data['list1']:
                code = sector[0]
                name = sector[1]
                volume_ratio = sector[2]
                amount = sector[3]
                strength = sector[4]
                main_net = sector[5]
                print(f"{code} {name}: 爆量{volume_ratio} 强度{strength}")
        """
        is_realtime = date is None
        
        # 根据是否实时选择不同的URL和headers
        if is_realtime:
            url = self.sector_base_url  # apphwhq.longhuvip.com
            headers = self.sector_headers
        else:
            url = self.base_url  # apphis.longhuvip.com
            headers = self.headers
        
        # 构造请求参数
        data_params = {
            "a": "GetBKJJ_W36",
            "c": "StockBidYiDong",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "Token": "0daffcf404348e2fb714795ba5bdff02",
            "apiv": "w42",
            "UserID": "4315515"
        }
        
        # 如果是历史数据，添加日期参数
        if not is_realtime:
            data_params["Day"] = date
        
        try:
            response = requests.post(
                url,
                data=data_params,
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("errcode") != "0":
                print(f"获取板块竞价异动失败: {result.get('errcode', 'unknown error')}")
                return {
                    "date": date if date else datetime.now().strftime("%Y-%m-%d"),
                    "is_realtime": is_realtime,
                    "list1": [],
                    "list2": [],
                    "list3": [],
                    "total_count": 0
                }
            
            # 解析数据
            list1 = result.get("List1", [])  # 今日新增竞价异动
            list2 = result.get("List2", [])  # 昨日爆发板块延续异动
            list3 = result.get("List3", [])  # 其他异动板块
            
            return {
                "date": result.get("Day", date if date else datetime.now().strftime("%Y-%m-%d")),
                "is_realtime": is_realtime,
                "list1": list1,
                "list2": list2,
                "list3": list3,
                "total_count": len(list1) + len(list2) + len(list3)
            }
            
        except Exception as e:
            print(f"请求板块竞价异动失败 ({date}): {e}")
            import traceback
            traceback.print_exc()
            return {
                "date": date if date else datetime.now().strftime("%Y-%m-%d"),
                "is_realtime": is_realtime,
                "list1": [],
                "list2": [],
                "list3": [],
                "total_count": 0
            }

    def get_etf_ranking(self, date=None, order=1, index=0, timeout=1600):
        """
        获取ETF榜单数据（支持分页）
        
        Args:
            date: 日期，格式YYYY-MM-DD，默认为None（获取实时数据）
            order: 排序方式，默认1（涨幅排序）
            index: 分页索引，默认0（第一页，每页30个）
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            dict: 包含ETF榜单信息
                - date: 日期
                - is_realtime: 是否为实时数据
                - etfs: ETF列表
                - total_count: ETF总数（来自Count字段）
                - page_count: 当前页返回数量
        
        ETF数据字段（list格式，索引说明）:
            [0]: ETF代码
            [1]: ETF名称
            [2]: 价格
            [3]: 涨幅（%）
            [4]: 成交额（元）
            [5]: 量比
            [6]: 昨日增减金额
            [7]: 昨日增减份额
            [8]: 昨日增减比例（%）
            [9]: 一周收益（%）
            [10]: 一月收益（%）
            [11]: 三个月收益（%）
            [12]: 半年收益（%）
            [13]: 总市值
            [14]: 未知14
            [15]: 未知15
            [16]: 未知16
            [17]: 未知17
            [18]: 未知18
            [19]: 今年以来涨幅（%）
            [20]: 未知20
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取实时ETF榜单（第一页）
            data = crawler.get_etf_ranking()
            
            # 获取历史ETF榜单
            data = crawler.get_etf_ranking("2026-02-09")
            
            # 获取第二页
            data = crawler.get_etf_ranking(index=30)
            
            print(f"日期: {data['date']}")
            print(f"ETF总数: {data['total_count']}")
            print(f"当前页: {data['page_count']} 个")
            
            # 遍历ETF
            for etf in data['etfs']:
                code = etf[0]
                name = etf[1]
                price = etf[2]
                change = etf[3]
                print(f"{code} {name}: {price} ({change:+.2f}%)")
        """
        is_realtime = date is None
        
        # 构造请求参数
        data_params = {
            "Order": str(order),
            "a": "ETFStockRanking",
            "st": "30",
            "c": "NewStockRanking",
            "Filtration": "0",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "Token": "0daffcf404348e2fb714795ba5bdff02",
            "Index": str(index),
            "PidType": "0",
            "apiv": "w42",
            "Type": "1",
            "UserID": "4315515"
        }
        
        # 如果是历史数据，添加日期参数
        if not is_realtime:
            data_params["Date"] = date
        
        try:
            response = requests.post(
                self.sector_base_url,  # 使用apphwhq.longhuvip.com
                data=data_params,
                headers=self.sector_headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("errcode") != "0":
                print(f"获取ETF榜单失败: {result.get('errcode', 'unknown error')}")
                return {
                    "date": date if date else datetime.now().strftime("%Y-%m-%d"),
                    "is_realtime": is_realtime,
                    "etfs": [],
                    "total_count": 0,
                    "page_count": 0
                }
            
            # 解析数据（注意：数据在info字段中，不是list字段）
            etfs = result.get("info", [])
            total_count = result.get("Count", 0)
            
            return {
                "date": date if date else datetime.now().strftime("%Y-%m-%d"),
                "is_realtime": is_realtime,
                "etfs": etfs,
                "total_count": total_count,
                "page_count": len(etfs)
            }
            
        except Exception as e:
            print(f"请求ETF榜单失败 ({date}, Index={index}): {e}")
            import traceback
            traceback.print_exc()
            return {
                "date": date if date else datetime.now().strftime("%Y-%m-%d"),
                "is_realtime": is_realtime,
                "etfs": [],
                "total_count": 0,
                "page_count": 0
            }
    
    def get_all_etf_ranking(self, date=None, order=1, max_pages=None, timeout=1600):
        """
        获取所有ETF榜单数据（自动分页）
        
        Args:
            date: 日期，格式YYYY-MM-DD，默认为None（获取实时数据）
            order: 排序方式，默认1（涨幅排序）
            max_pages: 最大请求页数，默认None（获取所有页）
            timeout: 超时时间（秒），默认1600秒
            
        Returns:
            dict: 包含所有ETF榜单信息
                - date: 日期
                - is_realtime: 是否为实时数据
                - etfs: 所有ETF列表
                - total_count: ETF总数
                - pages_fetched: 实际获取的页数
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取所有实时ETF
            data = crawler.get_all_etf_ranking()
            
            # 获取所有历史ETF
            data = crawler.get_all_etf_ranking("2026-02-09")
            
            # 只获取前5页
            data = crawler.get_all_etf_ranking(max_pages=5)
            
            print(f"ETF总数: {data['total_count']}")
            print(f"实际获取: {len(data['etfs'])} 个")
            print(f"获取页数: {data['pages_fetched']} 页")
        """
        is_realtime = date is None
        all_etfs = []
        page = 0
        
        while True:
            # 检查是否达到最大页数
            if max_pages is not None and page >= max_pages:
                break
            
            index = page * 30
            
            # 获取当前页数据
            page_data = self.get_etf_ranking(date=date, order=order, index=index, timeout=timeout)
            
            if not page_data['etfs']:
                break
            
            all_etfs.extend(page_data['etfs'])
            
            # 如果返回少于30个，说明是最后一页
            if len(page_data['etfs']) < 30:
                break
            
            page += 1
            
            # 添加延迟避免请求过快
            if page > 0 and page % 10 == 0:
                time.sleep(0.5)
        
        return {
            "date": date if date else datetime.now().strftime("%Y-%m-%d"),
            "is_realtime": is_realtime,
            "etfs": all_etfs,
            "total_count": len(all_etfs),
            "pages_fetched": page + 1
        }

    def get_stock_call_auction_tick(self, stock_code, date=None, timeout=300):
        """
        获取个股竞价tick数据（9:15:00-9:25:00）- 使用东方财富网API
        
        Args:
            stock_code: 股票代码，如 "000002"（不需要前缀）或 "SZ000002"
            date: 日期，格式YYYY-MM-DD，默认为None（获取实时数据）
            timeout: 超时时间（秒），默认300秒
            
        Returns:
            dict: 包含竞价tick数据
                - stock_code: 股票代码
                - date: 日期
                - is_realtime: 是否为实时数据
                - data: DataFrame，包含竞价tick数据
                    - time: 时间（HH:MM:SS格式）
                    - price: 匹配价（元）
                    - volume: 累计成交量（手）
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取实时竞价数据
            data = crawler.get_stock_call_auction_tick("000002")
            print(f"股票: {data['stock_code']}")
            
            # 查看9:15:00的数据
            df = data['data']
            first_tick = df[df['time'] == '09:15:00']
            if not first_tick.empty:
                print(f"9:15:00 匹配价: {first_tick['price'].values[0]}")
                print(f"9:15:00 累计成交量: {first_tick['volume'].values[0]}")
            
            # 获取历史竞价数据
            data = crawler.get_stock_call_auction_tick("000002", "2026-02-20")
        """
        # 处理股票代码格式
        if stock_code.startswith('SZ') or stock_code.startswith('SH'):
            # 提取市场代码和股票代码
            market = '0' if stock_code.startswith('SZ') else '1'
            code = stock_code[2:]
        else:
            # 根据股票代码判断市场
            if stock_code.startswith('6'):
                market = '1'  # 上海
            else:
                market = '0'  # 深圳
            code = stock_code
        
        # 构造东方财富网的secid格式: 市场代码.股票代码
        secid = f"{market}.{code}"
        
        is_realtime = date is None
        display_date = date if date else datetime.now().strftime("%Y-%m-%d")
        
        # 东方财富网竞价数据API
        # 参考URL: http://push2.eastmoney.com/api/qt/stock/details/get
        url = "http://push2.eastmoney.com/api/qt/stock/details/get"
        
        params = {
            "fields1": "f1,f2,f3,f4",
            "fields2": "f51,f52,f53,f54,f55",
            "mpi": "1000",  # 每页数量
            "ut": "fa5fd1943c7b386f172d6893dbfba10b",
            "fltt": "2",
            "pos": "-0",  # 从最新开始
            "secid": secid,
            "wbp2u": "|0|0|0|web",
            "_": str(int(time.time() * 1000))
        }
        
        try:
            # 添加请求延迟
            time.sleep(0.5)
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": f"http://quote.eastmoney.com/f1.html?newcode={market}.{code}"
            }
            
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout
            )
            response.raise_for_status()
            
            if not response.text.strip():
                print(f"请求竞价tick数据失败 ({stock_code}): 响应内容为空")
                return {}
            
            try:
                result = response.json()
            except (ValueError, requests.exceptions.JSONDecodeError) as json_error:
                print(f"请求竞价tick数据失败 ({stock_code}): JSON解析错误 - {json_error}")
                return {}
            
            if not result or result.get("rc") != 0:
                error_code = result.get('rc', 'unknown error') if result else 'empty response'
                print(f"获取竞价tick数据失败: {error_code}")
                return {}
            
            # 解析数据
            data_obj = result.get("data", {})
            if not data_obj:
                print(f"未获取到股票 {stock_code} 的竞价tick数据")
                return {}
            
            # 获取details字段（包含tick数据）
            details = data_obj.get("details", "")
            if not details:
                print(f"未获取到股票 {stock_code} 的竞价tick明细数据")
                return {}
            
            # 解析details数据
            # details可能是字符串或列表
            records = []
            
            if isinstance(details, str):
                # 字符串格式: "时间,价格,成交量,成交额,性质;时间,价格,成交量,成交额,性质;..."
                tick_list = details.split(";")
                
                for tick_str in tick_list:
                    if not tick_str.strip():
                        continue
                    
                    parts = tick_str.split(",")
                    if len(parts) < 3:
                        continue
                    
                    time_str = parts[0]  # 时间 HH:MM:SS
                    price = float(parts[1]) if parts[1] else 0.0  # 价格
                    volume = int(parts[2]) if parts[2] else 0  # 成交量（手）
                    
                    # 只保留9:15:00到9:25:00的竞价数据
                    if time_str >= "09:15:00" and time_str <= "09:25:00":
                        record = {
                            "time": time_str,
                            "price": price,
                            "volume": volume
                        }
                        records.append(record)
            
            elif isinstance(details, list):
                # 列表格式: [[时间, 价格, 成交量, 成交额, 性质], ...]
                for item in details:
                    if not isinstance(item, (list, tuple)) or len(item) < 3:
                        continue
                    
                    time_str = str(item[0])  # 时间
                    price = float(item[1]) if item[1] else 0.0  # 价格
                    volume = int(item[2]) if item[2] else 0  # 成交量（手）
                    
                    # 只保留9:15:00到9:25:00的竞价数据
                    if time_str >= "09:15:00" and time_str <= "09:25:00":
                        record = {
                            "time": time_str,
                            "price": price,
                            "volume": volume
                        }
                        records.append(record)
            
            if not records:
                print(f"未找到股票 {stock_code} 的竞价时段数据（9:15-9:25）")
                return {}
            
            df = pd.DataFrame(records)
            
            return {
                "stock_code": f"{market}.{code}",
                "date": display_date,
                "is_realtime": is_realtime,
                "data": df
            }
            
        except Exception as e:
            print(f"请求竞价tick数据失败 ({stock_code}): {e}")
            import traceback
            traceback.print_exc()
            return {}
