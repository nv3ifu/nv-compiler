from interpreter import *
from lexer import *
from parser import *
from utils import *
from vm import *
from compiler import *

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python nv.py <filename>")
    filename = sys.argv[1]
    print(filename)
    with open(filename, encoding='utf-8') as f:
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
        print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
        print(f'{Colors.GREEN}AST:{Colors.WHITE}')
        print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
        ast = Parser(tokens).parse()
        print_tree(ast)
        generate_ast_image(ast, "ast")
        print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
        print(f'{Colors.GREEN}INTERPRETER:{Colors.WHITE}')
        print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
        interpreter = Interpreter()
        interpreter.interpret_ast(ast)
        print(f'{Colors.GREEN}\n***************************************{Colors.WHITE}')
        print(f'{Colors.GREEN}COMPILER:{Colors.WHITE}')
        print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
        compiler = Compiler()
        code = compiler.compile_code(ast)
        print(code)
        #vm = VM()
        #vm.run(code)

