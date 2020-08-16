from .base import Base

class Stock(Base):
    def __init__(self, ticker):
        self.ticker = ticker

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
        else:
            print('no pricing data found for {}'.format(self.ticker))
