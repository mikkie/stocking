# 新股
import jqdata
import numpy as np
import talib as ta
import datetime

res = []
today = datetime.date.today()
startDate = '2018-06-21'
df_all = get_all_securities(types=['stock'], date=startDate)
for index,row in df_all.iterrows():
    try:
        stock = get_security_info(index)
        if (today - stock.start_date).days < 20:
           index = index.replace('.XSHE','').replace('.XSHG','') 
           res.append(index)
    except Exception as e:
           print(e)
        
print(res)            