import jqdata

res_codes = []
code_wrapper = [["600083.XSHG", "002045.XSHE", "002655.XSHE", "300136.XSHE", "002351.XSHE", "002681.XSHE", "002475.XSHE", "300458.XSHE", "002888.XSHE", "002241.XSHE", "002402.XSHE", "603626.XSHG", "300223.XSHE", "002230.XSHE"],["000046.XSHE", "300410.XSHE", "000157.XSHE", "000100.XSHE", "000027.XSHE", "300027.XSHE", "002024.XSHE", "000625.XSHE", "000155.XSHE", "601318.XSHG", "002076.XSHE", "300390.XSHE", "002472.XSHE", "000987.XSHE", "002340.XSHE", "000936.XSHE", "002611.XSHE", "002273.XSHE", "300490.XSHE", "300648.XSHE"],["000564.XSHE", "300656.XSHE", "002161.XSHE", "002697.XSHE", "002024.XSHE", "300306.XSHE", "600728.XSHG", "300609.XSHE", "000997.XSHE", "002419.XSHE", "300248.XSHE", "300479.XSHE", "300663.XSHE"]]
for codes in code_wrapper:
    res = []
    for code in codes:
        df_stock = get_price(code, end_date='2018-03-20', frequency='daily', fields=['close'], skip_paused=True, fq='pre', count=11)
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
          
    for index,obj in enumerate(res):
        if index < 5:
           code = obj['code']
           code = code.replace('.XSHE','').replace('.XSHG','')
           if code not in res_codes:
              res_codes.append(code)
       
print(res_codes)