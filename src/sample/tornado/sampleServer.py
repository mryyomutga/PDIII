import os

import tornado.ioloop
import tornado.web

BASE_DIR = os.path.dirname(__file__)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument("name", "Taro")
        members = ["xxxx", "yyyy", "zzzz"]
        self.render("index.html", title = "Takago.Lab", name = name, members = members)

application = tornado.web.Application([
    (r"/", MainHandler),
    ],
    template_path = os.path.join(BASE_DIR, "templates"),
    static_path = os.path.join(BASE_DIR, "static"),
)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
