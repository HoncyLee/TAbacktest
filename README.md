CS50x Final Project 

Project Topic: Backtest SMAs Crossover Investment Strategy

Hello greeting from Hong Kong! 

The subject of my Project is SMA crossover strategy in S&P500.

In my project, I use S&P 500 index data from Jan 1st, 1980 to Jan 1st, 2020. 40 years of S&P500 raw data pulled from Yahoo finance, 
and backtest one of the simple strategy - SMA crossover method. There are total 10,085 trading days.

Let’s take a look the latest 5 years S&P500 chart as example. The blue line is the the market close index. Red line is the 10-day 
simple moving average value. Green line is the 30-day simple moving average value. In the chart, we can learn the pattern of them.

While red line(10-SMA) crossed green line(30-SMA) from below, the index is most likely trending up. If the red line crossed green 
line from top, the index is dropping. When we know this as a pattern(significant), we could use Python to search more details. 
Such as which combination of SMAs crossover is the most effective, what is the performance outcome of them.

Before we move on, we need to know there are two major keys to evaluate our portfolio in the investment industry. First, the Alpha. 
It measures the the return comparison to Benchmark which is the S&P500. If Alpha is larger than 0, that means the strategy is 
outperformed than benchmark. Secondly, the Beta. It measures the volatility of the portfolio, which is the indication of the risk 
in investment. If Beta is smaller than 1, that means the portfolio is less volatile than the Benchmark.

In the tabacktest.py program, I used SMA-10 to SMA-200 for research area, and set the minimal interval as 20 days. So there are 
14,706 combinations of SMA pairs. My program will search the best from those combinations. It took 23:24:23 to completed the whole 
task. And here we had the result. The largest return and Alpha’s pairs are SMA144 - SMA 164. The smallest Beta pairs is SMA10 - SMA31.

This is my CS50 final project. I will keep research for other strategy and social sentiment effects on stock market.

Thank you Dr David Malan, Brian Yu, and Doug Lloyd from Harvard University! Thank you all so much!!

Honcy Lee
Hong Kong
