import pandas as pd


class CryptoTrendScreenerJobHelper:
    CATEGORY = "linear"

    def __init__(self, pybit_client):
        self.pybit_client = pybit_client

    def get_available_tickers(self):
        response = self.pybit_client.get_instruments_info(category=self.CATEGORY)
        return [x["symbol"] for x in
                response["result"]["list"] if "USDT" in x["symbol"]]

    def get_ohlc(self, ticker, time_frame):
        response = self.pybit_client.get_kline(category=self.CATEGORY, symbol=ticker, interval=time_frame)
        ohlc = pd.DataFrame(response["result"]["list"],
                            columns=["startTime", "open", "high", "low", "close", "volume", "turnover"])

        ohlc["open"] = pd.to_numeric(ohlc["open"])
        ohlc["high"] = pd.to_numeric(ohlc["high"])
        ohlc["low"] = pd.to_numeric(ohlc["low"])
        ohlc["close"] = pd.to_numeric(ohlc["close"])
        ohlc["volume"] = pd.to_numeric(ohlc["volume"])
        ohlc["turnover"] = pd.to_numeric(ohlc["turnover"])
        ohlc["startTime"] = pd.to_numeric(ohlc["startTime"])
        ohlc['startTime'] = pd.to_datetime(ohlc["startTime"], unit='ms')
        return ohlc

    def load_ohlc_cache(self, tickers):
        ohlc_cache = {
            "daily": {},
            "weekly": {},
            "monthly": {}
        }

        for ticker in tickers:
            ohlc_daily = self.get_ohlc(ticker, "D")
            ohlc_weekly = self.get_ohlc(ticker, "W")
            ohlc_monthly = self.get_ohlc(ticker, "M")

            ohlc_cache["daily"][ticker] = ohlc_daily
            ohlc_cache["weekly"][ticker] = ohlc_weekly
            ohlc_cache["monthly"][ticker] = ohlc_monthly

        return ohlc_cache

    @staticmethod
    def calculate_percentage_change(ohlc, days):
        count_days = ohlc.shape[0] - 1

        actual_price = ohlc.loc[0]["close"]
        old_price = ohlc.loc[days]["open"] if days < count_days else ohlc.loc[count_days]["open"]

        return round(((actual_price - old_price) / old_price) * 100, 2)

    @staticmethod
    def calculate_context(ohlc):
        ohlc_filtered = ohlc.head(4)

        if ohlc_filtered.shape[0] < 4:
            return "N/A"

        # Compute candle color
        ohlc_filtered.loc[ohlc_filtered['close'] < ohlc_filtered['open'], 'candleColor'] = 'Red'
        ohlc_filtered.loc[ohlc_filtered['close'] >= ohlc_filtered['open'], 'candleColor'] = 'Green'

        # Compute context
        if ohlc_filtered.loc[1]["candleColor"] == "Green" and ohlc_filtered.loc[2]["candleColor"] == "Green":
            return "Up-trend"

        if ohlc_filtered.loc[1]["candleColor"] == "Red" and ohlc_filtered.loc[2]["candleColor"] == "Green" and \
                ohlc_filtered.loc[3]["candleColor"] == "Green":
            return "Start rotation after up-trend"

        if ohlc_filtered.loc[1]["candleColor"] == "Red" and ohlc_filtered.loc[2]["candleColor"] == "Red":
            return "Down-trend"

        if ohlc_filtered.loc[1]["candleColor"] == "Green" and ohlc_filtered.loc[2]["candleColor"] == "Red" and \
                ohlc_filtered.loc[3]["candleColor"] == "Red":
            return "Start rotation after down-trend"

        return "Rotation"
