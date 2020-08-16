import time
import multiprocessing
from itertools import combinations


def is_prime(n):
    if n <= 1:
        return False

    if n <= 3:
        return True

    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True


def check_single_digit(number, prime_array):
    time.sleep(2)
    prime_array.append({number: is_prime(number)})


class TradeExplorer:
    def __init__(self, universe):
        self.pairs = self._get_pair_combinations(universe)

    def _get_pair_combinations(self, universe):
        return list(combinations(universe, 2))

    def is_valid_pair(self, stock_a, stock_b, valid_pairs):
        time.sleep(2)
        if stock_a is "GOOG":
            valid_pairs.append(f"{stock_a}+{stock_b}")

    def explore_universe(self):
        start = time.time()
        processes = []

        manager = multiprocessing.Manager()
        result = manager.list()

        for security_a, security_b in self.pairs:
            print(security_a, security_b)

            p = multiprocessing.Process(
                target=self.is_valid_pair, args=(security_a, security_b, result)
            )
            processes.append(p)
            p.start()

        for process in processes:
            process.join()

        print(result)
        print(f"Time Elapsed: {time.time() - start}")

        # return result


if __name__ == "__main__":

    SECURITY_LIST = ["FB", "GOOG", "AAPL", "MSFT"]

    explorer = TradeExplorer(universe=SECURITY_LIST)

    explorer.explore_universe()
