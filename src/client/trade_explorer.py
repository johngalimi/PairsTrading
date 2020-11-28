import time
import multiprocessing
import pandas as pd
from itertools import combinations
import client.constants as constants


class TradeExplorer:
    def get_spy_holdings(self, sector=None):
        df = pd.read_csv(constants.SPY_HOLDINGS_FILE)

        if sector is None:
            df = df[df[constants.COLUMN_SECTOR] != constants.SECTOR_UNASSIGNED]
        else:
            df = df[df[constants.COLUMN_SECTOR] == sector]

        df = df[
            [constants.COLUMN_TICKER, constants.COLUMN_SECTOR, constants.COLUMN_WEIGHT]
        ]

        df = df[~df[constants.COLUMN_TICKER].str.contains("\.")]

        print(f"{sector}: {len(df)}")

        return df[constants.COLUMN_TICKER].to_list()

    def get_pair_combinations(self, universe=None):
        if universe is None:
            universe = []

        return list(combinations(universe, 2))

    def explore_universe(
        self, pair_list, dataset_construction_pointer, validation_pointer
    ):
        start = time.time()
        processes = []

        manager = multiprocessing.Manager()
        result = manager.list()

        for security_a, security_b in pair_list:
            pricing_df = dataset_construction_pointer(security_a, security_b)

            # this should be more defensive + unpack arg tuples of varying lengths
            # it is reliant upon validation pointer taking 3 args (the pair + list to write to)
            p = multiprocessing.Process(
                target=validation_pointer,
                args=(security_a, security_b, pricing_df, result),
            )
            processes.append(p)
            p.start()

        for process in processes:
            process.join()

        print(f"Time Elapsed: {time.time() - start}")

        return result
