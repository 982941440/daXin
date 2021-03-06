import re

from fake_useragent import UserAgent
import requests
import json
import time
import random
import csv

from fontTools.misc import etree

urlYear = "http://fund.eastmoney.com/API/FundDXGJJ.ashx?callback=jQuery18303973379239507868_1634526975963&r=1634526976000&m=0&pageindex={}&sorttype=desc&SFName=STKNUM&IsSale=1&_=1634526976235"
urlMonth = "http://fund.eastmoney.com/API/FundDXGJJ.ashx?callback=jQuery18309756068947863759_1632273874569&r=1632273874000&m=8&pageindex={}&sorttype=desc&SFName=RATIO&IsSale=1&_=1632273874739"
urlInstitution = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=cyrjg&code={}&rt=0.7622758025769991"

optionals = ["001520","009476",
            "002272", "002174","011082", "400007", "003191","005776","003166","673020","001695"]
optionalsForBackup = ["000656","007807","010573","002943","010695","168105","003961","006327","270042 "]

totalPage=300

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

def getYearData():
    data_list = []

    for offset in range(1, totalPage, 1):
        url = urlYear.format(offset)
        data = getData(url)

        for i, dt in enumerate(data):
            if  dt['SUMPLACE'] != "" and  dt['ENDNAV'] != "" :
                dd = [dt['FCODE'], dt['SHORTNAME'], dt['STKNUM'],round(dt['SUMPLACE'] / 10000.00, 1),round(dt['ENDNAV']/ 100000000.00, 1)]

            if dt['FCODE'] in optionals:
                data_list.append(dd)
            if dt['FCODE'] in optionalsForBackup:
                data_list.append(dd)
        print(offset)
        time.sleep(random.randint(1, 3) / 5.0)
    return  data_list

def getMonthData():
    data_list = []

    rank = 1
    for offset in range(1, totalPage, 1):
        url = urlMonth.format(offset)
        dataMonth = getData(url)

        for i, dt in enumerate(dataMonth):
            dd = [str(round(rank / 50.00, 1)) + "%",dt['FCODE'], round(dt['SUMPLACE'] / 10000.00, 2), str(dt['RATIO']) + "%",dt['MAXSG']]

            if dt['FCODE'] in optionals:
               data_list.append(dd)
            if dt['FCODE'] in optionalsForBackup:
               dd.append("---------??????xueqiu")
               data_list.append(dd)
            rank += 1
        time.sleep(random.randint(1, 3) / 5.0)

    return  data_list

def getInstitutionPercent(code):
    url = urlInstitution.format(code)
    ua = UserAgent(verify_ssl=False)
    headers = {
        'User-Agent': ua.random,
        "Referer": 'http://fund.eastmoney.com/data/dxgjj_xgccjjyl.html'
    }
    html = requests.get(
        url=url,
        headers=headers
    ).content.decode('utf-8')
    # str =html[225:231]
    #????????????
    # institutionPercent=''.join(filter(lambda i: i in ['.'] or i.isdigit,html[220:235]))
    institutionPercents=re.findall(r"\d+\.?\d*", html[220:235])

    if len(institutionPercents)>0:
      return institutionPercents[0]+"%"


    return  "-----"

def  printMergeData():
    start = time.time()
    institutionPercent = getInstitutionPercent("002174")
    yearDataList=getYearData()
    monthDataList=getMonthData()

    for dt in monthDataList:
        for dd in yearDataList:
              if dt[1] in dd[0]:
                  # [dt['FCODE'], dt['SHORTNAME'] + "\t" * (15 - len(str(dt['SHORTNAME']))), dt['STKNUM'],
                  #       round(dt['SUMPLACE'] / 10000.00, 2), round(dt['ENDNAV'] / 100000000.00, 2)]
                  #
                  # [str(round(rank / 50.00, 1)) + "%", dt['FCODE'], round(dt['SUMPLACE'] / 10000.00, 2),
                  #       str(dt['RATIO']) + "%"]
                  institutionPercent=getInstitutionPercent(dt[1])
                  dt =[dt[0],dt[1],dd[2],dt[2],dd[3],dd[4],dt[3],dt[4],institutionPercent,dd[1]]
                  print(dt)

                  rows = [
                      [dt]
                  ]
                  saveToFile(rows)
      #  sumRankRatio +=
    end = time.time()
    logStr='????????????:%2.f' % ((end - start) / 60) + "??????" + '%2.f' % ((end - start) % 60) + "???"
    print(logStr)

    rows = [
     []
    ]

    saveToFile(rows)

    return  monthDataList


def saveData():
    start = time.time()

    data_list = []
    for offset in range(1, totalPage, 1):
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

    print("------------------------------????????????????????????????????????--------------------------------------")
    rank = 1
    sumRankRatio = 0
    for offset in range(1, totalPage, 1):
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
                        dd.append("---------??????xueqiu")
                        print(dd)
            rank += 1

        time.sleep(random.randint(1, 3) / 5.0)

    end = time.time()
    print("????????????%1.f" % len(data_list) + "???")
    print("?????????????????????%1.f" % (sumRankRatio / len(data_list)) + "%")
    print('????????????:%2.f' % ((end - start) / 60) + "??????" + '%2.f' % ((end - start) % 60) + "???")


def getStr():
    url= "http://fund.eastmoney.com/API/FundDXGJJ.ashx?callback=jQuery18303973379239507868_1634526975963&r=1634526976000&m=0&pageindex={}&sorttype=desc&SFName=STKNUM&IsSale=1&_=1634526976235"

    start = time.time()

    str=""
    for offset in range(1, totalPage, 1):
        url = url.format(offset)
        data = getData(url)

        for i, dt in enumerate(data):
           str=str+dt['SHORTNAME']
        print(offset)
        time.sleep(random.randint(1, 3) / 5.0)

    end = time.time()
    print('????????????:%2.f' % ((end - start) / 60) + "??????" + '%2.f' % ((end - start) % 60) + "???")
    return  str

def  saveToFile(rows):
     #headers = ['time']

     with open('test.csv', 'a',encoding='utf-8-sig')as f:
       f_csv = csv.writer(f)
      # f_csv.writerow(headers)
       f_csv.writerows(rows)
