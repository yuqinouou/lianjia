import threading
import sqlite3
import requests
import random
import time
from bs4 import BeautifulSoup as BS
from bs4 import SoupStrainer as SS
# load constants
from constants import *
import login
import db

def xiaoqu_spider(db_xq, url_page, lock):
    try:
        req = requests.session()
        cookie = login._loadCookie(cookieFile)
        req.cookies.update(cookie)
        req.headers = hds[random.randint(0, len(hds)-1)]
        plain_text = login._openURL(url_page, req).text
        soup = BS(plain_text, "html.parser")
    except (u2.HTTPError, u2.URLError) as e:
        print(e)
        exception_write('xiaoqu_spider', url_page, lock, logFile)
        exit(-1)
    except Exception as e:
        print(e)
        exception_write('xiaoqu_spider', url_page, lock, logFile)
        exit(-1)

    xiaoqu_list=soup.findAll('div',{'class':'info-panel'})
    for xq in xiaoqu_list:
        info_dict={}
        info_dict.update({u'Neighbourhood':xq.find('a').text})
        content=xq.find('div',{'class':'con'}).find("a", {'class':'ad'})
        if content:
            info_dict.update({u'District':content.text})
            info = content.next_sibling.next_sibling
            if info:
                info_dict.update({u'Area':info.text})
                info = info.next_sibling
                if info:
                    info = info.next_sibling
                    if info:
                        info_dict.update({u'Built':info.next_sibling.strip()})
        content = xq.findAll("span", {"class":"num"})
        if content:
            info_dict.update({u'Avg_Price':content[0].text.strip()})
            info_dict.update({u'N_Selling':content[1].text.strip()})
        command=db.gen_xiaoqu_insert_command(info_dict)
        db_xq.execute(command,1)
    print("Spidered", url_page)

def do_xiaoqu_spider(db_xq, lock):
    url = u"http://sh.lianjia.com/xiaoqu/"
    req = requests.session()
    cookie = login._loadCookie(cookieFile)
    req.cookies.update(cookie)
    req.headers = hds[random.randint(0,len(hds)-1)]
    plain_text = login._openURL(url, req).text
    soup = BS(plain_text, "html.parser")
    nXiaoqu = soup.find("h2").span.text
    total_pages = int(float(nXiaoqu) / 20 + 1)
    print("=" * 50)
    print("Shanghai has", total_pages, "pages", nXiaoqu, "Xiaoqus")
    print("=" * 50)

    threads=[]
    for i in range(total_pages):
        url_page=u"http://sh.lianjia.com/xiaoqu/d" + str(i+1)
        t=threading.Thread(target=xiaoqu_spider, args=(db_xq, url_page, lock))
        threads.append(t)
        # xiaoqu_spider(db_xq, url_page)

    print("initializing Threads...")
    pct = 1
    for index, t in enumerate(threads):
        time.sleep(1)
        t.start()
        if (float(index) / total_pages) > float(pct) / 100:
            print(pct, "% of Xiaoqu Query Started!")
            pct += 1
    pct = 1
    for index, t in enumerate(threads):
        t.join()
        if (float(index) / total_pages) > float(pct) / 100:
            print(pct, "% of Xiaoqu Records Finished!")
            pct += 1

    print(u"Spidered all Xiaoqus!")

