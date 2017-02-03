from tornado.options import parse_command_line
from tornado.ioloop import IOLoop
import tornado.httpserver
import tornado.web
import tornado.wsgi

import django_importer
import settings

from websocket.client import WebSocketClient
from sigma_api.notifier import notifier


if __name__ == "__main__":
    parse_command_line()
    
    # The HTTP server handling clients websockets
    web_application = tornado.web.Application([
        (r'/ws', WebSocketClient),
    ])
    
    port = getattr(settings, "WEBSOCKET", []).get("PORT", 80)
    http_server = tornado.httpserver.HTTPServer(web_application)
    http_server.listen(port)
    
    # Add the local dispatcher to the notification callbak
    # (The central dispatch server will not send us back the notif we send)
    notifier.add_publish_callback(WebSocketClient.publish)
    notifier.subscribe("notification", WebSocketClient.publish)
    
    
    IOLoop.current().add_callback(lambda: print("WebSocket server started on port", port))
    IOLoop.current().start()