from tornado.web import RequestHandler


class MainHandler(RequestHandler):
    def get(self):
        self.write('Hello, world')


class PackageHandler(RequestHandler):

    def get(self, package_name):
        # TODO: query the database here
        self.write('blah')
