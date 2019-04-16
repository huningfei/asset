"""
网页分页功能，封装了一个类，如果要使用需要传三个参数，current_page, total_count, url_prefix
"""


# 封装分页类
class MyPage(object):

    def __init__(self, current_page, total_count, url_prefix, per_page=10, max_show=7):
        """
        初始化一个我自己定义的分页实例
        :param current_page: 当前页码
        :param total_count: 总的数据量
        :param url_prefix: 分页中a标签的url前缀
        :param per_page: 每一个显示多少条数据
        :param max_show: 页面上最多显示多少个页码
        """
        self.total_count = total_count
        self.per_page = per_page
        self.max_show = max_show
        self.url_prefix = url_prefix

        # 最多显示页码数的一半
        half_show = max_show // 2
        #    因为URL取到的参数是字符串格式，需要转换成int类型
        try:
            current_page = int(current_page)
        except Exception as e:
            # 如果输入的页码不是正经页码，默认展示第一页
            current_page = 1
        # 求总共需要多少页显示
        total_page, more = divmod(total_count, per_page)
        if more:
            total_page += 1
        # 如果输入的当前页码数大于总数据的页码数，默认显示最后一页
        if current_page > total_page:
            current_page = total_page
        self.current_page = current_page

        # 计算一下显示页码的起点和终点
        show_page_start = current_page - half_show
        show_page_end = current_page + half_show
        # 特殊情况特殊处理
        # 1. 当前页码 - half_show <= 0
        if current_page - half_show <= 0:
            show_page_start = 1
            show_page_end = max_show
        # 2. 当前页码数 + hale_show >= total_page
        if current_page + half_show >= total_page:
            show_page_end = total_page
            show_page_start = total_page - max_show + 1
        # 3. 总共需要的页码数 < max_show
        if total_page < max_show:
            show_page_start = 1
            show_page_end = total_page

        self.show_page_start = show_page_start
        self.show_page_end = show_page_end
        self.total_page = total_page

    # 数据切片的起点
    @property
    def start(self):
        return (self.current_page - 1) * self.per_page

    # 数据切片的终点
    @property
    def end(self):
        return self.current_page * self.per_page
    # 序号也跟着变
    def num(self):
        return (self.current_page-1)*self.per_page

    # 分页的html代码
    def page_html(self):
        tmp = []
        page_html_start = '<nav aria-label="Page navigation" class="text-center"><ul class="pagination">'
        page_html_end = '</ul></nav>'
        tmp.append(page_html_start)
        # 添加一个首页
        tmp.append('<li><a href="/{}?page=1">首页</a></li>'.format(self.url_prefix))
        # 添加一个上一页
        # 当当前页是第一页的时候不能再点击上一页
        if self.current_page - 1 <= 0:
            tmp.append(
                '<li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>')
        else:
            tmp.append(
                '<li><a href="/{}?page={}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                    self.url_prefix, self.current_page - 1))
        # for循环添加要展示的页码
        for i in range(self.show_page_start, self.show_page_end + 1):
            # 如果for循环的页码等于当前页码，给li标签加一个active的样式
            if self.current_page == i:
                tmp.append('<li class="active"><a href="/{1}?page={0}">{0}</a></li>'.format(i, self.url_prefix))
            else:
                tmp.append('<li><a href="/{1}?page={0}">{0}</a></li>'.format(i, self.url_prefix))
        # 添加一个下一页
        # 当前 当前页已经是最后一页，应该不让下一页按钮能点击
        if self.current_page + 1 > self.total_page:
            tmp.append(
                '<li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            tmp.append(
                '<li><a href="/{}?page={}" aria-label="Previous"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                    self.url_prefix, self.current_page + 1))
        # 添加一个尾页
        tmp.append('<li><a href="/{}?page={}">尾页</a></li>'.format(self.url_prefix, self.total_page))
        tmp.append(page_html_end)

        page_html = "".join(tmp)
        return page_html