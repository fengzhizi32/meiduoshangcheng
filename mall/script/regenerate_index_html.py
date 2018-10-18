#!/usr/bin/env python

import sys
# 因为 脚本是在script中,所以需要 使用: ../指定到上一级目录ls
sys.path.insert(0, '../')
sys.path.insert(0, '../apps')

import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mall.settings'

import django
django.setup()

from contents.crons import generate_static_index_html


if __name__ == '__main__':
    generate_static_index_html()