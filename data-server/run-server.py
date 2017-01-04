#!/usr/bin/env python

import sys
import os
import signal

from tornado.options import parse_command_line
from tornado.ioloop import IOLoop
import tornado.httpserver
import tornado.web
import tornado.wsgi

from django.core.wsgi import get_wsgi_application

from push_app.notif_server_handler import NotifServerHandler


# Basic configuration
LISTEN_PORT = 8080

class NotifServerListHandler(tornado.web.RequestHandler):
    def get(self):
        pass


# Main loop

def main():
    parse_command_line()

    # Init and get DJANGO application
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_app.settings'
    sys.path.append( os.path.dirname(os.path.realpath(__file__)) + '/django_app')

    django_wsgi_app = get_wsgi_application()
    wsgi_django_container = tornado.wsgi.WSGIContainer(django_wsgi_app)

    # Create TORNADO application, and server
    tornado_app = tornado.web.Application(
        [
            ('/notif-server', NotifServerListHandler),
            ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_django_container)),
        ])
        
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(LISTEN_PORT)
    
    # Create the NOTIF SERVER handler
    NotifServerHandler.instance()

    # Run the whole loop
    signal.signal(signal.SIGINT, lambda x, y: IOLoop.current().stop())
    IOLoop.current().add_callback(lambda: print("Server started on port " + str(LISTEN_PORT)))
    IOLoop.current().start()

if __name__ == '__main__':
    main()