# -*- coding: utf-8 -*-
"""

@Author: lushaoxiao
@Date: 2019/5/5
@IDE: PyCharm
"""
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os
import datetime

from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler

define("PORT", default=2222, type=int)


class IndexHandler(RequestHandler):
    def get(self):
        self.render("index.html")


class MainHandler(WebSocketHandler):
    users = set()  # 用来存放在线用户的容器

    def open(self):
        self.users.add(self)  # 建立连接后添加用户到容器中
        for u in self.users:  # 向已在线用户发送消息
            u.write_message(
                u"[%s]-[%s]-进入" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def on_message(self, message):
        print(message)
        # from methodTest import Method
        # m = Method()
        # data = m.getPos()
        # self.write_message(data)

    def on_close(self):
        self.users.remove(self)  # 用户关闭连接后从容器中移除用户
        for u in self.users:
            u.write_message(
                u"[%s]-[%s]-离开聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求


if __name__ == '__main__':
    tornado.options.parse_command_line()
    # 设置静态文件的路径为当前路径加statis（只能设置为static）
    # static_path 注意此处只能使用static，不知道为啥，可能是 __init__.py 定义吧。部署可以使用cdn
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/tetris", MainHandler),
    ],
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), ""),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.PORT)
    tornado.ioloop.IOLoop.current().start()
