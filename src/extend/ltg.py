# 导入函数库
import jqdata

res = []
code_wrapper = [["300624.XSHE", "002925.XSHE", "603160.XSHG", "002230.XSHE", "603816.XSHG", "603083.XSHG", "603848.XSHG", "002713.XSHE", "002396.XSHE", "300701.XSHE", "002761.XSHE", "300007.XSHE", "300543.XSHE", "300367.XSHE", "600745.XSHG", "002444.XSHE", "002848.XSHE", "002818.XSHE", "300183.XSHE", "300423.XSHE", "002841.XSHE", "300403.XSHE", "300691.XSHE", "300250.XSHE", "300131.XSHE", "002139.XSHE", "002543.XSHE", "603385.XSHG", "002676.XSHE", "600677.XSHG", "603898.XSHG", "300247.XSHE", "002242.XSHE", "603008.XSHG", "002397.XSHE", "002375.XSHE", "300279.XSHE", "300352.XSHE", "002402.XSHE", "002528.XSHE", "000521.XSHE", "603118.XSHG", "002024.XSHE", "600060.XSHG", "002705.XSHE", "300241.XSHE", "002631.XSHE", "300155.XSHE", "002084.XSHE", "600804.XSHG", "600996.XSHG", "002851.XSHE", "300312.XSHE", "300074.XSHE", "000404.XSHE", "300128.XSHE", "600690.XSHG", "600050.XSHG", "002236.XSHE", "000100.XSHE", "600743.XSHG", "002421.XSHE", "000017.XSHE", "002706.XSHE", "002280.XSHE", "000662.XSHE", "002293.XSHE", "002482.XSHE", "600100.XSHG", "000333.XSHE", "603313.XSHG", "603030.XSHG"]]
for codes in code_wrapper:
    for code in codes:
        df_stock = get_price(code, end_date='2018-03-19', frequency='daily', fields=['close'], skip_paused=True, fq='pre', count=16)
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