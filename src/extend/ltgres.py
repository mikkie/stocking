import jqdata

res_codes = []
code_wrapper = [["002921.XSHE", "002046.XSHE", "002890.XSHE", "601038.XSHG", "300159.XSHE", "300022.XSHE", "603789.XSHG", "600805.XSHG", "000903.XSHE", "000157.XSHE", "603766.XSHG", "603029.XSHG", "000816.XSHE", "603767.XSHG", "603701.XSHG"],["000963.XSHE", "600276.XSHG", "002294.XSHE", "603858.XSHG", "000999.XSHE", "002424.XSHE", "600535.XSHG", "600196.XSHG", "600332.XSHG", "000423.XSHE", "601607.XSHG", "000935.XSHE", "600518.XSHG", "600085.XSHG", "600998.XSHG", "002670.XSHE", "600703.XSHG", "600547.XSHG", "000732.XSHE", "601877.XSHG", "600420.XSHG", "600804.XSHG", "000581.XSHE", "002310.XSHE", "600011.XSHG", "600297.XSHG", "601611.XSHG", "600737.XSHG", "600118.XSHG", "600027.XSHG", "600028.XSHG", "600893.XSHG", "600362.XSHG", "600372.XSHG", "601398.XSHG", "601718.XSHG", "000768.XSHE", "600887.XSHG", "600066.XSHG", "600489.XSHG", "601668.XSHG", "600036.XSHG", "601857.XSHG", "000738.XSHE", "600089.XSHG", "601111.XSHG", "601225.XSHG", "000402.XSHE", "000898.XSHE", "002304.XSHE", "600061.XSHG", "601699.XSHG", "601918.XSHG", "601939.XSHG", "000825.XSHE", "002470.XSHE", "600688.XSHG", "600808.XSHG", "601006.XSHG", "601169.XSHG", "601333.XSHG", "601985.XSHG", "601988.XSHG", "601991.XSHG", "601997.XSHG", "601998.XSHG", "000046.XSHE", "000540.XSHE", "000766.XSHE", "000876.XSHE", "002128.XSHE", "002142.XSHE", "002450.XSHE", "600008.XSHG", "600009.XSHG", "600023.XSHG", "600115.XSHG", "600150.XSHG", "600157.XSHG", "600179.XSHG", "600221.XSHG", "600256.XSHG", "600309.XSHG", "600515.XSHG", "600585.XSHG", "600660.XSHG", "600682.XSHG", "600685.XSHG", "600801.XSHG", "600919.XSHG", "600999.XSHG", "601118.XSHG", "601216.XSHG", "601766.XSHG", "601818.XSHG", "000413.XSHE", "000630.XSHE", "000883.XSHE", "002415.XSHE", "002497.XSHE", "600016.XSHG", "600208.XSHG", "600383.XSHG", "600507.XSHG", "600782.XSHG", "601099.XSHG", "601166.XSHG", "601229.XSHG", "601288.XSHG", "601328.XSHG", "601390.XSHG", "601669.XSHG", "601801.XSHG", "603288.XSHG", "000166.XSHE", "000425.XSHE", "000709.XSHE", "000783.XSHE", "600010.XSHG", "600029.XSHG", "600886.XSHG", "600900.XSHG", "600926.XSHG", "601018.XSHG", "601899.XSHG", "000157.XSHE", "002027.XSHE", "600015.XSHG", "600170.XSHG", "600415.XSHG", "600642.XSHG", "000717.XSHE", "002493.XSHE", "600000.XSHG", "600104.XSHG", "600674.XSHG", "601009.XSHG", "601567.XSHG", "601618.XSHG", "000750.XSHE", "000776.XSHE", "601688.XSHG", "601901.XSHG", "000063.XSHE", "000069.XSHE", "000831.XSHE", "002385.XSHE", "600369.XSHG", "600705.XSHG", "600936.XSHG", "601211.XSHG", "601377.XSHG", "601800.XSHG", "601992.XSHG", "603885.XSHG", "000001.XSHE", "000728.XSHE", "600018.XSHG", "600026.XSHG", "600031.XSHG", "600109.XSHG", "600177.XSHG", "600277.XSHG", "601717.XSHG", "601866.XSHG", "000027.XSHE", "000060.XSHE", "601600.XSHG", "000686.XSHE", "002736.XSHE", "600482.XSHG", "600583.XSHG", "600637.XSHG", "600820.XSHG", "600837.XSHG", "601155.XSHG", "601186.XSHG", "000725.XSHE", "002797.XSHE", "600260.XSHG", "600909.XSHG", "601555.XSHG", "000983.XSHE", "002202.XSHE", "600676.XSHG", "002146.XSHE", "002673.XSHE", "600604.XSHG", "002600.XSHE", "600959.XSHG", "601788.XSHG", "002500.XSHE", "600340.XSHG", "000338.XSHE", "000933.XSHE", "600048.XSHG", "600068.XSHG", "600545.XSHG", "600816.XSHG", "000895.XSHE","601198.XSHG", "002195.XSHE", "600895.XSHG", "600958.XSHG", "601958.XSHG", "603993.XSHG", "000625.XSHE", "002081.XSHE", "002091.XSHE", "601933.XSHG", "000559.XSHE", "000627.XSHE", "002024.XSHE", "002475.XSHE", "600037.XSHG", "600271.XSHG", "600352.XSHG", "600977.XSHG", "600030.XSHG", "600111.XSHG", "000839.XSHE", "001979.XSHE", "002292.XSHE", "600373.XSHG", "600827.XSHG", "601628.XSHG", "000980.XSHE", "600460.XSHG", "601238.XSHG", "000039.XSHE", "000830.XSHE", "002035.XSHE", "002236.XSHE", "600490.XSHG", "600600.XSHG", "600690.XSHG", "600570.XSHG", "000537.XSHE", "600779.XSHG", "601098.XSHG", "002241.XSHE", "000826.XSHE", "000792.XSHE", "600741.XSHG", "000938.XSHE", "601966.XSHG", "601601.XSHG", "601888.XSHG", "601021.XSHG", "601318.XSHG", "603369.XSHG", "002411.XSHE", "600848.XSHG", "002153.XSHE", "600702.XSHG", "600230.XSHG", "000333.XSHE", "002558.XSHE", "601336.XSHG", "002466.XSHE", "000568.XSHE", "002230.XSHE", "002508.XSHE", "002594.XSHE", "600338.XSHG", "000858.XSHE", "600519.XSHG"],["300226.XSHE", "600826.XSHG", "002162.XSHE", "600689.XSHG", "600630.XSHG", "600641.XSHG", "002451.XSHE", "600663.XSHG", "600115.XSHG", "600836.XSHG", "600009.XSHG", "600606.XSHG", "600284.XSHG", "002183.XSHE", "300012.XSHE", "600626.XSHG", "601866.XSHG", "600705.XSHG", "600018.XSHG", "600026.XSHG", "600650.XSHG", "600708.XSHG", "600637.XSHG", "002210.XSHE", "600675.XSHG", "002244.XSHE", "600651.XSHG", "600676.XSHG", "600409.XSHG", "603003.XSHG", "600146.XSHG", "600687.XSHG", "600643.XSHG", "600648.XSHG", "600679.XSHG", "300055.XSHE", "603128.XSHG", "600822.XSHG", "600119.XSHG", "600278.XSHG", "600621.XSHG", "600895.XSHG", "600639.XSHG", "300013.XSHE", "600827.XSHG", "603329.XSHG", "600848.XSHG", "603009.XSHG"],["002264.XSHE", "603877.XSHG", "000756.XSHE", "002336.XSHE", "600729.XSHG", "002403.XSHE", "000715.XSHE", "000785.XSHE", "600697.XSHG", "600694.XSHG", "600859.XSHG", "600861.XSHG", "002277.XSHE", "002561.XSHE", "300441.XSHE", "600306.XSHG", "600655.XSHG", "600682.XSHG", "600778.XSHG", "000564.XSHE", "603608.XSHG", "300005.XSHE", "603708.XSHG", "002461.XSHE", "600821.XSHG", "600774.XSHG", "600891.XSHG", "600824.XSHG", "600723.XSHG", "600725.XSHG", "600712.XSHG", "000882.XSHE", "002787.XSHE", "000679.XSHE", "600327.XSHG", "600838.XSHG", "600361.XSHG", "000725.XSHE", "300094.XSHE", "002187.XSHE", "600814.XSHG", "000417.XSHE", "600693.XSHG", "603101.XSHG", "600597.XSHG", "600628.XSHG", "600858.XSHG", "600122.XSHG", "600785.XSHG", "000571.XSHE", "600687.XSHG", "603031.XSHG", "002697.XSHE", "002127.XSHE", "600280.XSHG", "601933.XSHG", "000501.XSHE", "600828.XSHG", "002024.XSHE", "601086.XSHG", "600865.XSHG", "600271.XSHG", "000560.XSHE", "000759.XSHE", "000987.XSHE", "002582.XSHE", "600827.XSHG", "600398.XSHG", "000639.XSHE", "600738.XSHG", "002251.XSHE", "600600.XSHG", "002419.XSHE", "603777.XSHG", "601116.XSHG", "002153.XSHE"]]
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