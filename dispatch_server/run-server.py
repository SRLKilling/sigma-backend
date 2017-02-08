from tornado.options import parse_command_line
from tornado.ioloop import IOLoop

from client_handler import ClientHandler
LISTEN_PORT = 1316

if __name__ == "__main__":
    parse_command_line()
    
    # The server handling connections from Django backends
    server = ClientHandler()
    server.listen(LISTEN_PORT)
    
    IOLoop.current().add_callback(lambda: print("Dispatching server started on port", LISTEN_PORT))
    IOLoop.current().start()