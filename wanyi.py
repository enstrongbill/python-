import urllib.request
import http.cookiejar
url='http://news.163.com/17/1219/07/D60L8F3U000189FH.html'

headers={'Accept': '*/*','Accept-Encoding': '','Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0','Referer': 'http://news.163.com/'}

cjar=http.cookiejar.CookieJar();
proxy=urllib.request.ProxyHandler({'http':'127.0.0.1:8888'});
opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler,urllib.request.HTTPCookieProcessor(cjar))
headall=[]
for key,value in headers.items():
    item=(key,value)
    headall.append(item)
print(headall)
opener.addheaders=headall
urllib.request.install_opener(opener)
data=urllib.request.urlopen(url).read()
fhandle=open('C:/Users/Administrator/Desktop/Python/python-crawl/data/s.html','wb')
fhandle.write(data)
fhandle.close()