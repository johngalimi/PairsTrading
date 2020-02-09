import time
import random
from datetime import date

from .base import Base

class Position(Base):
    def __init__(self, ticker, quantity, initial_transaction):
        self.ticker = ticker
        self.quantity = quantity
        self.initial_transaction = initial_transaction
        self.position_id = self.set_position_id()
        self.component_transactions = [self.initial_transaction]
    
    def set_position_id(self):
        unique_id = "{}{}{}".format(self.ticker, str(round(time.time())), str(random.randint(10, 99)))
        return unique_id

    def update_position(self, transaction_quantity, transaction_id):
        self.quantity += transaction_quantity
        self.component_transactions.append(transaction_id)

