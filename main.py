import requests
from bs4 import BeautifulSoup
import re

# information['description'] = description
# information['img_url'] = img_url
# information['area'] = area
# information['position'] = position
# information['sendtime'] = sendtime
# information['money'] = money



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

trans = {'麣':'0','龒':'1','餼':'2','龤':'3', '驋':'4','鑶':'5','閏':'6','龥':'7','鸺':'8','齤':'9'}
pageNumber = 0

#print(response.text)
def info_download():
    for pageNumber in range(0,71):
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
            contents = li.children
            #print(type(contents))
            i = 0
            for tag in contents:
                if tag == '\n' or tag == ' ':
                    continue
                if i == 0:
                    #print(tag)
                    img_url = tag.a.img['src']
                    print(img_url)
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
            information = standard_data(information)
            print(information)




if __name__ == '__main__':
    info_download()
#print(uls)

#def getInfo(soup):
#    img_url = li.div.a.img['src']

