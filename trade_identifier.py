import yfinance as yf
import pandas as pd
import identifier_constants as constants


class TradeIdentifier:
    def __init__(self, frequency, start_date, end_date):
        self.frequency = frequency
        self.start_date = start_date
        self.end_date = end_date

    def _retrieve_historical_data(self, ticker):
        ticker_data = yf.Ticker(ticker)
        return ticker_data.history(
            period=self.frequency, start=self.start_date, end=self.end_date
        )

    def _process_historical_data(self, ticker, pricing_df):
        pricing_df = pricing_df.reset_index()
        pricing_df = pricing_df.rename(columns={constants.COLUMN_CLOSE: ticker})
        return pricing_df[[constants.COLUMN_DATE, ticker]]

    def get_historical_pricing_df(self, ticker):
        ticker_df = self._retrieve_historical_data(ticker)
        return self._process_historical_data(ticker, ticker_df)

    def construct_pair_pricing_df(self, ticker_a, ticker_b):
        return pd.merge(
            self.get_historical_pricing_df(ticker=ticker_a),
            self.get_historical_pricing_df(ticker=ticker_b),
            on=constants.COLUMN_DATE,
        )


if __name__ == "__main__":
    identifier = TradeIdentifier(
        frequency=constants.FREQUENCY_DAILY,
        start_date="2020-01-01",
        end_date="2020-01-25",
    )

    df = identifier.construct_pair_pricing_df(ticker_a="MSFT", ticker_b="FB")
    print(df)
