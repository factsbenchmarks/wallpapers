import requests
from bs4 import BeautifulSoup
import random
import re
import os
import hashlib
import time
import threading
from multiprocessing import Pool #进程池
from concurrent.futures import ThreadPoolExecutor

STORAGE_DIR = r'C:\STORAGE\wallpapers'
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
]

START_URL = 'https://wallhaven.cc/toplist?page={}'

def get_content(url):
    '''
    返回url的html内容
    :param url:
    :return:
    '''
    headers = {
        'User-Agent':random.choice(USER_AGENT_LIST),
    }
    r = requests.get(url,headers=headers,timeout=10)
    if r.status_code == 200:
        return r.text

def list_page_parse(content):
    '''
    列表页解析，获取详情页
    :param content:
    :return:
    '''
    new_urls = []
    soup = BeautifulSoup(content,'lxml')
    imgs = soup(name='a',class_='preview')
    for img in imgs:
        url = img.attrs['href']
        content1 = get_content(url)
        if content1:
            soup1 = BeautifulSoup(content1, 'lxml')
            a_1 = soup1(name='img',id='wallpaper')

            ur11 = a_1[0].attrs['src']
            print(ur11)
            new_urls.append(ur11)

    return new_urls


def download_picture(future):
    '''
    根据url，下载图片，保存到指定位置
    :param url:
    :return:
    '''
    headers = {
        'User-Agent':random.choice(USER_AGENT_LIST),
    }
    urls = future.result()
    for url in urls:
        print(url)
        r = requests.get(url,headers=headers,timeout=20)
        filepath = os.path.join(STORAGE_DIR,get_md5(url)+'.jpg')
        print(filepath)
        time.sleep(random.randint(4,100))
        if r.status_code == 200 and not os.path.exists(filepath):
            f = open(filepath,'wb')
            f.write(r.content)
            f.close()
            print('{} download success'.format(filepath))


def get_md5(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()



def fengniao(num):
    content = get_content(START_URL.format(num))
    print(threading.current_thread().getName())
    return list_page_parse(content)


if __name__ == '__main__':
    excutor = ThreadPoolExecutor()
    for i in range(5,20):
        excutor.submit(fengniao,i).add_done_callback(download_picture)

    excutor.shutdown()
    print('----------END-----------------')