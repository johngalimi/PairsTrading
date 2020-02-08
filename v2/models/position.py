import time

class Position:
    def __init__(self, ticker, price, quantity):
        self.ticker = ticker
        self.price = price
        self.quantity = quantity
        self.position_id = self.set_position_id()
    
    def set_position_id(self):
        unique_id = "{}{}{}{}".format(self.ticker, str(round(time.time())), str(self.price), str(self.quantity))
        return unique_id

