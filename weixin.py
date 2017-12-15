import queue
import threading
import re
import urllib.request
import time
import urllib.error

urlqueue=queue.Queue()
headers=('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')
opener=urllib.request.build_opener()
opener.addheaders=[headers]
urllib.request.install_opener(opener)
listurl=[]

# 使用代理服务器
def use_proxy(proxy_addr,url):
    try:
        proxy=urllib.request.ProxyHandler({'http:proxy_addr'})
        opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        data=urllib.request.urlopen(url).read().decode('utf-8')
        return data
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
        time.sleep(10)
    except Exception as e:
        print('exception:'+str(e))
        time.sleep(1)

# 线程1，专门获取对应网址并处理为真实网址
class geturl(threading.Thread):
    def __init__(self,key,pagestart,pageend,proxy,urlqueue):
        threading.Thread.__init__(self)
        self.pagestart=pagestart
        self.pageend=pageend
        self.proxy=proxy
        self.urlqueue=urlqueue
        self.key=key
    def run(self):
        page=self.pagestart
        keycode=urllib.request.quote(key)
        pagecode=urllib.request.quote('&page')
        for page in range(self.pagestart,self.pageend+1):
            url="http://weixin.sogou.com/weixin?type=2&query="+keycode+pagecode+str(page)

            # 用代理服务器爬取，解决ip被封杀问题
            data1=use_proxy(self.proxy,url)
            listurlpat='<div class="txt-box">.*?(http://.*?)"'
            listurl.append(re.compile(listurlpat,re.S).findall(data1))
        print('获取到'+str(len(listurl))+'页')   
        for i in range(0,len(listurl)):
            time.sleep(7)
            for j in range(0,len(listurl[i])):
                try:
                    url=listurl[i][j]
                    # 处理成为真实URL
                    url=url.replace("amp;","")
                    print("第"+str(i)+"i"+str(j)+"j次入队")
                    self.urlqueue.put(url)
                    self.urlqueue.task_done()
                except urllib.error.URLError as e:
                    if hasattr(e,"code"):
                        print(e.code)
                    if hasattr(e,"reason"):
                        print(e.reason)
                    time.sleep(10)
                except Exception as e:
                    print("exception:"+str(e))
                    time.sleep(1)
# 从线程1中获取文章网址依次爬取对应文章的信息
class getcontent(threading.Thread):
    def __init__(self,urlqueue,proxy):
        threading.Thread.__init__(self)
        self.urlqueue=urlqueue
        self.proxy=proxy
    def run(self):
        html1='''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>文章页面</title>
        </head>
        <body>'''
        fh=open("C:/Users/Administrator/Desktop/Python/python-crawl/2.html","wb")
        fh.write(html1.encode("utf-8"))
        fh.close()
        fh=open("C:/Users/Administrator/Desktop/Python/python-crawl/2.html","ab")
        i=1
        while(True):
            try:
                url=self.urlqueue.get()
                data=use_proxy(self.proxy,url)
                titlepat="<title>(.*?)</title>"
                contentpat='id="js_content">(.*?)id="js_sg_bar"'
                title=re.compile(titlepat).findall(data)
                content=re.compile(contentpat,re.S).findall(data)
                thistitle="此次没有获取到数据"
                thiscontent="此次没有获取到数据"
                if(title!=[]):
                     thistitle=title[0]
                if(content!=[]):
                      thiscontent=content[0]
                dataall="<p>标题为:"+thistitle+"</p><p>内容为:"+thiscontent+"</p><br>"
                fh.write(dataall.encode("utf-8"))
                print("第"+str(i)+"个网页处理") #便于调适
                i+=1
            except urllib.error.URLError as e:
                if hasattr(e,"code"):
                    print(e.code)
                if hasattr(e,"reason"):
                    print(e.reason)
                time.sleep(10)
            except Exception as e:
                print("exception:"+str(e))
                time.sleep(1)
        fh.close()
        html2='''</body>
        </html>
        '''
        fh=open("C:/Users/Administrator/Desktop/Python/python-crawl/2.html","ab")
        fh.write(html2.encode("utf-8"))
        fh.close()
# 主控制程序
class conrl(threading.Thread):
    def __init__(self,urlqueue):
        threading.Thread.__init__(self)
        self.urlqueue=urlqueue
    def run(self):
        while(True):
            print("程序执行中")
            time.sleep(60)
            if(self.urlqueue.empty()):
                print("程序执行完毕")
                exit()
key="前端"
proxy="45.123.3.105:8080"
proxy2=""
pagestart=1#起始页
pageend=2#爬取到哪页
#创建线程1对象
t1=geturl(key,pagestart,pageend,proxy,urlqueue)
t1.start()
#创建线程2对象
t2=getcontent(urlqueue,proxy)
t2.start()
#创建线程3对象
t3=conrl(urlqueue)
t3.start()

    