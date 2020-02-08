from position import Position

class Account:
    def __init__(self):
        self.balance = 0
        self.positions = []
    
    def update_balance(self, amount):
        self.balance += amount

    def enter_position(self, ticker, price, quantity):
        new_position = Position(ticker, price, quantity)
        self.positions.append(new_position)
        print(new_position.ticker, new_position.price, new_position.quantity, new_position.position_id)


if __name__ == '__main__':
    my_acct = Account()
    my_acct.enter_position('AAPL', 300, 10)
