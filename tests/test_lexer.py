import unittest
from eunomia.lexer import Lexer

class TestLexer(unittest.TestCase):
    
    def setUp(self):
        self.lexer = Lexer()

    def test_input_constant(self):
        self.lexer.input("a")
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'WORD')
        self.assertEqual(tok.value, "a")

    def test_input_var(self):
        self.lexer.input("?somevar")
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'VAR')
        self.assertEqual(tok.value, "?somevar")

    def test_input_if(self):
        self.lexer.input(":-")
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'IF')
        self.assertEqual(tok.value, ":-")

    def test_input_if_var(self):
        self.lexer.input(":- ?xa")
        tok1 = self.lexer.token()
        tok2 = self.lexer.token()
        self.assertEqual(tok1.type, 'IF')
        self.assertEqual(tok1.value, ":-")
        self.assertEqual(tok2.type, 'VAR')
        self.assertEqual(tok2.value, "?xa")

    def test_input_word_comma_var(self):
        self.lexer.input("a ,?xa")
        tok1 = self.lexer.token()
        tok2 = self.lexer.token()
        tok3 = self.lexer.token()
        self.assertEqual(tok1.type, 'WORD')
        self.assertEqual(tok1.value, "a")
        self.assertEqual(tok2.type, 'COMMA')
        self.assertEqual(tok2.value, ",")
        self.assertEqual(tok3.type, 'VAR')
        self.assertEqual(tok3.value, "?xa")

