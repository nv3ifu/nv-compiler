# The VM itself consists of a single stack.
#
# Instructions to push and pop from the stack:
#
#      ('PUSH', value)       # Push a value to the stack
#      ('POP',)              # Pop a value from the stack
#
# Stack values are tagged with their type using a tuple:
#
#      (TYPE_NUMBER, 4.0)
#      (TYPE_NUMBER, 15.6)
#      (TYPE_NUMBER, -3.141592)
#      (TYPE_STRING, 'This is a string')
#      (TYPE_BOOL, true)
#
# Instructions to add, subtract, multiply, divide, and compare values from the top of the stack
#
#      ('ADD',)              # Addition
#      ('SUB',)              # Subtraction
#      ('MUL',)              # Multiplication
#      ('DIV',)              # Division
#      ('OR',)               # Bitwise OR
#      ('AND',)              # Bitwise AND
#      ('XOR',)              # Bitwise XOR
#      ('NEG',)              # Negate
#      ('EXP',)              # Exponent
#      ('MOD',)              # Modulo
#      ('EQ',)               # Compare ==
#      ('NE',)               # Compare !=
#      ('GT',)               # Compare >
#      ('GE',)               # Compare >=
#      ('LT',)               # Compare <
#      ('LE',)               # Compare <=
#
# An example of the instruction stream for computing 7 + 2 * 3
#
#      ('PUSH', (TYPE_NUMBER, 7))
#      ('PUSH', (TYPE_NUMBER, 2))
#      ('PUSH', (TYPE_NUMBER, 3))
#      ('MUL',)
#      ('ADD',)
#
# Instructions to load and store variables
#
#      ('LOAD', name)        # Push a global variable name from memory to the stack
#      ('STORE, name)        # Save top of the stack into global variable by name
#      ('LOAD_LOCAL', name)  # Push a local variable name from memory to the stack
#      ('STORE_LOCAL, name)  # Save top of the stack to local variable by name
#
# Instructions to manage control-flow (if-else, while, etc.)
#
#      ('LABEL', name)       # Declares a label
#      ('JMP', name)         # Unconditionally jump to label name
#      ('JMPZ', name)        # Jump to label name if top of stack is zero (or false)
#      ('JSR', name)         # Jump to subroutine/function and keep track of the returning PC
#      ('RTS',)              # Return from subroutine/function

import codecs
from utils import *

TYPE_NUMBER = 'TYPE_NUMBER'  # Default to 64-bit float
TYPE_STRING = 'TYPE_STRING'  # String managed by the host language
TYPE_BOOL = 'TYPE_BOOL'  # true | false

class VM:
    def __init__(self):
        self.stack = []
        self.pc = 0
        self.sp = -1
        self.is_running = True

    def run(self,instructions):
        self.is_running = True
        while self.is_running:
            opcode,*args = instructions[self.pc]
            self.pc += 1
            getattr(self, opcode)(*args)

    def START(self,*args):
        self.is_running = True

    def HALT(self,*args):
        self.is_running = False

    def LABEL(self,*args):
        pass

    def JMP(self,*args):
        pass

    def JMPZ(self,*args):
        pass

    def JSR(self,*args):
        pass

    def RTS(self,*args):
        pass

    def PUSH(self,*args):
        self.stack.append(args[0])
        self.sp += 1

    def POP(self,*args):
        self.sp -= 1
        return self.stack.pop()

    def ADD(self,*args):
        lefttype,leftvalue = self.stack[self.sp]
        righttype,rightvalue = self.stack[self.sp-1]
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
            self.stack[self.sp-1] = (TYPE_NUMBER,leftvalue+rightvalue)
            self.stack.pop()
            self.sp -= 1
        else:
            vm_error("Invalid types for ADD",self.pc)

    def SUB(self,*args):
        lefttype,leftvalue = self.stack[self.sp]
        righttype,rightvalue = self.stack[self.sp-1]
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
            self.stack[self.sp-1] = (TYPE_NUMBER,rightvalue-leftvalue)
            self.stack.pop()
            self.sp -= 1
        else:
            vm_error("Invalid types for SUB",self.pc)

    def MUL(self,*args):
        lefttype,leftvalue = self.stack[self.sp]
        righttype,rightvalue = self.stack[self.sp-1]
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
            self.stack[self.sp-1] = (TYPE_NUMBER,leftvalue*rightvalue)
            self.stack.pop()
            self.sp -= 1
        else:
            vm_error("Invalid types for MUL",self.pc)

    def DIV(self,*args):
        lefttype,leftvalue = self.stack[self.sp]
        righttype,rightvalue = self.stack[self.sp-1]
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
            self.stack[self.sp-1] = (TYPE_NUMBER,rightvalue/leftvalue)
            self.stack.pop()
            self.sp -= 1
        else:
            vm_error("Invalid types for DIV",self.pc)

    def PRINT(self,*args):
        vatype,val = self.POP()
        print(codecs.escape_decode(bytes(stringify(val),"utf-8"))[0].decode("utf-8"),end="")

    def PRINTLN(self,*args):
        vatype,val = self.POP()
        print(codecs.escape_decode(bytes(stringify(val),"utf-8"))[0].decode("utf-8"),end="\n")
