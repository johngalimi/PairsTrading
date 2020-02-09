import time
import random
from datetime import date

class Position:
    def __init__(self, ticker, quantity):
        self.ticker = ticker
        self.quantity = quantity
        self.position_id = self.set_position_id()
        self.component_transactions = []
    
    def set_position_id(self):
        unique_id = "{}{}{}".format(self.ticker, str(round(time.time())), str(random.randint(10, 99)))
        return unique_id

    def update_position(self, transaction_quantity, transaction_id):
        self.quantity += transaction_quantity
        self.component_transactions.append(transaction_id)

    def get_position_details(self):
        print(self.__dict__)

