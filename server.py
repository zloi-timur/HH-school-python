import SocketServer
import threading
import time
import re

class CommandsParser():
    def __init__(self):
        self.commands = dict()

    def put_command(self, command):
        self.commands[command[0]] = re.compile(command[1])

    def parse(self, inp_command):
        for com in self.commands.keys():
            if re.match(self.commands[com], inp_command):
                return (com, re.match(self.commands[com], inp_command).groups())
        return None

class SubstitutionHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        query = self.server.get_parser().parse(self.rfile.readline())
        if query is None:
            self.wfile.write("BAD REQUEST FORMAT\n")
            return
        if query[0] == "get":
            time.sleep(self.server.get_sleep_time())
            self.wfile.write("VALUE\n"+self.server.get(query[1][0])+"\n")
            return
        if query[0] == "put":
            self.wfile.write("OK\n")
            self.server.put(query[1][0],query[1][1])
            return
        if query[0] == "set sleep":
            self.wfile.write("OK\n")
            self.server.set_sleep_time(query[1][0])
            return

        self.wfile.write("BAD REQUEST FORMAT\n")


class SubstitutionServer(SocketServer.TCPServer):
    def __init__(self, adr, subst, handler_class, sleep = 0):
        SocketServer.TCPServer.__init__(self, adr, handler_class)
        self.command_parser = CommandsParser()
        self.substitutor = subst
        self.sleep_time = sleep
        self.time_lock = threading.RLock()
        self.subst_lock = threading.RLock()
        self.command_parser.put_command(("get",r"GET ([\S]+)"))
        self.command_parser.put_command(("put",r"PUT ([\S]+) ([ \S]+)"))
        self.command_parser.put_command(("set sleep",r"SET SLEEP ([\d]+)"))

    def set_sleep_time(self, time):
        if time < 0:
            return
        with self.time_lock:
            self.sleep_time = int(time) / 1000.0

    def put(self, key, value):
        with self.subst_lock:
            self.substitutor.put(key, value)

    def get(self, key):
        with self.subst_lock:
            return self.substitutor.get(key)

    def get_sleep_time(self):
        with self.time_lock:
            return self.sleep_time

    def get_parser(self):
        with self.subst_lock:
            return self.command_parser

    def run(self):
        self.serve_forever()
