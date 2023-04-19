import logging

from pybit.unified_trading import HTTP
from crypto_trend_screener_job.crypto_trend_screener_job_helper import CryptoTrendScreenerJobHelper as Helper


class CryptoTrendScreenerJob:

    def __init__(self, config: dict) -> None:
        self.config = config
        self.pybit_client = HTTP(testnet=True,
                                 api_key=self.config["bybitApi"]["apiKey"],
                                 api_secret=self.config["bybitApi"]["secretKey"])

    def run(self):
        logging.info("Start job")

        logging.info("Finished job")
