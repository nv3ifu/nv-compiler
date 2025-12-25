from model import *
from tokens import *


class Interpreter:
    def __init__(self):
        pass

    def interpreter(self, node):
        if isinstance(node, Integer):
            return float(node.value)
        elif isinstance(node, Float):
            return float(node.value)
        elif isinstance(node, Grouping):
            return self.interpreter(node.value)
        elif isinstance(node, BinOp):
            left_value = self.interpreter(node.left)
            right_value = self.interpreter(node.right)
            if node.op.token_type == TOK_PLUS:
                return left_value + right_value
            if node.op.token_type == TOK_MINUS:
                return left_value - right_value
            if node.op.token_type == TOK_STAR:
                return left_value * right_value
            if node.op.token_type == TOK_SLASH:
                return left_value / right_value
        elif isinstance(node, UnOp):
            operand = self.interpreter(node.operand)
            if node.op.token_type == TOK_PLUS:
                return +operand
            if node.op.token_type == TOK_MINUS:
                return -operand
            #if node.op.token_type == TOK_NOT:
            #    return not operand
