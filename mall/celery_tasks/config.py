# coding:utf8

# 中间人 采用 redis 的14号库
broker_url = "redis://127.0.0.1/14"
# 保存返回结果于 redis 的15号库
result_backend = "redis://127.0.0.1/15"