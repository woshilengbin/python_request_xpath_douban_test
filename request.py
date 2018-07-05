import time
import requests
import urllib.request
from lxml import etree
import codecs
import os


# 该函数用于下载图片
# 传入函数： 网页的网址url
def download_picture(url):
    print('开始下载图片' + url)
    # 获取网页的源代码
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    req = requests.get(url, headers=headers)

    # 设置网页编码格式
    req.encoding = 'utf8'
    # 将request.content 转化为 Element
    selector = etree.HTML(req.content)
    items = selector.xpath('//ol/li/div[@class="item"]')
    # 这里使用 a 表示内容可以连续不清空写入

    for item in items:
        # 注意可能只有中文名，没有英文名；可能没有quote简评
        rank, name, alias, rating_num, quote, url = "", "", "", "", "", ""
        try:
            img = item.xpath('./div[@class="pic"]/a/img/@src')[0]
            url = item.xpath('./div[@class="pic"]/a/@href')[0]
            rank = item.xpath('./div[@class="pic"]/em/text()')[0]
            title = item.xpath('./div[@class="info"]//a/span[@class="title"]/text()')
            name = title[0].encode('gb2312', 'ignore').decode('gb2312')
            alias = title[1].encode('gb2312', 'ignore').decode('gb2312') if len(title) == 2 else ""
            rating_num = item.xpath('.//div[@class="bd"]//span[@class="rating_num"]/text()')[0]
            quote_tag = item.xpath('.//div[@class="bd"]//span[@class="inq"]')
            if len(quote_tag) is not 0:
                quote = quote_tag[0].text.encode('gb2312', 'ignore').decode('gb2312').replace('\xa0', '')
            # 输出 排名，评分，简介，地址，图片
            print(rank, rating_num, quote, url, img)
            # 输出 中文名，英文名
            print(name.encode('gb2312', 'ignore').decode('gb2312'),
                  alias.encode('gb2312', 'ignore').decode('gb2312').replace('/', ','))
            mkdir('./collection')
            craeteDir = mkdir('./collection/' + name)
            if craeteDir:
                mkdir('./collection/' + name + '/info/')
                with codecs.open('./collection/' + name + '/info/' + name + '.txt', 'a', 'utf-8') as f:
                    info = name + '  ' + alias + '  ' + "\n" + rank + '  ' + "\n" + quote + "\n" + url + "\n" + img;
                    f.write(info)
                # 利用urllib.request..urlretrieve正式下载图片
                mkdir('./collection/' + name + '/img/')
                content = './collection/' + name + '/img/第{}位_评分为{}分_{}.jpg'.format(rank, rating_num, name)
                print(content)
                urllib.request.urlretrieve(img, content)

        except:
            print('faild!')
            pass


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print(path + ' 创建成功')
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


def main():
    start_urls = ["https://movie.douban.com/top250"]
    for i in range(1, 10):
        start_urls.append("https://movie.douban.com/top250?start=%d&filter=" % (25 * i))

    # 统计该爬虫的消耗时间
    t1 = time.time()
    print('*' * 50)

    for url in start_urls:
        download_picture(url)

    t2 = time.time()

    print('不使用多线程，总共耗时：%s' % (t2 - t1))
    print('*' * 50)


def getMovie():
    url = 'https://movie.douban.com/subject/1292052/'
    data = requests.get(url).text
    s = etree.HTML(data)
    film = s.xpath('//*[@id="content"]/h1/span[1]/text()')
    director = s.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')
    screenwriter = s.xpath('//*[@id="info"]/span[2]/span[2]/a/text()')
    actor = s.xpath('//*[@id="info"]/span[3]/span[2]/a/text()')
    timeLen = s.xpath('//*[@id="info"]/span[13]/text()')
    info = s.xpath('//*[@id="link-report"]/span[1]/span/text()[1]')
    with open('./xiaozhu.txt', 'w', encoding='utf-8') as f:
        print('电影名称：', film)
        print('导演：', director)
        print('编剧：', screenwriter)
        print('主演：', actor)
        print('片长：', timeLen)
        print('简介：', info[0].strip())
        f.write("{},{},{},{}\n".format(film[0], timeLen[0], director[0], info[0].strip()))


# main()
getMovie()
