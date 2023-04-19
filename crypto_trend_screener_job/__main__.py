import logging.config

from crypto_trend_screener_job.constants import LOGGER_CONFIG_FILE_PATH, __logo__, CONFIG_FILE_PATH
from crypto_trend_screener_job.crypto_trend_screener_job import CryptoTrendScreenerJob
from crypto_trend_screener_job.utils import load_config

if __name__ == "__main__":
    logging.config.fileConfig(fname=LOGGER_CONFIG_FILE_PATH, disable_existing_loggers=False)
    logging.info(__logo__)

    try:
        config = load_config(CONFIG_FILE_PATH)

        job = CryptoTrendScreenerJob(config)
        job.run()
    except:
        logging.exception("Error in app: ")