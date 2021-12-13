from fake_useragent import UserAgent
import requests
import json
import time
import random


def getData(url):
    ua = UserAgent(verify_ssl=False)
    headers = {
        'User-Agent': ua.random,
        "Referer": 'http://fund.eastmoney.com/data/dxgjj_xgccjjyl.html'
    }

    html = requests.get(
        url=url,
        headers=headers
    ).content.decode('utf-8')

    parse_html = html
    ix1 = parse_html.find("[")
    ix2 = parse_html.find("]")
    res = parse_html[ix1:ix2 + 1]
    res = eval(repr(res).replace('\\', ''))
    data = json.loads(res)

    return data


def saveData():
    urlYear = "http://fund.eastmoney.com/API/FundDXGJJ.ashx?callback=jQuery18303973379239507868_1634526975963&r=1634526976000&m=0&pageindex={}&sorttype=desc&SFName=STKNUM&IsSale=1&_=1634526976235"
    urlMonth = "http://fund.eastmoney.com/API/FundDXGJJ.ashx?callback=jQuery18309756068947863759_1632273874569&r=1632273874000&m=8&pageindex={}&sorttype=desc&SFName=RATIO&IsSale=1&_=1632273874739"

    optionals = ["010573", "350005", "001520", "001121", "009476",
                 "001672", "007807", "002272", "002174", "004138", "011082", "400007", "003191"]
    optionalsForBackup = []

    start = time.time()

    data_list = []
    for offset in range(1, 250, 1):
        url = urlYear.format(offset)
        data = getData(url)

        for i, dt in enumerate(data):
            dd = [dt['FCODE'], dt['SHORTNAME'] + "\t" * (15 - len(str(dt['SHORTNAME']))), dt['STKNUM'],
                  round(dt['SUMPLACE'] / 10000.00, 2), round(dt['ENDNAV'] / 100000000.00, 2)]

            if dt['FCODE'] in optionals:
                data_list.append(dd)
            if dt['FCODE'] in optionalsForBackup:
                data_list.append(dd)
        print(offset)
        time.sleep(random.randint(1, 3) / 5.0)

    print("------------------------------开启最近一个月的数据添加--------------------------------------")
    rank = 1
    sumRankRatio = 0
    for offset in range(1, 250, 1):
        url = urlMonth.format(offset)
        dataMonth = getData(url)

        for i, dt in enumerate(dataMonth):
            for dd in data_list:
                if dt['FCODE'] in dd:
                    dd.insert(0, str(round(rank / 50.00, 1)) + "%")
                    sumRankRatio += rank / 50.00
                    dd.append(round(dt['SUMPLACE'] / 10000.00, 2))
                    dd.append(str(dt['RATIO']) + "%")
                    if dt['FCODE'] in optionals:
                        print(dd)
                    if dt['FCODE'] in optionalsForBackup:
                        dd.append("---------来自xueqiu")
                        print(dd)
            rank += 1

        time.sleep(random.randint(1, 3) / 5.0)

    end = time.time()
    print("匹配了：%1.f" % len(data_list) + "个")
    print("平均的排名为：%1.f" % (sumRankRatio / len(data_list)) + "%")
    print('执行时间:%2.f' % ((end - start) / 60) + "分钟" + '%2.f' % ((end - start) % 60) + "秒")

def getStr():
    url= "http://fund.eastmoney.com/API/FundDXGJJ.ashx?callback=jQuery18303973379239507868_1634526975963&r=1634526976000&m=0&pageindex={}&sorttype=desc&SFName=STKNUM&IsSale=1&_=1634526976235"

    start = time.time()

    str=""
    for offset in range(1, 250, 1):
        url = url.format(offset)
        data = getData(url)

        for i, dt in enumerate(data):
           str=str+dt['SHORTNAME']
        print(offset)
        time.sleep(random.randint(1, 3) / 5.0)

    end = time.time()
    print('执行时间:%2.f' % ((end - start) / 60) + "分钟" + '%2.f' % ((end - start) % 60) + "秒")
    return  str