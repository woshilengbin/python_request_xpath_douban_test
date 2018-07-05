# 可视化爬取结果
import requests
from bs4 import BeautifulSoup  # 从bs4引入BeautifulSoup
from pyecharts import Page, Pie, Bar

#请求网页
url = "https://movie.douban.com/cinema/later/chengdu/"
response = requests.get(url)

soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')

all_movies = soup.find('div', id="showing-soon")  # 先找到最大的div

all_movies_info = []
for each_movie in all_movies.find_all('div', class_="item"):  # 从最大的div里面找到影片的div
    # print(each_movie)  # 输出每个影片div的内容
    all_a_tag = each_movie.find_all('a')
    all_li_tag = each_movie.find_all('li')
    movie_name = all_a_tag[1].text
    moive_href = all_a_tag[1]['href']
    # 运行报错 index out of range：是因为有电影没显示日期
    if len(all_li_tag) == 4:
        movie_date = all_li_tag[0].text
        movie_type = all_li_tag[1].text
        movie_area = all_li_tag[2].text
        movie_lovers = all_li_tag[3].text.replace('人想看', '')
    else:  # 网站结构改变，跟着改变代码
        movie_date = "未知"
        movie_type = all_li_tag[0].text
        movie_area = all_li_tag[1].text
        movie_lovers = all_li_tag[2].text.replace('人想看', '')
    all_movies_info.append({'name': movie_name, 'date': movie_date, 'type': movie_type,
                            'area': movie_area, 'lovers': movie_lovers})
    # print('名字：{}，日期：{}，类型：{}，地区：{}， 关注者：{}'.format(
        # movie_name, movie_date, movie_type, movie_area, movie_lovers))
# print(all_movies_info)  # 输出一下检查数据是否传递成功

page = Page() # 同一个网页显示多个图

# 绘制关注者排行榜图

# i['name'] for i in all_movies_info 这个是Python的快捷方式
# 这一句的作用是从all_movies_info这个list里面依次取出每个元素，
# 并且取出这个元素的 name 属性
sort_by_lovers = sorted(all_movies_info, key=lambda x: int(x['lovers']))
all_names = [i['name'] for i in sort_by_lovers]
all_lovers = [i['lovers'] for i in sort_by_lovers]
lovers_rank_bar = Bar('电影关注者排行榜')
lovers_rank_bar.add('', all_names, all_lovers, is_convert=True, is_label_show=True, label_pos='right')
page.add(lovers_rank_bar)

# lovers_rank_bar

# 绘制电影类型占比图
all_types = [i['type'] for i in all_movies_info]
type_count = {}
for each_types in all_types:
    # 把 爱情 / 奇幻 这种分成[爱情, 奇幻]
    type_list = each_types.split(' / ')
    for e_type in type_list:
        if e_type not in type_count:
            type_count[e_type] = 1
        else:
            type_count[e_type] += 1
# print(type_count) # 检测是否数据归类成功

type_pie = Pie('上映类型占比', title_top=20)
type_pie.add('', list(type_count.keys()), list(type_count.values()), is_label_show=True)
# type_pie

page.add(type_pie)

# 绘制电影上映日期柱状图
all_dates = [i['date'] for i in all_movies_info]
dates_count = {}
for date in all_dates:
    if date not in dates_count:
        dates_count[date] = 1
    else:
        dates_count[date] += 1
# print(dates_count)  # 输出验证数据是否正确

dates_bar = Bar('上映日期占比')
dates_bar.add('',list(dates_count.keys()), list(dates_count.values()), is_label_show=True)
# dates_bar

page.add(dates_bar)

page  # jupyter下自动显示
