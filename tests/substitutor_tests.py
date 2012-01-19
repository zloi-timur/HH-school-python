import unittest
import substitutor

class Test(unittest.TestCase):
    def setUp(self):
        pass

    def testReplacement(self):
        sbst = substitutor.Substitutor3000()
        sbst.put("k1", "one")
        sbst.put("k2", "two")
        sbst.put("keys", "1: ${k1}, 2: ${k2}")
        self.assertEqual("1: one, 2: two", sbst.get("keys"))

    def testEmptyReplacement(self):
        sbst = substitutor.Substitutor3000()
        sbst.put("k", "bla-${inexistent}-bla")
        self.assertEqual("bla--bla", sbst.get("k"))

    def testEmptyGet(self):
        sbst = substitutor.Substitutor3000()
        self.assertEqual("", sbst.get("k"))

    def testComplex1(self):
        sbst = substitutor.Substitutor3000()
        sbst.put("k1","v1")
        sbst.put("k2","v2")
        sbst.put("k3","a${k1}b${k2}c")
        self.assertEqual("av1bv2c", sbst.get("k3"))

    def testComplex2(self):
        sbst = substitutor.Substitutor3000()
        sbst.put("k1","v1")
        sbst.put("k3","a${k1}b${k2}c")
        self.assertEqual("av1bc", sbst.get("k3"))

    def testComplex3(self):
        sbst = substitutor.Substitutor3000()
        sbst.put("k1","v1")
        sbst.put("k3","a${k1}b${k2}c")
        sbst.put("k1","v3")
        self.assertEqual("av3bc", sbst.get("k3"))

if __name__ == "__main__":
    unittest.main()