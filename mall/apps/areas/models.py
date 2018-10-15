from django.db import models
# Create your models here.

# 省的模型
class Area(models.Model):
    """行政区划"""

    name = models.CharField(max_length=20, verbose_name='名称')

    # ForeignKey('self')指向自己    自关联
    # related_name='subs' 可以设置  反向关联的属性名  默认是关联模型类名小写_set
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True, verbose_name='上级行政区划')

    # area_set
    # subs_set

    class Meta:
        db_table = 'tb_areas'
        # 上级行政区划
        verbose_name = '行政区划'
        verbose_name_plural = '行政区划'

    def __str__(self):

        return self.name
# 市的模型
# class Area1(models.Model):
#     """行政区划"""
#
#     name = models.CharField(max_length=20, verbose_name='名称')
#
#     # ForeignKey('self')指向自己    自关联
#     parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='上级行政区划')
#
#     class Meta:
#         db_table = 'tb_areas'
#         # 上级行政区划
#         verbose_name = '行政区划'
#         verbose_name_plural = '行政区划'
#
#     def __str__(self):
#
#         return self.name