import os
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pairs = pd.read_csv('pairs_data/candidates/candidate_pairs.csv', index_col=False)

today = datetime.now()
today_date = str(today.year) + str(today.month) + str(today.day)

stock_1 = 'FB'
stock_2 = 'KLAC'
days_1 = 30
days_2 = 90


def pair_analysis(security_a, security_b, days_a, days_b):
    
    industry = pairs['industry'][pairs['security1']==security_a].unique()[0]
    
    historical_prices = pd.read_csv('fin_data/' + industry + '.csv')
    
    historical_prices.index = historical_prices['date']
    
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
    
    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2, rowspan=1)
    
    try_pair[labels[0]].plot(label=labels[0])
    try_pair[labels[1]].plot(label=labels[1])
    
    ax1.legend()
    
    ax2 = plt.subplot2grid((2, 2), (1, 0), colspan=2, rowspan=1)
    
    try_pair['zscore'].plot(label=security_a + ' / ' + security_b)
    try_pair[days_a + ' MA zscore'].plot()
    try_pair[days_b + ' MA zscore'].plot()
    plt.axhline(try_pair['zscore'].mean(), color='black')
    plt.axhline(1.0, color='red')
    plt.axhline(-1.0, color='red')
    
    ax2.legend()
    
    plt.legend()
    
    plt.tight_layout()
    
    plt.savefig('pairs_data/' + today_date + '/' + industry.replace(' ', '') + 
                '_' + security_a + '_' + security_b + '.pdf', bbox_inches='tight')
    
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
    

all_candidates_visualize()
    
    

