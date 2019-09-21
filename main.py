import requests
from bs4 import BeautifulSoup
import re
from queue import PriorityQueue
import json
from collections import deque
import time
from selenium import webdriver

# information['description'] = description
# information['img_url'] = img_url
# information['area'] = area
# information['position'] = position
# information['sendtime'] = sendtime
# information['money'] = money
trans = {'驋':'0','龒':'1','閏':'2','鑶':'3', '餼':'4','麣':'5','龤':'6','鸺':'7','龥':'8','齤':'9'}
pageNumber = 0
q = PriorityQueue()
dq = deque()
MAXCOUNT = 10000
visit = {}
class INFO(object):
    def __init__(self,priority,information):
        self.priority = priority
        self.information = information

    def __lt__(self,other):
        return self.priority < other.priority

    def __str__(self):
        return json.dumps(self.information,ensure_ascii=False)
        #return '(' + str(self.priority) + '\'' + json.dumps(self.information) + '\')'


def transform(string):
    if string == '':
        return string
    if string is not None:
        for key in trans:
        #print(string)
        #print(key)
            string = string.replace(key,trans[key])
    #print(string)
    return string

def clear_information(q,dq):
    if q.qsize() < MAXCOUNT:
        return q
    else:
        while not q.empty():
            dq.append(q.get())
        while dq.count() > MAXCOUNT:
            dq.pop()
        while not dq.empty():
            q.put(dq.popleft())
        return q
    return q

def standard_data(information):
    information['description'] = transform(information['description'])
    information['img_url'] = information['img_url']
    information['area'] = transform(information['area'])
    information['position'] = transform(information['position'])
    temp = re.findall(r'\d+', information['sendtime'])[0]
    time = 0
    if '天' in information['sendtime']:
        time = 24 * 60 * int(temp)
    elif '时' in information['sendtime']:
        time = 60 * int(temp)
    else:
        time = int(temp)
    information['time'] = time
    information['money'] = transform(information['money'])
    return information



#print(response.text)
def info_download():
    for pageNumber in range(0,2):
        time.sleep(2)
        print(pageNumber)
        response = requests.get('https://sz.58.com/chuzu/pn' + str(pageNumber) + '/?PGTID=0d3090a7-0000-457b-6547-0b5d33338a1a&ClickID=2')
        soup = BeautifulSoup(response.text, 'lxml')
        lis = soup.findAll(name='li',attrs={'class':'house-cell'})
        for li in lis:
            description = ''
            img_url = ''
            area = ''
            position = ''
            sendtime = ''
            money = ''
            href = ''
            contents = li.children
            #print(type(contents))
            i = 0
            for tag in contents:
                if tag == '\n' or tag == ' ':
                    continue
                if i == 0:
                    #print(tag)
                    img_url = tag.a.img['lazy_src']
                    href = tag.a['href']
                    #print(img_url)
                if i == 1:
                    tagchildren = tag.children
                    j = 0
                    for tc in tagchildren:
                        if tc == '\n' or tc == ' ':
                            continue
                        if j == 0:
                            description = tag.h2.a.string.replace(' ', '').replace('\n', '')
                        if j == 1:
                            area = tc.string.replace(' ','').replace('\xa0\xa0\xa0\xa0',' ')
                            #print(area)
                        if j == 2:
                            tc = str(tc)
                            position = ''
                            regex = re.compile('<a.*?>(.*?)</a>',re.S)
                            result = regex.findall(tc)
                            regex2 = re.compile('>(.*?)</p>')
                            result2 = regex2.findall(tc)
                            #print(result2)
                            for res in result:
                                position = position + ' ' + res
        #                    print(result[0])
        #                    print(result[1])
                            if result2 != []:
                                position = (position + result2[0].replace(' ','')).replace('</em>',' ')
                            #print(position)
                        j = j + 1
                if i == 2:
                    tagchildren = tag.children
                    j = 0
                    for tc in tagchildren:
                        if tc == '\n' or tc == ' ':
                            continue
                        if j == 0:
                            sendtime = tc.string
                            if sendtime == '\n' or sendtime == '':
                                sendtime = str('0分钟前')
                            sendtime = sendtime.replace('\n','').replace(' ','')
                            #print(sendtime)
                        if j == 1:
                            money = tc.b.string
                            ttt = tc.string
                            #print(money)
                        j = j + 1
                #if i == 3:
                #    print(description)
                i = i + 1
            information = {}
            information['description'] = description
            information['img_url'] = img_url
            information['area'] = area
            information['position'] = position
            information['sendtime'] = sendtime
            #print(information)
            #print(temp[0])
                #print(temp.replace('0','9i9i'))
                #print(temp.replace('\n',''))
                #print(int(temp))
            information['money'] = money
            information['href'] = href
            information = standard_data(information)
            #print(information)

            info = INFO(information['time'],information)
            if href not in visit.keys():
                q.put(info)
                visit[href] = True


if __name__ == '__main__':

    #print(visit['1'])
    while True:
        info_download()
        clear_information(q,dq)
        temp = PriorityQueue()
        while not q.empty():
            t = q.get()
            print(t['href'])
            with open('E:/58House/information.txt','w+') as f:
                f.write(t['href'])
            #driver = webdriver.Firefox()
            #driver.get(t['href'])
            #temp.put(t)
            #time.sleep(60)
        while not temp.empty():
            q.put(temp.get())
        time.sleep(60)

#print(uls)

#def getInfo(soup):
#    img_url = li.div.a.img['src']

