import ssl
import util

ssl._create_default_https_context = ssl._create_unverified_context

class TianTianSpider(object):

    util.saveData()



