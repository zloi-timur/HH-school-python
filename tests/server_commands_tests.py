import unittest
from server_service import CommandsParser

class Test(unittest.TestCase):
    def setUp(self):
        pass

    def testNoTypeMatches(self):
        parser = CommandsParser()
        parser.put_command(("good",r"GOOD ([\d]+)"))
        self.assertEqual(None, parser.parse("BAD xxx"))

    def testBadParameters(self):
        parser = CommandsParser()
        parser.put_command(("good",r"GOOD ([\d]+)"))
        self.assertEqual(None, parser.parse("GOOD xxx"))


    def testCorrectType(self):
        parser = CommandsParser()
        parser.put_command(("good",r"GOOD ([\d]+)"))
        self.assertEqual("good", parser.parse("GOOD 111")[0])

    def testCorrectParameters(self):
        parser = CommandsParser()
        parser.put_command(("good",r"GOOD ([\d]+)"))
        self.assertEqual("111", parser.parse("GOOD 111")[1][0])

if __name__ == "__main__":
    unittest.main()


