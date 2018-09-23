import os
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# TODO - identify optimal time to exit position - momentum strat on ma of zscores maybe?

plt.style.use('default')

pairs = pd.read_csv('fin_data/candidate_pairs.csv', index_col=False)

today = datetime.now()
today_date = str(today.year) + str(today.month) + str(today.day)

stock_1 = 'PNC'
stock_2 = 'SCHW'
days_1 = 10
days_2 = 30


def pair_analysis(security_a, security_b, days_a, days_b):
    
    industry = pairs['industry'][pairs['security1']==security_a].unique()[0]
    
    historical_prices = pd.read_csv('fin_data/' + industry + '.csv')
    
    historical_prices.index = historical_prices['date']
    
    historical_prices.index = pd.to_datetime(historical_prices.index)
    
    pair_df = historical_prices.copy()
    pair_df = pair_df[[security_a, security_b]]
    
    pair_df['spread'] = pair_df[security_a] / pair_df[security_b]

    # This implicitly assumes normal dist when, in reality, financial data may not be
    pair_df['zscore'] = (pair_df['spread'] - pair_df['spread'].mean())/(np.std(pair_df['spread']))
    
    pair_df[str(days_a) + 'D MA zscore'] = pair_df['zscore'].rolling(window=days_a).mean()
    pair_df[str(days_b) + 'D MA zscore'] = pair_df['zscore'].rolling(window=days_b).mean()
    
    return pair_df, industry


def visualize(zscore_df):
    
    try_pair, industry = zscore_df
    labels = try_pair.columns
    
    security_a = labels[0]
    security_b = labels[1]
    days_a = labels[4].split()[0]
    days_b = labels[5].split()[0]
    
    fig = plt.figure()
    
    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2, rowspan=1)
    
    try_pair[labels[0]].plot(label=labels[0])
    try_pair[labels[1]].plot(label=labels[1])
    
    ax1.set_xlabel(try_pair.index)
    
    plt.title(industry + ' - ' + security_a + ' & ' + security_b + ' - ' + today_date
              , fontsize=18)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Closing Price', fontsize=12)
    
    ax1.legend()
    
    ax2 = plt.subplot2grid((2, 2), (1, 0), colspan=2, rowspan=1)
    
    try_pair['zscore'].plot(label=security_a + ' / ' + security_b)
    try_pair[days_a + ' MA zscore'].plot()
    try_pair[days_b + ' MA zscore'].plot()
    plt.axhline(try_pair['zscore'].mean(), color='black')
    plt.axhline(1.0, color='red')
    plt.axhline(-1.0, color='red')
    
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Z-Score', fontsize=12)
    
    ax2.legend()
    
    plt.legend()
    
    plt.tight_layout()
    
    fig.dpi = 100
    
#    plt.savefig('pairs_data/' + today_date + '/' + industry.replace(' ', '') + 
#                '_' + security_a + '_' + security_b + '.pdf', bbox_inches='tight', dpi=fig.dpi)
    
    plt.show()


def all_candidates_visualize():   
    
    try:
        os.makedirs('pairs_data/' + today_date)
    except FileExistsError:
        pass
    
    for i in range(0, len(pairs)):
        stock_a = pairs['security1'].iloc[i]
        stock_b = pairs['security2'].iloc[i]
        
        print(stock_a, stock_b)
        
        visualize(pair_analysis(stock_a, stock_b, days_1, days_2))
        

def generate_trades(zscore_df):

    candidate_pair, industry = zscore_df
    
    # spread defined as sec_a / sec_b
    
    # If spread z-score < -1, BUY ratio (long sec_a, short sec_b)
    # b/c sec_a is underperforming while sec_b is outperforming (driving spread lower)
    # If spread z-score > 1, SELL ratio (short sec_a, long sec_b)
    # b/c sec_a is outperforming while sec_b is underperforming (driving spread higher)
    
    candidate_pair['buy_ratio'] = np.where(candidate_pair['zscore'] < -1, 1, 0)
    candidate_pair['sell_ratio'] = np.where(candidate_pair['zscore'] > 1, 1, 0)
    
    candidate_pair['zscore'].plot(lw=1.5)
    plt.axhline(candidate_pair['zscore'].mean(), color='black')
    plt.axhline(1.0, color='purple', ls='--')
    plt.axhline(-1.0, color='purple', ls='--')
    
    candidate_pair['zscore'][candidate_pair['buy_ratio']==1].plot(marker='o',
                  color='green', ls='None', ms=4)
    
    candidate_pair['zscore'][candidate_pair['sell_ratio']==1].plot(marker='o',
                  color='red', ls='None', ms=4)
    
    plt.show()
    
    return candidate_pair


test_df = pair_analysis(stock_1, stock_2, days_1, days_2)
visualize(test_df)

#generate_trades(test_df)


        


    

