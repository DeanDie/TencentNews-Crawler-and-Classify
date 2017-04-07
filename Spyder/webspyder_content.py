
import pymysql
import os
import requests
import re
import dbHelper


class webSpyder(object):
    def __init__(self):
        self.count = 0
        self.flag = 0
        self.class_count = [0] * 10
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows)'}

        self.url = [['http://roll.news.qq.com/', 'news'], ['http://roll.ent.qq.com/', 'ent'],
                    ['http://roll.sports.qq.com/', 'sports'], ['http://roll.finance.qq.com/', 'finance'],
                    ['http://roll.tech.qq.com/', 'tech'], ['http://roll.games.qq.com/', 'games'],
                    ['http://roll.auto.qq.com/', 'auto'], ['http://roll.edu.qq.com/', 'edu'],
                    ['http://roll.house.qq.com/', 'house']]


    def getAllLinks(self):
        date = '2016-11-27'
        # self.count = 0
        # self.class_count[8] = 19950
        for mainUrl_id in range(0, len(self.url)):
            referer = self.url[mainUrl_id][0] + 'index.htm?date='
            while self.class_count[mainUrl_id] < 20000:
                page = 0
                while True:
                    page += 1
                    try:
                        url = self.url[mainUrl_id][0] + "interface/roll.php?of=json&date=" + date + "&mode=1&page=" + str(page) + '&site=' + self.url[mainUrl_id][1]
                        self.headers['Referer'] = referer + date + '&site=' + self.url[mainUrl_id][1]
                        table = requests.get(url=url, headers=self.headers).json()['data']['article_info']
                        pattern_link = re.compile(r'href="(.*?)"', re.S | re.M | re.I)
                        links = list(pattern_link.findall(table))
                        if mainUrl_id != 0:
                            if list != None:
                                for link in links:
                                    self.getEachWebContent(link, mainUrl_id)
                            if self.class_count[mainUrl_id] >= 20000:
                                break
                        else:
                            pattern_classes = re.compile(r'class="t-tit">(.*?)</span>', re.S | re.M | re.I)
                            classes = list(pattern_classes.findall(table))
                            l = len(classes)
                            if classes != None:
                                for i in range(len(classes)):
                                    if (classes[i] == '[国内]' or classes[i] == '[国际]'):
                                        self.getEachWebContent(links[i], mainUrl_id)
                                    if self.class_count[mainUrl_id] >= 20000:
                                        break
                    except:
                        break
                date = self.date_pre(date)
            date = '2016-11-27'


    def getEachWebContent(self, url, url_category):
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows)'}, timeout=10)
            self.get_content(response, url_category)
        except requests.RequestException as e:
                print(e)


    def get_content(self, response, category):
        source = response.text
        url = response.url
        pattern = []
        pattern.append(r'<h1>(.*?)</h1>')
        pattern.append(r'style=".*?TEXT-INDENT.*?".*?>(.*?)<')
        pattern[0] = re.compile(pattern[0], re.S | re.M | re.I)
        pattern[1] = re.compile(pattern[1], re.S | re.M | re.I)
        title = pattern[0].findall(source)[0]
        list = pattern[1].findall(source)
        content = title + '\n' + ''.join(list)
        if len(content) >= 80:
            # content.encode('utf8')
            dbHelper.insert_textinfo((self.count, category, content))
            self.class_count[category], self.count = self.class_count[category] + 1, self.count + 1
            print('#########Inserted!##########' + '    ' + url)

    def date_pre(self, date):   #2016-12-12
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])
        if day == 1:
            if month == 3:
                month = 2
                if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
                    day = 29
                else:
                    day = 28
            elif month == 1:
                month = 12
                year -= 1
                day = 31
            elif month in [2, 4, 6, 8, 9, 11]:
                month -= 1
                day = 31
            else:
                month -= 1
                day = 30
        else:
            day -= 1

        year, month, day = str(year), str(month), str(day)
        if len(month) < 2:
            month = '0' + month
        if len(day) < 2:
            day = '0' + day
        return year + '-' + month + '-' + day


if __name__ == '__main__':
    spyder = webSpyder()
    spyder.getAllLinks()