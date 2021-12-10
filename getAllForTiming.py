from fake_useragent import UserAgent
import time
import random
import ssl
import util

ssl._create_default_https_context = ssl._create_unverified_context

class TianTianSpider(object):



 while True:
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"-----------------------------------------------" )
        start = time.time()
        util.saveData()
        end = time.time()
        print('执行时间:%2.f' % ((end - start) / 60) + "分钟")
        time.sleep(600)













