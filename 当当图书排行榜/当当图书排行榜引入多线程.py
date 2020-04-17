import requests
from lxml import etree
from multiprocessing import Pool
from multiprocessing import Queue
import datetime
from handel_mongo import mongo_info

startime = datetime.datetime.now()
url_list = Queue()
#url = 'http://bang.dangdang.com/books/bestsellers'
def getdate(url):
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    r = requests.get(url,headers = header,timeout = 10)
    r.encoding = r.apparent_encoding
    r = r.text
    html = etree.HTML(r)
    bookname0 = html.xpath("//div[@class='name']/a/text()")
    bookauthor0 = html.xpath("//div[@class='publisher_info'][1]/a[1]/@title")
    booktime0 = html.xpath("//ul/li/div/span[1]/text()")
    dates = []
    for i in range(len(booktime0)):
        mdate = {
        '书名':'',
        '作者' : '',
        '出版日期' : ''
        }
        mdate['书名'] = str(bookname0[i]).replace(' ','')
        mdate['作者'] = str(bookauthor0[i]).replace(' ','').replace('\n','').replace('\u3000','')
        mdate['出版日期'] = booktime0[i].replace(' ','')
        #print(mdate)
        dates.append(mdate)
        mongo_info.insert_item(mdate)
    for date in dates:
        # date = date + '\n'
        print(date) 
    # dates = str(dates)
    #with open(r'D:\pythontest\test\当当图书排行榜\当当图书排行榜.txt','w',encoding='utf-8') as f:
    with open(r'D:\pythontest\test\当当图书排行榜\当当图书排行榜.csv','a',encoding='utf-8') as f:
        for date in dates:
            date = str(date)+'\n'
            f.write(date)
            print('保存成功')
# def main():
#     url_list.put(url)
#     pool = Pool(processes=2)
#     pool.map(getdate,url_list.get())
#     #print(url_list.get())
#     endtime = datetime.datetime.now()
#     print((endtime - startime).second)
if __name__ =='__main__':
    urls = []
    for i in range(1,20):
        url = 'http://bang.dangdang.com/books/bestsellers/1-{}'.format(str(i))
        urls.append(url)
    pool = Pool(processes=3)
    pool.map(getdate,urls)
    #getdate()
    endtime = datetime.datetime.now()
    print((endtime - startime).seconds)