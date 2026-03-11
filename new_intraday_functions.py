    def get_sector_intraday(self, sector_code, date=None, timeout=60):
        """
        获取板块分时数据（价格+成交量成交额）
        
        Args:
            sector_code: 板块代码，如 "801001"（申万一级）
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
            
            # 获取实时分时数据
            data = crawler.get_sector_intraday("801001")
            
            # 获取历史分时数据
            data = crawler.get_sector_intraday("801001", "2026-01-16")
            
            print(f"板块: {data['sector_code']}")
            print(f"收盘价: {data['close']}")
            print(f"涨跌幅: {((data['close'] - data['preclose']) / data['preclose'] * 100):.2f}%")
            
            # 分析分时数据
            df = data['data']
            print(f"总成交量: {df['volume'].sum():,} 手")
            print(f"总成交额: {df['turnover'].sum() / 1e8:.2f} 亿")
        """
        is_realtime = date is None
        
        # 实时数据使用sector_base_url，历史数据使用base_url
        if is_realtime:
            url = self.sector_base_url
            headers = self.sector_headers
            display_date = datetime.now().strftime("%Y-%m-%d")
            day_param = ""
        else:
            url = self.base_url
            headers = self.headers
            display_date = date
            day_param = date
        
        # 1. 获取价格数据
        price_params = {
            "a": "GetTrendIncremental",
            "c": "ZhiShuL2Data",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "apiv": "w42",
            "StockID": sector_code,
            "Day": day_param
        }
        
        # 2. 获取成交量成交额数据
        volume_params = {
            "a": "GetVolTurIncremental",
            "c": "ZhiShuL2Data",
            "PhoneOSNew": "1",
            "DeviceID": str(uuid.uuid4()),
            "VerSion": "5.21.0.2",
            "apiv": "w42",
            "StockID": sector_code,
            "Day": day_param
        }
        
        try:
            # 请求价格数据
            response1 = requests.post(
                url,
                data=price_params,
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response1.raise_for_status()
            price_result = response1.json()
            
            if not price_result or price_result.get("errcode") != "0":
                print(f"获取板块价格数据失败: {price_result.get('errcode', 'unknown error')}")
                return {}
            
            # 请求成交量成交额数据
            response2 = requests.post(
                url,
                data=volume_params,
                headers=headers,
                verify=False,
                proxies={'http': None, 'https': None},
                timeout=timeout
            )
            response2.raise_for_status()
            volume_result = response2.json()
            
            if not volume_result or volume_result.get("errcode") != "0":
                print(f"获取板块成交量数据失败: {volume_result.get('errcode', 'unknown error')}")
                return {}
            
            # 解析价格数据
            # trend 格式: [["09:30", 3752.971, 0, 0, 2], ["09:31", 3766.026, 0, 0, 1], ...]
            # 字段: [时间, 价格, 未知, 未知, 涨跌趋势]
            trend_data = price_result.get("trend", [])
            
            # 解析成交量成交额数据
            # volumeturnover 格式: [["09:30", 2962948, 6790315022, 2], ["09:31", 8819226, 20924013579, 1], ...]
            # 字段: [时间, 成交量, 成交额, 涨跌趋势]
            volume_data = volume_result.get("volumeturnover", [])
            
            if not trend_data or not volume_data:
                print(f"未获取到板块 {sector_code} 的分时数据")
                return {}
            
            # 合并数据（按时间匹配）
            # 创建时间到成交量成交额的映射
            volume_dict = {}
            for item in volume_data:
                if len(item) >= 3:
                    time_str = item[0]
                    volume_dict[time_str] = {
                        "volume": int(item[1]),
                        "turnover": float(item[2])
                    }
            
            # 合并价格和成交量数据
            records = []
            for item in trend_data:
                if len(item) >= 5:
                    time_str = item[0]
                    vol_info = volume_dict.get(time_str, {"volume": 0, "turnover": 0})
                    
                    record = {
                        "time": time_str,
                        "price": float(item[1]),
                        "volume": vol_info["volume"],
                        "turnover": vol_info["turnover"],
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
            
            # 获取昨收价
            preclose = float(price_result.get("preclose_px", open_price))
            
            return {
                "sector_code": sector_code,
                "date": price_result.get("day", display_date),
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
    
    def get_stock_intraday(self, stock_code, date=None, timeout=60):
        """
        获取个股分时数据
        
        注意：此功能暂未实现，因为API接口尚未确定
        
        Args:
            stock_code: 股票代码，如 "002498"
            date: 日期，格式YYYY-MM-DD，默认为None（获取实时数据）
            timeout: 超时时间（秒），默认60秒
            
        Returns:
            dict: 空字典（功能未实现）
        """
        print(f"警告: get_stock_intraday 功能暂未实现")
        print(f"个股分时数据API接口尚未确定，请联系开发者")
        return {}
