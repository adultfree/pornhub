# Pornhub视频爬取

## 简介

众所周知，[Pornhub](http://pornhub.com/)是广大宅男宅女酷爱的网站之一：深夜逛一逛，神清气爽，祝我快速进入梦乡。

这个网站已经做得相当完善，尤其是它的关联推荐，深得我心。

由于防火墙的原因，在大陆地址不允许访问该网站。我使用[国外服务器](https://justhost.ru/?ref=66813)搭梯子，才能勉强看到一些小视频和动图。

每次被动图诱惑得不行，但观看视频却卡得要死。对于深夜寂寞的人来说，这样的浏览无异于饮鸩止渴。

思来想去，决定还是花点时间，参考Github上其他同志的代码，做一个简单的爬虫吧。

## 爬取的内容

本程序提供自定义深度的视频爬取，即获得爬取的页面后，继续下载其推荐栏目的页面。

目前提供[评分最高(TopRated)](https://www.pornhub.com/video?o=tr)页面的所有视频爬取，也提供仅对你感兴趣的某个视频进行下载。

## 使用方法

```shell script
# 确认Python版本为Python3
python3 --version
root@adultfree:~/pornhub# python3 --version
Python 3.5.2
# 安装依赖包
root@adultfree:~/pornhub# python3 -m pip install -r requirements.txt
......
# 开始爬取评分最高的部分视频(及其推荐视频)
root@adultfree:~/pornhub# scrapy crawl top_rated

# 开始爬取感兴趣的某个视频(及其推荐视频)
root@adultfree:~/pornhub# scrapy crawl related_show
```

## 注意事项

注意pornhub/settings.py中的下载选项

```python
# 当DOWNLOAD_MP4_VIDEO设为True时，程序会试图下载视频
# 在大陆地区下载速度非常慢，因此强烈建议仅获取地址(设为False)
# 当以下两项设为False时，视频链接会被保存到"日期-时间-类型.log"文件中
# 打开文件，将地址批量拷贝，放入迅雷中下载，速度会快很多
DOWNLOAD_MP4_VIDEO = False
DOWNLOAD_WEBM_VIDEO = False
```

注意下载深度，默认只提取当前页面的视频。
* 对related_show而言，只下载`RelatedShow.py`中指定的视频(及当页的视频简介)
* 对top_rated而言，只下载主页上展示的所有视频(及视频页面的视频简介)

```python
# 相关视频下载的深度，默认下载当前页面的视频(不下载相关视频)
# 注意：每增加一层深度，下载视频数会呈指数级增加
DEPTH_LIMIT = 1
```

另外，我仅提取画质最高的版本链接。毕竟越清晰，就越真实 :-)

## 小技巧

爬取到的链接，通过迅雷下载，一开始速度会比较快，但大概过了10分钟左右，速度会逐渐降下来。
这是因为下载链接中包含了SessionId，而Pornhub服务器应该设置了对应的过期时间。
我每次下载大概会有2、3个链接下载不成功，只能把未下载完成的视频删除，重新爬取。
重新爬取的时候，代码会检查该视频是否已存在于`data`目录下，如果已存在则不再记录下载链接，为了实现视频检查，迅雷下载的目录最好定义在`pornhub/data`下。


另一个办法是直接在代理服务器上爬取。把代码上传到代理服务器，并将`DOWNLOAD_MP4_VIDEO`设置为`True`。
在代理服务器上的下载速度大概能达到30MB/s，很快硬盘就会被撑满。
目前没有代码检测硬盘剩余容量，因此自己注意一下爬取深度。
当数据爬取到代理服务器上以后，可以简单安装个Nginx静态服务器，把下载的内容放到DocumentRoot目录下，通过迅雷直接向代理服务器下载，这样则不会出现过期问题，并且下载速度基本相同。

## 效果展示

#### 爬取结果

![爬取结果](https://raw.githubusercontent.com/adultfree/pornhub/master/images/crawl_result.png)

#### 下载状态

![下载状态](https://raw.githubusercontent.com/adultfree/pornhub/master/images/download_xunlei.png)

## 补充说明

如果发现爬虫无法爬取信息，那应该是因为没有使用翻墙工具。

我最近发现，俄罗斯的Josthost服务器速度非常靠谱。尤其对电信和联通用户而言，速度可以说是非常快了。
我自己搭建了ShadowSocks环境。网速最高能达到20MB/s，平时能达到3MB/s左右。

**访问Justhost，建议使用Chrome浏览器+Google Translate，否则只有俄语版本**

价格极其感人，我直接购买了一年，费用1047RUB，按当时的汇率，折算成105.81RMB。
想起前天请客吃饭，就花掉了230，这价格真的很便宜了。
JustHost也有一个推荐返利活动，通过[此链接注册](https://justhost.ru/?ref=66813)，我可以获得5%的返利。
