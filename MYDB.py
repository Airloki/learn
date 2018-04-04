import tushare as ts
import numpy as np
import pandas as pd
import pymysql

def update_hs300(connect,start_D='2018-01-01',end_D=None):
    cursor = connect.cursor()
    hs300 = ts.get_hs300s().code
    for i in hs300:
        print('Update Stock '+i)
        sql01 = "drop table if exists s"+i
        sql02 = "create table s"+i+"""(date date,open float,high float,close float,low float,volume float)"""
        sql03 = "insert into s"+i+"(date,open,high,close,low,volume)values(%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql01)
        cursor.execute(sql02)
        s_DB = ts.get_hist_data(i,start=start_D,end=end_D)
        if s_DB is None:
            print('Can not get the data of'+i)
            continue
        s_DB = s_DB.iloc[:,0:5]
        s_DB.insert(0,'date',s_DB.index)
        insert_data = np.array(s_DB)
        try:
            for row in insert_data:
                cursor.execute(sql03,list(row))
            connect.commit()
        except:
            connect.rollback()
            print('Fail to insert data of '+i+' into table')
			
	
def df_of_stock(connect,stock):
    sql04 = """select * from s"""+stock
    cursor = connect.cursor()
    cursor.execute(sql04)
    p_df = pd.DataFrame(np.array(cursor.fetchall()))
    df = p_df.iloc[:,1:]
    df.index = p_df[0]
    df.columns = ['open','high','close','low','volume']
    return df