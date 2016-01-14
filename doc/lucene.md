## lucene

### 一、基本原理
http://www.cnblogs.com/dewin/archive/2009/11/24/1609905.html
http://www.cnblogs.com/forfuture1978/archive/2009/12/14/1623594.html

倒排索引

分词组件 Tokenizer：词元(Token)

- 将文档分成一个一个单独的单词。 中文分词
- 去除标点符号。  中文标点符号
- 去除停词(Stop word)。 中文有哪些？

语言处理组件 Linguistic Processor : 词(Term)

- 变为小写(Lowercase)。繁体-简体
- 将单词缩减为词根形式，如“cars”到“car”等。这种操作称为：stemming。 同音字-谐音
- 将单词转变为词根形式，如“drove”到“drive”等。这种操作称为：lemmatization。

关键词在文章中出现次数和出现的位置

- 字符位置，即记录该词是文章中第几个字符（优点是关键词亮显时定位快）；
- 关键词位置，即记录该词是文章中第几个关键词（优点是节约索引空间、词组（phase）查询快）

词典文件（Term Dictionary）、频率文件(frequencies)、位置文件 (positions)

针对索引文件的压缩技术

Query解析

结果相关度排序
a) tf-idf
b) 向量空间模型的算法(VSM)


二元搜索算法

### 二、lucene实现
http://www.cnblogs.com/dewin/archive/2009/11/26/1611377.html
http://www.cnblogs.com/forfuture1978/archive/2009/12/14/1623596.html
http://www.cnblogs.com/forfuture1978/archive/2010/02/22/1671487.html

### 三、下载安装
http://blog.163.com/zhoutao_1001/blog/static/979024220123177225922/
http://www.open-open.com/lib/view/open1393378311037.html

### 四、基本示例
http://svn.apache.org/viewcvs.cgi/lucene/pylucene/trunk/samples
http://svn.apache.org/viewcvs.cgi/lucene/pylucene/trunk/test


### 五、其他问题
大数据量情况下？ 分布式的索引文件？
lucene+hdfs? http://www.cnblogs.com/huangfox/archive/2010/10/15/1852206.html
