#!/usr/bin/env python
# encoding: utf-8

import tornado.ioloop
import tornado.web
import tornado.log
import tornado.httpserver
from tornado.options import define, options
import logging
import tornado.gen
import tornado.process
import os
import os.path
import magic
import mimetypes

define('debug', type=bool, default=True, help="enable debug, default False")
define('host', type=str, default="127.0.0.1", help="http listen host, default 127.0.0.1")
define('port', type=int, default=8080, help="http listen port, default 8080")
define('storage_path', type=str, default="storage", help="file storage path")
options.parse_command_line()

logger = logging.getLogger('fileserver')

project_dir_path = os.path.abspath(os.path.dirname(__file__))

if not os.path.exists(options.storage_path):
    os.mkdir(options.storage_path)


class LinuxUtils(object):

    @staticmethod
    @tornado.gen.coroutine
    def mv(src, dest):
        cmd = ["mv", src, dest]
        proc = tornado.process.Subprocess(cmd)
        ret = yield proc.wait_for_exit(raise_error=False)
        raise tornado.gen.Return(ret == 0)

    @staticmethod
    @tornado.gen.coroutine
    def rm(file):
        cmd = ["rm", file]
        proc = tornado.process.Subprocess(cmd)
        ret = yield proc.wait_for_exit(raise_error=False)
        raise tornado.gen.Return(ret == 0)



class UploadHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        keys = self.request.arguments.keys()
        print keys
        if "file.path" not in keys:
            self.set_status(status_code=400, reason="file field not exist.")
            self.write("400")
            return
        #if filter(lambda x: not x.startswith("file."), keys):
        #    self.set_status(status_code=402, reason="only allow file field upload")
        #    self.write("402")
        #    return
        files = list()
        file_path = self.request.arguments['file.path']
        for index in xrange(len(file_path)):
            file = {}
            file['name'] = self.request.arguments['file.name'][index]
            print file['name']
            file['content_type'] = self.request.arguments['file.content_type'][index]
            file['path'] = self.request.arguments['file.path'][index]
            file['md5'] = self.request.arguments['file.md5'][index]
            file['size'] = self.request.arguments['file.size'][index]
            files.append(file)
            print file
        # mv tmp file to save store storage
        for file in files:
            # debug
            src_file = file['path']
            mime = magic.from_file(src_file, mime=True)
            mimetypes.init()
            ext = mimetypes.guess_extension(mime, False)
            print ext
            dest_file = os.path.join(
                options.storage_path,
                file['md5'] + ext
            )
            if not os.path.exists(dest_file):
                yield LinuxUtils.mv(
                    src_file,
                    dest_file
                )
            else:
                yield LinuxUtils.rm(
                    src_file
                )
            file['path'] = file['md5'] + ext
        self.write({"data": files})

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/upload', UploadHandler),
        ]

        settings = dict()
        settings['debug'] = True
        super(Application, self).__init__(handlers, **settings)

if __name__ == '__main__':
    application = Application()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(
        options.port,
        address=options.host
    )
    logger.info("http server listen on %s:%d", options.host, options.port)
    tornado.ioloop.IOLoop.current().start()
