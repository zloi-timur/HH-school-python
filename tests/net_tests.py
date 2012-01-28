import socket
import threading
import unittest
import substitute_service

class Test(unittest.TestCase):
    def setUp(self):
        self.server = substitute_service.SubstitutionServer(("localhost", 0), substitute_service.SubstitutionHandler)
        self.server_address = self.server.server_address
        thread = threading.Thread(target = self.server.serve_forever)
        thread.start()

    def testPutResponseOK(self):
        client = socket.create_connection(self.server_address)
        client.send("PUT x y\n")
        answer = client.recv(1024)
        client.close()
        self.assertEqual("OK\n", answer)

    def testPutResponseError(self):
        client = socket.create_connection(self.server_address)
        client.send("PUT x\n")
        answer = client.recv(1024)
        client.close()
        self.assertEqual("NOT CORRECT COMMAND\n", answer)

    def testGet(self):
        client = socket.create_connection(self.server_address)
        client.send("PUT x y\n")
        client.close()
        client = socket.create_connection(self.server_address)
        client.send("GET x\n")
        answer = client.recv(1024)
        client.close()
        self.assertEqual("VALUE\ny\n", answer)


    def testReplacement(self):
        client = socket.create_connection(self.server_address)
        client.send("PUT k1 one\n")
        client.close()
        client = socket.create_connection(self.server_address)
        client.send("PUT k2 two\n")
        client.close()
        client = socket.create_connection(self.server_address)
        client.send("PUT keys 1: ${k1} 2: ${k2}\n")
        client.close()
        client = socket.create_connection(self.server_address)
        client.send("GET keys\n")
        ans = client.recv(1024)
        client.close()
        self.assertEqual("VALUE\n1: one 2: two\n", ans)

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

if __name__ == "__main__":
    unittest.main()