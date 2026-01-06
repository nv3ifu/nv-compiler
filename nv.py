from interpreter import *
from lexer import *
from parser import *
from utils import *
from vm import *
from compiler import *
from optimizer import *

if __name__ == "__main__":
    optimize = False
    args = sys.argv[1:]
    
    if '-O' in args:
        optimize = True
        args.remove('-O')
    
    if len(args) != 1:
        raise SystemExit("Usage: python nv.py [-O] <filename>")
    
    filename = args[0]
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
        
        if optimize:
            optimizer = ASTOptimizer()
            ast = optimizer.optimize(ast)
        
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
        print_code(code)
        print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
        print(f'{Colors.GREEN}VM:{Colors.WHITE}')
        print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
        vm = VM()
        vm.run(code)
