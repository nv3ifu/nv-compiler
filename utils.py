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

def vm_error(message,pc):
    print(f'{Colors.RED}[PC {pc}]: {message}{Colors.WHITE}')
    sys.exit(1)

def compile_error(message, lineno):
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
    from model import Integer, Float, String, Bool, Grouping, UnOp, BinOp, Identifier, Assignment, LogicalOp, Stmts, PrintStmt, IfStmt, WhileStmt, ForStmt, FuncDecl, FuncCall, Params, FuncCallStmt, RetStmt

    connector = "└── " if is_last else "├── "
    label_str = f"{label}: " if label else ""

    # 处理 None 节点
    if node is None:
        print(f"{prefix}{connector}{label_str}None")
        return

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
        if node.else_stmts is not None:
            print_tree(node.then_stmts, new_prefix, False, "then")
            print_tree(node.else_stmts, new_prefix, True, "else")
        else:
            print_tree(node.then_stmts, new_prefix, True, "then")
    elif isinstance(node, WhileStmt):
        print(f"{prefix}{connector}{label_str}WhileStmt")
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(node.test, new_prefix, False, "test")
        print_tree(node.body_stmts, new_prefix, True, "body")
    elif isinstance(node, ForStmt):
        print(f"{prefix}{connector}{label_str}ForStmt")
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(node.ident, new_prefix, False, "ident")
        print_tree(node.start, new_prefix, False, "start")
        print_tree(node.end, new_prefix, False, "end")
        if node.step is not None:
            print_tree(node.step, new_prefix, False, "step")
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
    elif isinstance(node, FuncDecl):
        print(f"{prefix}{connector}{label_str}FuncDecl({node.name})")
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, param in enumerate(node.params):
            is_last_param = (i == len(node.params) - 1) and node.body_stmts is None
            print_tree(param, new_prefix, is_last_param, f"param[{i}]")
        print_tree(node.body_stmts, new_prefix, True, "body")
    elif isinstance(node, FuncCall):
        print(f"{prefix}{connector}{label_str}FuncCall({node.name})")
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, arg in enumerate(node.args):
            is_last_arg = (i == len(node.args) - 1)
            print_tree(arg, new_prefix, is_last_arg, f"arg[{i}]")
    elif isinstance(node, Params):
        print(f"{prefix}{connector}{label_str}Param({node.name})")
    elif isinstance(node, FuncCallStmt):
        print(f"{prefix}{connector}{label_str}FuncCallStmt")
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(node.expr, new_prefix, True, "expr")
    elif isinstance(node, RetStmt):
        print(f"{prefix}{connector}{label_str}RetStmt")
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(node.expr, new_prefix, True, "expr")
    else:
        print(f"{prefix}{connector}{label_str}{node}")

def stringify(val):
    if isinstance(val,bool) and val == True:
        return 'true'
    elif isinstance(val,bool) and val == False:
        return 'false'
    elif isinstance(val,float) and val.is_integer():
        return str(int(val))
    else:
        return str(val)


def print_code(code):
    """打印 VM 指令，格式化输出类似汇编风格"""
    for i, op in enumerate(code):
        opcode = op[0]
        idx = f"{i:08d}"
        if opcode in ('START', 'HALT'):
            # 标签式指令，顶格加冒号
            print(f"{idx} {opcode}:")
        elif opcode == 'LABEL':
            # 标签定义，顶格显示
            print(f"{idx} {op[1]}:")
        elif opcode in ('JMP', 'JMPZ', 'JSR'):
            # 跳转指令，参数是标签名字符串
            print(f"{idx}     {opcode}  {op[1]}")
        elif opcode in ('LOAD_GLOBAL', 'STORE_GLOBAL'):
            # 全局变量指令，参数是变量名字符串
            print(f"{idx}     {opcode}  {op[1]}")
        elif opcode in ('LOAD_LOCAL', 'STORE_LOCAL'):
            # 局部变量指令，参数是 slot 整数
            print(f"{idx}     {opcode}  {op[1]}")
        elif len(op) == 1:
            # 无参数指令，缩进显示
            print(f"{idx}     {opcode}")
        else:
            # 有参数指令（如 PUSH）
            # op[1] 是 (TYPE, value) 元组
            _, value = op[1]
            print(f"{idx}     {opcode}  {stringify(value)}")

