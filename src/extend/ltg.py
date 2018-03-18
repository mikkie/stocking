# 导入函数库
import jqdata

res = []
code_wrapper = [["300490.XSHE", "300390.XSHE", "002472.XSHE", "002273.XSHE", "000936.XSHE", "002076.XSHE", "000987.XSHE", "000625.XSHE", "002611.XSHE", "000155.XSHE", "300490.XSHE", "300390.XSHE", "002472.XSHE", "002273.XSHE", "000936.XSHE", "002076.XSHE", "000987.XSHE", "000625.XSHE", "002611.XSHE", "000155.XSHE", "300490.XSHE", "300390.XSHE", "002472.XSHE", "002273.XSHE", "000936.XSHE", "002076.XSHE", "000987.XSHE", "000625.XSHE", "002611.XSHE", "000155.XSHE", "002340.XSHE", "601318.XSHG", "000100.XSHE", "000157.XSHE", "300410.XSHE", "000046.XSHE", "300027.XSHE", "002024.XSHE"],["002913.XSHE", "002861.XSHE", "002885.XSHE", "300567.XSHE", "603626.XSHG", "002903.XSHE", "600207.XSHG", "300632.XSHE", "300503.XSHE", "002681.XSHE", "300227.XSHE", "601137.XSHG", "000727.XSHE", "002845.XSHE", "300537.XSHE", "002600.XSHE", "002217.XSHE", "300400.XSHE", "300476.XSHE", "002241.XSHE", "002341.XSHE", "002916.XSHE", "603595.XSHG"]]
for codes in code_wrapper:
    for code in codes:
        df_stock = get_price(code, end_date='2018-03-18', frequency='daily', fields=['close'], skip_paused=True, fq='pre', count=16)
        last = df_stock.iloc[-1]
        first = df_stock.iloc[0]
        p_change = (last['close'] - first['close']) / first['close'] * 100  
        if len(res) == 0:
           res.append({'code' : code, 'p_change' : p_change})  
        else:
            flag = False        
            for index,obj in enumerate(res):
                if obj['p_change'] < p_change:
                   res.insert(index,{'code' : code, 'p_change' : p_change}) 
                   flag = True
                   break
            if flag == False:   
               res.append({'code' : code, 'p_change' : p_change})  
          
    res_codes = []
    for index,obj in enumerate(res):
        if index < 3:
           res_codes.append(obj['code'])
       
    print(res_codes)