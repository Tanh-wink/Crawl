import re
import os
import requests
from bs4 import BeautifulSoup

work_dir = os.getcwd()
project_dir = os.path.split(work_dir)[0]

start_url = 'http://www.hydcd.com/show/chengyudaquan3.htm'
headsers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'}

def getUrls():
    type_urls = []
    idiom_urls = []
    try:
        response = requests.get(start_url, headers=headsers, timeout=2)
    except:
        print('{} can not requests'.format(start_url))
    else:
        if response.status_code == 200:
            response.encoding = "gbk"
            soup = BeautifulSoup(response.text, 'lxml')
            links = soup.find_all('td', class_="style1")[0].find_all('a')
            for item in links:
                color = item.find_all('font')[0].get('color')
                if color == "#A000F0":
                    link = "http://www.hydcd.com/show/" + item.get("href")
                    type_urls.append(link)
        while type_urls:
            url = type_urls.pop()
            try:
                response = requests.get(url, headers=headsers, timeout=2)
            except:
                print('{} can not requests'.format(start_url))
            else:
                if response.status_code == 200:
                    response.encoding = "gbk"
                    soup = BeautifulSoup(response.text, 'lxml')
                    ps = soup.find_all('td', valign="top")[0].find_all('p')
                    for item in ps:
                        links = item.find_all('a')
                        if links:
                            for link in links:
                                if link.get("href", 0) != 0:
                                    lin = link.get("href").replace("..", "http://www.hydcd.com")
                                    idiom_urls.append(lin)

    return idiom_urls


if __name__ == '__main__':
    idiom_urls = getUrls()
    idiom_urls = set(idiom_urls)
    with open(project_dir + "/data/hydcd_idiom_urls.txt", "w") as fout:
        txt = " ".join(idiom_urls)
        fout.write(txt)
    print("一共有{}个成语。".format(len(idiom_urls)))