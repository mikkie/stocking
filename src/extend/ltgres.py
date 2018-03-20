import jqdata

res_codes = []
code_wrapper = [["600645.XSHG", "600535.XSHG", "600400.XSHG", "600869.XSHG", "002126.XSHE", "002208.XSHE", "000532.XSHE", "300367.XSHE", "600755.XSHG", "601801.XSHG", "600635.XSHG", "600207.XSHG", "600577.XSHG", "600229.XSHG", "002226.XSHE", "300300.XSHE", "600728.XSHG", "300390.XSHE", "000987.XSHE", "002769.XSHE", "000936.XSHE", "300020.XSHE", "000810.XSHE", "002137.XSHE", "002367.XSHE", "300479.XSHE", "300100.XSHE", "002354.XSHE", "002230.XSHE"]]
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