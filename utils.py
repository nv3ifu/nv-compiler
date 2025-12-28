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
    from model import Integer, Float, String, Bool, Grouping, UnOp, BinOp, Identifier, Assignment, LogicalOp, Stmts, PrintStmt, IfStmt, WhileStmt

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
    elif isinstance(node, Identifier):
        print(f"{prefix}{connector}{label_str}Identifier({node.name})")
    elif isinstance(node, Assignment):
        print(f"{prefix}{connector}{label_str}Assignment")
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(node.left, new_prefix, False, "left")
        print_tree(node.right, new_prefix, True, "right")
    elif isinstance(node, Grouping):
        print(f"{prefix}{connector}{label_str}Grouping")
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(node.value, new_prefix, True)
    elif isinstance(node, UnOp):
        print(f"{prefix}{connector}{label_str}UnOp({node.op.lexeme!r})")
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(node.operand, new_prefix, True)
    elif isinstance(node, LogicalOp):
        print(f"{prefix}{connector}{label_str}LogicalOp({node.op.lexeme!r})")
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(node.left, new_prefix, False, "left")
        print_tree(node.right, new_prefix, True, "right")
    elif isinstance(node, BinOp):
        print(f"{prefix}{connector}{label_str}BinOp({node.op.lexeme!r})")
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(node.left, new_prefix, False, "left")
        print_tree(node.right, new_prefix, True, "right")
    elif isinstance(node, IfStmt):
        print(f"{prefix}{connector}{label_str}IfStmt")
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(node.test, new_prefix, False, "test")
        print_tree(node.then_stmts, new_prefix, False, "then")
        print_tree(node.else_stmts, new_prefix, True, "else")
    elif isinstance(node, WhileStmt):
        print(f"{prefix}{connector}{label_str}WhileStmt")
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(node.test, new_prefix, False, "test")
        print_tree(node.body_stmts, new_prefix, True, "body")
    elif isinstance(node, Stmts):
        print(f"{prefix}{connector}{label_str}Stmts")
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, stmt in enumerate(node.stmts):
            is_last_stmt = (i == len(node.stmts) - 1)
            print_tree(stmt, new_prefix, is_last_stmt, f"[{i}]")
    elif isinstance(node, PrintStmt):
        print(f"{prefix}{connector}{label_str}PrintStmt")
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(node.value, new_prefix, True, "value")
    else:
        print(f"{prefix}{connector}{label_str}{node}")


def generate_ast_image(node, filename="ast"):
    try:
        from graphviz import Digraph
        from model import Integer, Float, String, Bool, Grouping, UnOp, BinOp, Identifier, Assignment, LogicalOp, Stmts, PrintStmt, IfStmt, WhileStmt
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
        elif isinstance(n, Identifier):
            dot.node(node_id, f"Identifier\n{n.name}", shape="ellipse", style="filled", fillcolor="lightcyan")
        elif isinstance(n, Assignment):
            dot.node(node_id, "Assignment", shape="box", style="filled", fillcolor="plum")
            add_node(n.left, node_id, "left")
            add_node(n.right, node_id, "right")
        elif isinstance(n, Grouping):
            dot.node(node_id, "()", shape="box", style="filled", fillcolor="lightgray")
            add_node(n.value, node_id)
        elif isinstance(n, UnOp):
            dot.node(node_id, f"UnOp\n{n.op.lexeme!r}", shape="circle", style="filled", fillcolor="lightsalmon")
            add_node(n.operand, node_id)
        elif isinstance(n, LogicalOp):
            dot.node(node_id, f"LogicalOp\n{n.op.lexeme!r}", shape="diamond", style="filled", fillcolor="lightpink")
            add_node(n.left, node_id, "L")
            add_node(n.right, node_id, "R")
        elif isinstance(n, BinOp):
            dot.node(node_id, f"BinOp\n{n.op.lexeme!r}", shape="circle", style="filled", fillcolor="lightsalmon")
            add_node(n.left, node_id, "L")
            add_node(n.right, node_id, "R")
        elif isinstance(n, IfStmt):
            dot.node(node_id, "IfStmt", shape="box", style="filled", fillcolor="lightskyblue")
            add_node(n.test, node_id, "test")
            add_node(n.then_stmts, node_id, "then")
            add_node(n.else_stmts, node_id, "else")
        elif isinstance(n, WhileStmt):
            dot.node(node_id, "WhileStmt", shape="box", style="filled", fillcolor="lightskyblue")
            add_node(n.test, node_id, "test")
            add_node(n.body_stmts, node_id, "body")
        elif isinstance(n, Stmts):
            dot.node(node_id, "Stmts", shape="box", style="filled", fillcolor="lavender")
            for i, stmt in enumerate(n.stmts):
                add_node(stmt, node_id, f"[{i}]")
        elif isinstance(n, PrintStmt):
            dot.node(node_id, "PrintStmt", shape="box", style="filled", fillcolor="palegreen")
            add_node(n.value, node_id, "value")

        if parent_id:
            dot.edge(parent_id, node_id, label=edge_label)

    add_node(node)
    dot.render(filename, format="png", cleanup=True)
    print(f"AST img generated: {filename}.png")
