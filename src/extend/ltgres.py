import jqdata

res_codes = []
code_wrapper = [["300550.XSHE", "600588.XSHG", "002424.XSHE", "000150.XSHE", "300015.XSHE", "600196.XSHG", "002223.XSHE", "603990.XSHG", "002262.XSHE", "600587.XSHG", "002589.XSHE", "002432.XSHE", "300104.XSHE", "600518.XSHG", "600998.XSHG", "002390.XSHE", "002433.XSHE", "600572.XSHG", "300078.XSHE", "600568.XSHG", "600767.XSHG", "002312.XSHE", "000502.XSHE", "000566.XSHE", "300049.XSHE", "300273.XSHE", "300253.XSHE", "002421.XSHE", "600718.XSHG", "600260.XSHG", "002004.XSHE", "002148.XSHE", "002065.XSHE", "002038.XSHE", "002727.XSHE", "300003.XSHE", "300007.XSHE", "300020.XSHE", "300168.XSHE", "300288.XSHE", "600797.XSHG", "600570.XSHG", "000503.XSHE", "300479.XSHE"],["300462.XSHE", "002912.XSHE", "300130.XSHE", "603019.XSHG", "300579.XSHE", "600487.XSHG", "000066.XSHE", "300738.XSHE", "603232.XSHG", "002268.XSHE", "300588.XSHE", "300188.XSHE", "300546.XSHE", "300010.XSHE", "002544.XSHE", "000158.XSHE", "300297.XSHE", "600701.XSHG", "600485.XSHG", "300038.XSHE", "000034.XSHE", "300659.XSHE", "002212.XSHE", "603636.XSHG", "600289.XSHG", "600410.XSHG", "600718.XSHG", "000063.XSHE", "300352.XSHE", "600776.XSHG", "300079.XSHE", "300077.XSHE", "002491.XSHE", "600536.XSHG", "600100.XSHG", "300369.XSHE", "600105.XSHG", "300333.XSHE", "300311.XSHE", "300229.XSHE", "600271.XSHG", "300379.XSHE", "300017.XSHE", "002197.XSHE", "002439.XSHE", "300324.XSHE", "300479.XSHE", "002447.XSHE", "300386.XSHE", "601360.XSHG", "300113.XSHE"],["300383.XSHE", "000555.XSHE", "600588.XSHG", "603019.XSHG", "000977.XSHE", "600590.XSHG", "300730.XSHE", "300738.XSHE", "002456.XSHE", "000806.XSHE", "300367.XSHE", "002268.XSHE", "300085.XSHE", "600756.XSHG", "300078.XSHE", "300249.XSHE", "300297.XSHE", "300128.XSHE", "300290.XSHE", "600767.XSHG", "002075.XSHE", "600845.XSHG", "002301.XSHE", "000034.XSHE", "300302.XSHE", "002463.XSHE", "300271.XSHE", "600410.XSHG", "600654.XSHG", "600718.XSHG", "000063.XSHE", "600225.XSHG", "002417.XSHE", "600602.XSHG", "000100.XSHE", "002415.XSHE", "600589.XSHG", "300235.XSHE", "300074.XSHE", "600536.XSHG", "300025.XSHE", "600100.XSHG", "002093.XSHE", "300369.XSHE", "603003.XSHG", "002089.XSHE", "000971.XSHE", "002279.XSHE", "000665.XSHE", "300051.XSHE", "600633.XSHG", "300431.XSHE", "000948.XSHE", "603528.XSHG", "300366.XSHE", "300311.XSHE", "300229.XSHE", "002065.XSHE", "600770.XSHG", "600850.XSHG", "300274.XSHE", "600996.XSHG", "600037.XSHG", "002368.XSHE", "300287.XSHE", "600728.XSHG", "300168.XSHE", "300020.XSHE", "300379.XSHE", "002642.XSHE", "300212.XSHE", "300052.XSHE", "300017.XSHE", "300245.XSHE", "002197.XSHE", "002439.XSHE", "300044.XSHE", "600797.XSHG", "000938.XSHE", "002315.XSHE", "000007.XSHE", "002281.XSHE", "002837.XSHE", "601360.XSHG", "300365.XSHE", "300113.XSHE", "603881.XSHG", "603138.XSHG"]]
for codes in code_wrapper:
    res = []
    for code in codes:
        df_stock = get_price(code, end_date='2018-03-26', frequency='daily', fields=['close'], skip_paused=True, fq='pre', count=11)
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