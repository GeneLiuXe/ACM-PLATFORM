# 服务器
import tornado.web
import tornado.ioloop
import tornado.httpserver
import config
from urls import urls
from application import Application
from views import index

if __name__ == "__main__":
    app = Application(
        urls,
        **config.settings
    )
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.bind(config.options["port"])
    httpServer.start(1)
    tornado.ioloop.IOLoop.current().start()