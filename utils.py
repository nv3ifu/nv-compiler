import sys


class Colors:
    WHITE = '\033[0m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'


def lexing_error(message, lineno):
    print(f'{Colors.RED}[Line {lineno}]: {message}{Colors.WHITE}')
    sys.exit(1)


def parse_error(message, lineno):
    print(f'{Colors.RED}[Line {lineno}]: {message}{Colors.WHITE}')
    sys.exit(1)

def runtime_error(message, lineno):
    print(f'{Colors.RED}[Line {lineno}]: {message}{Colors.WHITE}')
    sys.exit(1)


def print_pretty_ast(ast_text):
    i = 0
    newline = False
    for ch in str(ast_text):
        if ch == '(':
            if not newline:
                print(end='')
            print(ch)
            i += 2
            newline = True
        elif ch == ')':
            if not newline:
                print()
            i -= 2
            newline = True
            print(' ' * i + ch)
        else:
            if newline:
                print(' ' * i, end='')
            print(ch, end='')
            newline = False


def print_tree(node, prefix="", is_last=True, label=""):
    from model import Integer, Float, String, Bool, Grouping, UnOp, BinOp
    
    connector = "└── " if is_last else "├── "
    label_str = f"{label}: " if label else ""
    
    if isinstance(node, Integer):
        print(f"{prefix}{connector}{label_str}Integer({node.value})")
    elif isinstance(node, Float):
        print(f"{prefix}{connector}{label_str}Float({node.value})")
    elif isinstance(node, String):
        print(f"{prefix}{connector}{label_str}String({node.value!r})")
    elif isinstance(node, Bool):
        print(f"{prefix}{connector}{label_str}Bool({node.value})")
    elif isinstance(node, Grouping):
        print(f"{prefix}{connector}{label_str}Grouping")
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(node.value, new_prefix, True)
    elif isinstance(node, UnOp):
        print(f"{prefix}{connector}{label_str}UnOp({node.op.lexeme!r})")
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(node.operand, new_prefix, True)
    elif isinstance(node, BinOp):
        print(f"{prefix}{connector}{label_str}BinOp({node.op.lexeme!r})")
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(node.left, new_prefix, False, "left")
        print_tree(node.right, new_prefix, True, "right")
    else:
        print(f"{prefix}{connector}{label_str}{node}")


def generate_ast_image(node, filename="ast"):
    try:
        from graphviz import Digraph
        from model import Integer, Float, String, Bool, Grouping, UnOp, BinOp
    except ImportError:
        print("plz install graphviz: pip install graphviz")
        return
    
    dot = Digraph(comment='AST')
    dot.attr(rankdir='TB', fontname='Consolas')
    dot.attr('node', fontname='Consolas')
    
    def add_node(n, parent_id=None, edge_label=""):
        node_id = str(id(n))
        
        if isinstance(n, Integer):
            dot.node(node_id, f"Integer\n{n.value}", shape="ellipse", style="filled", fillcolor="lightblue")
        elif isinstance(n, Float):
            dot.node(node_id, f"Float\n{n.value}", shape="ellipse", style="filled", fillcolor="lightblue")
        elif isinstance(n, String):
            dot.node(node_id, f"String\n{n.value!r}", shape="ellipse", style="filled", fillcolor="lightyellow")
        elif isinstance(n, Bool):
            dot.node(node_id, f"Bool\n{n.value}", shape="ellipse", style="filled", fillcolor="lightgreen")
        elif isinstance(n, Grouping):
            dot.node(node_id, "()", shape="box", style="filled", fillcolor="lightgray")
            add_node(n.value, node_id)
        elif isinstance(n, UnOp):
            dot.node(node_id, f"UnOp\n{n.op.lexeme!r}", shape="circle", style="filled", fillcolor="lightsalmon")
            add_node(n.operand, node_id)
        elif isinstance(n, BinOp):
            dot.node(node_id, f"BinOp\n{n.op.lexeme!r}", shape="circle", style="filled", fillcolor="lightsalmon")
            add_node(n.left, node_id, "L")
            add_node(n.right, node_id, "R")
        
        if parent_id:
            dot.edge(parent_id, node_id, label=edge_label)
    
    add_node(node)
    dot.render(filename, format="png", cleanup=True)
    print(f"AST img generated: {filename}.png")
