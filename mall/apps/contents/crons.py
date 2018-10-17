import time
import os
from goods.models import GoodsChannel
from .models import ContentCategory
from collections import OrderedDict
from django.template import loader
from django.conf import settings



def generate_static_index_html():
    """
    生成静态的主页html
    """

    print('%s:generate_static_index' % time.ctime())
    # 商品频道及分类菜单
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

    context = {
        'categories': categories,
        'contents': contents
    }

    # 1.加载模板    get_template可以到模板文件夹中 获取制定的模板
    template = loader.get_template('index.html')

    # 2.我们应该将查询好的数据 传递给模板, 让模板进行渲染
        # 渲染成功后,返回给我们的html
    html_data = template.render(context)

    #将文件写入  把html数据写入到指定的路径
    # GENERATED_STATIC_HTML_FILES_DIR --->相当于meiduoshangcheng/front
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR,'index.html')
    with open(file_path,'w') as f:
        f.write(html_data)