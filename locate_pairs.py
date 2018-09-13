import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint


def find_pairs(industry, pairs):

    pricing_data = pd.read_csv('Data/' + industry + '.csv')
    pricing_data.index = pricing_data['date']
    
    candidates = pricing_data.columns.tolist()
    candidates.remove('date')
    
    stock_qty = len(candidates)
    
    for i in range(stock_qty):
        for j in range(i+1, stock_qty):
            try:

                first = candidates[i]
                second = candidates[j]
                
                security_pair = pd.DataFrame()
                security_pair[first] = pricing_data[first]
                security_pair[second] = pricing_data[second]
                
                if security_pair.isnull().values.any():
                    pass
                else:
                    result = coint(security_pair[first], security_pair[second])
                    pvalue = result[1]
                    if pvalue > 0 and pvalue <= 0.01:
                        print(first, second, pvalue)
                        pairs.append((industry, first, second, pvalue))
  
            except:
                print('Except: ' + candidates[i], candidates[j])
                pass
        

snp_500 = pd.read_csv('spy_holdings.csv')
sector_list = snp_500['Sector'].unique().tolist()
sector_list.remove('Unassigned')

pair_list = []

for sector in sector_list:
    print('----------' + sector.upper())
    find_pairs(sector, pair_list)
    
pair_df = pd.DataFrame(pair_list, 
                       columns=['industry', 'security1', 'security2', 'pvalue'])

pair_df.to_csv('candidate_pairs.csv')


            



