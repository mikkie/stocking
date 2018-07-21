格式:
main.py init [0/50/300/zx] [hy/c] [行业或概念]
i.e.
main.py init 50 hy 金融行业
main.py init 300 c 节能

策略:
[leftTrade] 左侧交易
[rightTrade] 右侧交易
[flat]横盘
[volume] 成交量
[turnover] 换手率
[macd] 指标
[kdj] 指标
[ma] 均线
[bigMoney] 主力净流入

1. main.py init cy [turnover,leftTrade]
2. main.py init 0 hy [xxx] [leftTrade]
3. main.py init zz [turnover,rightTrade,macd]
4. main.py init 0 [turnover,rightTrade,macd,volume]

0.get all today
1.filter by common.sql (price < 30)
2.filter by twodayten.py (keep yesterday 10%)
3.filter by NewStock.py
4.filter by bull.py
5.filter by bull2.py 
6.filter by xsg.js
7.filter by yesterday buy
8.filter by remove trade > 20