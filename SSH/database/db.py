import tornado.web
from MySQL import MySQL

class database(tornado.web.RequestHandler):
    def save(self):
        sql = ""
        self.application.db.insert(sql)

    def delete(self):
        pass

    def update(self):
        pass

    def all(self):
        pass

    def select(self):
        pass
