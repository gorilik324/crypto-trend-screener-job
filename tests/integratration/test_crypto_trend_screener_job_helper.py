import unittest

from pybit.unified_trading import HTTP

from crypto_trend_screener_job.crypto_trend_screener_job_helper import CryptoTrendScreenerJobHelper


class CryptoTrendScreenerJobHelperTest(unittest.TestCase):

    def setUp(self):
        print("Start setUp")

        pybit_client = HTTP()
        self.helper = CryptoTrendScreenerJobHelper(pybit_client)

        print("Finished setUp")

    def test_get_available_tickers(self):
        pass

    def test_get_ohlc(self):
        pass

    def test_load_ohlc_cache(self):
        pass

    def test_calculate_percentage_change(self):
        pass

    def test_calculate_context(self):
        pass
