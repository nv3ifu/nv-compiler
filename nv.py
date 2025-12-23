from tokens import *
from lexer import *
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python nv.py <filename>")
    filename = sys.argv[1]
    print(filename)
    with open(filename) as f:
        source = f.read()
        print("Lexer:")
        tokens = Lexer(source).tokenize()
        for token in tokens:
            print(token)