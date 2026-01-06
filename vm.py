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

class Frame:
    def __init__(self,name,ret_pc,frame_pointer):
        self.name = name
        self.ret_pc = ret_pc
        self.frame_pointer = frame_pointer

class VM:
    def __init__(self):
        self.stack = []
        self.pc = 0
        self.sp = -1
        self.bp = 0  
        self.labels = {}
        self.globals = {}
        self.frames = []
        self.is_running = True

    def create_label_table(self,instructions):
        self.labels = {}
        for i,op in enumerate(instructions):
            if op[0] == 'LABEL':
                self.labels[op[1]] = i


    def run(self,instructions):
        self.create_label_table(instructions)  # 先建立标签表
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

    def PUSH(self,*args):
        self.stack.append(args[0])
        self.sp += 1

    def POP(self,*args):
        self.sp -= 1
        return self.stack.pop()

    def ADD(self,*args):
        righttype, rightvalue = self.POP()
        lefttype, leftvalue = self.POP()
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
            self.PUSH((TYPE_NUMBER, leftvalue + rightvalue))
        elif lefttype == TYPE_STRING or righttype == TYPE_STRING:
            self.PUSH((TYPE_STRING, stringify(leftvalue) + stringify(rightvalue)))
        else:
            vm_error("Invalid types for ADD", self.pc-1)

    def SUB(self,*args):
        righttype, rightvalue = self.POP()
        lefttype, leftvalue = self.POP()
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
            self.PUSH((TYPE_NUMBER, leftvalue - rightvalue))
        else:
            vm_error("Invalid types for SUB", self.pc-1)

    def MUL(self,*args):
        righttype, rightvalue = self.POP()
        lefttype, leftvalue = self.POP()
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
            self.PUSH((TYPE_NUMBER, leftvalue * rightvalue))
        else:
            vm_error("Invalid types for MUL", self.pc-1)

    def DIV(self,*args):
        righttype, rightvalue = self.POP()
        lefttype, leftvalue = self.POP()
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
            self.PUSH((TYPE_NUMBER, leftvalue / rightvalue))
        else:
            vm_error("Invalid types for DIV", self.pc-1)

    def EXP(self,*args):
        righttype, rightvalue = self.POP()
        lefttype, leftvalue = self.POP()
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
            self.PUSH((TYPE_NUMBER, leftvalue ** rightvalue))
        else:
            vm_error("Invalid types for EXP", self.pc-1)

    def MOD(self,*args):
        righttype, rightvalue = self.POP()
        lefttype, leftvalue = self.POP()
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
            self.PUSH((TYPE_NUMBER, leftvalue % rightvalue))
        else:
            vm_error("Invalid types for MOD", self.pc-1)

    def PRINT(self,*args):
        vatype, val = self.POP()
        print(codecs.escape_decode(bytes(stringify(val),"utf-8"))[0].decode("utf-8"), end="")

    def PRINTLN(self,*args):
        vatype, val = self.POP()
        print(codecs.escape_decode(bytes(stringify(val),"utf-8"))[0].decode("utf-8"), end="\n")

    def AND(self,*args):
        righttype, rightvalue = self.POP()
        lefttype, leftvalue = self.POP()
        if lefttype == TYPE_BOOL and righttype == TYPE_BOOL:
            self.PUSH((TYPE_BOOL, leftvalue and rightvalue))
        else:
            vm_error("Invalid types for AND", self.pc-1)
    
    def OR(self,*args):
        righttype, rightvalue = self.POP()
        lefttype, leftvalue = self.POP()
        if lefttype == TYPE_BOOL and righttype == TYPE_BOOL:
            self.PUSH((TYPE_BOOL, leftvalue or rightvalue))
        else:
            vm_error("Invalid types for OR", self.pc-1)

    def XOR(self,*args):
        righttype, rightvalue = self.POP()
        lefttype, leftvalue = self.POP()
        if lefttype == TYPE_BOOL and righttype == TYPE_BOOL:
            self.PUSH((TYPE_BOOL, leftvalue ^ rightvalue))
        else:
            vm_error("Invalid types for XOR", self.pc-1)

    def NEG(self,*args):
        valtype, value = self.POP()
        if valtype == TYPE_NUMBER:
            self.PUSH((TYPE_NUMBER, -value))
        else:
            vm_error("Invalid types for NEG", self.pc-1)

    def LT(self,*args):
        righttype, rightvalue = self.POP()
        lefttype, leftvalue = self.POP()
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
            self.PUSH((TYPE_BOOL, leftvalue < rightvalue))
        else:
            vm_error("Invalid types for LT", self.pc-1)

    def GT(self,*args):
        righttype, rightvalue = self.POP()
        lefttype, leftvalue = self.POP()
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
            self.PUSH((TYPE_BOOL, leftvalue > rightvalue))
        else:
            vm_error("Invalid types for GT", self.pc-1)

    def LE(self,*args):
        righttype, rightvalue = self.POP()
        lefttype, leftvalue = self.POP()
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
            self.PUSH((TYPE_BOOL, leftvalue <= rightvalue))
        else:
            vm_error("Invalid types for LE", self.pc-1)

    def GE(self,*args):
        righttype, rightvalue = self.POP()
        lefttype, leftvalue = self.POP()
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
            self.PUSH((TYPE_BOOL, leftvalue >= rightvalue))
        else:
            vm_error("Invalid types for GE", self.pc-1)

    def EQ(self,*args):
        righttype, rightvalue = self.POP()
        lefttype, leftvalue = self.POP()
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
            self.PUSH((TYPE_BOOL, leftvalue == rightvalue))
        elif lefttype == TYPE_STRING and righttype == TYPE_STRING:
            self.PUSH((TYPE_BOOL, leftvalue == rightvalue))
        elif lefttype == TYPE_BOOL and righttype == TYPE_BOOL:
            self.PUSH((TYPE_BOOL, leftvalue == rightvalue))
        else:
            vm_error("Invalid types for EQ", self.pc-1)

    def NE(self,*args):
        righttype, rightvalue = self.POP()
        lefttype, leftvalue = self.POP()
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
            self.PUSH((TYPE_BOOL, leftvalue != rightvalue))
        elif lefttype == TYPE_STRING and righttype == TYPE_STRING:
            self.PUSH((TYPE_BOOL, leftvalue != rightvalue))
        elif lefttype == TYPE_BOOL and righttype == TYPE_BOOL:
            self.PUSH((TYPE_BOOL, leftvalue != rightvalue))
        else:
            vm_error("Invalid types for NE", self.pc-1)

    def JMP(self,*args):
        self.pc = self.labels[args[0]]

    def CALL(self,*args):
        func_name = args[0]
        arg_count = args[1] if len(args) > 1 else 0
        new_frame = Frame(func_name, self.pc, self.bp)
        self.frames.append(new_frame)
        self.bp = self.sp - arg_count + 1
        self.pc = self.labels[func_name]

    def RET(self,*args):
        return_value = self.POP()
        frame = self.frames.pop()
        while self.sp >= self.bp:
            self.POP()
        self.bp = frame.frame_pointer
        self.pc = frame.ret_pc
        self.PUSH(return_value)
 
    def JMPZ(self,*args):
        vatype, val = self.POP()    
        if vatype == TYPE_BOOL and val == False:
            self.pc = self.labels[args[0]]

    def LOAD_GLOBAL(self,*args):
        self.PUSH((self.globals[args[0]]))

    def STORE_GLOBAL(self,*args):
        self.globals[args[0]] = self.POP()

    def LOAD_LOCAL(self,*args):
        # Load local variable from stack at bp + slot
        slot = args[0]
        self.PUSH(self.stack[self.bp + slot])

    def STORE_LOCAL(self,*args):
        # Store value to stack at bp + slot
        slot = args[0]
        value = self.POP()
        # Extend stack if necessary
        target_index = self.bp + slot
        while len(self.stack) <= target_index:
            self.stack.append(None)
            self.sp += 1
        self.stack[target_index] = value