from push_app.notif_server_client import NotifServerClient
import settings

class NotifServerHandler:
    
    __instance = None
    
    @staticmethod
    def instance():
        if NotifServerHandler.__instance == None:
            NotifServerHandler.__instance = NotifServerHandler()
        return NotifServerHandler.__instance
    
    
    
    def __init__(self):
        self.notif_servers = []
        
        for a in settings.NOTIF_SERVERS_ADDR:
            client = NotifServerClient(self, a[0], a[1])
            self.notif_servers.append(client)
            
            
    def put(self, msg):
        for s in self.notif_servers:
            s.queue.put_nowait(msg)