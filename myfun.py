import pandas as pd
import numpy as np



def get_atr(high,low,close,index):
    true_amplitude = []
    atr = []
    for i in range(len(index)-1):
        c1=(high[i+1] - low[i+1])
        c2=(abs(close[i+1] - high[i]))
        c3=(abs(close[i+1] - low[i]))
        true_amplitude.append(max(c1,c2,c3))
    for i in range(len(true_amplitude)):
        if  i < len(true_amplitude)-5:
            atr.append(sum(true_amplitude[i:i+5])/5)
        else:
            atr.append(sum(true_amplitude[i:])/len(true_amplitude[i:]))
    atr = pd.Series(atr,index=index[:-1])
    return atr


def get_CE(high,low,close,index):
    atr = get_atr(high,low,close,index)
    CE_long = []    #Chandelier Exit (long)
    CE_short = []   #Chandelier Exit (short)
    for i in range(len(atr)):
        if i < len(atr)-22:
            CE_long.append(max(high[i:i+22]) - atr[i]*3)
            CE_short.append(min(low[i:i+22]) + atr[i]*3)
        else:
            CE_long.append(max(high[i:]) - atr[i]*3)
            CE_short.append(min(low[i:]) + atr[i]*3)
    CE_long = pd.Series(CE_long,index=atr.index)
    CE_short = pd.Series(CE_short,index=atr.index)
    return CE_long,CE_short

def get_SMA(prices,dates,n=20):
    MA = []
    for i in range(0,len(dates)):
        if i < len(prices)-n:
            MA.append(sum(prices[i:i+n])/n)
        else:
            MA.append(sum(prices[i:])/len(prices[i:]))
    MA = pd.Series(MA,index = dates)
    return MA

def get_boll(prices,dates,n=20):
    ma = get_SMA(prices,dates)
    up_band = []
    low_band = []
    mid_band = ma[:-n]
    for i in range(0,len(prices)-n):
        var = sum(pow((prices[i:i+n]-ma[i:i+n]),2))/n
        std = pow(var,0.5)
        up_band.append(ma[i] + std*2)
        low_band.append(ma[i] - std*2)
    up_band = pd.Series(up_band,index = mid_band.index)
    low_band = pd.Series(low_band,index = mid_band.index)
    return up_band,mid_band,low_band
