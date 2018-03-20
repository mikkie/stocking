# 导入函数库
import jqdata

res_codes = []
code_wrapper = [["000963.XSHE", "000028.XSHE", "600763.XSHG", "300015.XSHE", "600535.XSHG", "600332.XSHG", "600276.XSHG", "000999.XSHE", "600557.XSHG", "000538.XSHE", "000423.XSHE", "601607.XSHG", "600750.XSHG", "002223.XSHE", "600267.XSHG", "600196.XSHG", "600161.XSHG", "002275.XSHE", "600518.XSHG", "600079.XSHG", "600422.XSHG", "600993.XSHG", "600380.XSHG", "000078.XSHE", "600789.XSHG", "600062.XSHG", "600285.XSHG", "600479.XSHG", "600297.XSHG", "600329.XSHG", "000597.XSHE", "002118.XSHE", "600252.XSHG", "600216.XSHG", "600351.XSHG", "000623.XSHE", "600572.XSHG", "000756.XSHE", "300181.XSHE", "000788.XSHE", "000919.XSHE", "600085.XSHG", "600055.XSHG", "002099.XSHE", "000516.XSHE", "600713.XSHG", "600666.XSHG", "300049.XSHE", "000766.XSHE", "002107.XSHE", "300006.XSHE", "600812.XSHG", "600829.XSHG", "600664.XSHG", "000952.XSHE", "000990.XSHE", "600511.XSHG"],["603939.XSHG", "600332.XSHG", "600557.XSHG", "002603.XSHE", "601607.XSHG", "002262.XSHE", "002462.XSHE", "600993.XSHG", "002589.XSHE", "600998.XSHG", "002433.XSHE", "000756.XSHE", "300151.XSHE", "600572.XSHG", "300146.XSHE", "600713.XSHG", "000788.XSHE", "002727.XSHE", "600511.XSHG", "603883.XSHG", "300003.XSHE", "603368.XSHG", "300288.XSHE"]]
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