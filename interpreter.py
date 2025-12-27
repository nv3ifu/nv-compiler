from model import *
from tokens import *
from utils import *
import codecs
################################################################################
# Constants for different runtime value types
################################################################################
TYPE_NUMBER = 'TYPE_NUMBER'  # Default to 64-bit float
TYPE_STRING = 'TYPE_STRING'  # String managed by the host language
TYPE_BOOL = 'TYPE_BOOL'  # true | false


class Interpreter:
    def interpret(self, node):
        if isinstance(node, Integer):
            return (TYPE_NUMBER, float(node.value))
        elif isinstance(node, Float):
            return (TYPE_NUMBER, float(node.value))
        elif isinstance(node, String):
            return (TYPE_STRING, str(node.value))
        elif isinstance(node, Bool):
            return (TYPE_BOOL, node.value)
        elif isinstance(node, Grouping):
            return self.interpret(node.value)
        elif isinstance(node, BinOp):
            lefttype, leftval = self.interpret(node.left)
            righttype, rightval = self.interpret(node.right)
            if node.op.token_type == TOK_PLUS:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval + rightval)
                elif lefttype == TYPE_STRING or righttype == TYPE_STRING:
                    return (TYPE_STRING, str(leftval) + str(rightval))
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.',
                                  node.op.line)
            elif node.op.token_type == TOK_MINUS:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval - rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.',
                                  node.op.line)
            elif node.op.token_type == TOK_STAR:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval * rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.',
                                  node.op.line)
            elif node.op.token_type == TOK_SLASH:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval / rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.',
                                  node.op.line)
            elif node.op.token_type == TOK_MOD:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval % rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.',
                                  node.op.line)
            elif node.op.token_type == TOK_CARET:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
                    return (TYPE_NUMBER, leftval ** rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.',
                                  node.op.line)
            elif node.op.token_type == TOK_GT:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER or lefttype == TYPE_STRING and righttype == TYPE_STRING:
                    return (TYPE_BOOL, leftval > rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.',
                                  node.op.line)
            elif node.op.token_type == TOK_GE:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER or lefttype == TYPE_STRING and righttype == TYPE_STRING:
                    return (TYPE_BOOL, leftval >= rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.',
                                  node.op.line)
            elif node.op.token_type == TOK_LT:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER or lefttype == TYPE_STRING and righttype == TYPE_STRING:
                    return (TYPE_BOOL, leftval < rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.',
                                  node.op.line)
            elif node.op.token_type == TOK_LE:
                if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER or lefttype == TYPE_STRING and righttype == TYPE_STRING:
                    return (TYPE_BOOL, leftval <= rightval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.',
                                  node.op.line)
            elif node.op.token_type == TOK_EQEQ:
                return (TYPE_BOOL, lefttype == righttype and leftval == rightval)
            elif node.op.token_type == TOK_NE:
                return (TYPE_BOOL, lefttype != righttype or leftval != rightval)

        elif isinstance(node, UnOp):
            operandtype, operandval = self.interpret(node.operand)
            if node.op.token_type == TOK_MINUS:
                if operandtype == TYPE_NUMBER:
                    return (TYPE_NUMBER, -operandval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} with {operandtype}.', node.op.line)
            if node.op.token_type == TOK_PLUS:
                if operandtype == TYPE_NUMBER:
                    return (TYPE_NUMBER, operandval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} with {operandtype}.', node.op.line)
            elif node.op.token_type == TOK_NOT:
                if operandtype == TYPE_BOOL:
                    return (TYPE_BOOL, not operandval)
                else:
                    runtime_error(f'Unsupported operator {node.op.lexeme!r} with {operandtype}.', node.op.line)
        elif isinstance(node, LogicalOp):
            if node.op.token_type == TOK_AND:
                lefttype, leftval = self.interpret(node.left)
                if not leftval:
                    return (TYPE_BOOL, False)
                else:
                    righttype, rightval = self.interpret(node.right)
                    return TYPE_BOOL, bool(rightval)
            elif node.op.token_type == TOK_OR:
                lefttype, leftval = self.interpret(node.left)
                if leftval:
                    return (TYPE_BOOL, True)
                else:
                    righttype, rightval = self.interpret(node.right)
                    return TYPE_BOOL, bool(rightval)
        elif isinstance(node, Stmts):
            for stmt in node.stmts:
                self.interpret(stmt)
        elif isinstance(node,PrintStmt):
            expr_type ,expr_val=self.interpret(node.value)
            print(codecs.escape_decode(bytes(str(expr_val), "utf-8"))[0].decode("utf-8"), end=node.end)
        elif isinstance(node, IfStmt):
            testtype,testval = self.interpret(node.test)
            if testtype!=TYPE_BOOL:
                runtime_error("if condition is not a bool type",node.line)
            if testval:
                self.interpret(node.then_stmts)
            else:
                self.interpret(node.else_stmts)



