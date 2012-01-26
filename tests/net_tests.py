import socket
import unittest
import substitute_service

class Test(unittest.TestCase):
    def setUp(self):
        self.server = substitute_service.SubstitutionServer(("localhost",800), substitute_service.SubstitutionHandler)
        self.server_address = self.server.server_address
        self.server.serve_forever()

    def testPutResponseOK(self):
        client = socket.create_connection(self.server_address)
        client.send("PUT x y")
        answer = client.recv(1024)
        client.close()
        self.assertEqual("OK\n", answer)

    def testPutResponseError(self):
        client = socket.create_connection(self.server_address)
        client.send("PUT x")
        answer = client.recv(1024)
        client.close()
        self.assertEqual("NOT CORRECT COMMAND\n", answer)

    def testGet(self):
        client = socket.create_connection(self.server_address)
        client.send("GET x")
        answer = client.recv(1024)
        client.close()
        self.assertEqual("VALUE\ny\n", answer)


    def testReplacement(self):
        client = socket.create_connection(self.server_address)
        client.send("PUT k1 one")
        client.close()
        client.send("PUT k2 two")
        client.close()
        client.send("PUT keys ${k1} 2: ${k2}")
        client.close()
        client.send("GET keys")
        ans = client.recv(1024)
        client.close()
        self.assertEqual("1: one, 2: two", ans)

if __name__ == "__main__":
    unittest.main()