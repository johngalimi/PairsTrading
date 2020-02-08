from position import Position

class Account:
    def __init__(self):
        self.balance = 0
        self.positions = []
    
    def update_balance(self, amount):
        self.balance += amount

    def enter_position(self, ticker, price, quantity):

        if self.balance > (price * quantity):
            new_position = Position(ticker, price, quantity)
            self.update_balance(-(price * quantity))
            self.positions.append(new_position)
            print('transaction executed, remaining funds: {}'.format(self.balance))
        else:
            print("insufficient funds to complete transaction")

    def fund_account(self, amount):
        self.update_balance(amount)
        print('funds updated, new account balance: {}'.format(self.balance))

    def view_portfolio(self):
        if len(self.positions) > 0:
            print('---Portfolio Details---')
            for position in self.positions:
                position.get_position_details()
        else:
            print('no positions to display')


if __name__ == '__main__':
    my_acct = Account()
    my_acct.fund_account(10000)
    my_acct.enter_position('AAPL', 300, 10)
    my_acct.enter_position('W', 80, 20)
    my_acct.enter_position('W', 80, 20)
    my_acct.view_portfolio()
    my_acct.fund_account(5000)
