import SocketServer
import substitute_service, server_service

parser = server_service.CommandsParser()


SocketServer.ThreadingTCPServer(("localhost",808), substitute_service.SubstitutionHandler).serve_forever()



