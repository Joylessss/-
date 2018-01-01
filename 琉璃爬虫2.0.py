import re
import os
import threading
import requests
from bs4 import BeautifulSoup

#flag表示是否为更新 如果为True则表明是更新模式
# continueed表示遇到爬取过的是否继续爬取
flag = False
continueed = True
#为了让用户友好
def index():
    print('1.动画')
    print('2.漫画')
    print('3.游戏')
    print('4.全部下载')
    print('5.爬取最新资源')
    choice = input('输入你打算爬取的区域:')
    choice = int(choice)
    t1 = threading.Thread(target=get_homepage,args=('http://www.hacg.dog/wp/category/all/anime/',),name='动漫')
    t2 = threading.Thread(target=get_homepage,args=('http://www.hacg.dog/wp/category/all/comic/',),name='漫画')
    t3 = threading.Thread(target=get_homepage,args=('http://www.hacg.dog/wp/category/all/game/',),name='游戏')
    if choice == 1:
        t1.start()
    elif choice == 2:
        t2.start()
    elif choice == 3:
        t3.start()
    elif choice == 4:
        t1.start()
        t2.start()
        t3.start()
    elif choice == 5:
        global flag
        flag = True
        t1.start()
        t2.start()
        t3.start()
    else:
        print('请输入数字\'1\',\'2\',\'3\',\'4\',\'5\'')
        index()


#获取网址的内容
def gethtml(url):
    r = requests.get(url)
    html = r.content
    return html


def get_homepage(url):
    i = 1
    print('第%d页的链接为 :%s'%(i,url))
    next_page = getlink(url, i)
    global flag
    while True:
        global  continueed
        if next_page != [] and continueed == True:
            print('第%d页的链接为 :%s' % (i + 1, next_page[0]))
            i = i+1
            next_page = getlink(next_page[0],i)
        else:
            break
    print('%s爬取完毕!!'%threading.current_thread().getName())



#获取每页中的链接并进行操作（返回下一页的链接）
def getlink(url,i):
    print('开始爬取第%d页'%i)
    html = gethtml(url)
    html = html.decode('utf-8')
    #获取本页所有作品的链接
    threadname = threading.current_thread().getName()
    if threadname == '游戏':
        reg_key_name = 'game'
    elif threadname == '动漫':
        reg_key_name = 'anime'
    elif threadname == '漫画':
        reg_key_name = 'comic'
    linkreg = r'(?<=href=\")http://www.hacg.dog/wp/all/%s/.*(?=\" class=\"more-link\">继续阅读)'%reg_key_name
    linkreg = re.compile(linkreg)
    linklist = linkreg.findall(html)
    for x in linklist:
        getcontent(x)
    #获取下一页（如果有的话）的链接
    next_page_reg = r'(?<=rel=\"next\" href=\").*?(?=\")'
    next_page_re = re.compile(next_page_reg)
    next_page_link = re.findall(next_page_re,html)

    return next_page_link


#抓取链接中的有效信息
def getcontent(url):
    html = gethtml(url)
    html = html.decode('utf-8')
    name_reg = r'(?<=<title>)[\s\S]*?(?= \| 琉璃神社 ★ HACG)'
    name_reg = re.compile(name_reg)
    name = name_reg.findall(html)
    forbid_name = ['\\','/',':','*','?','\"','<','>','|']
    for x in forbid_name:
        if x in name[0]:
            name[0] = name[0].replace(x,'')
    print('正在爬取%s:%s'%(threading.current_thread().getName(),name[0]))
    path = 'D:\\琉璃宝库\\' + threading.current_thread().name + '\\' + name[0]
    isExists = os.path.exists(path)
    global flag
    if not isExists and name[0] != '未找到页面':
        os.makedirs(path)
    elif flag == True:
        global continueed
        continueed = False
        return
    else:
        return
    content_reg = r'(?<=<div class=\"entry-content\">)[\s\S]*(?=<div style="width: 100%; margin: 0 auto;" class="ml-slider-3-6-6 metaslider metaslider-flex metaslider-\d{4} ml-slider nav-hidden nav-hidden">)'
    content_re = re.compile(content_reg)
    content = content_re.findall(html)
    os.chdir(path)
    f = open('%s.html'% name[0],'w',encoding='utf-8')
    f.write(content[0])

index()
