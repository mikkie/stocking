# -*-coding=utf-8-*-
__author__ = 'aqua'

class Config(object):

      def __init__(self):
          self.__priceRange = {'min' : 1.00, 'max' : 60.00} #价格区间
          self.__timeStart = '14:25:00' #监控起始时间
          self.__pKm5Change = 0.01 #当日5分钟振幅
          self.__pKM3Change = 0.05 #3个月振幅
          self.__superSold = [0.05,0.5] #超卖
          self.__leftTrade = [5,4,3] #左侧交易
          self.__flatTrade = [90, 10, 1.2, 1.5] #长时间横盘后突破
          self.__longPeriod = 365 #1年
          self.__trendPeriod = 180 #主要分析范围 最近120天
          self.__dbUrl = 'mysql://root:aqua@127.0.0.1/stocking?charset=utf8' #数据库地址
          self.__turnOver = 3 #换手率
          self.__updateToday = True #更新当前实时价格
          self.__strategy = ['ma'] #使用策略
          self.__kLineMA = [3] #K线超过MA5,MA10数量
          self.__volume = [2,2.5] #量的突变
          self.__basics = [2017,3,20,1,5,15,30] #基础过滤
          self.__bigMoney = [1.2,600,300000] #大单净流入
          self.__report = [2017,4] #报告日期
          self.__testCodes = ['002460','300104','603799','000825','000063','300382','002049','000830','002440','601899','002320','601939','002497','600567','000401','002411','300166','600903','002008','300431','002626','600016','300644','002466','600130','002609','000932','600146','600276','601169','300740','002916','601601','002176','002110','300409','300684','600068','002742','002415','600868','601699','601992','002304','002229','601328','000636','002073','601818','600282','300124','600740','000576','601229','000672','000673','300167','001965','600015','600593','000717','000786','002594','600623','600022','601888','601998','000587','600499','002240','600518','300586','000488','000961','000898','600808','300140','002418','002192','002128','600596','300487','600004','002078','300369','002839','000933','002001','600699','300136','603085','000605','603515','002457','600422','000807','600720','300355','600198','000615','002797','002190','000018','600354','600487','002926','601800','002016','600739','601333','000630','002330','300003','600313','600532','300085','300180','300319','002271','600702','600643','000789','000002','601988','603936','600050','002018','601225','002485','300612','000792','600025','300334','300170','600559','000998','300088','000507','002589','002468','601258','002094','002092','002390','600754','002194','002737','600018','000413','002302','600801','600346','002640','600837','002642','002396','600497','300700','002500','002714','600433','002254','600779','002095','600466','000895','002203','300677','000983','601009','002336','002842','000989','300144','000958','600966','002911','600123','002597','603833','000963','600153','000505','002343','600874','002279','002074','603186','000778','002658','600256','300725','300621','300457','300699','300270','600238','600584','002511','000723','600406','002067','603269','300738','600436','600502','601666','002883','000581','600036','300070','000968','600358','601011','600985','002086','601018','000686','002572','002242','000662','002458','300308','300514','002425','300041','600486','002127','600565','000656','002840','601086','601000','002583','600125','002342','600839','002915','300291','002537','000893','300027','601555','601006','600579','002673','000935','002617','601618','300012','300115','603429','002465','300011','002263','000600','000878','002231','002645','002503','603030','601636','300222','300373','600571','002080','000910','600326','600355','000885','002167','601228','600019','600000','300282','002893','601898','300021','600377','000959','603996','002445','600462','600171','600919','600841','300678','300202','600600','000938','300197','600885','002491','600871','600771','002019','600176','002906','000671','600892','600308','600348','600872','600469','600439','002419','600500','300065','600535','002035','601717','600085','000718','600009','600388','600846','300497','300091','600698','300344','600820','300737','000750','000923','000851','002514','002352','000761','002477','600598','002576','300102','300735','002921','600674','002059','000408','600307','000937','000608','600289','002227','300002','002220','600062','000783','300602','002473','002668','600879','300233','002666','002138','002677','601881','000997','300072','000402','603918','000010','000520','002923','600548','600958','002908','000016','603969','002766','600873','002505','002493','600017','600566','000821','600760','000901','002182','300031','603997','600067','601669','000758','600266','600970','600160','600435','600023','300227','002341','603098','300510','600573','000572','000592','600420','000887','300654','002556','002371','603037','002385','603899','600108','002235','002297','002108','600522','000712','002792','002644','600152','600848','600763','000735','600493','600506','002020','002630','600149','002907','600230','600057','000905','000552','002760','600258','000860','600120','600618','601991','002044','300547','000603','300423','300474','600418','600291','002757','002155','002308','002740','002399','300603','002610','002374','000059','002569','300326','002051','601326','601163','300503','600095','600731','600231','002504','300248','600251','600900','600528','601116','600323','603638','300075','000731','600668','000697','603703','601117','600692','600684','600193','300692','600315','002264','002864','600280','000928','002654','603707','300698','300601','300733','300359','603877','002434','000965','601058','000708','300333','300520','603260','002889','300736','002756','600467','603161','603912','600236','300211','600246','002910','002158','300117','600717','002697','300478','000009','300311','002669','002686','600642','600038','300582','002068','600461','002809','000931','603356','600141','300679','300279','002114','002325','300708','600750','600562','601919','600297','600161','002280','002208','600011','300022','300592','300585','603126','603268','300727','000736','300716','300561','600759','000738','000301','000631','300729','002651','002672','300536','000669','002368','300672','600376','000972','601155','603506','600103','603188','002713','601718','600373','603722','300412','002438','002444','600653','002382','000153','600088','000755','300249','601700','002479','300062','600218','002564','600337','300711','002866','600744','002196','600382','603757','300437','002588','600687','600416','000591','002417','002807','601918','603025','300388','002145','002449','002875','600619','000869','600792','000818','000555','603078','002400','002824','002093','603165','600056','603320','000889','603050','600162','300378','000799','600338','600185','002391','600890','002753','002055','603444','600611','002860','600586','000559','000957','300348','002023','002612','002769','601177','300263','002865','300234','002540','000918','002106','300068','600895','300663','600080','002307','600470','001696','300415','603716','300229','300147','300269','600201','603180','300310','002876','603869','600317','002606','002276','600331','000721','600601','002224','300298','000062','300350','600333','300189','600284','600933','002920','300349','601588','002565','601801','300567','300118','300665','603881','300114','002625','600096','000687','600998','600647','002154','600898','600083','002002','000626','000078','000737','603226','600773','002752','600503','002899','601238','603108','300405','300649','002821','002170','300486','600195','600301','600312','002335','002295','002543','000981','300488','601611','300627','600327','600876','300259','603036','002897','002558','002025','600239','300651','600501','002664','300162','300387','600582','600299','002303','300389','600908','002481','603883','600681','300100','300353','600704','002667','300196','002679','300036','002829','002759','002389','002030','000666','600990','002100','002901','600755','603896','002501','300607','600163','600359','600233','300689','300531','300719','000711','601128','002420','000976','603882','002624','300191','600770','600857','002828','600686','000888','603688','002083','002859','000803','002891','002544','603989','300008','600463','600747','300304','002166','600295','600556','000055','002392','603968','000890','600743','600479','002333','600151','300153','601799','300364','600155','000768','600039','300131','603363','002021','600210','600107','600884','300343','002496','603283','600803','600729','300093','600511','002013','600078','601595','002649','000519','002277','300370','600478','601099','603578','600330','603789','600737','300352','000400','601021','000822','300470'] #测试代码
          self.__ignore = [] #不买的
          self.__conceptCodes = ['000099', '600029', '600115', '600221', '601111','000089', '600004', '600009', '600897','000022', '000088', '000507', '000523', '000659', '002016', '600004', '600325','000592', '000632', '000753', '000905', '600057', '600755', '600897','000652', '000695', '000836', '000897', '000965', '002134', '600082', '600225', '600322', '600583', '600717', '600751', '600821', '600874', '601808', '601919'] #最近题材的股票代码
          self.__topsis = {
              'basics' : {
                  'pe' : 0.07,  #市盈率
                  'pb' : 0.01,  #市净率
                  'esp' : 0.04,  #每股收益率
                  'bvps' : 0.01, #每股净资产
                  'roe' : 0.02, #净资产收益率
                  'nprg' : 0.04, #净利润增长
                  'epsg' : 0.01, #每股收益增长
              },
              'indicator' : {
                   'turnover' : 0.15, #换手率
                   'volume' : 0.15, #成交量
                   'macd' : 0.05, #macd金叉
                   'kdj' : 0.05, #kdj金叉
                   'ma' : 0.1, #均线
                   'bigMoney' : 0.1, #主力资金流入,
                   'concept' : 0.2 #概念题材
              }
          } 
          self.__t1 = {
              'process_num' : 3,
              'stop' : {
                  'am_start' : '09:14:00',
                  'am_stop' : '11:30:00',
                  'pm_start' : '13:00:00',
                  'pm_stop' : '15:00:00',
              },
              'trade' : {
                 'addPrice' : 0.02,
                 'minusPrice' : 0.01,
                 'volume' : 300,
                 'enable' : False,
                 'enableMock' : True,
                 'max_buyed' : 3,
                 'balance' : 200000
              },
              'topsis' : {
                  'net' : 0.3,
                  'v300' : 0.15,
                  'v120' : 0.15,
                  'v30' : 0.2,
                  'r_break' : 0.2
              },
              'big_money' : {
                  'amount' : 500000,
                  'volume' : 100000,
                  'threshold' : 0.3
              },
              'speed' : {
                  'v30_ratio' : 0.8,
                  'v30' : 0.036,
                  'v120' : 0.02,
                  'v300' : 0.013
              },
              'get_hygn_inter' : 15,
              'get_data_inter' : 2,
              'need_recover_data' : False,
              'split_size' : 880,
              'pvRatio' : 1.5,
              'R_line' : {
                  'R1' : 0.191,
                  'R2' : 0.382,
                  'R3' : 0.5,
                  'R4' : 0.618,
                  'R5' : 0.892
              },
              'A' : {
                  'open_p' : [5.0, 10.0],
                  'time' : '10:00:00',
                  'min_R' : 'R2',
                  'big_money' : {
                      'net' : 200000
                  }
              },
              'B' : {
                  'open_p' : [2.0, 5.0],
                  'time' : '11:00:00',
                  'min_R' : 'R2',
                  'big_money' : {
                      'net' : 250000
                  }
              },
              'C' : {
                  'open_p' : [-1.0, 2.0],
                  'time' : '14:50:00',
                  'min_R' : 'R4',
                  'big_money' : {
                      'net' : 250000
                  }
              },
              'x_speed' : {
                  'a' : 0.7,
                  'b' : {'s' : 0.75, 'm' : 0.75, 'b' : 0.75},
                  'c' : {'s' : 0.6, 'm' : 0.6, 'b' : 0.6},
                  'lowerThanBefore' : 1.3
              },
              'strategy' : ['time','minR','xspeed'],
              'seller' : {
                  'margin' : 1.5,
                  'min_threshold' : -8,
                  'cancelTime' : 30
              } 
          }

      def get_ignore(self):
          return self.__ignore

      def get_t1(self):
          return self.__t1    

      def get_conceptCodes(self):
          return self.__conceptCodes

      def get_report(self):
          return self.__report

      def get_pKm5Change(self):
          return self.__pKm5Change

      def get_SuperSold(self):
          return self.__superSold  

      def get_DBurl(self):
          return self.__dbUrl  


      def get_StartTime(self):
          return self.__timeStart  


      def get_PriceRange(self):
          return self.__priceRange  


      def get_pKM3Change(self):
          return self.__pKM3Change  

      def get_longPeriod(self):
          return self.__longPeriod  

      def get_TurnOver(self):
          return self.__turnOver  

      def get_LeftTrade(self):
          return self.__leftTrade

      def get_updateToday(self):
          return self.__updateToday

      def get_trendPeriod(self):
          return self.__trendPeriod  

      def get_Strategy(self):
          return self.__strategy 

      def get_KLineMA(self):
          return self.__kLineMA   


      def get_FlatTrade(self):
          return self.__flatTrade  


      def get_Volume(self):
          return self.__volume  

      def get_Basic(self):
          return self.__basics 

      def get_BigMoney(self):
          return self.__bigMoney

      def get_TestCodes(self):
          return self.__testCodes

      def get_topsis(self):
          return self.__topsis  

      pass