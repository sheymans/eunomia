import ply.yacc as yacc

# We need the tokens from the lexer (required)
import lexer 

from models import Term, Atom, Rule, Program


# Logging to file

import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)


class Parser():
    """
    Parser for Programs
    """
    def __init__(self, start=False):
        """
        start is the start symbol of the grammar, by default it is just the
        top level goal.
        """
        self.tokens = lexer.tokens # this is required
        self.log = logging.getLogger()
        if start:
            # We'll not write tables when we specified a start symbol, this
            # means we are jumping in places in the grammar to test out
            # different subgrammars. And we do not want these tables to
            # persist.
            self.parser = yacc.yacc(module=self, start=start, debug=0, write_tables=0, errorlog=self.log)
        else:
            self.parser = yacc.yacc(module=self)

    def parse(self, input):
        # input is the program input (a string)
        lex = lexer.Lexer()
        # This returns a eunomia.models.Program
        return self.parser.parse(input, lex)

    def p_atom(self, p):
        """
        atom : term LPAREN terms RPAREN
        """
        p[0] = Atom(p[1], p[3])

    def p_terms(self, p):
        """
        terms : terms COMMA term
              | term
              |
        """
        if len(p) == 1:
            # then empty args (3rd case)
            p[0] = []
        elif len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]
            p[0].append(p[3])

    def p_term_var(self, p):
        """
        term : VAR
        """
        p[0] = Term(p[1], True)

    def p_term_const(self, p):
        """
        term : WORD
        """
        p[0] = Term(p[1])

    def p_error(self, p):
        raise SyntaxError('Syntax error in input: %s' % p)

