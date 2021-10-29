from pyecharts import options as opts
from pyecharts.charts import Map
import time
from lxml import etree
from selenium import webdriver

import csv


def map_visualmap() -> Map:
    c = (
        Map(init_opts=opts.InitOpts(page_title="中国疫情地图", bg_color="#FDF5E6"))
            .add("现存确诊人数", data_pair=current_data_dic, maptype="china")
            .set_series_opts(label_opts=opts.LabelOpts(color="#8B4C39", font_size=10))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="中国疫情地图", subtitle="数据更新于"+time_format),
            visualmap_opts=opts.VisualMapOpts(pieces=[
                {"value": 0, "label": "无", "color": "#00ccFF"},
                {"min": 1, "max": 9, "color": "#FFCCCC"},
                {"min": 10, "max": 99, "color": "#DB5A6B"},
                {"min": 100, "max": 499, "color": "#FF6666"},
                {"min": 500, "max": 999, "color": "#CC2929"},
                {"min": 1000, "max": 9999, "color": "#8C0D0D"},
                {"min": 10000, "color": "#9d2933"}
            ], is_piecewise=True),
        )
    )
    return c

if __name__ == '__main__':
    url="https://news.qq.com/zt2020/page/feiyan.htm#/?nojump=1"
    try:
        driver = webdriver.Chrome(executable_path="D:\chromedriver.exe")
        driver.get(url)
        text = driver.page_source
    except:
        print('访问失败')
    html = etree.HTML(text)
    current_data_dic = []
    tbodys = html.xpath('//*[@id="listWraper"]/table[2]/tbody')
    for tbody in tbodys:
        area = tbody.xpath('./tr/th/p/span/text()')[0]
        Existing_confirmed = tbody.xpath('./tr[1]/td[1]/p[1]/text()')[0]
        pcurrent_data_dic=[]
        pcurrent_data_dic.append(area)
        pcurrent_data_dic.append(Existing_confirmed)
        current_data_dic.append(pcurrent_data_dic)
    time_format = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    map_visualmap().render("国内疫情地图.html")
