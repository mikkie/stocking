# 还未启动的
import jqdata
import numpy as np
import talib as ta

codes = ['000009', '000061', '000155', '000159', '000415', '000416', '000419', '000421', '000502', '000521', '000526', '000565', '000601', '000609', '000622', '000627', '000655', '000666', '000676', '000678', '000692', '000700', '000701', '000702', '000705', '000712', '000779', '000791', '000799', '000833', '000859', '000881', '000911', '000919', '000929', '000962', '000966', '001696', '002011', '002090', '002096', '002106', '002140', '002172', '002200', '002211', '002231', '002249', '002269', '002272', '002274', '002278', '002287', '002291', '002360', '002375', '002393', '002401', '002420', '002490', '002510', '002522', '002535', '002541', '002554', '002566', '002590', '002613', '002623', '002625', '002633', '002634', '002639', '002670', '002686', '002708', '002724', '002728', '002731', '002733', '002778', '002786', '002788', '002796', '002800', '002801', '002802', '002811', '002816', '002822', '002825', '002828', '002835', '002845', '002846', '002850', '002855', '002865', '002866', '002871', '002875', '002880', '002888', '002890', '002897', '002901', '002906', '002918', '300030', '300046', '300135', '300139', '300140', '300191', '300206', '300218', '300234', '300249', '300265', '300267', '300321', '300322', '300405', '300442', '300445', '300452', '300453', '300484', '300499', '300508', '300517', '300521', '300522', '300525', '300526', '300530', '300535', '300538', '300539', '300540', '300548', '300551', '300553', '300555', '300562', '300563', '300573', '300579', '300583', '300587', '300592', '300597', '300599', '300610', '300615', '300625', '300635', '300636', '300637', '300652', '300665', '300667', '300669', '300683', '300689', '300690', '300696', '300699', '300703', '300708', '300710', '300711', '300712', '300717', '300718', '300720', '600084', '600090', '600091', '600151', '600156', '600184', '600191', '600208', '600218', '600220', '600222', '600223', '600227', '600232', '600250', '600270', '600302', '600327', '600329', '600355', '600406', '600418', '600505', '600513', '600547', '600626', '600629', '600644', '600651', '600676', '600701', '600713', '600744', '600749', '600759', '600778', '600796', '600805', '600812', '600819', '600830', '600854', '600864', '600976', '600992', '601002', '601126', '601127', '601188', '601199', '601218', '601558', '601611', '601727', '601789', '603015', '603022', '603023', '603029', '603035', '603036', '603037', '603040', '603067', '603076', '603078', '603090', '603110', '603131', '603136', '603139', '603159', '603168', '603178', '603181', '603183', '603196', '603226', '603232', '603266', '603278', '603316', '603320', '603330', '603331', '603358', '603366', '603389', '603396', '603444', '603496', '603527', '603559', '603566', '603567', '603577', '603580', '603586', '603589', '603605', '603607', '603608', '603617', '603633', '603656', '603663', '603690', '603701', '603721', '603726', '603729', '603757', '603758', '603767', '603768', '603826', '603828', '603829', '603858', '603882', '603890', '603912', '603917', '603922', '603955', '603958', '603976']

res = []

df_stocks = get_all_securities(types=['stock'], date=None)
all_codes = list(df_stocks.index)
for code in all_codes: 
    df_price = get_price(code, start_date='2018-03-23', end_date='2018-03-24', frequency='daily', fields=['close','pre_close'], skip_paused=False, fq='pre', count=None)
    if len(df_price) == 0:
       continue    
    last_line = df_price.iloc[-1]
    if (last_line['close'] - last_line['pre_close']) / last_line['pre_close'] * 100 >= 9.93:
       code = code.replace('.XSHG','').replace('.XSHE','')
       if code in codes:
          res.append(code)
print(res)