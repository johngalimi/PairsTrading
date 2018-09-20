from datetime import datetime
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
from statsmodels.tsa.stattools import coint

years_back = 5

snp_500 = pd.read_csv('Input/spy_holdings.csv')


def industry_dataframe(industry, years):
    
    today = datetime.now()
    start = datetime(today.year - years, today.month, today.day)
    
    pricing_data = pd.DataFrame()
    
    tickers = snp_500['Identifier'][snp_500['Sector'] == industry].tolist()
    
    for ticker in tickers:
        try:
            stock = web.DataReader(ticker, 'iex', start)['close']
            pricing_data[ticker] = stock
            
        except:
            pass
        
    pricing_data.to_csv('Data/' + industry + '.csv')
    

def generate_files():
    
    sector_list = snp_500['Sector'].unique().tolist()
    sector_list.remove('Unassigned')
    
    for sector in sector_list:
        industry_dataframe(sector, years_back)


def find_pairs(industry, pairs):

# TODO -> Return Pandas Df from industry_dataframe fxn rather than re-reading csv
    
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
        

def locate_pairs():

    generate_files()
    
    sector_list = snp_500['Sector'].unique().tolist()
    sector_list.remove('Unassigned')
    
    pair_list = []
    
    for sector in sector_list:
        print('----------' + sector.upper())
        find_pairs(sector, pair_list)
        
    pair_df = pd.DataFrame(pair_list, 
                           columns=['industry', 'security1', 'security2', 'pvalue'])
    
    pair_df.to_csv('Pairs/Candidates/candidate_pairs.csv')
    
    
locate_pairs()

# need to eliminate stocks like F & UPS b/c coint to everything when low vol



            








        
        
        
        
        