from fake_useragent import UserAgent
import time
import random
import ssl
import requests
import json
import csv

ssl._create_default_https_context = ssl._create_unverified_context

class TianTianSpider(object):


    def __init__(self):
        self.url="http://fund.eastmoney.com/API/FundDXGJJ.ashx?callback=jQuery18303973379239507868_1634526975963&r=1634526976000&m=0&pageindex={}&sorttype=desc&SFName=STKNUM&IsSale=1&_=1634526976235";

        ua = UserAgent(verify_ssl=False)
        self.headers = {
            'User-Agent': ua.random,
            "Referer": 'http://fund.eastmoney.com/data/dxgjj_xgccjjyl.html'
        }
        self.page = 1

    def get_page(self, url):
        html = requests.get(
            url=url,
            headers=self.headers
        ).content.decode('utf-8')
        self.parse_page(html)

    def parse_page(self, html):
        parse_html = html
        ix1 = parse_html.find("[")
        ix2 = parse_html.find("]")
        res = parse_html[ix1:ix2 + 1]
        res=  eval(repr(res).replace('\\', ''))
        data = json.loads(res)
        self.write_page(data)

    def write_page(self, data):
            data_list = []
            optionals = ["006034", "007413", "003647", "005314", "005935", "003191", "007111", "002300",
                         "011147", "006080", "005983", "004315", "002051", "006133", "004784", "010356"]
            # optionalsForBackup=["005232","005600","000934"]
            optionalsForBackup = ["002505", "002718", "003166", "009614"]
            with open('fund.csv', 'a', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                for i, dt in enumerate(data):
                    # if  "300" not in dt['SHORTNAME'] and "C" not in dt['SHORTNAME'] and "B" not in dt['SHORTNAME'] and "E" not in dt['SHORTNAME'] and dt['SUMPLACE']>15000000 and  dt['ENDNAV'] < 300000000 :
                    dd = [dt['FCODE'], dt['SHORTNAME'] + "\t" * (15 - len(str(dt['SHORTNAME']))), dt['STKNUM'],
                          round(dt['SUMPLACE'] / 10000.00, 2)]

                    if dt['FCODE'] in  optionals:
                          print(dd)
                          data_list.append(dd)
                    if dt['FCODE'] in  optionalsForBackup:
                          print(dd)
                          print("----------------??????xueqiu-------------")
                          data_list.append(dd)

                writer.writerows(data_list)

    def main(self):
        for offset in range(1, 250, 1):
            print('???%d?????????' % self.page)
            url = self.url.format(offset)
            self.get_page(url)
            time.sleep(random.randint(1, 3))
            self.page += 1



if __name__ == '__main__':
    start = time.time()
    spider = TianTianSpider()
    spider.main()
    end = time.time()
    print('????????????:%2.f' % (end - start))