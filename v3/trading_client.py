import requests

HOSTNAME_ROOT = "http://localhost:8090"
POST_HEADERS = {'Content-type': 'application/json'}

TRANSACTIONS_ENDPOINT = "/transactions"
POSITIONS_ENDPOINT = "/positions"
TRANSACTION_ENDPOINT = "/transaction"

def _get_helper(endpoint):
    response = requests.get(f"{HOSTNAME_ROOT}{endpoint}")
    return response.json()

def _post_helper(endpoint, data):
    response = requests.post(f"{HOSTNAME_ROOT}{endpoint}", headers=POST_HEADERS, json=data)
    return response.json()

def get_transactions():
    return _get_helper(endpoint=TRANSACTIONS_ENDPOINT)

def get_positions():
    return _get_helper(endpoint=POSITIONS_ENDPOINT)

def execute_transaction(ticker, price, quantity):
    transaction_object = {'ticker': ticker, 'price': price, 'quantity': quantity}
    return _post_helper(endpoint=TRANSACTION_ENDPOINT, data=transaction_object)


if __name__ == '__main__':
    transactions = get_transactions()
    print('Transactions:', transactions)

    print("\n")

    positions = get_positions()
    print('Positions:', positions)

    print("\n")

    transaction = execute_transaction(ticker='FB', price=182.76, quantity=12)
    transaction = execute_transaction(ticker='FB', price=190.1, quantity=-8)
    transaction = execute_transaction(ticker='F', price=50, quantity=8)
    transaction = execute_transaction(ticker='AAPL', price=221.23, quantity=-3)

    print("\n")

    transactions = get_transactions()
    print('Transactions:', transactions)

    print("\n")

    positions = get_positions()
    print('Positions:', positions)

    print("\n")