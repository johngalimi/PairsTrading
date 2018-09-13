import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None

pair_df = pd.read_csv('candidate_pairs.csv', index_col=False)

pair_df = pair_df.iloc[:, 1:]

print(pair_df.tail(5))

def visualize_relationship(sec_a, sec_b):
    
    pricing_data = pd.read_csv('Data/' + 
            pair_df['industry'][pair_df['security1']==sec_a].unique()[0] + '.csv')
    
    pricing_data.index = pricing_data['date']
    
    try_pair = pricing_data[[sec_a, sec_b]]
    try_pair['spread'] = try_pair[sec_a] / try_pair[sec_b]

    try_pair['zscore'] = (try_pair['spread'] - try_pair['spread'].mean())/(np.std(try_pair['spread']))
    
    fig = plt.figure()
    
    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2, rowspan=1)
    
    try_pair[sec_a].plot(label=sec_a)
    try_pair[sec_b].plot(label=sec_b)
    
    ax1.legend()
    
    ax2 = plt.subplot2grid((2, 2), (1, 0), colspan=2, rowspan=1)
    
    try_pair['zscore'].plot(label=sec_a + ' / ' + sec_b)
    plt.axhline(try_pair['zscore'].mean(), color='black')
    plt.axhline(1.0, color='red')
    plt.axhline(-1.0, color='red')
    
    ax2.legend()
    
    plt.legend()
    plt.show()
        
    
visualize_relationship('SRE', 'ETR')
    
