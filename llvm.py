import sys
import subprocess
import os
import platform
from utils import compile_error
from parser import Parser
from tokens import *
from lexer import Lexer
from model import *
from llvmlite import ir

TYPE_NUMBER = 'TYPE_NUMBER'
TYPE_STRING = 'TYPE_STRING'
TYPE_BOOL = 'TYPE_BOOL'

void = ir.VoidType()
i1 = ir.IntType(1)
i8 = ir.IntType(8)
i8_ptr = ir.PointerType(i8)
i32 = ir.IntType(32)
i64 = ir.IntType(64)
f64 = ir.DoubleType()


class LLVMModule:
    def __init__(self):
        self.module = ir.Module(name="nv_module")
        
        system = platform.system()
        machine = platform.machine()
        
        if system == "Windows":
            self.module.triple = "x86_64-w64-windows-gnu"
        elif system == "Linux":
            if machine == "x86_64":
                self.module.triple = "x86_64-pc-linux-gnu"
            elif machine == "aarch64":
                self.module.triple = "aarch64-unknown-linux-gnu"
            else:
                self.module.triple = f"{machine}-pc-linux-gnu"
        elif system == "Darwin":
            if machine == "arm64":
                self.module.triple = "arm64-apple-macosx"
            else:
                self.module.triple = "x86_64-apple-macosx"
        else:
            self.module.triple = ""
        
        self.vars = {}
        self.str_counter = 0
        self.functions = {}
        self.current_function = None
        self.builder = None
        
        self._declare_runtime_functions()
        self._create_main()
    
    def _declare_runtime_functions(self):
        printf_ty = ir.FunctionType(i32, [i8_ptr], var_arg=True)
        self.printf = ir.Function(self.module, printf_ty, name="printf")
        
        pow_ty = ir.FunctionType(f64, [f64, f64])
        self.pow = ir.Function(self.module, pow_ty, name="pow")
    
    def _create_main(self):
        main_ty = ir.FunctionType(i32, [])
        self.main = ir.Function(self.module, main_ty, name="main")
        self.functions['main'] = self.main
        
        block = self.main.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        self.current_function = self.main
    
    def create_string_constant(self, s):
        s_bytes = (s + '\0').encode('utf-8')
        str_ty = ir.ArrayType(i8, len(s_bytes))
        
        name = f".str.{self.str_counter}"
        self.str_counter += 1
        
        global_str = ir.GlobalVariable(self.module, str_ty, name=name)
        global_str.global_constant = True
        global_str.linkage = 'private'
        global_str.initializer = ir.Constant(str_ty, bytearray(s_bytes))
        
        zero = ir.Constant(i32, 0)
        return self.builder.gep(global_str, [zero, zero], inbounds=True)
    
    def alloc_var(self, name, type_tag):
        if type_tag == TYPE_NUMBER:
            alloca = self.builder.alloca(f64, name=name)
        elif type_tag == TYPE_BOOL:
            alloca = self.builder.alloca(i1, name=name)
        elif type_tag == TYPE_STRING:
            alloca = self.builder.alloca(i8_ptr, name=name)
        else:
            raise ValueError(f"Unknown type: {type_tag}")
        
        self.vars[name] = (type_tag, alloca)
        return alloca
    
    def get_var(self, name):
        if name not in self.vars:
            return None
        return self.vars[name]
    
    def store_var(self, name, type_tag, value):
        if name not in self.vars:
            self.alloc_var(name, type_tag)
        
        _, alloca = self.vars[name]
        self.builder.store(value, alloca)
    
    def load_var(self, name):
        if name not in self.vars:
            return None
        type_tag, alloca = self.vars[name]
        return (type_tag, self.builder.load(alloca, name=name + ".val"))


