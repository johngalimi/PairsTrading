from position import Position
from stock import Stock

class Account:
    def __init__(self):
        self.balance = 0
        self.positions = {}
    
    def update_balance(self, amount):
        self.balance += amount

    def enter_position(self, ticker, quantity):

        new_stock = Stock(ticker)
        current_price = new_stock.get_current_price()

        if self.balance >= (current_price * quantity):
            new_position = Position(ticker, current_price, quantity)
            self.update_balance(-(current_price * quantity))

            if self.check_portfolio(ticker):
                self.positions[ticker].quantity += quantity
            else:
                self.positions[ticker] = new_position

            print('transaction executed, remaining funds: {}'.format(self.balance))
        else:
            print("insufficient funds to complete transaction")

    def check_portfolio(self, ticker):
        # check to see if stock already exists, if yes, add on to current position
        # else, net new position
        if ticker in self.positions.keys():
            return True
        return False

    def update_existing_position(self, quantity):
        pass

    def fund_account(self, amount):
        self.update_balance(amount)
        print('funds updated, new account balance: {}'.format(self.balance))

    def view_portfolio(self):
        if len(self.positions) > 0:
            print('---Portfolio Details---')
            for ticker, position in self.positions.items():
                position.get_position_details()
        else:
            print('no positions to display')
        print('total investable cash: {}'.format(self.balance))


if __name__ == '__main__':
    my_acct = Account()
    my_acct.fund_account(10000)
    my_acct.enter_position('AAPL', 10)
    my_acct.enter_position('W', 20)
    my_acct.enter_position('W', 30)
    my_acct.view_portfolio()
    my_acct.fund_account(5000)
    my_acct.check_portfolio('W')
