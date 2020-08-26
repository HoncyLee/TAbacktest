# tabacktest.py 
import os , time
import csv
import datetime as DT
from pandas_datareader import data
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, rrulewrapper, RRuleLocator, YEARLY

from scipy import stats
import seaborn as sns
#from pyparsing import Word, alphas    ## OK installed

#data = {'SMA_a': [], 'SMA_b': [], 'Alpha': [], 'Beta': [], 'Benchmark_AR': [], 'Portfolio_AR': [] }
#pairs_df = pd.DataFrame(columns = ['SMA_a', 'SMA_b', 'Alpha', 'Beta', 'Benchmark_AR', 'Portfolio_AR'])


def main():
    start_time = time.time()
    # Load data from CSV while offline
    #csvfilename = 'GSPC-2yrs.csv' ## Total: 503 rows of data
    csvfilename = 'GSPC-40yrs.csv' ## Total: 10,086 rows of data
    df = pd.read_csv(csvfilename) # get data from CSV

    #tickers = '^GSPC'   # TO Create a list of tickers and weights; tickers = ['BND', 'VB', 'VEA', 'VOO', 'VWO'] ; wts = [0.1,0.2,0.25,0.25,0.2]
    #df = data.get_data_yahoo(tickers, start = '2018-01-01', end = '2020-01-01') # get data from yahoof online

    # Config
    global min_SMA, max_SMA, min_interval
    min_SMA = 10
    max_SMA = 200
    min_interval = 20  # set the minimum interval days between two SMA

    pair_SMA(df)
    
    #pd.set_option("display.max_rows", None)
    #print(df)
    #print(pairs_df)
    #plotgraph(df) # only the df and may not the actual SMAs
    elapsed_time = time.time() - start_time
    print("Program elapsed: ", time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

    ## Pair up combination of SMA and call start_run    
def pair_SMA(df):
    col = ['SMA_a', 'SMA_b', 'Alpha', 'Beta', 'Benchmark_AR', 'Portfolio_AR']
    pairs_df = pd.DataFrame(columns=col)
    SMA_a = min_SMA # initiate SMA_a to compare
    SMA_b = max_SMA
    index = 0
    for i in range(max_SMA - min_SMA - min_interval+1):
        for j in range(max_SMA - min_SMA - min_interval+1):
            pairs_df.loc[index] = run_test(df, SMA_a, SMA_b)
            index += 1
            SMA_b -= 1 
            if SMA_b - SMA_a < min_interval:
                break
        SMA_b = max_SMA    
        SMA_a += 1
        if SMA_b - SMA_a < min_interval:
            break

    print(pairs_df)
    print("Largest Return Combination: \n",pairs_df.nlargest(3, ['Portfolio_AR']))
    print("Largest Alpha Combination: \n",pairs_df.nlargest(3, ['Alpha']))
    print("Smalles Beta Combination: \n",pairs_df.nsmallest(3, ['Beta']))
    return pairs_df
    

    ## Run SMA test and generate/return its portfolio's data
   
def run_test(df, SMA_a, SMA_b):
    df['SMA_a'] = df.iloc[:,1].rolling(window= SMA_a ).mean()
    df['SMA_b'] = df.iloc[:,1].rolling(window= SMA_b ).mean()
    
    for ind in range(len(df)):
        # create Cash and Stock column and assign value
        if ind < SMA_b :   
            df.loc[ind, 'Cash'] = df.loc[0, 'Close']
            df.loc[ind, 'Stock'] = 0

        else :  
            # if SMA_s and SMA_l didn't cross, set Cash and Stock no change
            if df.loc[ind, 'SMA_a'] > df.loc[ind, 'SMA_b'] and df.loc[ind-1, 'SMA_a'] > df.loc[ind-1, 'SMA_b'] :
                df.loc[ind, 'Cash'] =  df.loc[ind-1, 'Cash']
                df.loc[ind, 'Stock'] = df.loc[ind-1, 'Stock']

            elif df.loc[ind, 'SMA_a'] < df.loc[ind, 'SMA_b'] and df.loc[ind-1, 'SMA_a'] < df.loc[ind-1, 'SMA_b']  :
                df.loc[ind, 'Cash'] =  df.loc[ind-1, 'Cash']
                df.loc[ind, 'Stock'] = df.loc[ind-1, 'Stock']
            
            # Trigger cross but no stock, then no sell, set Cash and Stock no change
            elif df.loc[ind-1, 'SMA_a'] > df.loc[ind-1, 'SMA_b'] and df.loc[ind, 'SMA_a'] < df.loc[ind, 'SMA_b'] and df.loc[ind-1, 'Stock']==0:
                df.loc[ind, 'Cash'] =  df.loc[ind-1, 'Cash']
                df.loc[ind, 'Stock'] = df.loc[ind-1, 'Stock']

            else: # if there is SMA_s and SMA_l cross, trigger buy/sell
                # Trigger buy
                if df.loc[ind-1, 'SMA_a'] < df.loc[ind-1, 'SMA_b'] and df.loc[ind, 'SMA_a'] > df.loc[ind, 'SMA_b']:
                    df.loc[ind, 'Cash'] = 0
                    df.loc[ind, 'Stock'] = df.loc[ind-1, 'Cash'] / df.loc[ind, 'Close']
                
                # Trigger sell
                if df.loc[ind-1, 'SMA_a'] > df.loc[ind-1, 'SMA_b'] and df.loc[ind, 'SMA_a'] < df.loc[ind, 'SMA_b']:
                    df.loc[ind, 'Stock'] = 0
                    df.loc[ind, 'Cash'] = df.loc[ind-1, 'Stock'] * df.loc[ind, 'Close']

        df['Portfolio'] = df['Cash'] + df['Stock'] * df['Close']
    
    num_of_years = int(round(len(df) / 250))
    benchmark_ar = (df.loc[len(df)-1, 'Close'] / df.loc[0,'Close']) ** (1/num_of_years) - 1 # BM Annual Return
    port_ar = (df.loc[len(df)-1, 'Portfolio'] / df.loc[0,'Portfolio']) ** (1/num_of_years) - 1 # Portf Annual Return
    port_ret = df['Portfolio'].pct_change()[1:] # daily return percentage change
    benchmark_ret = df["Close"].pct_change()[1:] # daily return percentage change
    (beta, alpha) = stats.linregress(benchmark_ret.values, port_ret.values)[0:2]    
    
    #plotgraph(df, benchmark_ret, port_ret)
    #plotreg(benchmark_ret,port_ret)
    #port_summary(df)
    return [SMA_a, SMA_b, alpha, beta, benchmark_ar, port_ar] # return data as a list


def port_summary(df):
    num_of_years = int(round(len(df) / 250))
    benchmark_ar = (df.loc[len(df)-1, 'Close'] / df.loc[0,'Close']) ** (1/num_of_years) - 1 # BM Annual Return
    port_ar = (df.loc[len(df)-1, 'Portfolio'] / df.loc[0,'Portfolio']) ** (1/num_of_years) - 1 # Portf Annual Return

    port_ret = df['Portfolio'].pct_change()[1:]
    benchmark_ret = df["Close"].pct_change()[1:]
    
    (beta, alpha) = stats.linregress(benchmark_ret.values, port_ret.values)[0:2]
    print("The portfolio Alpha is", '%.8f'%alpha)                  
    print("The portfolio Beta is", round(beta, 8))
    print("Benchmark Compounded Annual Return is", benchmark_ar)
    print("Portfolio Compounded Annual Return is", port_ar)
      

def plotgraph(df, benchmark_ret, port_ret):    
    fig = plt.figure(figsize=(16,9))
    ax = fig.subplots(2, sharex='col')

    ax[0].plot(df['Close'],label="S&P 500 - Close",color='blue')
    ax[0].plot(df['Portfolio'],label="Portfolio",color='green')
    ax[0].plot(df['SMA_a'],label="SMA_a",color='red',linestyle='--')
    ax[0].plot(df['SMA_b'],label="SMA_b",color='purple',linestyle='--')
    
    ax[0].set_title('S&P 500 vs Portfolio\nas of '+df.loc[0, 'Date']+' to '+df.loc[len(df)-1, 'Date'],  color='blue')
    ax[0].set_ylabel('S&P 500 index - closing', color='blue')
    ax[0].grid(True)
    
    ax[1].plot(benchmark_ret, label='Benchmark Return',color='blue')
    ax[1].plot(port_ret, label='Portfolio Return',color='green')

    ax[1].set_ylabel('Benchmark vs Portfolio Return', color='blue')
    ax[1].set_xlabel(f'{len(df)} Trading Days from {df.loc[0,"Date"]} to {df.loc[len(df)-1,"Date"]}', color='blue') 
    ax[1].grid(True)

    plt.show()

def plotreg(benchmark_ret,port_ret): # linear regression plot
    sns.regplot(benchmark_ret.values, port_ret.values, scatter_kws={"color": "blue"}, line_kws={"color": "red"})
    plt.xlabel("Benchmark Returns", color ="red")
    plt.ylabel("Portfolio Returns")
    plt.title("Portfolio Returns vs Benchmark Returns")
    plt.show()



main()        

