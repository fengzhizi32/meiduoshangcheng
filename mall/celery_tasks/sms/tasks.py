# coding:utf8

from libs.yuntongxun.sms import CCP
from celery_tasks.main import app


# 定义任务
# 任务必须经过 celery 的实例对象 tasks 装饰器装饰
# 注意:装饰器是 tasks   name 就是任务名
@app.task(name='send_code')
def send_sms_code(mobile, sms_code):

    ccp = CCP()

    ccp.send_template_sms(mobile, [sms_code, 5], 1)