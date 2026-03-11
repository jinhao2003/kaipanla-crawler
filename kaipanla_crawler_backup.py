# -*- coding: utf-8 -*-
"""
开盘啦APP数据爬虫

主要功能�?
- get_daily_data(end_date, start_date=None): 获取指定日期范围的交易数�?
  - 只传end_date: 返回单日Series
  - 传start_date和end_date: 返回日期范围DataFrame
- get_new_high_data(end_date, start_date=None): 获取百日新高数据
- get_sector_intraday(sector_code, date=None): 获取板块分时数据
- get_stock_intraday(stock_code, date=None): 获取个股分时数据
- get_abnormal_stocks(): 获取异动个股数据（实时）
- get_sentiment_indicator(plate_id, stocks=None): 获取多头空头风向�?
- get_sector_ranking(date, index): 获取涨停原因板块数据
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import uuid
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
    
    def _request(self, data_params, date, timeout=1600):
        """发送POST请求
        
        Args:
            data_params: 请求参数
            date: 日期
            timeout: 超时时间（秒），默认1600�?
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
            "涨停�?: int(info1.get("ZT", 0)),
            "实际涨停": int(info1.get("SJZT", 0)),
            "跌停�?: int(info1.get("DT", 0)),
            "实际跌停": int(info1.get("SJDT", 0)),
            "上涨家数": int(info1.get("SZJS", 0)),
            "下跌家数": int(info1.get("XDJS", 0)),
            "平盘家数": int(info1.get("0", 0)),
            "上证指数": float(sh_index.get("last_px", 0)) if sh_index else 0,
            "最新价": float(sh_index.get("last_px", 0)) if sh_index else 0,
            "涨跌�?: sh_index.get("increase_rate", "") if sh_index else "",
            "成交�?: int(sh_index.get("turnover", 0)) if sh_index else 0,
            "首板数量": info3[0] if len(info3) > 0 else 0,
            "2连板数量": info3[1] if len(info3) > 1 else 0,
            "3连板数量": info3[2] if len(info3) > 2 else 0,
            "4连板以上数量": info3[3] if len(info3) > 3 else 0,
            "连板�?: round(info3[4], 2) if len(info3) > 4 else 0,
            "大幅回撤家数": withdrawal_num,
        }
        
        return data
    
    def get_daily_data(self, end_date, start_date=None):
        """
        获取交易日数�?
        
        Args:
            end_date: 结束日期，格式YYYY-MM-DD
            start_date: 起始日期，格式YYYY-MM-DD，可�?
            
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
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        if start > end:
            print("警告: 起始日期晚于结束日期，已自动交换")
            start, end = end, start
        
        # 生成日期列表（包含所有日期，包括周末�?
        date_list = []
        current = start
        while current <= end:
            date_list.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)
        
        # 获取每日数据
        records = []
        for date in date_list:
            print(f"正在获取 {date} 的数�?..")
            data = self._get_single_day_data(date)
            records.append(data)
        
        df = pd.DataFrame(records)
        
        # 过滤掉没有数据的日期（周末、节假日�?
        df = df[df["涨停�?] > 0]
        
        return df
    
    def get_new_high_data(self, end_date, start_date=None, timeout=1600):
        """
        获取百日新高数据
        
        Args:
            end_date: 结束日期，格式YYYY-MM-DD
            start_date: 起始日期，格式YYYY-MM-DD，可�?
            timeout: 超时时间（秒），默认1600�?
            
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
        # 构造请求参�?
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
            
            # 解析所有日期数�?
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
            
            # 如果只传了结束日期，返回单个�?
            if start_date is None:
                if end_date in series.index:
                    return series[end_date]
                else:
                    print(f"警告: 未找到日�?{end_date} 的数�?)
                    return pd.Series()
            
            # 如果传了起始和结束日期，返回范围数据
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            
            if start > end:
                start, end = end, start
            
            # 筛选日期范�?
            mask = (pd.to_datetime(series.index) >= start) & (pd.to_datetime(series.index) <= end)
            return series[mask]
            
        except Exception as e:
            print(f"请求新高数据失败: {e}")
            return pd.Series()
    
    # ========== 保留原有的单独接口（向后兼容�?=========
    
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
            "涨停�?: [int(info.get("ZT", 0))],
            "实际涨停": [int(info.get("SJZT", 0))],
            "跌停�?: [int(info.get("DT", 0))],
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
            "涨跌�?: float(s.get("increase_amount", 0)),
            "涨跌�?: s.get("increase_rate", ""),
            "成交�?�?": int(s.get("turnover", 0))
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
            "一�?: [info[0]],
            "二板": [info[1]],
            "三板": [info[2]],
            "高度�?: [info[3]],
            "连板�?%)": [round(info[4], 2)],
            "昨日首板今日上涨�?: [info[5]],
            "昨日首板今日下跌�?: [info[6]],
            "今日涨停破板�?%)": [round(info[7], 2)],
            "昨日涨停今表�?%)": [round(info[8], 2)],
            "昨日连板今表�?%)": [round(info[9], 2)],
            "昨日破板今表�?%)": [round(info[10], 2)],
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
            "当日涨跌�?%)": round(i[2], 2),
            "回撤幅度(%)": round(i[3], 2),
            "最新价": round(i[4], 2),
            "总数": total_num
        } for i in result.get("info", []) if len(i) >= 5])
    
    def get_sentiment_indicator(self, plate_id="801225", stocks=None, timeout=1600):
        """
        获取多头空头风向�?
        
        Args:
            plate_id: 板块ID，默�?801225"
            stocks: 股票代码列表，如果不提供则使用默认列�?
            timeout: 超时时间（秒），默认1600�?
            
        Returns:
            dict: 包含多头和空头风向标
                - date: 日期
                - plate_id: 板块ID
                - bullish_codes: 多头风向标股票代码列表（�?只）
                - bearish_codes: 空头风向标股票代码列表（�?只）
                - all_stocks: 所有股票代码列�?
        
        示例:
            crawler = KaipanlaCrawler()
            data = crawler.get_sentiment_indicator()
            print("多头风向�?", data['bullish_codes'])
            print("空头风向�?", data['bearish_codes'])
        """
        # 默认股票列表
        if stocks is None:
            stocks = [
                "002112", "603667", "600550", "601179", "600089", "600879", "603986",
                "002156", "002202", "002050", "002865", "002413", "002716", "000559",
                "000981", "002131", "603938", "603650", "000547", "600362", "600266",
                "600410", "002195", "603000", "001255", "000681", "002465"
            ]
        
        # 构造请求参�?
        stocks_str = ",".join(stocks)
        data = {
            "a": "PlateIntroduction_Info",
            "c": "ZhiShuRanking",
            "PhoneOSNew": "1",
            "Stocks": stocks_str,
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "apiv": "w42",
            "PlateID": plate_id
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
                print(f"获取风向标数据失�? {result.get('errcode', 'unknown error')}")
                return {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "plate_id": plate_id,
                    "bullish_codes": [],
                    "bearish_codes": [],
                    "all_stocks": []
                }
            
        except Exception as e:
            print(f"请求风向标数据失�? {e}")
            return {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "plate_id": plate_id,
                "bullish_codes": [],
                "bearish_codes": [],
                "all_stocks": []
            }
        
        # 解析股票列表
        stock_list = result.get("List", [])
        stock_codes = [item[0] for item in stock_list if item[0]]
        
        if not stock_codes:
            stock_codes = stocks  # 使用输入的股票列�?
        
        # 获取�?只和�?�?
        bullish_codes = stock_codes[:3]
        bearish_codes = stock_codes[-3:]
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "plate_id": plate_id,
            "bullish_codes": bullish_codes,
            "bearish_codes": bearish_codes,
            "all_stocks": stock_codes
        }
    
    def get_sector_ranking(self, date=None, index=0, timeout=1600):
        """
        获取涨停原因板块数据
        
        Args:
            date: 日期，格式YYYY-MM-DD，默认为当前日期
            index: 分页索引，默�?（第一页）
            timeout: 超时时间（秒），默认1600�?
            
        Returns:
            dict: 包含板块统计和详细列表的字典
                - summary: 市场概况（涨停数、跌停数等）
                - sectors: 板块列表，每个板块包含：
                    - sector_code: 板块代码
                    - sector_name: 板块名称
                    - stocks: 该板块涨停股票列�?
                    - stock_count: 涨停股票数量
        
        示例:
            crawler = KaipanlaCrawler()
            data = crawler.get_sector_ranking("2026-01-16")
            
            # 访问市场概况
            print(data['summary'])
            
            # 遍历板块
            for sector in data['sectors']:
                print(f"板块: {sector['sector_name']}, 涨停�? {sector['stock_count']}")
                for stock in sector['stocks']:
                    print(f"  {stock['股票代码']} {stock['股票名称']}")
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 构造请求参�?
        data = {
            "a": "GetPlateInfo_w38",
            "st": "100",
            "c": "DailyLimitResumption",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "Index": str(index),
            "apiv": "w42"
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
                "涨停�?: nums.get("ZT", 0),
                "跌停�?: nums.get("DT", 0),
                "涨跌�?: round(nums.get("ZBL", 0), 2),
                "昨日涨跌�?: round(nums.get("yestRase", 0), 2)
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
                for stock in sector_data.get("StockList", []):
                    if len(stock) >= 19:  # 确保数据完整
                        stock_info = {
                            "股票代码": stock[0],
                            "股票名称": stock[1],
                            "涨停�?: round(stock[4], 2) if stock[4] else 0,
                            "成交�?: stock[7],
                            "流通市�?: stock[8],
                            "连板天数": stock[9],
                            "连板次数": stock[10],
                            "概念标签": stock[11],
                            "封单�?: stock[12],
                            "总市�?: stock[13],
                            "涨停时间": stock[14],
                            "主力资金": stock[15],
                            "涨停原因": stock[16],
                            "主题": stock[17],
                            "是否首板": stock[18] if len(stock) > 18 else 0
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
    
    def get_consecutive_limit_up(self, date=None, timeout=1600):
        """
        获取指定日期的连板梯队情�?
        
        Args:
            date: 日期，格式YYYY-MM-DD，默认为当前日期
            timeout: 超时时间（秒），默认1600�?
            
        Returns:
            dict: 包含连板梯队信息
                - date: 日期
                - max_consecutive: 最高连板高�?
                - max_consecutive_stocks: 最高连板个股名称（多个�?分隔�?
                - max_consecutive_concepts: 最高连板个股题材（多个�?分隔�?
                - ladder: 连板梯队详细数据
                    - 2: 二连板股票列�?
                    - 3: 三连板股票列�?
                    - 4: 四连板股票列�?
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
        
        # 存储所有连板数�?
        ladder_data = {}
        max_consecutive = 0
        max_stocks = []
        
        # 从高到低尝试获取连板数据（最多尝试到20连板�?
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
                            
                            # 更新最高连�?
                            if pid_type > max_consecutive:
                                max_consecutive = pid_type
                                max_stocks = stocks
            
            except Exception as e:
                # 忽略错误，继续尝试下一个连板高�?
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
        
        # 提取最高板个股名称和题�?
        stock_names = []
        stock_concepts_list = []  # 每只股票的概念列�?
        
        for stock in max_stocks:
            stock_names.append(stock["股票名称"])
            
            # 合并题材和概�?
            all_concepts = []
            if stock["题材"]:
                # �?�?�?/"分割
                concepts = [c.strip() for c in stock["题材"].replace("/", "�?).split("�?) if c.strip()]
                all_concepts.extend(concepts)
            if stock["概念"]:
                # �?�?�?/"分割
                concepts = [c.strip() for c in stock["概念"].replace("/", "�?).split("�?) if c.strip()]
                all_concepts.extend(concepts)
            
            # 去重但保持顺�?
            unique_concepts = []
            seen = set()
            for c in all_concepts:
                if c not in seen:
                    unique_concepts.append(c)
                    seen.add(c)
            
            # 使用"�?分隔同一个股的多个题�?
            stock_concept = "�?.join(unique_concepts) if unique_concepts else ""
            stock_concepts_list.append(stock_concept)
        
        # 使用"/"分隔不同个股
        max_consecutive_stocks = "/".join(stock_names)
        # 使用"/"分隔不同个股的概�?
        max_consecutive_concepts = "/".join([c for c in stock_concepts_list if c])
        
        return {
            "date": date,
            "max_consecutive": max_consecutive,
            "max_consecutive_stocks": max_consecutive_stocks,
            "max_consecutive_concepts": max_consecutive_concepts,
            "ladder": ladder_data
        }
    
    def get_sector_limit_up_ladder(self, date=None, timeout=1600):
        """
        获取板块连板梯队（历史或实时�?
        
        Args:
            date: 日期，格式YYYY-MM-DD，默认为None（获取实时数据）
            timeout: 超时时间（秒），默认1600�?
            
        Returns:
            dict: 包含板块连板梯队信息
                - date: 日期
                - is_realtime: 是否为实时数�?
                - sectors: 板块列表，每个板块包含：
                    - sector_name: 板块名称
                    - limit_up_count: 涨停�?
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
                print(f"{sector['sector_name']}: {sector['limit_up_count']}只涨�?)
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
            
            # 解析板块数据（注意：字段名是大写的List�?
            sectors = []
            sector_list = result.get("List", [])
            
            for sector_data in sector_list:
                sector_name = sector_data.get("ZSName", "")
                sector_code = sector_data.get("ZSCode", "")
                td_list = sector_data.get("TD", [])
                
                # 解析股票列表
                stocks = []
                broken_stocks = []  # 反包板股票（TDType=0�?
                
                for td_group in td_list:
                    td_type = td_group.get("TDType", "1")
                    stock_list = td_group.get("Stock", [])
                    
                    # TDType说明�?
                    # 0: 反包板（记录但不计入连板梯队�?
                    # 1: 首板
                    # 2: 2连板
                    # 3: 3连板
                    # 9: 打开高度标注
                    # ...
                    
                    for stock_data in stock_list:
                        stock_code = stock_data.get("StockID", "")
                        stock_name = stock_data.get("StockName", "")
                        tips = stock_data.get("Tips", "")
                        
                        # 处理TDType=0（反包板�?
                        if td_type == "0":
                            # 反包板：从Tips中解析连板天�?
                            consecutive_days = 0
                            if tips:
                                import re
                                match = re.search(r'(\d+)�?\d+)�?, tips)
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
                        
                        # 处理TDType=9（打开高度标注�?
                        elif td_type == "9":
                            stock_info = {
                                "stock_code": stock_code,
                                "stock_name": stock_name,
                                "consecutive_days": 0,
                                "tips": tips,
                                "is_height_mark": True  # 标记为打开高度
                            }
                            stocks.append(stock_info)
                        
                        # 处理正常连板（TDType=1,2,3...�?
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
                
                if stocks or broken_stocks:  # 只添加有涨停股票的板�?
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
    
    def get_market_limit_up_ladder(self, date=None, timeout=1600):
        """
        获取全市场连板梯队（历史或实时）
        
        Args:
            date: 日期，格式YYYY-MM-DD，默认为None（获取实时数据）
            timeout: 超时时间（秒），默认1600�?
            
        Returns:
            dict: 包含全市场连板梯队信�?
                - date: 日期
                - is_realtime: 是否为实时数�?
                - ladder: 连板梯队数据
                    - 1: 首板股票列表
                    - 2: 2连板股票列表
                    - 3: 3连板股票列表
                    - ...
                - broken_stocks: 反包板股票列�?
                - height_marks: 打开高度标注股票列表
                - statistics: 统计信息
                    - total_limit_up: 总涨停数
                    - max_consecutive: 最高连�?
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
            print(f"最高连�? {data['statistics']['max_consecutive']}")
            
            # 遍历连板梯队
            for consecutive, stocks in sorted(data['ladder'].items(), reverse=True):
                print(f"{consecutive}连板: {len(stocks)}�?)
                for stock in stocks[:5]:  # 显示�?�?
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
                print(f"获取全市场连板梯队失�? {result.get('errcode', 'unknown error')}")
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
                    
                    # 处理Tip=0（反包板�?
                    if tip == "0":
                        consecutive_days = 0
                        if tips:
                            import re
                            match = re.search(r'(\d+)�?\d+)�?, tips)
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
                    
                    # 处理Tip=9（打开高度标注�?
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
            print(f"请求全市场连板梯队失�?({display_date}): {e}")
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
    
    def get_sector_capital_data(self, sector_code, date=None, timeout=1600):
        """
        获取板块资金成交额数�?
        
        Args:
            sector_code: 板块代码，如 "801235"（化工）
            date: 日期，格式YYYY-MM-DD，默认为空（获取实时数据�?
            timeout: 超时时间（秒），默认60�?
            
        Returns:
            dict: 包含板块资金数据
                - sector_code: 板块代码
                - date: 日期
                - turnover: 成交额（元）
                - change_pct: 涨跌幅（%�?
                - market_cap: 市值（亿元�?
                - main_net_inflow: 主力净额（元）
                - main_sell: 主卖（元�?
                - net_amount: 净额（元）
                - up_count: 上涨家数
                - down_count: 下跌家数
                - flat_count: 平盘家数
                - circulating_market_cap: 流通市值（元）
                - total_market_cap: 总市值（元）
                - turnover_rate: 换手率（%�?
                - main_net_inflow_pct: 主力净占比�?�?
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取化工板块实时数据
            data = crawler.get_sector_capital_data("801235")
            print(f"成交�? {data['turnover'] / 100000000:.2f}�?)
            print(f"主力净�? {data['main_net_inflow'] / 100000000:.2f}�?)
            
            # 获取指定日期数据
            data = crawler.get_sector_capital_data("801235", "2026-01-20")
        """
        # 根据是否传入日期，选择不同的API地址和headers
        if date:
            # 历史数据：使�?apphis.longhuvip.com
            url = self.base_url
            headers = self.headers
        else:
            # 实时数据：使�?apphwhq.longhuvip.com
            url = self.sector_base_url
            headers = self.sector_headers
        
        # 构造请求参�?
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
            # 实时数据pankou数组格式�?2个元素）�?
            # [成交�? 涨跌�? 市�? 主力净�? 主卖, 净�? 上涨, 下跌, 平盘, 流通市�? 总市�? 换手率]
            # 
            # 历史数据pankou数组格式�?1个元素）�?
            # [成交�? 涨跌�? 市�? 主力净�? 主卖, 净�? 上涨, 下跌, 平盘, 流通市�? 总市值]
            # 注意：历史数据没有换手率字段
            pankou = result.get("pankou", [])
            
            if len(pankou) < 11:
                print(f"板块数据格式不完�? {pankou}")
                return {}
            
            # 解析数据
            capital_data = {
                "sector_code": result.get("code", sector_code),
                "date": date if date else datetime.now().strftime("%Y-%m-%d"),
                "turnover": float(pankou[0]) if pankou[0] else 0,  # 成交额（元）
                "change_pct": float(pankou[1]) if pankou[1] else 0,  # 涨跌幅（%�?
                "market_cap": float(pankou[2]) if pankou[2] else 0,  # 市值（亿元�?
                "main_net_inflow": float(pankou[3]) if pankou[3] else 0,  # 主力净额（元）
                "main_sell": float(pankou[4]) if pankou[4] else 0,  # 主卖（元�?
                "net_amount": float(pankou[5]) if pankou[5] else 0,  # 净额（元）
                "up_count": int(pankou[6]) if pankou[6] else 0,  # 上涨家数
                "down_count": int(pankou[7]) if pankou[7] else 0,  # 下跌家数
                "flat_count": int(pankou[8]) if pankou[8] else 0,  # 平盘家数
                "circulating_market_cap": float(pankou[9]) if pankou[9] else 0,  # 流通市值（元）
                "total_market_cap": float(pankou[10]) if pankou[10] else 0,  # 总市值（元）
                "turnover_rate": float(pankou[11]) if len(pankou) > 11 and pankou[11] else 0,  # 换手率（%�? 历史数据可能没有
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
    
    def get_sector_strength_ndays(self, end_date, num_days=7, timeout=1600):
        """
        获取N日板块强度排名数�?
        
        Args:
            end_date: 结束日期，格式YYYY-MM-DD
            num_days: 获取天数，默�?�?
            timeout: 超时时间（秒），默认60�?
            
        Returns:
            pd.DataFrame: 包含N日板块强度数�?
                - 日期: 交易日期
                - 板块代码: 板块代码
                - 板块名称: 板块名称
                - 涨停�? 该板块涨停股票数�?
                - 涨停股票: 涨停股票列表（股票代码）
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取最�?日板块强�?
            df = crawler.get_sector_strength_ndays("2026-01-20", num_days=7)
            
            # 分析板块热度趋势
            sector_trend = df.groupby('板块名称')['涨停�?].sum().sort_values(ascending=False)
            print("7日最强板�?")
            print(sector_trend.head(10))
            
            # 查看特定板块的每日涨停数
            sector_name = "化工"
            sector_data = df[df['板块名称'] == sector_name]
            print(f"\n{sector_name}板块每日涨停�?")
            print(sector_data[['日期', '涨停�?]])
        """
        # 生成日期列表（向前推算num_days个交易日�?
        end = datetime.strptime(end_date, "%Y-%m-%d")
        dates = []
        current = end
        
        # 简单向前推算，实际交易日会在请求时过滤
        for i in range(num_days * 2):  # 多推算一些天数以确保有足够的交易�?
            date_str = current.strftime("%Y-%m-%d")
            dates.append(date_str)
            current -= timedelta(days=1)
            if len(dates) >= num_days * 2:
                break
        
        all_data = []
        trading_days_count = 0
        
        print(f"开始获取{num_days}日板块强度数�?..")
        
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
                
                # 解析每个板块的数�?
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
                        "涨停�?: stock_count,
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
        print(f"�?成功获取 {trading_days_count} 个交易日的板块数�?)
        
        return df
    
    def get_realtime_market_mood(self, timeout=1600):
        """
        获取实时市场情绪数据（涨停家数、跌停家数、上涨下跌家数及大盘数据�?
        
        Args:
            timeout: 超时时间（秒），默认60�?
            
        Returns:
            dict: 包含市场情绪数据
                - 上涨家数: 上涨股票数量
                - 下跌家数: 下跌股票数量
                - 涨停家数: 涨停股票数量
                - 跌停家数: 跌停股票数量
                - 全市场流通量: 全市场流通量
                - 前日流通量: 前一交易日流通量
                - 涨跌�? 上涨家数/下跌家数
                - 市场颜色: 1=红色(上涨), 0=绿色(下跌)
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取实时市场情绪
            mood = crawler.get_realtime_market_mood()
            print(f"涨停: {mood['涨停家数']}�?)
            print(f"跌停: {mood['跌停家数']}�?)
            print(f"上涨: {mood['上涨家数']}�?)
            print(f"下跌: {mood['下跌家数']}�?)
            print(f"涨跌�? {mood['涨跌�?]}")
        """
        # 构造请求参�?
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
                "涨跌�?: float(list_data.get("bl", 0)),
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
    
    def get_realtime_actual_limit_up_down(self, timeout=1600):
        """
        获取实时实际涨跌停数�?
        
        Args:
            timeout: 超时时间（秒），默认60�?
            
        Returns:
            dict: 包含实际涨跌停数�?
                - actual_limit_up: 实际涨停�?
                - actual_limit_down: 实际跌停�?
                - limit_up: 涨停数（包含一字板�?
                - limit_down: 跌停数（包含一字板�?
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取实时实际涨跌停数�?
            data = crawler.get_realtime_actual_limit_up_down()
            print(f"实际涨停: {data['actual_limit_up']}�?)
            print(f"实际跌停: {data['actual_limit_down']}�?)
        """
        # 构造请求参�?
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
                print(f"获取实时实际涨跌停数据失�? {result.get('errcode', 'unknown error')}")
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
            print(f"请求实时实际涨跌停数据失�? {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def get_realtime_board_stocks(self, board_type=1, timeout=1600):
        """
        获取实时指定连板的股票列�?
        
        Args:
            board_type: 连板类型
                1: 首板
                2: 二板
                3: 三板
                4: 四板
                5: 五板及以�?
            timeout: 超时时间（秒），默认60�?
            
        Returns:
            list: 股票列表，每个股票包含：
                - stock_code: 股票代码
                - stock_name: 股票名称
                - board_type: 连板类型
                - limit_up_reason: 涨停原因
                - turnover: 成交�?
                - circulating_market_cap: 流通市�?
                - total_market_cap: 总市�?
                - main_net_inflow: 主力净�?
                - seal_amount: 封单�?
                - concepts: 概念标签
                - amplitude: 振幅
                - consecutive_days: 连板天数
                - sector_code: 板块代码
                - limit_up_price: 涨停�?
                - limit_up_pct: 涨停幅度
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取首板股票
            first_board = crawler.get_realtime_board_stocks(board_type=1)
            print(f"首板股票: {len(first_board)}�?)
            
            # 获取二板股票
            second_board = crawler.get_realtime_board_stocks(board_type=2)
            print(f"二板股票: {len(second_board)}�?)
        """
        # 构造请求参�?
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
                print(f"获取实时{board_type}板股票失�? {result.get('errcode', 'unknown error')}")
                return []
            
            # 解析股票列表
            # 数据结构: result['info'][0] 是股票数组列�?
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
            print(f"请求实时{board_type}板股票失�? {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_realtime_all_boards_stocks(self, timeout=1600):
        """
        获取实时所有连板的股票列表（首板到五板以上�?
        
        Args:
            timeout: 超时时间（秒），默认60�?
            
        Returns:
            dict: 包含各连板的股票列表
                - first_board: 首板股票列表
                - second_board: 二板股票列表
                - third_board: 三板股票列表
                - fourth_board: 四板股票列表
                - fifth_board_plus: 五板及以上股票列�?
                - statistics: 统计信息
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取所有连板股�?
            data = crawler.get_realtime_all_boards_stocks()
            
            print(f"首板: {len(data['first_board'])}�?)
            print(f"二板: {len(data['second_board'])}�?)
            print(f"三板: {len(data['third_board'])}�?)
            print(f"四板: {len(data['fourth_board'])}�?)
            print(f"五板以上: {len(data['fifth_board_plus'])}�?)
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
        
        print("获取实时所有连板股�?..")
        
        for board_type, board_name in board_names.items():
            print(f"  获取{board_type}板股�?..")
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
        
        # 计算连板�?
        if total_stocks > 0:
            consecutive = total_stocks - len(all_boards["first_board"])
            all_boards["statistics"]["consecutive_rate"] = (consecutive / total_stocks) * 100
        else:
            all_boards["statistics"]["consecutive_rate"] = 0
        
        print(f"�?成功获取 {total_stocks} 只涨停股�?)
        
        return all_boards
    
    def get_board_stocks_count_and_list(self, board_type, timeout=1600):
        """
        获取指定连板的个股数量和个股列表
        
        Args:
            board_type: 连板类型
                1: 首板
                2: 二板
                3: 三板
                4: 四板
                5: 五板及以上（最高板�?
            timeout: 超时时间（秒），默认60�?
            
        Returns:
            tuple: (个股数量, 个股列表)
                - count: int, 该连板的个股数量
                - stocks: list, 个股列表，每个股票包含详细信�?
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取首板数量和列�?
            count, stocks = crawler.get_board_stocks_count_and_list(1)
            print(f"首板: {count}�?)
            for stock in stocks:
                print(f"  {stock['stock_name']} ({stock['stock_code']})")
            
            # 获取二板数量和列�?
            count, stocks = crawler.get_board_stocks_count_and_list(2)
            print(f"二板: {count}�?)
            
            # 获取最高板数量和列�?
            count, stocks = crawler.get_board_stocks_count_and_list(5)
            print(f"最高板: {count}�?)
        """
        # 获取该连板的股票列表
        stocks = self.get_realtime_board_stocks(board_type, timeout)
        
        # 返回数量和列�?
        count = len(stocks)
        
        return count, stocks
    
    def get_realtime_index_trend(self, stock_id="801900", time="15:00", timeout=1600):
        """
        获取实时指数趋势数据（昨日涨停今日表现、昨日断板今日表现等�?
        
        Args:
            stock_id: 指数代码
                - 801900: 昨日涨停今日表现
                - 801903: 昨日断板今日表现
                - 其他指数代码
            time: 时间点，格式"HH:MM"，默�?15:00"（收盘）
            timeout: 超时时间（秒），默认60�?
            
        Returns:
            dict: 包含指数趋势数据
                - stock_id: 指数代码
                - date: 日期
                - time: 时间
                - value: 指数�?
                - change_pct: 涨跌�?(%)
                - intraday_data: 分时数据列表
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取昨日涨停今日表现
            data = crawler.get_realtime_index_trend(stock_id="801900")
            print(f"昨日涨停今表�? {data['value']}")
            
            # 获取昨日断板今日表现
            data = crawler.get_realtime_index_trend(stock_id="801903")
            print(f"昨日断板今表�? {data['value']}")
        """
        # 构造请求参�?
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
            # 返回格式可能包含分时数据
            return {
                "stock_id": stock_id,
                "date": result.get("date", ""),
                "time": time,
                "value": result.get("value", 0),
                "change_pct": result.get("change_pct", 0),
                "intraday_data": result.get("intraday", []),
                "raw_data": result
            }
            
        except Exception as e:
            print(f"请求实时指数趋势失败: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def get_realtime_index_list(self, stock_ids=None, timeout=1600):
        """
        获取实时指数列表数据（批量获取多个指数）
        
        Args:
            stock_ids: 指数代码列表，默认获取主要指�?
                - SH000001: 上证指数
                - SZ399001: 深证成指
                - SZ399006: 创业板指
                - SH000688: 科创50
            timeout: 超时时间（秒），默认60�?
            
        Returns:
            dict: 包含各指数数�?
                - indexes: 指数列表
                    - stock_id: 指数代码
                    - name: 指数名称
                    - value: 最新�?
                    - change_pct: 涨跌�?(%)
                    - change_amount: 涨跌�?
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取主要指数
            data = crawler.get_realtime_index_list()
            for index in data['indexes']:
                print(f"{index['name']}: {index['change_pct']:.2f}%")
        """
        if stock_ids is None:
            stock_ids = ["SH000001", "SZ399001", "SZ399006", "SH000688"]
        
        # 构造请求参�?
        stock_id_list = ",".join(stock_ids)
        data_params = {
            "a": "RefreshStockList",
            "c": "UserSelectStock",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "Token": "",  # 可能需要token，但测试时可以为�?
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

    def get_realtime_sharp_withdrawal(self, timeout=1600):
        """
        获取实时大幅回撤股票数据
        
        Args:
            timeout: 超时时间（秒），默认60�?
            
        Returns:
            dict: 包含大幅回撤数据
                - date: 日期
                - count: 大幅回撤股票数量
                - stocks: 股票列表，每个股票包含：
                    - stock_code: 股票代码
                    - stock_name: 股票名称
                    - board_type: 连板类型
                    - tag: 标签（如"游资"�?
                    - latest_price: 最新价
                    - change_pct: 涨跌�?(%)
                    - pullback_pct: 回撤幅度 (%)
        
        示例:
            crawler = KaipanlaCrawler()
            
            # 获取实时大幅回撤数据
            data = crawler.get_realtime_sharp_withdrawal()
            print(f"日期: {data['date']}")
            print(f"大幅回撤: {data['count']}�?)
            
            for stock in data['stocks']:
                print(f"{stock['stock_name']}: 回撤{stock['pullback_pct']:.2f}%")
        """
        # 构造请求参�?
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
            # info 格式: [["股票代码", "股票名称", 连板类型, "标签", 最新价, 涨跌�? 回撤幅度], ...]
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
            print(f"涨停: {data['limit_up_count']}�?)
            print(f"跌停: {data['limit_down_count']}�?)
            print(f"炸板�? {data['blown_limit_up_rate']:.2f}%")
            print(f"昨日涨停今表�? {data['yesterday_limit_up_performance']:.2f}%")

    def get_realtime_rise_fall_analysis(self, timeout=1600):
        """
        获取实时涨跌分析数据

        Args:
            timeout: 超时时间（秒），默认60�?

        Returns:
            dict: 包含涨跌分析数据
                - date: 日期
                - limit_up_count: 涨停�?
                - limit_down_count: 跌停�?
                - blown_limit_up_count: 炸板�?
                - broken_limit_up_count: 破板�?
                - blown_limit_up_rate: 炸板�?(%)
                - yesterday_limit_up_performance: 昨日涨停今表�?(%)
                - yesterday_broken_performance: 昨日断板今日表现 (%)
                - raw_data: 原始数据

        示例:
            crawler = KaipanlaCrawler()

            # 获取实时涨跌分析
            data = crawler.get_realtime_rise_fall_analysis()
            print(f"日期: {data['date']}")
            print(f"涨停: {data['limit_up_count']}�?)
            print(f"跌停: {data['limit_down_count']}�?)
            print(f"炸板�? {data['blown_limit_up_rate']:.2f}%")
            print(f"昨日涨停今表�? {data['yesterday_limit_up_performance']:.2f}%")
        """
        # 构造请求参�?
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
            # info 格式: [[涨停�? 跌停�? 破板�? 炸板�? 炸板�? 昨日涨停今表�? 日期], ...]
            # 示例: [[78,4,72,8,24.2718,25,"2026-01-21"],[53,16,48,5,22.0588,15,"2026-01-20"]]
            info = result.get("info", [])
            
            if not info or len(info) < 1:
                print("未获取到涨跌分析数据")
                return {}
            
            # 取第一条数据（最新日期）
            latest = info[0]
            
            if len(latest) < 7:
                print(f"数据格式不完�? {latest}")
                return {}
            
            # 解析字段
            limit_up_count = int(latest[0])  # 涨停�?
            limit_down_count = int(latest[1])  # 跌停�?
            broken_limit_up_count = int(latest[2])  # 破板�?
            blown_limit_up_count = int(latest[3])  # 炸板�?
            blown_limit_up_rate = float(latest[4])  # 炸板�?(%)
            yesterday_limit_up_performance = float(latest[5])  # 昨日涨停今表�?(%)
            date_str = latest[6]  # 日期
            
            # 计算昨日断板今日表现（如果有第二条数据）
            yesterday_broken_performance = 0.0
            if len(info) > 1 and len(info[1]) >= 6:
                # 从昨日数据中获取断板今日表现
                # 注意：这个字段可能需要从其他接口获取
                pass
            
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
    

    def get_sector_intraday(self, sector_code, date=None, timeout=60):
        """
