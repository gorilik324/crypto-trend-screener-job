import logging
from datetime import datetime

import pandas as pd
from pybit.unified_trading import HTTP

from crypto_trend_screener_job.crypto_trend_screener_job_helper import CryptoTrendScreenerJobHelper


class CryptoTrendScreenerJob:

    def __init__(self, config: dict) -> None:
        self.config = config
        self.pybit_client = HTTP()
        self.helper = CryptoTrendScreenerJobHelper(self.pybit_client)

    def run(self):
        logging.info("Start job")

        logging.info("Loading data")
        tickers = self.helper.get_available_tickers()
        ohlc_cache = self.helper.load_ohlc_cache(tickers)

        logging.info("Find intraday daily trends")
        intraday_daily_trends = self.find_intraday_daily_trends(tickers, ohlc_cache)

        logging.info("Find swing weekly trends")
        swing_weekly_trends = self.find_swing_weekly_trends(tickers, ohlc_cache)

        logging.info("Find swing monthly trends")
        swing_monthly_trends = self.find_swing_monthly_trends(tickers, ohlc_cache)

        logging.info("Save result to excel file")
        self.save_result_to_excel(intraday_daily_trends, swing_weekly_trends, swing_monthly_trends)

        logging.info("Finished job")

    def find_intraday_daily_trends(self, tickers, ohlc_cache):
        intraday_daily_trends = []

        for ticker in tickers:
            ohlc_daily = ohlc_cache["daily"][ticker]

            intraday_daily_trends.append({
                "ticker": ticker,
                "Change 7 days, %": self.helper.calculate_percentage_change(ohlc=ohlc_daily, days=7),
                "Context D": self.helper.calculate_context(ohlc_daily)
            })

        return pd.DataFrame(intraday_daily_trends)

    def find_swing_weekly_trends(self, tickers, ohlc_cache):
        swing_weekly_trends = []
        for ticker in tickers:
            ohlc_daily = ohlc_cache["daily"][ticker]
            ohlc_weekly = ohlc_cache["weekly"][ticker]

            swing_weekly_trends.append({
                "ticker": ticker,
                "Change 30 days, %": self.helper.calculate_percentage_change(ohlc=ohlc_daily, days=30),
                "Context W": self.helper.calculate_context(ohlc_weekly)
            })
        return pd.DataFrame(swing_weekly_trends)

    def find_swing_monthly_trends(self, tickers, ohlc_cache):
        swing_monthly_trends = []
        for ticker in tickers:
            ohlc_daily = ohlc_cache["daily"][ticker]
            ohlc_monthly = ohlc_cache["monthly"][ticker]

            swing_monthly_trends.append({
                "ticker": ticker,
                "Change 90 days, %": self.helper.calculate_percentage_change(ohlc=ohlc_daily, days=90),
                "Context M": self.helper.calculate_context(ohlc_monthly)
            })
        return pd.DataFrame(swing_monthly_trends)

    @staticmethod
    def save_result_to_excel(intraday_daily_trends, swing_weekly_trends, swing_monthly_trends):
        now = datetime.now().strftime("%Y%m%d")
        filename = "CryptoTrendScreener_" + now + ".xlsx"
        writer = pd.ExcelWriter(filename, engine="openpyxl")

        intraday_daily_trends["ticker"] = "BYBIT:" + intraday_daily_trends["ticker"] + ".P"
        swing_weekly_trends["ticker"] = "BYBIT:" + swing_weekly_trends["ticker"] + ".P"
        swing_monthly_trends["ticker"] = "BYBIT:" + swing_monthly_trends["ticker"] + ".P"

        intraday_daily_trends.to_excel(writer, sheet_name="Intraday D trends", index=False)
        swing_weekly_trends.to_excel(writer, sheet_name="Swing W trends", index=False)
        swing_monthly_trends.to_excel(writer, sheet_name="Swing M trends", index=False)

        writer.close()
