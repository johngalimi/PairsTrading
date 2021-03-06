import inspect
import time
import random
from datetime import date

from .base import Base

class Transaction(Base):
    def __init__(self, action, ticker, price, quantity):
        self.action = action
        self.ticker = ticker
        self.price = price
        self.quantity = quantity
        self.date_executed = date.today()
        self.transaction_id = self.set_transaction_id()
    
    def set_transaction_id(self):
        unique_id = "{}{}{}{}{}".format(self.ticker, str(round(time.time())), str(self.price), str(self.quantity), str(random.randint(10, 99)))
        return unique_id

    def get_transaction_details(self):
        print(self.__dict__)

    def inspect_instance(self):
        signature = inspect.signature(self.__init__)
        for name, parameter in signature.items():
                print(name, parameter.default, parameter.annotation, parameter.kind)
                
