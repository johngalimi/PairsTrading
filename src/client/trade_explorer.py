import time
import multiprocessing
from itertools import combinations


class TradeExplorer:
    def __init__(self, universe):
        self.pairs = self._get_pair_combinations(universe)

    def _get_pair_combinations(self, universe):
        return list(combinations(universe, 2))

    def explore_universe(self, dataset_construction_pointer, validation_pointer):
        start = time.time()
        processes = []

        manager = multiprocessing.Manager()
        result = manager.list()

        for security_a, security_b in self.pairs:
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
