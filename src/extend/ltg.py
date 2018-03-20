import jqdata

res_codes = []
code_wrapper = [code_content]
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