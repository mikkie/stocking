import jqdata
import numpy as np
import talib as ta
import datetime as dt

## 初始化函数，设定要操作的股票、基准等等
def initialize(context):
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # True为开启动态复权模式，使用真实价格交易
    set_option('use_real_price', True) 
    # 设定成交量比例
    set_option('order_volume_ratio', 1)
    # 股票类交易手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(open_tax=0, close_tax=0.001, \
                             open_commission=0.0003, close_commission=0.0003,\
                             close_today_commission=0, min_commission=5), type='stock')
    # 持仓数量
    g.daily_buy_count = 3 

    # g.stockCodes = []

    # g.today_bought_stocks = []

    run_daily(morning_sell_all, 'open')

def before_trading_start(context):
    g.stockCodes = []
    g.today_bought_stocks = []
    res = []
    df_all = get_all_securities(types=['stock'], date=context.current_dt)
    for index,row in df_all.iterrows():
        df_stock = get_price(index, end_date=context.current_dt, frequency='daily', fields=['close','high','low'], skip_paused=True, fq='pre', count=90)
        high_row = df_stock.loc[df_stock['high'].idxmax()]
        high = high_row.get('high')
        low_row = df_stock.loc[df_stock['low'].idxmin()]
        low = low_row.get('low')
        lastClose = df_stock.iloc[-1].get('close')
        close = df_stock['close'].values
        df_stock['ma5'] = ta.SMA(close,timeperiod=5)
        df_stock['ma10'] = ta.SMA(close,timeperiod=10)
        df_stock = df_stock[-15:]
        pre_close = None
        flag = True
        count_close = 0
        count_ma5 = 0
        count_high_5 = 0
        count_10 = 0
        for index_s,row_s in df_stock.iterrows():
            if pre_close is None:
               pre_close = row_s['close']
               continue
            if (row_s['close'] - pre_close) / pre_close * 100 > 5 or (row_s['close'] - pre_close) / pre_close * 100 < -5:
               count_high_5 = count_high_5 + 1
            if (row_s['close'] - pre_close) / pre_close * 100 >= 9.93:
               count_10 = count_10 + 1
            ma5 = row_s['ma5']
            ma10 = row_s['ma10']
            if not np.isnan(ma5) and not np.isnan(ma10):
               if row_s['close'] > ma5:
                  count_close = count_close + 1
               if ma5 > ma10:
                  count_ma5 = count_ma5 + 1      
            pre_close = row_s['close']
        if count_close < 10 or count_ma5 < 10:
           flag = False 
        if (lastClose - low) / (high - low) > 0.4:
           flag = False 
        if count_high_5 > 3 or count_10 > 2:
           flag = False
        if flag:
           res.append(index)
    # print(res)      
    g.stockCodes = res


def isXSpeedMatch(code,current_dt,preUnitData):
    # print('ct = ' + current_dt.strftime('%Y-%m-%d %H:%M:%S'))
    startDate = dt.datetime(current_dt.year,current_dt.month,current_dt.day,9,30)
    # print('startDate = ' + startDate.strftime('%Y-%m-%d %H:%M:%S'))
    currentData = get_current_data()[code]
    diff_seconds = (current_dt - startDate).seconds
    count = int(round(diff_seconds/60,0))
    # print('count = ' + str(count))
    if count <= 0:
       return False    
    historyData = get_bars(code, count, unit='1m',fields=['date','close'],include_now=False)
    lastDayClose = historyData[0][1]
    # print('lastDayClose=' + str(lastDayClose))
    historyData[0][0] = startDate
    historyData[0][1] = currentData.day_open
    # print('historyData:') 
    # print(historyData)
    ccp = (currentData.last_price - lastDayClose) / lastDayClose * 100
    # print('ccp = ' + str(ccp))
    ocp = (currentData.day_open - lastDayClose) / lastDayClose * 100
    # print('ocp = ' + str(ocp))
    historyData = historyData[::-1]
    for row in historyData:
        pcp = (row['close'] - lastDayClose) / lastDayClose * 100
        # print('pcp = ' + str(pcp))
        if ccp - pcp >= (10 - pcp) * 0.7:
           ratio_b = 0.7
           if ocp <= 2:
              ratio_b = 0.65
           if ocp > 5:
              ratio_b = 0.75
           if ccp - pcp >= (ccp - ocp) * ratio_b: 
              pt = row['date']
            #   print('pt = ' + pt.strftime('%Y-%m-%d %H:%M:%S'))
              p_change = ccp - pcp
              ratio_c = 0.8
              if p_change <= 2:
                 ratio_c = 0.6
              elif p_change > 5:
                   ratio_c = 1   
              if (current_dt - pt).seconds / 60 < (ccp - pcp) * ratio_c:
                #  print('[%s] match cond a, ccp = %s, pcp = %s' % (code,ccp,pcp)) 
                #  print('[%s] match cond b, ccp = %s, ocp = %s' % (code,ccp,ocp)) 
                #  print('[%s] match cond c, ct = %s, pt = %s' % (code,current_dt,pt))
                 return True
    return False   

def handle_data(context, data):
    for code in g.stockCodes:
        if isXSpeedMatch(code,context.current_dt,data):
           trade(context,code)      
  
## 交易函数
def trade(context,code):
    if code in g.today_bought_stocks:
       return
    cash = context.portfolio.cash
    # 计算今天还需要买入的股票数量
    need_count = g.daily_buy_count - len(g.today_bought_stocks)
    if need_count == 0:
       return 
    # 把现金分成几份,
    buy_cash = context.portfolio.cash / need_count
    # 买入这么多现金的股票
    order_value(code, buy_cash)
    # 放入今日已买股票的集合
    g.today_bought_stocks.append(code)

    log.info("Buying %s" % (code))


def morning_sell_all(context):
    # 将目前所有的股票卖出
    for security in context.portfolio.positions:
        # 全部卖出
        order_target(security, 0)
        # 记录这次卖出
        log.info("Selling %s" % (security))    

