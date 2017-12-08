import urllib.request
import urllib.parse
url='http://www.iqianyue.com/mypost'
#post请求的数据封装
postdata=urllib.parse.urlencode({
    'name':'bill',
    'pass':'gate'
}).encode('utf-8')
#创建post请求，没有数据这是get请求
req=urllib.request.Request(url,postdata) 
#设置报头来模拟浏览器
req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36')
data=urllib.request.urlopen(req).read()
# 创建本地文件
fhandle=open('C:/Users/Administrator/Desktop/Python/test4.html','wb')
# 数据写入
fhandle.write(data)
fhandle.close()

