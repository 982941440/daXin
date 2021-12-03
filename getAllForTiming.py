from fake_useragent import UserAgent
import time
import random
import ssl
import requests
import json
import util

ssl._create_default_https_context = ssl._create_unverified_context

class TianTianSpider(object):



 def saveData(self):
        urlYear = "http://fund.eastmoney.com/API/FundDXGJJ.ashx?callback=jQuery18303973379239507868_1634526975963&r=1634526976000&m=0&pageindex={}&sorttype=desc&SFName=STKNUM&IsSale=1&_=1634526976235"
        urlMonth = "http://fund.eastmoney.com/API/FundDXGJJ.ashx?callback=jQuery18309756068947863759_1632273874569&r=1632273874000&m=8&pageindex={}&sorttype=desc&SFName=RATIO&IsSale=1&_=1632273874739"

        optionals = ["010573", "350005", "001520", "001121", "008239", "009476",
                     "001672", "007807", "002272", "002174", "004138", "011082", "400007", "003191"]
        optionalsForBackup = []

        data_list = []
        for offset in range(1, 250, 1):
            url = urlYear.format(offset)
            data = util.getData(url)

            for i, dt in enumerate(data):
                dd = [dt['FCODE'], dt['SHORTNAME'] + "\t" * (15 - len(str(dt['SHORTNAME']))), dt['STKNUM'],
                      round(dt['SUMPLACE'] / 10000.00, 2), round(dt['ENDNAV'] / 100000000.00, 2)]

                if dt['FCODE'] in optionals:
                    data_list.append(dd)
                if dt['FCODE'] in optionalsForBackup:
                    data_list.append(dd)
            print(offset)
            time.sleep(random.randint(0, 0.5))

        print("------------------------------开启最近一个月的数据添加--------------------------------------")
        rank = 1
        for offset in range(1, 10, 1):
            url = urlMonth.format(offset)
            dataMonth = util.getData(url)
            for i, dt in enumerate(dataMonth):
                for dd in data_list:
                    if dt['FCODE'] in dd:
                        dd.insert(0, rank)
                        dd.append(round(dt['SUMPLACE'] / 10000.00, 2))
                        dd.append(str(dt['RATIO']) + "%")
                        if dt['FCODE'] in optionals:
                            print(dd)
                        if dt['FCODE'] in optionalsForBackup:
                            dd.append("---------来自xueqiu")
                            print(dd)
                rank += 1

            time.sleep(random.randint(0, 0.5))


 while True:
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"-----------------------------------------------" )
        start = time.time()
        saveData(self)
        end = time.time()
        print('执行时间:%2.f' % ((end - start) / 60) + "分钟")
        time.sleep(600)













