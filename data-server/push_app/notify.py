from push_app.notif_server_handler import NotifServerHandler

def notify(msg):
    NotifServerHandler.instance().put(msg)