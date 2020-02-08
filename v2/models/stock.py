class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.price = self.get_current_price()

    def get_current_price(self):
        mock_stocks = {
                'W': {
                    'price': 10
                    },
                'AAPL': {
                    'price': 200
                    }
                }

        if self.ticker in mock_stocks.keys():
            return mock_stocks[self.ticker]['price']
