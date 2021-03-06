# -*- coding: UTF-8 -*-
import requests
import csv
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup
from .info import info


def get_content(url):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url, headers=header, timeout=timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))
        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))
        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))
        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))
    return rep.text


def get_data(html_text, info):
    # final = []
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body  # 获取body部分
    data = body.find('div', {'id': '7d'})  # 找到id=7d的div
    ul = data.find('ul', {'class': 't clearfix'})
    li = ul.find_all('li')
    # print(li)

    for day in li:  # 对每个li标签中的内容进行遍历
        # temp = []
        # 这里有问题
        date = day.find('h1').string  # 找到日期
        # final.append(date)
        inf = day.find_all('p')  # 找到li标签中所有的p标签
        # print(inf[0].string)
        # final.append(inf[0].string)  # 将第一个p标签中的内容（天气状况）加入到temp中
        info['weather'] = inf[0].string
        if inf[1].find('span') is None:
            temperature_higgest = None  # 天气预报可能没有当天的最高气温（到了傍晚，就是这样），需要加一个判断，来输出最低气温
        else:
            temperature_higgest = inf[1].find('span').string + '℃'  # 找到最高气温
            # print(temperature_higgest)
            # temperature_higgest = temperature_higgest.replace('℃', '') # 到了晚上网站内容会有变动，去掉这个符号
        temperature_lowest = inf[1].find('i').string  # 找到最低温度
        # temperature_lowest = temperature_lowest.replace('℃', '')
        info['temp'] = temperature_lowest + '~' + temperature_higgest
        # final.append(temperature_lowest)
        # final.append(temperature_higgest)
        # final.append(temp)
        break  # 只获取当天天气信息
    clothes = body.find('li', {'id': 'chuanyi'}).find('p').string  # 获取穿衣指数
    info['tips'] = clothes[0:len(clothes)-1]
    # print(clothes)
    # print(info)
    return info


# 将数据抓取到的文件写入文件
def write_data(data, name):
    file_name = name
    with open(file_name, 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)


def crawling_weather(dic):
    url = 'http://www.weather.com.cn/weather/'+dic['city_id']+'.shtml'
    html = get_content(url)
    temp = dic
    return get_data(html, temp)


# 主函数
if __name__ == '__main__':
    crawling_weather(info)
    pass
    # print(info)
    # write_data(result, 'weather.csv')
