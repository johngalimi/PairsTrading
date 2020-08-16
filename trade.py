from src.client.trade_client import TradeClient
from src.client.trade_identifier import TradeIdentifier
from src.client.trade_processor import TradeProcessor
from src.client.trade_explorer import TradeExplorer

import time


if __name__ == "__main__":
    SECURITY_LIST = ["ALXN", "FB", "GOOG", "AAPL", "MSFT", "MCK"]

    START = "2015-01-01"
    END = "2020-01-25"
    MOVING_AVG_SHORT = 10
    MOVING_AVG_LONG = 30
    Z_THRESHOLD = 1.5

    identifier = TradeIdentifier(start_date=START, end_date=END)

    explorer = TradeExplorer(universe=SECURITY_LIST)

    valid_pairs = explorer.explore_universe(
        dataset_construction_pointer=identifier.construct_pair_pricing_df,
        validation_pointer=identifier.test_and_record_relationship,
    )

    for security_a, security_b in valid_pairs:

        # there's a layer of redundancy here, we also construct the df in the validation step
        df = identifier.construct_pair_pricing_df(
            ticker_a=security_a, ticker_b=security_b
        )

        processor = TradeProcessor(
            window_short=MOVING_AVG_SHORT,
            window_long=MOVING_AVG_LONG,
            z_threshold=Z_THRESHOLD,
        )
        df = processor.calculate_statistics(
            pricing_df=df, window_short=MOVING_AVG_SHORT, window_long=MOVING_AVG_LONG,
        )

        processor.identify_historical_opportunities(pricing_df=df)

        processor.visualize_relationship(pricing_df=df)

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