import re
import urllib.request
def getlink(url):
    # 模拟浏览器
    headers=('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')
    opener=urllib.request.build_opener()
    opener.addheaders=[headers]
    urllib.request.install_opener(opener)
    file=urllib.request.urlopen(url)
    data=str(file.read())
    pattern='(https?://[^\s");]+\.(\w|/)*)'
    link=re.compile(pattern).findall(data)
    # 去除重复的连接
    link=list(set(link))
    return link
url="http://blog.csdn.net"
linklist=getlink(url)
for link in linklist:
    print(link[0])