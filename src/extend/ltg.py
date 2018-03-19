# 导入函数库
import jqdata

res = []
code_wrapper = [["000681.XSHE", "603258.XSHG", "002396.XSHE", "300253.XSHE", "002264.XSHE", "300188.XSHE", "600332.XSHG", "002415.XSHE", "601601.XSHG", "300274.XSHE", "601116.XSHG", "300638.XSHE", "300349.XSHE", "300271.XSHE", "300047.XSHE", "300244.XSHE", "000503.XSHE", "300161.XSHE", "600410.XSHG", "002368.XSHE", "600315.XSHG", "002094.XSHE", "300027.XSHE", "002223.XSHE", "300245.XSHE", "600476.XSHG", "002488.XSHE", "002139.XSHE", "300279.XSHE", "600633.XSHG", "600055.XSHG", "600718.XSHG", "000902.XSHE", "300251.XSHE", "600258.XSHG", "002024.XSHE", "600028.XSHG", "300339.XSHE", "600640.XSHG", "002065.XSHE", "000665.XSHE", "600723.XSHG", "002236.XSHE", "002543.XSHE", "600662.XSHG", "000670.XSHE", "603001.XSHG", "601866.XSHG", "600588.XSHG", "600757.XSHG", "002401.XSHE", "000058.XSHE", "600280.XSHG", "002697.XSHE", "002153.XSHE", "600398.XSHG", "600289.XSHG", "300020.XSHE", "000607.XSHE", "601216.XSHG", "603888.XSHG", "000698.XSHE", "002505.XSHE", "601216.XSHG", "002739.XSHE", "000516.XSHE", "601929.XSHG", "000156.XSHE", "002530.XSHE", "000639.XSHE", "600936.XSHG", "002170.XSHE", "002530.XSHE", "600026.XSHG", "002421.XSHE", "601928.XSHG", "002157.XSHE", "000882.XSHE", "002609.XSHE", "600130.XSHG", "600446.XSHG", "300212.XSHE", "601777.XSHG", "600604.XSHG", "600037.XSHG", "600827.XSHG", "000756.XSHE", "000831.XSHE", "600690.XSHG", "600229.XSHG", "600728.XSHG", "000333.XSHE", "603881.XSHG"]]
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