def chengjiao_spider(db_cj, url_page, lock):
    try:
        req = requests.session()
        cookie = login._loadCookie(cookieFile)
        req.cookies.update(cookie)
        req.headers = hds[random.randint(0,len(hds)-1)]
        plain_text = login._openURL(url_page, req, delay = 1, timeout = 10).text
        soup = BS(plain_text, "html.parser")
    except (u2.HTTPError, u2.URLError) as e:
        print(e)
        exception_write('chengjiao_spider', url_page, lock, logFile)
        return
    except Exception as e:
        print(e)
        exception_write('chengjiao_spider', url_page, lock, logFile)
        return

    cj_list=soup.findAll('div',{'class':'info-panel'})
    for cj in cj_list:
        info_dict={}
        href=cj.find('a')
        if not href:
            continue
        info_dict.update({u'Hyperlink':href.attrs['href']})
        content=cj.find('h2').text.split()
        if content:
            info_dict.update({u'Neighbourhood':content[0]})
            info_dict.update({u'Layout':content[1]})
            info_dict.update({u'Square':content[2]})
        content=cj.find('div',{'class':'con'})
        if content:
            content = content.text.strip().split()
            info_dict.update({u'District':content[0]})
            info_dict.update({u'Area':content[1]})
            for c in content:
                if c.find(u'层')!=-1:
                    info_dict.update({u'Floor':c})
                elif c.find(u'朝')!=-1:
                    info_dict.update({u'Facing':c})
                elif c.find(u'装')!=-1 or c.find(u'毛')!=-1:
                    info_dict.update({u'Remodel':c})
        content=cj.findAll('div',{'class':'div-cun'})
        if content:
            info_dict.update({u'Date':content[0].text})
            info_dict.update({u'Price_per_sq':content[1].text})
            info_dict.update({u'Price':content[2].text})
        content=cj.find('div',{'class':'introduce'})
        if content:
            content = content.text.strip().split()
            for c in content:
                if c.find(u'满')!=-1:
                    info_dict.update({u'Type':c})
                elif c.find(u'学')!=-1:
                    info_dict.update({u'School':c})
                elif c.find(u'距')!=-1:
                    info_dict.update({u'Metro':c})

        command=db.gen_chengjiao_insert_command(info_dict)
        db_cj.execute(command,1)
    print("Spidered", url_page)

def do_chengjiao_spider(db_cj, lock):
    url=u"http://sh.lianjia.com/chengjiao/"
    req = requests.session()
    cookie = login._loadCookie(cookieFile)
    req.cookies.update(cookie)
    req.headers = hds[random.randint(0,len(hds)-1)]
    plain_text = login._openURL(url, req, delay = 1, timeout = 10).text
    soup = BS(plain_text, "html.parser")
    nChengjiao = soup.find("h2").span.text

    total_pages = int(float(nChengjiao) / 20 + 1)
    print("=" * 50)
    print("Shanghai had", total_pages, "pages", nChengjiao, "transactions")
    print("=" * 50)

    threads=[]
    for i in range(total_pages):
        url_page=u"http://sh.lianjia.com/chengjiao/d" + str(i + 1)
        t=threading.Thread(target=chengjiao_spider, args=(db_cj, url_page, lock))
        threads.append(t)
        # chengjiao_spider(db_cj, url_page)
        # print("Spidered Page", i, "from", ps.quote_plus(xq_name))
    print("initializing Threads...")
    pct = 1
    for index, t in enumerate(threads):
        time.sleep(1)
        t.start()
        if (float(index) / total_pages) > float(pct) / 100:
            print(pct, "% of Chengjiao Query Started!")
            pct += 1
    pct = 1
    for index, t in enumerate(threads):
        t.join()
        if (float(index) / total_pages) > float(pct) / 100:
            print(pct, "% of Chengjiao Records Finished!")
            pct += 1
    print(u"Spidered all Chengjiao Records!")

def exception_write(fun_name, url, lock, logFile):
    lock.acquire()
    f = open(logFile,'a')
    line="%s %s\n" % (fun_name, url)
    f.write(line)
    f.close()
    lock.release()

def exception_read(lock):
    lock.acquire()
    f=open('log.txt','r')
    lines=f.readlines()
    f.close()
    f=open('log.txt','w')
    f.truncate()
    f.close()
    lock.release()
    return lines

def exception_spider(db_xq, db_cj, lock):
    count_cj=0
    count_xq=0
    excep_list=exception_read(lock)
    while excep_list:
        for excep in excep_list:
            excep=excep.strip()
            if excep=="":
                continue
            excep_name, url = excep.split(" ",1)
            if excep_name=="chengjiao_spider":
                chengjiao_spider(db_cj, url)
                count_cj += 1
            elif excep_name=="xiaoqu_spider":
                xiaoqu_spider(db_xq, url)
                count_xq += 1
            else:
                print("wrong format")
        print("Have spidered %d exception xiaoqu" % count_xq)
        print("Have spidered %d exception chengjiao" % count_cj)
        excep_list=exception_read(lock)
    print('Finished Exceptions!')
