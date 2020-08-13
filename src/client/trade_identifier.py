import yfinance as yf
import pandas as pd
from statsmodels.tsa.stattools import coint, adfuller
import src.client.constants.identifier_constants as constants


class TradeIdentifier:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = constants.FREQUENCY_DAILY

    def _retrieve_historical_data(self, ticker):
        ticker_data = yf.Ticker(ticker)
        return ticker_data.history(
            period=self.frequency, start=self.start_date, end=self.end_date
        )

    def _process_historical_data(self, ticker, pricing_df):
        pricing_df = pricing_df.reset_index()
        pricing_df = pricing_df.rename(columns={constants.COLUMN_CLOSE: ticker})
        return pricing_df[[constants.COLUMN_DATE, ticker]]

    def _get_historical_pricing_df(self, ticker):
        ticker_df = self._retrieve_historical_data(ticker)
        return self._process_historical_data(ticker, ticker_df)

    def construct_pair_pricing_df(self, ticker_a, ticker_b):
        return pd.merge(
            self._get_historical_pricing_df(ticker=ticker_a),
            self._get_historical_pricing_df(ticker=ticker_b),
            on=constants.COLUMN_DATE,
        )

    def _harvest_p_value(self, statsmodels_result):
        return statsmodels_result[1]

    def _compare_against_tolerance(self, p_value, tolerance):
        return p_value <= tolerance

    def _test_cointegration(self, ticker_a, ticker_b, df):
        result = coint(df[ticker_a], df[ticker_b])

        return self._compare_against_tolerance(
            p_value=self._harvest_p_value(result),
            tolerance=constants.COINTEGRATION_THRESHOLD,
        )

    def _test_stationarity(self, ticker_a, ticker_b, df):
        df[constants.COLUMN_SPREAD] = df[ticker_a] / df[ticker_b]
        result = adfuller(df[constants.COLUMN_SPREAD])

        return self._compare_against_tolerance(
            p_value=self._harvest_p_value(result),
            tolerance=constants.ADFULLER_TOLERANCE,
        )

    def test_relationship(self, ticker_a, ticker_b, pricing_df):
        is_cointegrated = self._test_cointegration(ticker_a, ticker_b, pricing_df)
        is_stationary = self._test_stationarity(ticker_a, ticker_b, pricing_df)

        return is_cointegrated and is_stationary
