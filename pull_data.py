from datetime import datetime
import numpy as np
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web

years_back = 5

snp_500 = pd.read_csv('spy_holdings.csv')


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
        
generate_files()




        
        
        
        
        