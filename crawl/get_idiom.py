import os
import random
import requests
import threading
import time
from bs4 import BeautifulSoup
from bs4.element import Tag

work_dir = os.getcwd()
project_dir = os.path.split(work_dir)[0]

ip_pool = ["124.94.253.104:9999", "175.43.179.146:9999", "123.101.207.99:9999", "123.163.116.170:9999",
           "123.52.96.63:9999", "114.102.6.8:9999", "125.123.153.177:3000", "123.54.40.143:9999", "59.50.26.216:32676",
           "123.169.124.234:9999", "122.4.44.54:41007", "110.243.13.134:9999", "123.169.117.241:9999",
           "42.59.100.6:9999", "171.11.59.110:9999"]

all_idioms = []
fail_urls = []
crawded_urls = []

class myWorm(threading.Thread):
    def __init__(self, id=0, headers=None, idiom_urls=None):

        super(myWorm, self).__init__()

        self.id = id
        self.idiom_urls = idiom_urls
        self.headers = headers

    def clearErrorLogOl(self):
        with open(project_dir + '/log/{}_errorLog'.format(self.id), 'w', encoding='utf-8') as fp:
            fp.write('\n')

    def writeLog(self, str):
        with open(project_dir + '/log/myLog_{}_V2.log'.format(self.id), 'a', encoding='utf-8') as fp:
            fp.write(str)
            fp.write('\n')

    def writeErrorLogOl(self, str):
        with open(project_dir + '/log/{}_errorLog'.format(self.id), 'a', encoding='utf-8') as fp:
            fp.write(str)
            fp.write('\n')

    def requestsUrl(self, url):
        failcount = 0
        ip = ip_pool[random.randrange(0, len(ip_pool))]
        proxy = {'HTTP': ip}
        while True:
            try:
                response = requests.get(url, headers=self.headers, proxies=proxy, timeout=10)
            except:
                self.writeErrorLogOl('wormID:{} crawling current url:{}:'
                                     'can not request'.format(self.id, url))
            else:
                if response.status_code == 200:
                    return response
                else:
                    failcount += 1
                    if failcount > 10:
                        return []
                    else:
                        continue

    def get_idiom(self):
        global fail_count
        idiom_urls = self.idiom_urls
        global LinksNum
        while idiom_urls:
            url = idiom_urls.pop(0)
            if url in fail_urls:
                continue
            response = self.requestsUrl(url)
            if response:
                try:
                    response.encoding = "gbk"
                    soup = BeautifulSoup(response.text, 'lxml')
                    td = soup.find('td', valign="top")
                    texts = td.find('font', color="#000000").text.replace("\r", "").replace("\t", "").split("\n")
                    fields = ["成语", "拼音", "出处", "举例造句", "近义词", "反义词", "英文", "故事", "解释"]
                    cur_idiom = {}
                    for item in texts:
                        if item != "":
                            splits = [it.strip() for it in item.split("：")]
                            left = splits.pop(0).replace("【", "").replace("】", "")
                            right = ":".join(splits)
                            if left in fields:
                                cur_idiom[left] = right
                    all_idioms.append(cur_idiom)
                    crawded_urls.append(url)
                    print('wormID:{} crawling current url:{}'
                          '\n\tsuccessfully\tthe rest number of Idiom Links:{:.2%}/{}'
                          .format(self.id, url, len(idiom_urls) / LinksNum, len(idiom_urls)))
                    div = soup.find('div', style="margin-left: 6px;line-height: 180%")
                    for tag in div.childGenerator():
                        if isinstance(tag, Tag):
                            if tag.text == "成语分类导航：":
                                break
                            if tag.get("href", 0) != 0:
                                link = tag.get("href").replace("..", "http://www.hydcd.com/cy")
                                if link not in crawded_urls:
                                    idiom_urls.append(link)
                    idiom_urls = list(set(idiom_urls))
                except:
                    print('wormID:{} crawling  current url:{}:'
                          '\n\tfail\tthe rest number of Idiom Links:{:.2%}/{}'
                          .format(self.id, url, len(idiom_urls) / LinksNum, len(idiom_urls)))
                    fail_urls.append(url)
            else:
                print('wormID:{} crawling current url:{}'
                      '\n\tcan not get current link response\tthe rest number of Idiom Links:{:.2%}/{}'
                      .format(self.id, url, len(idiom_urls) / LinksNum, len(idiom_urls)))
                self.writeLog('wormID:{} crawling current url:{}:'
                              'can not get current link response'.format(self.id, url))
                fail_urls.append(url)

    def run(self):
        self.get_idiom()


def get_idioms(headers=None, wormNum=30):
    global LinksNum
    with open(project_dir + "/data/hydcd_idiom_urls.txt", "r") as fin:
        text = fin.read()
        idiom_urls = text.split(" ")
    LinksNum = len(idiom_urls)
    worm_pool = []
    for i in range(wormNum):
        curWorm = myWorm(id=i+1, headers=headers, idiom_urls=idiom_urls)
        worm_pool.append(curWorm)
    for curWorm in worm_pool:
        curWorm.start()
        time.sleep(2)
    for curWorm in worm_pool:
        curWorm.join()

    print("成功爬取{}条".format(len(all_idioms)))
    print("失败爬取{}条".format(len(fail_urls)))
    with open(project_dir + "/data/hydcd_idioms.txt", "w", encoding="utf-8") as fout:
        for idiom in all_idioms:
            fout.write(str(idiom) + "\n")


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        #   'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    get_idioms(headers=headers, wormNum=30)