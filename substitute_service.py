import SocketServer
import re
import threading
import time

class Substitutor3000(object):
    def __init__(self):
        self.subst_pairs = dict()
        self.pattern = re.compile(r"\$\{(.+?)\}")

    def put(self, key, value):
        self.subst_pairs[key] = value

    def process_query(self, query):
        res = ""
        current_position = 0
        for m in re.finditer(self.pattern, query):
            res += query[current_position:m.start()] + self.get(m.group(1))
            current_position = m.end()
        return res + query[current_position:]

    def get(self, key):
        if self.subst_pairs.has_key(key):
            return self.process_query(self.subst_pairs[key])
        return ""


class SubstitutionHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        query = self.rfile.readline()
        for command, function in self.server.command_binder:
            if re.match(command, query):
                function(self, *re.match(command, query).groups())

    def set_sleep_time(self, time):
        if int(time) < 0:
            return
        self.wfile.write("OK\n")
        with self.server.time_lock:
            self.server.sleep_time = int(time) / 1000.0

    def put(self, key, value):
        with self.server.subst_lock:
            self.server.substitutor.put(key, value)
        self.wfile.write("OK\n")

    def get(self, key):
        with self.server.subst_lock:
            value = self.server.substitutor.get(key)
        time.sleep(self.server.sleep_time)
        self.wfile.write("VALUE\n" + value + "\n")


class SubstitutionServer(SocketServer.ThreadingTCPServer):
    def __init__(self, address, handler):
        SocketServer.ThreadingTCPServer.__init__(self, address, handler)
        self.substitutor = Substitutor3000()
        self.sleep_time = 0
        self.time_lock = threading.RLock()
        self.subst_lock = threading.RLock()
        self.command_binder = ((re.compile(r"GET ([\S]+)"), SubstitutionHandler.get),
                                (re.compile(r"PUT ([\S]+) ([ \S]+)"), SubstitutionHandler.put),
                                (re.compile(r"SET SLEEP ([\d]+)"), SubstitutionHandler.set_sleep_time))
