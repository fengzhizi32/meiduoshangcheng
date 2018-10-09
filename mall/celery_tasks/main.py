# coding:utf8

# tasks-->broker-->worker

# 第一步,创建一个Celery的实例对象
# 第二步,通过celery的配置文件来设置broker
# 第三步,celery自动检测项目

from celery import Celery

# 进行Celery允许配置
# 为celery使用django配置文件进行设置
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
# 参数为列表形式: []
# 每一项 就是 对应的 celery_tasks.sms
app.autodiscover_tasks(['celery_tasks.sms'])


# worker 执行 是在 虚拟环境中 通过指令 等待broker 分配任务

# celery -A 脚本路径.celery实例所对应的文件 worker -l info
# celery -A celery_tasks.main worker -l info