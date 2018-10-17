from collections import OrderedDict

from django.shortcuts import render

# Create your views here.
# 1.我们在定义模型类的时候, 尽量多的分析字段(把字段罗列出来),不要分析表和表之间的关系
#    比较明显的表, 使可以分析和实现的(单独定义一个表,不是说表和表之间的关系
# 2.找一个安静的时间和地方 去分析表和表之间的关系
# 三个表 --> 多对多
# 多对多 --> 三个表


# 首页的优化---->为什么要优化?
# 1.首页的访问量较大
# 2.频率查询数据的话,造成数据库的压力也比较大
# 3.首页数据也会经常的变化

# 优化的方向:
# 1.我们可以缓存数据
# 2.静态化--->所谓静态化,其实就是:让用户访问我们提前准备好的html页面
    # 2.1确保业务逻辑(数据)是正确的

from django.views import View

from contents.models import ContentCategory
from goods.models import GoodsChannel


class HomeView(View):
    def get(self, request):
        # 使用有序字典保存类别的顺序
        # categories = {
        #     1: { # 组1
        #         'channels': [{'id':, 'name':, 'url':},{}, {}...],
        #         'sub_cats': [{'id':, 'name':, 'sub_cats':[{},{}]}, {}, {}, ..]
        #     },
        #     2: { # 组2
        #
        #     }
        # }
        # 初始化存储容器
        categories = OrderedDict()
        # 获取一级分类
        channels = GoodsChannel.objects.order_by('group_id', 'sequence')

        # 对一级分类进行遍历
        for channel in channels:
            # 获取group_id
            group_id = channel.group_id
            # 判断group_id 是否在存储容器,如果不在就初始化
            if group_id not in categories:
                categories[group_id] = {
                    'channels': [],
                    'sub_cats': []
                }

            one = channel.category
            # 为channels填充数据
            categories[group_id]['channels'].append({
                'id': one.id,
                'name': one.name,
                'url': channel.url
            })
            # 为sub_cats填充数据
            for two in one.goodscategory_set.all():
                # 初始化 容器
                two.sub_cats = []
                # 遍历获取
                for three in two.goodscategory_set.all():
                    two.sub_cats.append(three)

                # 组织数据
                categories[group_id]['sub_cats'].append(two)

        # 广告和首页数据
        contents = {}
        content_categories = ContentCategory.objects.all()
        # content_categories = [{'name':xx , 'key': 'index_new'}, {}, {}]

        # {
        #    'index_new': [] ,
        #    'index_lbt': []
        # }
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')


        # 将数据传递给模板,再验证
        context = {
            'categories': categories,
            'contents': contents
        }
        return render(request, 'index.html', context)