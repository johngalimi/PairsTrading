import requests

HOSTNAME_ROOT = "http://localhost:8090"
POST_HEADERS = {'Content-type': 'application/json'}

TRANSACTIONS_ENDPOINT = "/transactions"
POSITIONS_ENDPOINT = "/positions"
TRANSACTION_ENDPOINT = "/transaction"

class TradingClient:

    def _get_helper(self, endpoint):
        response = requests.get(f"{HOSTNAME_ROOT}{endpoint}")
        return response.json()

    def _post_helper(self, endpoint, data):
        response = requests.post(f"{HOSTNAME_ROOT}{endpoint}", headers=POST_HEADERS, json=data)
        return response.json()

    def get_transactions(self):
        return self._get_helper(endpoint=TRANSACTIONS_ENDPOINT)

    def get_positions(self):
        return self._get_helper(endpoint=POSITIONS_ENDPOINT)

    def execute_transaction(self, ticker, price, quantity):
        transaction_object = {'ticker': ticker, 'price': price, 'quantity': quantity}
        return self._post_helper(endpoint=TRANSACTION_ENDPOINT, data=transaction_object)


if __name__ == '__main__':
    trader = TradingClient()

    transactions = trader.get_transactions()
    print('Transactions:', transactions)

    print("\n")

    positions = trader.get_positions()
    print('Positions:', positions)

    print("\n")

    transaction = trader.execute_transaction(ticker='FB', price=182.76, quantity=12)
    transaction = trader.execute_transaction(ticker='FB', price=190.1, quantity=-8)
    transaction = trader.execute_transaction(ticker='F', price=50, quantity=8)
    transaction = trader.execute_transaction(ticker='AAPL', price=221.23, quantity=-3)

    print("\n")

    transactions = trader.get_transactions()
    print('Transactions:', transactions)

    print("\n")

    positions = trader.get_positions()
    print('Positions:', positions)

    print("\n")