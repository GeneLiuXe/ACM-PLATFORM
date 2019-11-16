import os

from views import index
from tornado.web import StaticFileHandler

urls = [
    (r'/register', index.RegisterHandler),
    (r'/login', index.LoginHandler),
    (r'/logout', index.LogoutHandler),
    (r'/HomePage', index.HomePageHandler),
    (r'/Problem(.*)', index.ProblemHandler),
    (r'/Algorithm(.*)', index.AlgorithmHandler),
    (r'/Contest(.*)', index.ContestHandler),
    (r'/AddContest(.*)', index.AddContestHandler),
    (r'/AddConError(.*)', index.AddConErrorHandler),
    (r'/ConInformation(.*)', index.ConInformationHandler),
    (r'/TeamInformation(.*)', index.TeamInformationHandler),
    (r'/User(.*)', index.UserHandler),
    (r'/PerInformation(.*)', index.PerInformationHandler),
    (r'/ChangeSerect(.*)', index.ChangeSerectHandler),
    (r'/(.*)', index.IndexHandler),
    # 静态文件路径配置
    # (r"/(.*)", StaticFileHandler,
    #     {"path": os.path.join(os.path.dirname(__file__), "static"),
    #     "default_filename": "html/index.html"
    # }),
]