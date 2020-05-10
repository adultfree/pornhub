# Pornhub视频爬取

## 简介

众所周知，[Pornhub](http://pornhub.com/)是广大宅男宅女酷爱的网站之一：深夜逛一逛，神清气爽，祝我快速进入梦乡。

这个网站已经做得相当完善，尤其是它的关联推荐，深得我心。

由于防火墙的原因，在大陆地址不允许访问该网站。我使用[国外服务器](https://www.vultr.com/?ref=8377893-6G)搭梯子，才能勉强看到一些小视频和动图。

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

我使用的是Vultr提供的服务器，自己搭建的ShadowSocks环境。如果上图所示，网速大概能达到3MB/s，基本能应付我日常的享用。

目前价格是$5/month，大概就是一个月35块钱。目前它的网站在搞活动，对推荐Vultr的人进行奖励，有两种方式。
* 推荐一个人，获得$10(被推荐人至少消费$10) -> [点击注册](https://www.vultr.com/?ref=7567000)
* 推荐一个人，获得$25(被推荐人至少消费$25)，好处是被推荐人可以获得$100体验券($100仅1个月内有效) -> [点击注册](https://www.vultr.com/?ref=8377893-6G)

如果您注册了以上链接，并满足最小金额，我就可以获得不小的奖励~~谢谢大家
