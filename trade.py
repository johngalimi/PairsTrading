import identifier_constants as constants
from trade_identifier import TradeIdentifier

if __name__ == "__main__":
    STOCK_A = "ALXN"
    STOCK_B = "MCK"

    START = "2015-01-01"
    END = "2020-01-25"

    identifier = TradeIdentifier(
        frequency=constants.FREQUENCY_DAILY, start_date=START, end_date=END,
    )

    df = identifier.construct_pair_pricing_df(ticker_a=STOCK_A, ticker_b=STOCK_B)

    is_valid_pair = identifier.test_relationship(
        ticker_a=STOCK_A, ticker_b=STOCK_B, pricing_df=df
    )

    if is_valid_pair:
        print(df.head())
