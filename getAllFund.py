# by concyclics
import requests
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
}

funds = {
    '004432': 2673.06,
    '001156': 739.65,
    '009265': 893.87,
    '160222': 2888.71,
    '009821': 1000.00,
    '008903': 2215.10,
    '161725': 2513.26,
    '001475': 1781.60,
    '161028': 2571.06,
    '270002': 2772.19,
    '008168': 9905.49}


def getfund(code: str):
    url = 'http://fund.eastmoney.com/' + code + '.html'
    page = requests.get(url)

    html = str(page.content, 'utf-8')
    # 把content中的内容重新编码成utf-8

    soup = BeautifulSoup(html, 'lxml')

    value = soup.find_all('dd', {'class': 'dataNums'})[1].find('span').getText()
    name = soup.find('a', {'href': url, 'target': "_self"}).getText()
    date = soup.find('dl', {'class': "dataItem02"}).find('p').getText()[6:-1]

    print("基金编号:", code, '\n基金名:', name, "\n日期:", date, "净值:", value)
    return float(value)


if __name__ == '__main__':
    total = 0
    for code in funds:
        share = funds[code]
        price = share * getfund(code)
        total += price

        print('份额:', share, '市值:', '%.2f' % price)

    print('总计:', '%.2f' % total)

