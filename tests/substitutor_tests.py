import unittest
import substitute_service

class Test(unittest.TestCase):
    def setUp(self):
        pass

    def testReplacement(self):
        sbst = substitute_service.Substitutor3000()
        sbst.put("k1", "one")
        sbst.put("k2", "two")
        sbst.put("keys", "1: ${k1}, 2: ${k2}")
        self.assertEqual("1: one, 2: two", sbst.get("keys"))

    def testEmptyReplacement(self):
        sbst = substitute_service.Substitutor3000()
        sbst.put("k", "bla-${inexistent}-bla")
        self.assertEqual("bla--bla", sbst.get("k"))

    def testEmptyGet(self):
        sbst = substitute_service.Substitutor3000()
        self.assertEqual("", sbst.get("k"))

if __name__ == "__main__":
    unittest.main()