import SocketServer
import re
import threading
import time
import server_service

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

class SubstitutionResources(object):
    def __init__(self):
        self.substitutor = Substitutor3000()
        self.sleep_time = 0
        self.time_lock = threading.RLock()
        self.subst_lock = threading.RLock()
        self.parser = server_service.CommandsParser()
        self.parser.put_command(("get",r"GET ([\S]+)"))
        self.parser.put_command(("put",r"PUT ([\S]+) ([ \S]+)"))
        self.parser.put_command(("set sleep",r"SET SLEEP ([\d]+)"))


class SubstitutionHandler(SocketServer.StreamRequestHandler):
    resources = SubstitutionResources()
    def handle(self):
        query = SubstitutionHandler.resources.parser.parse(self.rfile.readline())
        if query is None:
            self.wfile.write("BAD REQUEST FORMAT\n")
            return
        if query[0] == "get":
            time.sleep(SubstitutionHandler.resources.sleep_time)
            self.wfile.write("VALUE\n"+self.get(query[1][0])+"\n")
            return
        if query[0] == "put":
            self.wfile.write("OK\n")
            self.put(query[1][0],query[1][1])
            return
        if query[0] == "set sleep":
            self.wfile.write("OK\n")
            self.set_sleep_time(query[1][0])
            return
        self.wfile.write("BAD REQUEST FORMAT\n")

    def set_sleep_time(self, time):
        if time < 0:
            return
        with SubstitutionHandler.resources.time_lock:
            SubstitutionHandler.resources.sleep_time = int(time) / 1000.0

    def put(self, key, value):
        with SubstitutionHandler.resources.subst_lock:
            SubstitutionHandler.resources.substitutor.put(key, value)

    def get(self, key):
        with SubstitutionHandler.resources.subst_lock:
            return SubstitutionHandler.resources.substitutor.get(key)


