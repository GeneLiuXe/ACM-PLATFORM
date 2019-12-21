# 路由
import tornado.web
import config
from views import index
import os
from database.MySQL import MySQL


class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.db = MySQL(config.mysql["host"], config.mysql["user"], config.mysql["passwd"], config.mysql["dbName"],
                        config.mysql["port"])
