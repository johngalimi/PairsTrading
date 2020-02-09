from .base import Base

class Order(Base):
    def __init__(self, buys, sells):
        self.buys = {}
        self.sells = {}

    def get_orders(self):
        order_array = {}
        for buy in self.buys:
            pass
        for sell in self.sells:
            pass
