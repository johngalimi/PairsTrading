#!/usr/bin/python3

from models.account import Account

if __name__ == '__main__':
    
    my_acct = Account(1)
    my_acct.fund_account(10000)
    my_acct.enter_position('AAPL', 10)
    my_acct.enter_position('W', 20)
    my_acct.enter_position('W', 30)
    my_acct.view_portfolio()
    my_acct.fund_account(5000)
    
    print('--------------------------')

    acct2 = Account(2)
    acct2.fund_account(10000)
    acct2.execute_transaction('BUY', 'AAPL', 10)
    acct2.execute_transaction('BUY', 'W', 20)
    acct2.execute_transaction('BUY', 'W', 30)
    acct2.view_portfolio()
    acct2.fund_account(5000)

