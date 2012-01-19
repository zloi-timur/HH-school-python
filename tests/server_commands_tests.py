import unittest
from server import CommandsParser

class Test(unittest.TestCase):
    def setUp(self):
        pass

    def testSimpleBad1(self):
        parser = CommandsParser()
        parser.put_command(("good",r"GOOD ([\d]+)"))
        self.assertEqual(None, parser.parse("BAD xxx"))

    def testSimpleBad2(self):
        parser = CommandsParser()
        parser.put_command(("good",r"GOOD ([\d]+)"))
        self.assertEqual(None, parser.parse("GOOD xxx"))

    def testSimpleBad3(self):
        parser = CommandsParser()
        parser.put_command(("good",r"GOOD ([\d]+)"))
        self.assertEqual(None, parser.parse("GOOD"))

    def testSimpleGood1(self):
        parser = CommandsParser()
        parser.put_command(("good",r"GOOD ([\d]+)"))
        self.assertEqual("good", parser.parse("GOOD 111")[0])

    def testSimpleGood2(self):
        parser = CommandsParser()
        parser.put_command(("good",r"GOOD ([\d]+)"))
        self.assertEqual("111", parser.parse("GOOD 111")[1][0])

if __name__ == "__main__":
    unittest.main()


