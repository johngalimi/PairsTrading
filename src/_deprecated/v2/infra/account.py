from .transaction import Transaction
from .stock import Stock
from .base import Base
from .position import Position

class Account(Base):
    def __init__(self, account_id):
        self.account_id = account_id
        self.balance = 0
        self.positions = {}
    
    def update_balance(self, amount):
        self.balance += amount

    def execute_transaction(self, action, ticker, quantity):
        new_stock = Stock(ticker)
        current_price = new_stock.get_current_price()
        transaction_value = current_price * quantity

        new_transaction = Transaction(action, ticker, current_price, quantity)

        if action == 'BUY':
            if self.balance >= transaction_value:
                self.update_balance(-transaction_value)
                if self.check_portfolio(ticker):
                    self.positions[ticker].update_position(quantity, new_transaction.transaction_id)
                else:
                    new_position = Position(ticker, quantity, new_transaction.transaction_id)
                    self.positions[ticker] = new_position
            else:
                print("insufficient funds to complete transaction")

        elif action == 'SELL':
            # verify that stock exists in portfolio
            if self.check_portfolio(ticker):
                if new_transaction.quantity <= self.positions[ticker].quantity:
                    self.update_balance(transaction_value)
                    self.positions[ticker].update_position(-quantity, new_transaction.transaction_id)
                else:
                    print('trying to sell more shares than you own')
            else:
                print('trying to sell stock you do not own')
            
        print('---> transaction executed:')
        new_transaction.get_details()

        self.clean_positions()

    def check_portfolio(self, ticker):
        if ticker in self.positions.keys():
            return True
        return False

    def fund_account(self, amount):
        self.update_balance(amount)
        print('added {} to account, new balance: {}'.format(amount, self.balance))

    def view_portfolio(self):
        if len(self.positions) > 0:
            print('---Portfolio Details---')
            for ticker, position in self.positions.items():
                position.get_details()
        else:
            print('no positions to display')
        print('total investable cash: {}'.format(self.balance))

    def clean_positions(self):
        print('---> cleaning portfolio')
        new_positions = {ticker: position for (ticker, position) in self.positions.items() if self.positions[ticker].quantity > 0}
        self.positions = new_positions

                

