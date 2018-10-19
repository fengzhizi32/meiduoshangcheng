from haystack import indexes
from .models import SKU

# SKU索引数据模型类
class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """SKU索引数据模型类"""

    # document=True 确定那个字段是搜索的主要字段
    # use_template=True 可以使用模板来定义全文检索的字段
    text = indexes.CharField(document=True, use_template=True)
    
    # 在搜索的结果中现实的字段
    id = indexes.IntegerField(model_attr='id')
    name = indexes.CharField(model_attr='name')
    price = indexes.DecimalField(model_attr='price')
    default_image_url = indexes.CharField(model_attr='default_image_url')
    comments = indexes.IntegerField(model_attr='comments')

    def get_model(self):
        """返回建立索引的模型类"""
        return SKU

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter(is_launched=True)