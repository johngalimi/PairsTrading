from datetime import datetime
import numpy as np
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
pd.options.mode.chained_assignment = None
import pandas_datareader.data as web
from statsmodels.tsa.stattools import coint, adfuller

years_back = 5
coint_tolerance = 0.01
adfuller_tolerance = 0.05

snp_500 = pd.read_csv('input_data/spy_holdings.csv')


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
        
    pricing_data.to_csv('fin_data/' + industry + '.csv')
    

def generate_files():
    
    sector_list = snp_500['Sector'].unique().tolist()
    sector_list.remove('Unassigned')
    
    for sector in sector_list:
        industry_dataframe(sector, years_back)


def find_pairs(industry, pairs, threshold):
    
    pricing_data = pd.read_csv('fin_data/' + industry + '.csv')
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
                    if pvalue > 0 and pvalue <= threshold:
                        print(first, second, pvalue)
                        pairs.append((industry, first, second, pvalue))
  
            except:
                print('Except: ' + candidates[i], candidates[j])
                pass
        

def locate_cointegrated_pairs():

    generate_files()
    
    sector_list = snp_500['Sector'].unique().tolist()
    sector_list.remove('Unassigned')
    
    pair_list = []
    
    for sector in sector_list:
        print('----------' + sector.upper())
        find_pairs(sector, pair_list, coint_tolerance)
        
    pair_df = pd.DataFrame(pair_list, 
                           columns=['industry', 'security1', 'security2', 'coint_pval'])
    
    return pair_df
    
    
def stationarity_test(security_a, security_b):
    
    candidate_df = pd.read_csv('fin_data/candidate_pairs.csv')
    
    industry = candidate_df['industry'][candidate_df['security1']==security_a].unique()[0]
    
    historical_prices = pd.read_csv('fin_data/' + industry + '.csv')
    historical_prices.index = historical_prices['date']
    historical_prices.index = pd.to_datetime(historical_prices.index)
    
    pair_df = historical_prices.copy()
    pair_df = pair_df[[security_a, security_b]]
    
    pair_df['spread'] = pair_df[security_a] / pair_df[security_b]
    
    # Test for stationarity of time series
    p_value = adfuller(pair_df['spread'])[1]
    
    print(security_a, security_b, p_value)
    
    return p_value


def locate_stationary_pairs(threshold):
    
    candidate_df = locate_cointegrated_pairs()
    
    candidate_df['adfuller_pval'] = np.zeros(len(candidate_df))
    
    for i in range(0, len(candidate_df)):
        
        stock_a = candidate_df['security1'].iloc[i]
        stock_b = candidate_df['security2'].iloc[i]
    
        try:
    
            adf_p_value = stationarity_test(stock_a, stock_b)
        
            candidate_df['adfuller_pval'][(candidate_df['security1']==stock_a) &
                (candidate_df['security2']==stock_b)] = adf_p_value
            
        except:
            print('ERROR: ' + stock_a + '_' + stock_b)
    
    candidate_df = candidate_df[(candidate_df['adfuller_pval'] <= threshold) & 
                                (candidate_df['adfuller_pval'] > 0)]
    
    candidate_df.to_csv('fin_data/candidate_pairs.csv')

    
locate_stationary_pairs(adfuller_tolerance)

    




            








        
        
        
        
        