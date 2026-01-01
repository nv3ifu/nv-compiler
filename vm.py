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

class VM:
    def __init__(self):
        self.stack = []
        self.ip = 0

    def run(self,instructions):
        pass