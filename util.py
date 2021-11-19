from fake_useragent import UserAgent
import requests
import json


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