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
        self.url="http://fund.eastmoney.com/API/FundDXGJJ.ashx?callback=jQuery18309756068947863759_1632273874569&r=1632273874000&m=8&pageindex={}&sorttype=desc&SFName=RATIO&IsSale=1&_=1632273874739";
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
                         "011147", "006080", "005983", "004315", "002051", "006133", "004784","010356"]
            optionalsForBackup = ["002505", "002718", "003166", "009614"]

            with open('fund.csv', 'a', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                for i, dt in enumerate(data):
                    # if  "300" not in dt['SHORTNAME'] and "C" not in dt['SHORTNAME'] and "B" not in dt['SHORTNAME'] and "E" not in dt['SHORTNAME'] and dt['SUMPLACE']>15000000 and  dt['ENDNAV'] < 300000000 :
                    dd = [dt['FCODE'], dt['SHORTNAME'] + "\t" * (15 - len(str(dt['SHORTNAME']))), dt['STKNUM'],
                          round(dt['SUMPLACE'] / 10000.00, 2), str(dt['RATIO']) + "%"]

                    if dt['FCODE'] in  optionals:
                          print(dd)
                          data_list.append(dd)
                    if dt['FCODE'] in  optionalsForBackup:
                          print(dd)
                          print("---------来自xueqiu------------")
                          data_list.append(dd)

                writer.writerows(data_list)



    def main(self):
        for offset in range(1, 250, 1):
            print('第%d页爬取' % self.page)
            url = self.url.format(offset)
            self.get_page(url)
            time.sleep(random.randint(1, 3))
            self.page += 1



if __name__ == '__main__':
    start = time.time()
    spider = TianTianSpider()
    spider.main()
    end = time.time()
    print('执行时间:%2.f' % (end - start))