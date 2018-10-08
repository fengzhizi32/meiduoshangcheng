# 静态化首页的手动脚本 {#静态化首页的手动脚本}

为了方便开发，随时生成静态化首页，我们可以在scripts中新建静态化首页的脚本

regenerate\_index\_html.py

```
#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../apps')

import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mall.settings'

 # 让django进行初始化设置
import django
django.setup()

from contents.crons import generate_static_index_html


if __name__ == '__main__':
    generate_static_index_html()
```

为文件增加可执行权限

```
chmod +x regenerate_index_html.py
```

然后测试执行

![](/assets/script_test.png)

