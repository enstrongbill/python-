import re
import urllib.request
def craw(url,page):
    html=urllib.request.urlopen(url).read()
    html=str(html)
    # 选择区域，把侧边栏的图片过滤掉
    pattern1='<div id="plist".+?<div class="page clearfix">'
    result1=re.compile(pattern1).findall(html)
    result1=result1[0]
    # 过滤图片地址
    pattern2='<img width="220" height="220" data-img="1" data-lazy-img="//(.+?\.jpg)">'
    imagelist=re.compile(pattern2).findall(result1)
    x=1
    for imageurl in imagelist:
        imagename="C:/Users/Administrator/Desktop/Python/python-crawl/img/"+str(page)+str(x)+".jpg"
        imageurl="http://"+imageurl
        # print(imageurl)
        try:
            urllib.request.urlretrieve(imageurl,filename=imagename)
        except urllib.error.URLError as e:
            if hasattr(e,"code"):
                x+=1
            if hasattr(e,"reason"):
                x+=1
        x+=1
# 自己设置遍历的页数，京东共167页
for i in range(1,20):
    url="http://list.jd.com/list.html?cat=9987,653,655&page="+str(i)
    craw(url,i)