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
    substitutor = Substitutor3000()
    sleep_time = 0
    time_lock = threading.RLock()
    subst_lock = threading.RLock()

    def handle(self):
        query = self.rfile.readline()
        for command, function in SubstitutionHandler.command_binder:
            if re.match(command, query):
                function(self, *re.match(command, query).groups())

    def set_sleep_time(self, time):
        if int(time) < 0:
            return
        self.wfile.write("OK\n")
        with SubstitutionHandler.time_lock:
            SubstitutionHandler.sleep_time = int(time) / 1000.0

    def put(self, key, value):
        with SubstitutionHandler.subst_lock:
            SubstitutionHandler.substitutor.put(key, value)
        self.wfile.write("OK\n")

    def get(self, key):
        with SubstitutionHandler.subst_lock:
            value = SubstitutionHandler.substitutor.get(key)
        time.sleep(SubstitutionHandler.sleep_time)
        self.wfile.write("VALUE\n" + value + "\n")

    command_binder = ((re.compile(r"GET ([\S]+)"), get),
                      (re.compile(r"PUT ([\S]+) ([ \S]+)"), put),
                      (re.compile(r"SET SLEEP ([\d]+)"),set_sleep_time))

