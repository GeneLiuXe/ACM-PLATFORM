import os
import tornado.web
BASE_DIRS = os.path.dirname(__file__)

# 参数
options = {
    "port": 8000
}# 这个可以换为解析命令参数

mysql = {
    "host": "localhost",
    "user": "root",
    "passwd": "15858793858ok",
    "dbName": "Gene",
    "port": 3306
}

# 配置
settings = {
    "static_path": os.path.join(BASE_DIRS, "static"),
    "template_path": os.path.join(BASE_DIRS, "templates"),
    "cookie_secret": 'test-secret,',
    "debug": True,
}