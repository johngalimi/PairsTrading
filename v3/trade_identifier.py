import yfinance as yf
import pandas as pd
import identifier_constants as constants


class TradeIdentifier:
    def __init__(self, frequency, start_date, end_date):
        self.frequency = frequency
        self.start_date = start_date
        self.end_date = end_date

    def get_historical_pricing_df(self, ticker):
        ticker_data = yf.Ticker(ticker)
        ticker_df = ticker_data.history(
            period=self.frequency, start=self.start_date, end=self.end_date
        )

        ticker_df.reset_index(inplace=True)
        ticker_df.rename(columns={constants.COLUMN_CLOSE: ticker}, inplace=True)

        return ticker_df[[constants.COLUMN_DATE, ticker]]

    def construct_pair_pricing_df(self, ticker_a, ticker_b):

        stock_a = self.get_historical_pricing_df(ticker=ticker_a)
        stock_b = self.get_historical_pricing_df(ticker=ticker_b)

        pair_df = pd.merge(stock_a, stock_b, on=constants.COLUMN_DATE)
        return pair_df


if __name__ == "__main__":
    identifier = TradeIdentifier(
        frequency=constants.FREQUENCY_DAILY,
        start_date="2020-01-01",
        end_date="2020-01-25",
    )

    df = identifier.construct_pair_pricing_df(ticker_a="MSFT", ticker_b="FB")
    print(df)
