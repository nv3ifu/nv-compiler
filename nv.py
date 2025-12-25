import sys

from parser import *
from utils import *

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python nv.py <filename>")
    filename = sys.argv[1]
    print(filename)
    with open(filename) as f:
        source = f.read()
        print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
        print(f'{Colors.GREEN}SOURCE:{Colors.WHITE}')
        print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
        print(source)

        print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
        print(f'{Colors.GREEN}TOKENS:{Colors.WHITE}')
        print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
        tokens = Lexer(source).tokenize()
        for tok in tokens: print(tok)

        print()
        print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
        print(f'{Colors.GREEN}AST:{Colors.WHITE}')
        print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
        ast = Parser(tokens).parse()
        print_pretty_ast(ast)
