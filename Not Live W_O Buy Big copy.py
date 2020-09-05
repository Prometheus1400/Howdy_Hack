#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 20:01:04 2020

@author: danielcahak
"""
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import datetime
#from MainAlgorithms import MovingAverageAlgorithm,BuyOrSell,Plotter
plt.rcParams["figure.figsize"] = (10,8)
#Initiaal Investing Account Value
AccountVal = 2000
InitAccountVal = AccountVal
actions = []
#Choose Which Stop to Back-Test Over
#Choose Time Period and Interval
print('\nInitial Value: $'+str(InitAccountVal))
#Initializing Variables
PriceList = []
downDiffs = []
upDiffs = []
HaveStock = 0
trades = 0
count = 0
maxcount = 2
Actslopes = []
AcctVals = []
Count = 0
ticker = yf.Ticker('TSLA')
Hist = ticker.history(interval='1m',start='2020-08-30',end='2020-09-04')
prices = []
RSIvals   = []    
slopes = []
n=0
m=0
point = 0
i = 1

while Count < len(Hist):
    price = Hist['Close'][Count]
    prices.append(price)
    Count +=1


#Beginning Trade Simulation

def calcAcctVal(AccountVal, action, i):
    shareVal = prices[i]
    if action == 'buy':
        AccountVal-=shareVal
        return AccountVal
    elif action == 'sell':
        AccountVal+=shareVal
        return AccountVal
    
# (y-b)/x = m
        
"""  
def findRS(PriceList,Actslopes):
    for i, j in zip(PriceList, Actslopes):  
        if j<0:
            downDiff = i-PriceList[PriceList.index(i)-1]
            downDiffs.append(downDiff)
            print(j)
        elif j>0:
            upDiff = i-PriceList[PriceList.index(i)-1]
            upDiffs.append(upDiff)
    RS = stat.mean(upDiffs)/stat.mean(downDiffs)
    return RS            
"""           
     
def buy(i,prices,count):
    going = True
    while going:
        term = i+count
        if ((prices[term]-prices[term-1])/(term-(term-1)))>=np.quantile(slopes, .25) and AccountVal>prices[term]:
            count+=1
            if count == maxcount:
                action = 'buy'
                actions.append(action)
                count = 0
                going = False
                return action
        else:
            going = False

def sell(i,prices,count):
    going = True
    while going:
        term = i+count
        if (prices[term]-prices[term-1])/(term-(term-1))<=np.quantile(slopes, .75) and HaveStock>0:
            count+=1
            if count == maxcount:
                action = 'sell'
                actions.append(action)
                count = 0
                going = False
                return action
        else:
            going = False

while i <int(len(prices)-maxcount):
    if InitAccountVal<prices[i]:
        print('Not enough funds')
        break
    if i == 1:
        action = 'buy'
        trades+=1
        HaveStock+=1
        plt.scatter(i-1,prices[i-1],color = 'red',label = 'Buy' if n==0 else "")
        n +=1
        AccountVal = calcAcctVal(AccountVal, action, i)
    slopes.append(abs(((prices[i]-prices[i-1])/(i-(i-1)))))
    if prices[i]>prices[i-1]:
        action = buy(i,prices,count)
        if action == 'buy':
            trades+=1
            HaveStock+=1
            plt.scatter(i-1,prices[i-1],color = 'red',label = 'Buy' if n==0 else "")
            n +=1
            AccountVal = calcAcctVal(AccountVal, action, i)
            actions.append(action)
        i+=1
    elif prices[i]<prices[i-1] and HaveStock>=1:
        action = sell(i,prices,count)
        if action == 'sell':
            trades+=1
            HaveStock-=1
            plt.scatter(i-1,prices[i-1],color = 'green',label = 'Sell' if m==0 else "")
            m+=1
            AccountVal = calcAcctVal(AccountVal, action, i)
        i+=1
        actions.append(action)
    else:
        action = 'hold'
        i+=1
        actions.append(action)
        AcctVals.append(AccountVal)
while HaveStock!=0:
    action = 'sell'
    AccountVal = calcAcctVal(AccountVal, action, i)
    trades+=1
    HaveStock-=1
print('Final Account Value: $'+ str(round(AccountVal,2)))
print('Shares Remaining: ',HaveStock)
print('# of trades',trades)
plt.plot(prices)
plt.legend()
