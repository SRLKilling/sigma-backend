from tornado.options import parse_command_line
from tornado.ioloop import IOLoop

import tornado.httpserver
import tornado.web
import tornado.wsgi

import signal

from api_handler_server import APIHandlerServer
from websocket_client import WebSocketClient

LISTEN_PORT = 8081
HTTP_PORT = 8888

TRUSTED_EMITTERS = [
    "127.0.0.1"
]

if __name__ == "__main__":
    parse_command_line()
    
    # The server handling connections from Django backends
    server = APIHandlerServer()
    server.listen(LISTEN_PORT)
    
    
    # The HTTP server handling clients websockets
    web_application = tornado.web.Application([
        (r'/ws', WebSocketClient),
    ])
 
    http_server = tornado.httpserver.HTTPServer(web_application)
    http_server.listen(HTTP_PORT)
    
    signal.signal(signal.SIGINT, lambda x, y: IOLoop.current().stop())
    IOLoop.current().start()