def generate_ast_image(node, filename="ast"):
    try:
        from graphviz import Digraph
        from model import Integer, Float, String, Bool, Grouping, UnOp, BinOp, Identifier, Assignment, LogicalOp, Stmts, PrintStmt, IfStmt, WhileStmt, ForStmt, FuncDecl, FuncCall, Params, FuncCallStmt, RetStmt
    except ImportError:
        print("plz install graphviz: pip install graphviz")
        return

    dot = Digraph(comment='AST')
    dot.attr(rankdir='TB', fontname='Consolas')
    dot.attr('node', fontname='Consolas')

    def add_node(n, parent_id=None, edge_label=""):
        # 处理 None 节点
        if n is None:
            node_id = str(id(n)) + "_none_" + str(parent_id)
            dot.node(node_id, "None", shape="ellipse", style="filled", fillcolor="lightgray")
            if parent_id:
                dot.edge(parent_id, node_id, label=edge_label)
            return

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
            if n.else_stmts is not None:
                add_node(n.else_stmts, node_id, "else")
        elif isinstance(n, WhileStmt):
            dot.node(node_id, "WhileStmt", shape="box", style="filled", fillcolor="lightskyblue")
            add_node(n.test, node_id, "test")
            add_node(n.body_stmts, node_id, "body")
        elif isinstance(n, ForStmt):
            dot.node(node_id, "ForStmt", shape="box", style="filled", fillcolor="lightcoral")
            add_node(n.ident, node_id, "ident")
            add_node(n.start, node_id, "start")
            add_node(n.end, node_id, "end")
            if n.step is not None:
                add_node(n.step, node_id, "step")
            add_node(n.body_stmts, node_id, "body")
        elif isinstance(n, Stmts):
            dot.node(node_id, "Stmts", shape="box", style="filled", fillcolor="lavender")
            for i, stmt in enumerate(n.stmts):
                add_node(stmt, node_id, f"[{i}]")
        elif isinstance(n, PrintStmt):
            dot.node(node_id, "PrintStmt", shape="box", style="filled", fillcolor="palegreen")
            add_node(n.value, node_id, "value")
        elif isinstance(n, FuncDecl):
            dot.node(node_id, f"FuncDecl\n{n.name}", shape="box", style="filled", fillcolor="orchid")
            for i, param in enumerate(n.params):
                add_node(param, node_id, f"param[{i}]")
            add_node(n.body_stmts, node_id, "body")
        elif isinstance(n, FuncCall):
            dot.node(node_id, f"FuncCall\n{n.name}", shape="box", style="filled", fillcolor="gold")
            for i, arg in enumerate(n.args):
                add_node(arg, node_id, f"arg[{i}]")
        elif isinstance(n, Params):
            dot.node(node_id, f"Param\n{n.name}", shape="ellipse", style="filled", fillcolor="lightcyan")
        elif isinstance(n, FuncCallStmt):
            dot.node(node_id, "FuncCallStmt", shape="box", style="filled", fillcolor="gold")
            add_node(n.expr, node_id, "expr")
        elif isinstance(n, RetStmt):
            dot.node(node_id, "RetStmt", shape="box", style="filled", fillcolor="salmon")
            add_node(n.expr, node_id, "expr")
        else:
            # 处理未知节点类型
            dot.node(node_id, str(type(n).__name__), shape="box", style="filled", fillcolor="white")

        if parent_id:
            dot.edge(parent_id, node_id, label=edge_label)

    add_node(node)
    dot.render(filename, format="png", cleanup=True)
    print(f"AST img generated: {filename}.png")
