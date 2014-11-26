import ply.lex as lex

tokens = (
  'LPAREN', # ( 
  'RPAREN',  # )
  'COMMA',  # ,
  'DOT',  # .
  'IF',  # The symbol :-
  'WORD', # A string of digits and chars
  'VAR', # A question mark followed by a WORD
  'CONSTANT', # A WORD that is not a VAR
)

def Lexer():
    """
    Use it as follows
    lexer = Lexer()
    lexer.input("something)
    tok = lexer.token()

    Those tokens have a type and value (tok.type and tok.value).
    """
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_COMMA  = r'\,'
    t_DOT  = r'\.'
    t_IF  = r'\:\-'
    t_WORD = r'[\w]+'
    t_VAR = r'\?[\w]+'

    t_ignore  = ' \t\n'

    return lex.lex()
