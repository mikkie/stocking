# 导入函数库
import jqdata

res = []
code_wrapper = [["603799.XSHG", "300484.XSHE", "002741.XSHE", "300073.XSHE", "600338.XSHG", "300543.XSHE", "002407.XSHE", "300477.XSHE", "300619.XSHE", "603993.XSHG", "002108.XSHE", "600525.XSHG", "002389.XSHE", "601877.XSHG", "300019.XSHE", "300648.XSHE", "002346.XSHE", "600482.XSHG", "002418.XSHE", "600152.XSHG", "002334.XSHE", "000697.XSHE", "603826.XSHG", "300655.XSHE", "000066.XSHE", "002070.XSHE", "002080.XSHE", "603186.XSHG", "603928.XSHG", "300432.XSHE", "002510.XSHE", "300068.XSHE", "600869.XSHG", "603611.XSHG", "000733.XSHE", "002805.XSHE", "000408.XSHE", "300153.XSHE", "600872.XSHG", "002057.XSHE", "600884.XSHG", "600673.XSHG", "002759.XSHE", "300014.XSHE", "300117.XSHE", "002091.XSHE", "002245.XSHE", "002089.XSHE", "002240.XSHE", "002617.XSHE", "600135.XSHG", "600444.XSHG", "000636.XSHE", "002139.XSHE", "300077.XSHE", "600232.XSHG", "600367.XSHG", "000887.XSHE", "002631.XSHE", "300097.XSHE", "600522.XSHG", "000559.XSHE", "000973.XSHE", "002404.XSHE", "000541.XSHE", "300035.XSHE", "600330.XSHG", "601011.XSHG", "002176.XSHE", "002594.XSHE", "300207.XSHE", "300487.XSHE", "300510.XSHE", "600096.XSHG", "002347.XSHE", "002535.XSHE", "000009.XSHE", "000511.XSHE", "000616.XSHE", "000962.XSHE", "002085.XSHE", "002121.XSHE", "002168.XSHE", "002256.XSHE", "002263.XSHE", "002309.XSHE", "002427.XSHE", "002506.XSHE", "002580.XSHE", "002662.XSHE", "300116.XSHE", "300198.XSHE", "300201.XSHE", "300317.XSHE", "300409.XSHE", "300410.XSHE", "300444.XSHE", "300457.XSHE", "300586.XSHE", "600076.XSHG", "600084.XSHG", "600241.XSHG", "600255.XSHG", "600390.XSHG", "600432.XSHG", "600680.XSHG", "600711.XSHG", "601311.XSHG", "603659.XSHG", "000570.XSHE", "002056.XSHE", "002326.XSHE", "002386.XSHE", "002632.XSHE", "002723.XSHE", "600074.XSHG", "600500.XSHG", "600854.XSHG", "002165.XSHE", "002171.XSHE", "600094.XSHG", "600219.XSHG", "600839.XSHG", "601633.XSHG", "002455.XSHE", "300037.XSHE", "300080.XSHE", "600139.XSHG", "600067.XSHG", "000413.XSHE", "300082.XSHE", "002125.XSHE", "002141.XSHE", "002340.XSHE", "002533.XSHE", "600478.XSHG", "600499.XSHG", "000571.XSHE", "600192.XSHG", "603026.XSHG", "000760.XSHE", "002145.XSHE", "600773.XSHG", "002426.XSHE", "002756.XSHE", "002074.XSHE", "600110.XSHG", "600175.XSHG", "603959.XSHG", "000625.XSHE", "300340.XSHE", "600580.XSHG", "000716.XSHE", "002077.XSHE", "002192.XSHE", "300115.XSHE", "002076.XSHE", "600418.XSHG", "002497.XSHE", "000792.XSHE", "000839.XSHE", "002289.XSHE", "600303.XSHG", "300568.XSHE", "000913.XSHE", "000993.XSHE", "002341.XSHE", "600405.XSHG", "000762.XSHE", "600409.XSHG", "002012.XSHE", "002466.XSHE", "000821.XSHE", "300438.XSHE", "000155.XSHE", "002009.XSHE", "002045.XSHE", "002411.XSHE", "300490.XSHE", "002136.XSHE", "002611.XSHE", "600516.XSHG", "002709.XSHE", "600549.XSHG", "002733.XSHE", "002460.XSHE", "000023.XSHE", "000049.XSHE", "002190.XSHE", "002684.XSHE", "603806.XSHG", "300450.XSHE", "002850.XSHE", "002812.XSHE", "300618.XSHE"]]
for codes in code_wrapper:
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
          
    res_codes = []
    for index,obj in enumerate(res):
        if index < 5:
           res_codes.append(obj['code'])
       
    print(res_codes)