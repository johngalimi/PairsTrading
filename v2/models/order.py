from .base import Base

class Order(Base):
    def __init__(self, buys, sells):
        self.buys = buys
        self.sells = sells

    def generate_order(self):
        orders = {'BUY':[], 'SELL':[]}
        for ticker in self.buys:
            orders['BUY'].append((ticker, self.buys[ticker]))
        for ticker in self.sells:
            orders['SELL'].append((ticker, self.sells[ticker]))

        return orders
