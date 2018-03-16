# 导入函数库
import jqdata

res = []
df_all = get_all_securities(types=['stock'], date='2018-03-16')
for index,row in df_all.iterrows():
    df_stock = get_price(index, end_date='2018-03-16', frequency='daily', fields=['close'], skip_paused=True, fq='pre', count=6)
    count = 0
    pre_close = None
    for index_s,row_s in df_stock.iterrows():
        if pre_close is None:
           pre_close = row_s['close']
           continue
        if (row_s['close'] - pre_close) / pre_close * 100 > 9.3:
           count = count + 1
        pre_close = row_s['close']   
    if count >= 1:
       res.append(index)
print(res)