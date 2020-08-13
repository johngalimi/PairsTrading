import requests
import constants as const


class TradingClient:
    def _construct_url(self, endpoint):
        return f"{const.HOSTNAME_ROOT}{endpoint}"

    def _get_helper(self, endpoint):
        response = requests.get(url=self._construct_url(endpoint))
        return response.json()

    def _post_helper(self, endpoint, data):
        response = requests.post(
            url=self._construct_url(endpoint), headers=const.POST_HEADERS, json=data
        )
        return response.json()

    def get_transactions(self):
        return self._get_helper(endpoint=const.TRANSACTIONS_ENDPOINT)

    def get_positions(self):
        return self._get_helper(endpoint=const.POSITIONS_ENDPOINT)

    def execute_transaction(self, ticker, price, quantity):
        transaction_object = {
            const.FIELD_TICKER: ticker,
            const.FIELD_PRICE: price,
            const.FIELD_QUANTITY: quantity,
        }
        return self._post_helper(
            endpoint=const.TRANSACTION_ENDPOINT, data=transaction_object
        )


if __name__ == "__main__":
    trader = TradingClient()

    transactions = trader.get_transactions()
    print("Transactions:", transactions)

    print("\n")

    positions = trader.get_positions()
    print("Positions:", positions)

    print("\n")

    transaction = trader.execute_transaction(ticker="FB", price=182.76, quantity=12)
    transaction = trader.execute_transaction(ticker="FB", price=190.1, quantity=-8)
    transaction = trader.execute_transaction(ticker="F", price=50, quantity=8)
    transaction = trader.execute_transaction(ticker="AAPL", price=221.23, quantity=-3)

    print("\n")

    transactions = trader.get_transactions()
    print("Transactions:", transactions)

    print("\n")

    positions = trader.get_positions()
    print("Positions:", positions)

    print("\n")
