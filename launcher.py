import substitutor, server

server.SubstitutionServer(("localhost",808), substitutor.Substitutor3000(), server.SubstitutionHandler).run()



