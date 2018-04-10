import pandas as pd
import numpy as np
import tushare as ts



def get_eps(Years = [2017]):
    A_EPS = pd.Series()
    for Year in Years:
        for q in range(1,5):
            df = ts.get_report_data(Year,q)
            for i in df.code:
                try:
                    List = df[df.code == i]
                    eps = List.eps.values[0]
                    md = List.report_date.values[0]
                    Date = str(Year)+'-'+md
                    Date = pd.to_datetime(Date,format='%Y-%m-%d')
                    if q > 2:
                        if Date < pd.Timestamp(Year,6,1):
                            Date = pd.to_datetime(str(Year+1)+'-'+md)
                    try:
                        A_EPS[i][Date] = eps
                    except:
                        A_EPS[i] = pd.Series() 
                        A_EPS[i][Date] = eps
                except:
                    continue
    return A_EPS
	
	
	
def get_pe(stock,prices,dates,EPS = get_eps()):
    Leps = EPS[stock]
    if len(Leps[np.isnan(Leps)])>0:
        print(Leps)
        for i in Leps[np.isnan(Leps)].index:
            print('Please input the value of '+str(i))
            Leps[i] = input()
    Lprices = pd.Series(prices,index = pd.to_datetime(dates))
    PE = pd.Series()
    for i in Lprices.index:
        for eps_date in Leps.index:
            if  i >= eps_date:
                PE[i] = Lprices[i]/Leps[eps_date]
            elif i < eps_date:
                break
    return PE