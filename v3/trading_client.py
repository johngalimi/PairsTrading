import requests

HOSTNAME_ROOT = "http://localhost:8090"
TRANSACTIONS_ENDPOINT = "/transactions"
POSITIONS_ENDPOINT = "/positions"

def _get_helper(endpoint):
    response = requests.get(f"{HOSTNAME_ROOT}{endpoint}")
    return response.json()

def get_transactions():
    return _get_helper(TRANSACTIONS_ENDPOINT)

def get_positions():
    return _get_helper(POSITIONS_ENDPOINT)

if __name__ == '__main__':
    transactions = get_transactions()
    print('Transactions;', transactions)

    print("\n")

    positions = get_positions()
    print('Positions:', positions)