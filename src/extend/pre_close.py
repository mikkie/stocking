end_date = '2018-10-09'
output = []


df_all = get_all_securities(types=['stock'], date=end_date)
for index,row in df_all.iterrows():
    df = get_price(index, end_date=end_date, frequency='daily', fields=['open','high','close','high_limit','pre_close'], skip_paused=False, fq='pre', count=1)
    if len(df) > 0:
       row = df.iloc[0]
       if row['close'] == row['high_limit'] and row['open'] != row['high_limit']:
          code = index.replace('.XSHE','').replace('.XSHG','')    
          pre_close = str(row['pre_close'])
          output.append(('%s' % code, '%s' % pre_close))
print(output)