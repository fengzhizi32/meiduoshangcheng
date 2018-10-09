# coding:utf8

# tasks-->broker-->worker

# 第一步,创建一个Celery的实例对象
from celery import Celery
import os


if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mall.settings'

# 2.需要创建celery的对象
# 参数main 设置脚本名,因为是第一个参数,可以不写
# app = Celery(main='celery_tasks')
app = Celery('celery_tasks')

# 3.设置broker  加载配置文件
app.config_from_object('celery_tasks.config')

# 4.自动检测任务,让broker去执行
app.autodiscover_tasks(['celery_tasks.sms'])