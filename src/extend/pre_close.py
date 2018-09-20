codes = ['300013','002261']
end_date = '2018-09-19'
output = []

for code in codes:
    if code.startswith('6'):
       code = code + '.XSHG'   
    else:
        code = code + '.XSHE'
    df = get_price(code, end_date=end_date, frequency='daily', fields=['pre_close'], skip_paused=False, fq='pre', count=1)
    if len(df) > 0:
       code = code.replace('.XSHE','').replace('.XSHG','')    
       pre_close = str(df.iloc[0]['pre_close'])
       output.append(('%s' % code, '%s' % pre_close))
print(output)