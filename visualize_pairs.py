import os
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None

today = datetime.now()
today_date = str(today.year) + str(today.month) + str(today.day)

plt.style.use('default')

pair_df = pd.read_csv('candidate_pairs.csv', index_col=False)

pair_df = pair_df.iloc[:, 1:]


def visualize_relationship(sec_a, sec_b, days_1, days_2):
    
    pair_industry = pair_df['industry'][pair_df['security1']==sec_a].unique()[0]
    
    pricing_data = pd.read_csv('Data/' + pair_industry + '.csv')
    
    pricing_data.index = pricing_data['date']
    
    try_pair = pricing_data[[sec_a, sec_b]]
    try_pair['spread'] = try_pair[sec_a] / try_pair[sec_b]

    # This implicitly assumes normal dist when, in reality, financial data may not be
    try_pair['zscore'] = (try_pair['spread'] - try_pair['spread'].mean())/(np.std(try_pair['spread']))
    
    window_1 = days_1
    window_2 = days_2
    
    try_pair[str(window_1) + 'D MA zscore'] = try_pair['zscore'].rolling(window=window_1).mean()
    try_pair[str(window_2) + 'D MA zscore'] = try_pair['zscore'].rolling(window=window_2).mean()
    
#    fig = plt.figure()
    
    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2, rowspan=1)
    
    try_pair[sec_a].plot(label=sec_a)
    try_pair[sec_b].plot(label=sec_b)
    
    ax1.legend()
    
    ax2 = plt.subplot2grid((2, 2), (1, 0), colspan=2, rowspan=1)
    
    try_pair['zscore'].plot(label=sec_a + ' / ' + sec_b)
    try_pair[str(window_1) + 'D MA zscore'].plot()
    try_pair[str(window_2) + 'D MA zscore'].plot()
    plt.axhline(try_pair['zscore'].mean(), color='black')
    plt.axhline(1.0, color='red')
    plt.axhline(-1.0, color='red')
    
    ax2.legend()
    
    plt.legend()
    
    plt.tight_layout()
    
    plt.savefig('Pairs/' + today_date + '/' + pair_industry.replace(' ', '') + '_' + sec_a + '_' + sec_b + '.pdf', 
                bbox_inches='tight')


def generate_files():   
    
    try:
        os.makedirs('Pairs/' + today_date)
    except FileExistsError:
        pass
    
    for i in range(0, len(pair_df)):
        stock_a = pair_df['security1'].iloc[i]
        stock_b = pair_df['security2'].iloc[i]
        
        print(stock_a, stock_b)
        
        visualize_relationship(stock_a, stock_b, 25, 100)
    

generate_files()
    
# TESTING
    
#first_stock = ['TMO', 'GS', 'CRM']
#second_stock = ['PKI', 'LNC', 'INTU']
#
#for i in range(0, len(first_stock)):
#    visualize_relationship(first_stock[i], second_stock[i], 25, 100)

    



    
