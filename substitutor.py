import re

class Substitutor3000():
    def __init__(self):
        self.subst_pairs = dict()
        self.pat = re.compile(r"\$\{(.+?)\}")

    def put(self, key, value):
        self.subst_pairs[key] = value

    def process_query(self, query):
        res = ""
        current_position = 0
        for m in re.finditer(self.pat, query):
            res += query[current_position:m.start()] + self.get(m.group(1))
            current_position = m.end()
        return res + query[current_position:]

    def get(self, key):
        if self.subst_pairs.has_key(key):
            return self.process_query(self.subst_pairs[key])
        return ""