## Scrapy
Scrapy官方文档对于先后顺序、关联关系组织的不是很合理

### 1.  实现网络爬虫，需要解决哪些问题？
http://www.cnblogs.com/onlytiancai/archive/2008/04/19/1161425.html

### 2. Scrapy的架构
Scrapy的应用场景，垂直、定向爬取网页并从网页中提取结构化数据

http://doc.scrapy.org/en/1.0/topics/architecture.html

### 3. 下载安装
http://doc.scrapy.org/en/1.0/intro/install.html

- mac
- ubuntu
- windows

### 4. Scrapy入门
http://doc.scrapy.org/en/1.0/intro/tutorial.html

### 5. 从网页中提取结构化数据
http://doc.scrapy.org/en/1.0/topics/selectors.html

http://www.cnblogs.com/ziyunfei/archive/2012/10/05/2710631.html

可视化获取xpath/csspath,开发一个chrome或者firefox的插件，拖拽方式选中元素节点？
http://stackoverflow.com/questions/2631820/im-storing-click-coordinates-in-my-db-and-then-reloading-them-later-and-showing/2631931#2631931
http://jsfiddle.net/luisperezphd/L8pXL/

chrome exten
http://www.cnblogs.com/walkingp/archive/2011/03/31/2001628.html

python shell url 
可以在开发调试阶段避免重复下载网页，有效节省下载过程中的等待时间

### 6. 保存提取的结构化数据
格式&存储介质
http://doc.scrapy.org/en/1.0/topics/feed-exports.html
http://doc.scrapy.org/en/1.0/topics/exporters.html
http://doc.scrapy.org/en/1.0/topics/item-pipeline.html

格式：
FEED_FORMAT: jsonlines/json/csv/xml/

1. 命令行输出 Standard output
scrapy crawer xxx  -o xxx.json -t jsonlines
FEED_URI: stdout

2. 输出到文件 Local filesystem 
setting
FEED_URI: file:///tmp/export.csv #可以使用相对路径？


3. item pipline
写入文件需要考虑到多线程锁情况，锁的处理非常复杂，(scrapy已实现的Local filesystem？Feed Exports)
因此推荐使用已有的数据库技术mysql，redis，CouchDB,MongoDB等。

JsonItemExporter/JsonLinesItemExporter,数据量大时用JsonLinesItemExporter

使用mongodb的好处？

### 7. crawlspider
http://doc.scrapy.org/en/1.0/topics/spiders.html#crawlspider

### 8. 使用http代理
可以在rule的process_request中加入http代理，也可以写一个独立的downloadmiddleware,后者解耦好，可以保持代码结构的清洁。

http://doc.scrapy.org/en/1.0/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.httpproxy

scrapy.spiders.Rule process_request 
Request.meta proxy http://some_proxy_server:port

https://github.com/aivarsk/scrapy-proxies/blob/master/randomproxy.py

### 9.pausing and resuming crawls
http://doc.scrapy.org/en/1.0/topics/jobs.html

### 10. Stats Collection
能够方便的查看状态，运行时间，request次数，成功次数，提取数据条数，代理的健康状况等
http://doc.scrapy.org/en/1.0/topics/stats.html

### 10. 日志策略
scrapy的log不在使用，建议使用python官方log。

### 9. 参数设置
DOWNLOAD_DELAY = 1
AUTOTHROTTLE_ENABLED = True
COOKIES_ENABLED = False
RETRY_TIMES = 10
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

### 11. 常见问题

登录后抓取

selenium