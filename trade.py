from src.client.trade_client import TradeClient
from src.client.trade_identifier import TradeIdentifier
from src.client.trade_processor import TradeProcessor
from src.client.trade_explorer import TradeExplorer

import time
def is_valid_pair(stock_a, stock_b, pricing_df, valid_pairs):
    time.sleep(2)
    if stock_a is "GOOG":
        valid_pairs.append((stock_a, stock_b))


if __name__ == "__main__":
    trader = TradeClient()

    if trader.probe_server():

        transaction = trader.execute_transaction(ticker="FB", price=182.76, quantity=12)
        transaction = trader.execute_transaction(ticker="FB", price=190.1, quantity=-8)
        transaction = trader.execute_transaction(ticker="F", price=50, quantity=8)
        transaction = trader.execute_transaction(
            ticker="AAPL", price=221.23, quantity=-3
        )

        transactions = trader.get_transactions()
        print("Transactions:", transactions)

        print("\n")

        positions = trader.get_positions()
        print("Positions:", positions)

        print("\n")

    SECURITY_LIST = ["FB", "GOOG", "AAPL", "MSFT"]

    explorer = TradeExplorer(universe=SECURITY_LIST)

    valid_pairs = explorer.explore_universe(validation_pointer=is_valid_pair)

    print(valid_pairs)

    if False:

        STOCK_A = "ALXN"
        STOCK_B = "MCK"

        START = "2015-01-01"
        END = "2020-01-25"

        identifier = TradeIdentifier(start_date=START, end_date=END)

        df = identifier.construct_pair_pricing_df(ticker_a=STOCK_A, ticker_b=STOCK_B)

        is_valid_pair = identifier.test_relationship(
            ticker_a=STOCK_A, ticker_b=STOCK_B, pricing_df=df
        )

        if is_valid_pair:

            MOVING_AVG_SHORT = 10
            MOVING_AVG_LONG = 30
            Z_THRESHOLD = 1.5

            processor = TradeProcessor(
                window_short=MOVING_AVG_SHORT,
                window_long=MOVING_AVG_LONG,
                z_threshold=Z_THRESHOLD,
            )
            df = processor.calculate_statistics(
                pricing_df=df, window_short=MOVING_AVG_SHORT, window_long=MOVING_AVG_LONG
            )

            processor.identify_historical_opportunities(pricing_df=df)

            processor.visualize_relationship(pricing_df=df)
