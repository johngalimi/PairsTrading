import requests
import src.py.constants.client_constants as constants


class TradeClient:
    def probe_server(self):
        try:
            requests.get(url=self._construct_url(constants.INDEX_ENDPOINT))
        except requests.exceptions.ConnectionError:
            return False

        return True

    def _construct_url(self, endpoint):
        return f"{constants.HOSTNAME_ROOT}{endpoint}"

    def _get_helper(self, endpoint):
        response = requests.get(url=self._construct_url(endpoint))
        return response.json()

    def _post_helper(self, endpoint, data):
        response = requests.post(
            url=self._construct_url(endpoint), headers=constants.POST_HEADERS, json=data
        )
        return response.json()

    def get_transactions(self):
        return self._get_helper(endpoint=constants.TRANSACTIONS_ENDPOINT)

    def get_positions(self):
        return self._get_helper(endpoint=constants.POSITIONS_ENDPOINT)

    def execute_transaction(self, ticker, price, quantity):
        transaction_object = {
            constants.FIELD_TICKER: ticker,
            constants.FIELD_PRICE: price,
            constants.FIELD_QUANTITY: quantity,
        }
        return self._post_helper(
            endpoint=constants.TRANSACTION_ENDPOINT, data=transaction_object
        )
