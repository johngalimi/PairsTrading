#!/usr/bin/python3

from models.account import Account
from models.order import Order

if __name__ == '__main__':
    
    acct2 = Account(2)
    acct2.fund_account(10000)
    acct2.execute_transaction('BUY', 'AAPL', 10)
    acct2.execute_transaction('BUY', 'W', 20)
    acct2.execute_transaction('BUY', 'W', 30)
    acct2.execute_transaction('SELL', 'AAPL', 5)
    acct2.view_portfolio()
    acct2.execute_transaction('SELL', 'AAPL', 5)
    acct2.fund_account(5000)
    acct2.view_portfolio()

    target_buys = {'W':85, 'AAPL': 126}
    target_sells = {'W': 17, 'AAPL': 29}

    order = Order(target_buys, target_sells)
    consolidated_orders = order.generate_order()
    
    for order_type in consolidated_orders:
        for ticker, quantity in consolidated_orders[order_type]:
            acct2.execute_transaction(order_type, ticker, quantity)



