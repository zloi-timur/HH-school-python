from substitute_service import SubstitutionHandler, SubstitutionServer

SubstitutionServer(("localhost",808), SubstitutionHandler).serve_forever()



