# -*- coding: utf-8 -*-
# python: 3.4.3
# user: liu
# time: 2015/8/15 0015
# email: humooo@outlook.com
import urllib.request
import re

# 糗事百科爬虫类
class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.page_data = None
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'
        # 存放段子的变量，每一个元素是每一页的段子们
        self.stories = []

    # 按页取原始数据
    def get_raw_data(self, page_index):
        url = 'http://www.qiushibaike.com/hot/page/' + str(page_index)
        request = urllib.request.Request(url)
        request.add_header('Content-Type', 'text/html; charset=UTF-8')
        request.add_header('User-Agent', self.user_agent)
        response = urllib.request.urlopen(request)
        # 将页面转化为UTF-8编码
        page = response.read().decode('utf-8')
        return page

    # 按页取具体数据
    def get_by_page(self, page_index):
        page_data = self.get_raw_data(page_index)
        items = []
        # 匹配作者
        author_regex = r'<div class="author">\s*<a[^>]*?>\s*<img src="(.*?)"\s*/>(.*?)</a>\s*</div>\s+'
        # 匹配内容
        content_regex = r'<div class="content">(.*?)<!--\d+-->\s+</div>\s+'
        # 匹配图片
        thumb_regex = r'(<div class="thumb">\s*<a[^>]*?>\s*<img src="(.*?)".*?/>\s*</a>\s*</div>\s+|\s+)?'
        # 匹配图片
        video_regex = r'(<div class="video_holder"[^>]*?>.*?<source src="(.*?)".*?>\s*</div>\s+|\s+)?'
        # 匹配赞
        stats_vote_regex = r'<div class="stats">\s+<span[^>]*?><i\s*class="number">(\d*)</i>.*?</span>'
        # 匹配标签
        stats_tag_regex = r'.*?<span class="stats-tag">(.*?)</span>\s+</div>'
        stats_regex = stats_vote_regex + stats_tag_regex

        # 取得数据
        if page_data:
            item_pattern = re.compile(author_regex
                                      + content_regex
                                      + thumb_regex
                                      + video_regex
                                      + stats_regex
                                      , re.S)
            items = re.findall(item_pattern, page_data)

        f = open('result.txt', 'a', encoding='utf-8')
        print('page：' + str(page_index),
              sep='\n', end='\n',
              file=f)
        count = 1
        # 输出该页的每一条内容
        for item in items:
            item_tmp = []
            for v in item:
                v = v.strip().replace('\n', '')
                v = v.strip().replace('<br/>', '')
                item_tmp.append(v)
            item = item_tmp
            author_pic = item[0]  # 头像
            author_name = item[1]  # 名字
            content = item[2]  # 内容
            # item[3] 是thumb div
            thumb = item[4]  # 图片
            # item[5] 是video div
            video = item[6]  # 视频
            stats_vote = item[7]  # 赞
            tag_regex = r'<a[^>]*?>\s*(.*?)</a>'  # 匹配tag
            tag_pattern = re.compile(tag_regex, re.S)
            stats_tag = re.findall(tag_pattern, item[8])  # 标签
            story = [author_pic, author_name, content, thumb, stats_vote, stats_tag]
            self.stories.append(story)

            # TODO 可以存到数据库、存到文件、打印输出etc，下面是以追加方式输出到文件
            print('#：' + str(count), '头像：' + author_pic, '昵称：' + author_name, '内容：' + content,
                  '图片：' + thumb, '视频：' + video, '赞：' + stats_vote, '标签：' + str(list(stats_tag)),
                  sep='\n', end='\n\n',
                  file=f)
            count += 1

# run
qsbk = QSBK()
page = 1  # 想要获取的页面号
qsbk.get_by_page(page)