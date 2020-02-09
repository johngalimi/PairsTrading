import time
import random
from datetime import date

from base import Base

class Position(Base):
    def __init__(self, ticker, price, quantity):
        self.ticker = ticker
        self.price = price
        self.quantity = quantity
        self.date_entered = date.today()
        self.position_id = self.set_position_id()
        self.component_posititions = []
        # position should be derived from component transactions
    
    def set_position_id(self):
        unique_id = "{}{}{}{}{}".format(self.ticker, str(round(time.time())), str(self.price), str(self.quantity), str(random.randint(10, 99)))
        return unique_id

   # def get_position_details(self):
    #    print(self.__dict__)