class LLVMGenerator:
    def __init__(self):
        self.module = None
        self.fmt_float = None
        self.fmt_float_nl = None
        self.fmt_str = None
        self.fmt_str_nl = None
        self.fmt_int = None
        self.fmt_int_nl = None
    
    def _init_format_strings(self):
        self.fmt_float = self.module.create_string_constant("%g")
        self.fmt_float_nl = self.module.create_string_constant("%g\n")
        self.fmt_str = self.module.create_string_constant("%s")
        self.fmt_str_nl = self.module.create_string_constant("%s\n")
        self.fmt_int = self.module.create_string_constant("%d")
        self.fmt_int_nl = self.module.create_string_constant("%d\n")
    
    def generate(self, node):
        if node is None:
            return None
        
        if isinstance(node, Integer):
            return (TYPE_NUMBER, ir.Constant(f64, float(node.value)))
        
        if isinstance(node, Float):
            return (TYPE_NUMBER, ir.Constant(f64, node.value))
        
        if isinstance(node, Bool):
            return (TYPE_BOOL, ir.Constant(i1, 1 if node.value else 0))
        
        if isinstance(node, String):
            ptr = self.module.create_string_constant(node.value)
            return (TYPE_STRING, ptr)
        
        if isinstance(node, Grouping):
            return self.generate(node.value)
        
        if isinstance(node, Identifier):
            result = self.module.load_var(node.name)
            if result is None:
                compile_error(f"[LLVM] Undefined variable '{node.name}'", node.line)
            return result
        
        if isinstance(node, Assignment):
            right_type, right_val = self.generate(node.right)
            self.module.store_var(node.left.name, right_type, right_val)
            return (right_type, right_val)
        
        if isinstance(node, LocalStmt):
            right_type, right_val = self.generate(node.expr)
            self.module.store_var(node.ident, right_type, right_val)
            return None
        
        if isinstance(node, BinOp):
            return self._generate_binop(node)
        
        if isinstance(node, UnOp):
            return self._generate_unop(node)
        
        if isinstance(node, LogicalOp):
            return self._generate_logical(node)
        
        if isinstance(node, PrintStmt):
            self._generate_print(node)
            return None
        
        if isinstance(node, IfStmt):
            self._generate_if(node)
            return None
        
        if isinstance(node, WhileStmt):
            self._generate_while(node)
            return None
        
        if isinstance(node, ForStmt):
            self._generate_for(node)
            return None
        
        if isinstance(node, Stmts):
            for stmt in node.stmts:
                self.generate(stmt)
            return None
        
        if isinstance(node, FuncDecl):
            self._generate_func_decl(node)
            return None
        
        if isinstance(node, FuncCall):
            return self._generate_func_call(node)
        
        if isinstance(node, FuncCallStmt):
            self.generate(node.expr)
            return None
        
        if isinstance(node, RetStmt):
            ret_type, ret_val = self.generate(node.expr)
            self.module.builder.ret(ret_val)
            return None
        
        compile_error(f"[LLVM] Unknown node type: {type(node).__name__}", getattr(node, 'line', 0))
    
    def _generate_binop(self, node):
        left_type, left_val = self.generate(node.left)
        right_type, right_val = self.generate(node.right)
        builder = self.module.builder
        op = node.op.token_type
        
        if left_type == TYPE_NUMBER and right_type == TYPE_NUMBER:
            if op == TOK_PLUS:
                return (TYPE_NUMBER, builder.fadd(left_val, right_val, name="add"))
            elif op == TOK_MINUS:
                return (TYPE_NUMBER, builder.fsub(left_val, right_val, name="sub"))
            elif op == TOK_STAR:
                return (TYPE_NUMBER, builder.fmul(left_val, right_val, name="mul"))
            elif op == TOK_SLASH:
                return (TYPE_NUMBER, builder.fdiv(left_val, right_val, name="div"))
            elif op == TOK_MOD:
                return (TYPE_NUMBER, builder.frem(left_val, right_val, name="mod"))
            elif op == TOK_CARET:
                result = builder.call(self.module.pow, [left_val, right_val], name="pow")
                return (TYPE_NUMBER, result)
            elif op == TOK_GT:
                cmp = builder.fcmp_ordered('>', left_val, right_val, name="gt")
                return (TYPE_BOOL, cmp)
            elif op == TOK_GE:
                cmp = builder.fcmp_ordered('>=', left_val, right_val, name="ge")
                return (TYPE_BOOL, cmp)
            elif op == TOK_LT:
                cmp = builder.fcmp_ordered('<', left_val, right_val, name="lt")
                return (TYPE_BOOL, cmp)
            elif op == TOK_LE:
                cmp = builder.fcmp_ordered('<=', left_val, right_val, name="le")
                return (TYPE_BOOL, cmp)
            elif op == TOK_EQEQ:
                cmp = builder.fcmp_ordered('==', left_val, right_val, name="eq")
                return (TYPE_BOOL, cmp)
            elif op == TOK_NE:
                cmp = builder.fcmp_ordered('!=', left_val, right_val, name="ne")
                return (TYPE_BOOL, cmp)
        
        if left_type == TYPE_STRING and right_type == TYPE_STRING:
            if op == TOK_PLUS:
                compile_error("[LLVM] String concatenation not yet supported", node.line)
            elif op in (TOK_GT, TOK_GE, TOK_LT, TOK_LE, TOK_EQEQ, TOK_NE):
                compile_error("[LLVM] String comparison not yet supported", node.line)
        
        compile_error(f"[LLVM] Unsupported operator '{node.op.lexeme}' for types {left_type}, {right_type}", node.line)
    
    def _generate_unop(self, node):
        operand_type, operand_val = self.generate(node.operand)
        builder = self.module.builder
        op = node.op.token_type
        
        if op == TOK_MINUS:
            if operand_type == TYPE_NUMBER:
                return (TYPE_NUMBER, builder.fneg(operand_val, name="neg"))
        elif op == TOK_PLUS:
            if operand_type == TYPE_NUMBER:
                return (operand_type, operand_val)
        elif op == TOK_NOT:
            if operand_type == TYPE_BOOL:
                result = builder.xor(operand_val, ir.Constant(i1, 1), name="not")
                return (TYPE_BOOL, result)
        
        compile_error(f"[LLVM] Unsupported unary operator '{node.op.lexeme}'", node.line)
    
    def _generate_logical(self, node):
        builder = self.module.builder
        op = node.op.token_type
        
        if op == TOK_AND:
            left_type, left_val = self.generate(node.left)
            
            check_right = builder.append_basic_block(name="and.right")
            merge = builder.append_basic_block(name="and.merge")
            
            builder.cbranch(left_val, check_right, merge)
            
            builder.position_at_end(check_right)
            right_type, right_val = self.generate(node.right)
            check_right_end = builder.block
            builder.branch(merge)
            
            builder.position_at_end(merge)
            phi = builder.phi(i1, name="and.result")
            phi.add_incoming(ir.Constant(i1, 0), self.module.current_function.entry_basic_block if hasattr(self.module.current_function, 'entry_basic_block') else builder.block)
            phi.add_incoming(right_val, check_right_end)
            
            return (TYPE_BOOL, phi)
        
        elif op == TOK_OR:
            left_type, left_val = self.generate(node.left)
            
            check_right = builder.append_basic_block(name="or.right")
            merge = builder.append_basic_block(name="or.merge")
            
            builder.cbranch(left_val, merge, check_right)
            left_block = builder.block
            
            builder.position_at_end(check_right)
            right_type, right_val = self.generate(node.right)
            check_right_end = builder.block
            builder.branch(merge)
            
            builder.position_at_end(merge)
            phi = builder.phi(i1, name="or.result")
            phi.add_incoming(ir.Constant(i1, 1), left_block)
            phi.add_incoming(right_val, check_right_end)
            
            return (TYPE_BOOL, phi)
        
        compile_error(f"[LLVM] Unknown logical operator", node.line)
    
    def _generate_print(self, node):
        val_type, val = self.generate(node.value)
        builder = self.module.builder
        
        if val_type == TYPE_NUMBER:
            fmt = self.fmt_float_nl if node.end == '\n' else self.fmt_float
            builder.call(self.module.printf, [fmt, val])
        elif val_type == TYPE_STRING:
            fmt = self.fmt_str_nl if node.end == '\n' else self.fmt_str
            builder.call(self.module.printf, [fmt, val])
        elif val_type == TYPE_BOOL:
            true_str = self.module.create_string_constant("true")
            false_str = self.module.create_string_constant("false")
            str_val = builder.select(val, true_str, false_str)
            fmt = self.fmt_str_nl if node.end == '\n' else self.fmt_str
            builder.call(self.module.printf, [fmt, str_val])
    
    def _generate_if(self, node):
        builder = self.module.builder
        
        cond_type, cond_val = self.generate(node.test)
        
        then_block = builder.append_basic_block(name="if.then")
        else_block = builder.append_basic_block(name="if.else") if node.else_stmts else None
        merge_block = builder.append_basic_block(name="if.end")
        
        if else_block:
            builder.cbranch(cond_val, then_block, else_block)
        else:
            builder.cbranch(cond_val, then_block, merge_block)
        
        builder.position_at_end(then_block)
        self.generate(node.then_stmts)
        if not builder.block.is_terminated:
            builder.branch(merge_block)
        
        if else_block:
            builder.position_at_end(else_block)
            self.generate(node.else_stmts)
            if not builder.block.is_terminated:
                builder.branch(merge_block)
        
        builder.position_at_end(merge_block)
    
    def _generate_while(self, node):
        builder = self.module.builder
        
        cond_block = builder.append_basic_block(name="while.cond")
        body_block = builder.append_basic_block(name="while.body")
        exit_block = builder.append_basic_block(name="while.end")
        
        builder.branch(cond_block)
        
        builder.position_at_end(cond_block)
        cond_type, cond_val = self.generate(node.test)
        builder.cbranch(cond_val, body_block, exit_block)
        
        builder.position_at_end(body_block)
        self.generate(node.body_stmts)
        if not builder.block.is_terminated:
            builder.branch(cond_block)
        
        builder.position_at_end(exit_block)
    
    def _generate_for(self, node):
        builder = self.module.builder
        var_name = node.ident.name
        
        start_type, start_val = self.generate(node.start)
        self.module.store_var(var_name, TYPE_NUMBER, start_val)
        
        cond_block = builder.append_basic_block(name="for.cond")
        body_block = builder.append_basic_block(name="for.body")
        step_block = builder.append_basic_block(name="for.step")
        exit_block = builder.append_basic_block(name="for.end")
        
        builder.branch(cond_block)
        
        builder.position_at_end(cond_block)
        curr_type, curr_val = self.module.load_var(var_name)
        end_type, end_val = self.generate(node.end)
        cond = builder.fcmp_ordered('<', curr_val, end_val, name="for.cmp")
        builder.cbranch(cond, body_block, exit_block)
        
        builder.position_at_end(body_block)
        self.generate(node.body_stmts)
        if not builder.block.is_terminated:
            builder.branch(step_block)
        
        builder.position_at_end(step_block)
        curr_type, curr_val = self.module.load_var(var_name)
        if node.step:
            step_type, step_val = self.generate(node.step)
        else:
            step_val = ir.Constant(f64, 1.0)
        new_val = builder.fadd(curr_val, step_val, name="for.next")
        self.module.store_var(var_name, TYPE_NUMBER, new_val)
        builder.branch(cond_block)
        
        builder.position_at_end(exit_block)
    
    def _generate_func_decl(self, node):
        func = self.module.functions.get(node.name)
        if func is None:
            param_types = [f64] * len(node.params)
            func_ty = ir.FunctionType(f64, param_types)
            func = ir.Function(self.module.module, func_ty, name=node.name)
            self.module.functions[node.name] = func
        
        old_builder = self.module.builder
        old_func = self.module.current_function
        old_vars = self.module.vars.copy()
        
        block = func.append_basic_block(name="entry")
        self.module.builder = ir.IRBuilder(block)
        self.module.current_function = func
        self.module.vars = {}
        
        for param, arg in zip(node.params, func.args):
            arg.name = param.name
            self.module.store_var(param.name, TYPE_NUMBER, arg)
        
        self.generate(node.body_stmts)
        
        if not self.module.builder.block.is_terminated:
            self.module.builder.ret(ir.Constant(f64, 0.0))
        
        self.module.builder = old_builder
        self.module.current_function = old_func
        self.module.vars = old_vars
    
    def _generate_func_call(self, node):
        if node.name not in self.module.functions:
            compile_error(f"[LLVM] Undefined function '{node.name}'", node.line)
        
        func = self.module.functions[node.name]
        args = []
        for arg in node.args:
            arg_type, arg_val = self.generate(arg)
            args.append(arg_val)
        
        result = self.module.builder.call(func, args, name=f"call.{node.name}")
        return (TYPE_NUMBER, result)
    
    def generate_module(self, ast):
        self.module = LLVMModule()
        self._init_format_strings()
        
        self._collect_functions(ast)
        
        self.generate(ast)
        
        if not self.module.builder.block.is_terminated:
            self.module.builder.ret(ir.Constant(i32, 0))
        
        return self.module
    
    def _collect_functions(self, node):
        if isinstance(node, Stmts):
            for stmt in node.stmts:
                self._collect_functions(stmt)
        elif isinstance(node, FuncDecl):
            param_types = [f64] * len(node.params)
            func_ty = ir.FunctionType(f64, param_types)
            func = ir.Function(self.module.module, func_ty, name=node.name)
            self.module.functions[node.name] = func


def compile_to_executable(ll_file, output_file):
    helper_c = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'helper.c')
    
    cmd = ['clang', ll_file, '-o', output_file, '-lm']
    if os.path.exists(helper_c):
        cmd.insert(2, helper_c)
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Compilation failed:\n{result.stderr}")
        return False
    
    print(f"Successfully compiled to {output_file}")
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python llvm.py <filename.nv> [--compile]')
        sys.exit(1)
    
    filename = sys.argv[1]
    do_compile = '--compile' in sys.argv
    
    with open(filename, encoding='utf-8') as file:
        source = file.read()
    
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    
    generator = LLVMGenerator()
    module = generator.generate_module(ast)
    
    ll_filename = os.path.splitext(filename)[0] + '.ll'
    with open(ll_filename, 'w') as f:
        f.write(str(module.module))
    
    print(str(module.module))
    print(f"\n*** LLVM IR generated: {ll_filename} ***")
    
    if do_compile:
        exe_filename = os.path.splitext(filename)[0] + '.exe'
        if compile_to_executable(ll_filename, exe_filename):
            print(f"\n*** Running {exe_filename} ***\n")
            subprocess.run([exe_filename])