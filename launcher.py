import SocketServer
from substitute_service import SubstitutionHandler

SocketServer.ThreadingTCPServer(("localhost",808), SubstitutionHandler).serve_forever()



