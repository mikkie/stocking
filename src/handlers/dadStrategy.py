# -*-coding=utf-8-*-
__author__ = 'aqua'


class DadStrategy(object):

    def chooseStock(self, km5, config):
        print('today 5 min k line = ' , km5)
        high, low = self.getHighAnLowFromToday5MinK(km5)
        currentClose = km5.iloc[-1].get('close')
        print('max, min, close of today %f, %f, %f' % (high, low, currentClose))
        change = (currentClose - low) / (high - low)
        print('change = %f' % change)
        if change < config.get_SuperSold():
           print('yes is supersold now in today')
        else:
           print('no is not supersold now in today')                 

    def getHighAnLowFromToday5MinK(self, km5):
        return km5.loc[km5['close'].idxmax(), 'close'], km5.loc[km5['close'].idxmin(), 'close']

