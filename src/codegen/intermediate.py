"""
Intermediate Representation (IR) for MinLang Compiler
Defines Three-Address Code (TAC) instructions and data structures
"""

from dataclasses import dataclass
from typing import List, Optional, Union
from enum import Enum


class TACOpcode(Enum):
    """Three-Address Code operation codes"""
    # Arithmetic operations
    ADD = "add"           # t1 = t2 + t3
    SUB = "sub"           # t1 = t2 - t3
    MUL = "mul"           # t1 = t2 * t3
    DIV = "div"           # t1 = t2 / t3
    MOD = "mod"           # t1 = t2 % t3
    NEG = "neg"           # t1 = -t2
    
    # Relational operations
    LT = "lt"             # t1 = t2 < t3
    GT = "gt"             # t1 = t2 > t3
    LE = "le"             # t1 = t2 <= t3
    GE = "ge"             # t1 = t2 >= t3
    EQ = "eq"             # t1 = t2 == t3
    NE = "ne"             # t1 = t2 != t3
    
    # Logical operations
    AND = "and"           # t1 = t2 && t3
    OR = "or"             # t1 = t2 || t3
    NOT = "not"           # t1 = !t2
    
    # Assignment and copy
    ASSIGN = "assign"     # t1 = t2
    COPY = "copy"         # t1 = t2
    
    # Jump and control flow
    LABEL = "label"       # L1:
    GOTO = "goto"         # goto L1
    IF_FALSE = "iffalse"  # iffalse t1 goto L1
    IF_TRUE = "iftrue"    # iftrue t1 goto L1
    
    # Function operations
    PARAM = "param"       # param t1
    CALL = "call"         # t1 = call f, n
    RETURN = "return"     # return t1
    RETURN_VOID = "return_void"  # return
    BEGIN_FUNC = "begin_func"    # begin_func f
    END_FUNC = "end_func"        # end_func f
    
    # I/O operations
    READ = "read"         # read t1
    PRINT = "print"       # print t1
    
    # Type conversion
    INT_TO_FLOAT = "int2float"   # t1 = (float)t2
    FLOAT_TO_INT = "float2int"   # t1 = (int)t2


@dataclass
class TACInstruction:
    """
    Base class for Three-Address Code instructions
    
    Attributes:
        opcode: Operation code
        result: Result operand (destination)
        arg1: First argument operand
        arg2: Second argument operand (optional)
        label: Label for this instruction (optional)
    """
    opcode: TACOpcode
    result: Optional[str] = None
    arg1: Optional[str] = None
    arg2: Optional[str] = None
    label: Optional[str] = None
    
    def __str__(self) -> str:
        """String representation of the instruction"""
        if self.opcode == TACOpcode.LABEL:
            return f"{self.result}:"
        
        elif self.opcode in [TACOpcode.GOTO]:
            return f"    goto {self.result}"
        
        elif self.opcode in [TACOpcode.IF_FALSE, TACOpcode.IF_TRUE]:
            op = "iffalse" if self.opcode == TACOpcode.IF_FALSE else "iftrue"
            return f"    {op} {self.arg1} goto {self.result}"
        
        elif self.opcode in [TACOpcode.PARAM]:
            return f"    param {self.arg1}"
        
        elif self.opcode == TACOpcode.CALL:
            if self.result:
                return f"    {self.result} = call {self.arg1}, {self.arg2}"
            return f"    call {self.arg1}, {self.arg2}"
        
        elif self.opcode == TACOpcode.RETURN:
            return f"    return {self.arg1}"
        
        elif self.opcode == TACOpcode.RETURN_VOID:
            return f"    return"
        
        elif self.opcode == TACOpcode.BEGIN_FUNC:
            return f"\nbegin_func {self.result}"
        
        elif self.opcode == TACOpcode.END_FUNC:
            return f"end_func {self.result}\n"
        
        elif self.opcode in [TACOpcode.READ]:
            return f"    read {self.result}"
        
        elif self.opcode in [TACOpcode.PRINT]:
            return f"    print {self.arg1}"
        
        elif self.opcode in [TACOpcode.ASSIGN, TACOpcode.COPY]:
            return f"    {self.result} = {self.arg1}"
        
        elif self.opcode in [TACOpcode.NEG, TACOpcode.NOT, 
                            TACOpcode.INT_TO_FLOAT, TACOpcode.FLOAT_TO_INT]:
            op_str = {
                TACOpcode.NEG: "-",
                TACOpcode.NOT: "!",
                TACOpcode.INT_TO_FLOAT: "(float)",
                TACOpcode.FLOAT_TO_INT: "(int)",
            }[self.opcode]
            return f"    {self.result} = {op_str}{self.arg1}"
        
        elif self.arg2 is not None:
            # Binary operation
            op_str = {
                TACOpcode.ADD: "+",
                TACOpcode.SUB: "-",
                TACOpcode.MUL: "*",
                TACOpcode.DIV: "/",
                TACOpcode.MOD: "%",
                TACOpcode.LT: "<",
                TACOpcode.GT: ">",
                TACOpcode.LE: "<=",
                TACOpcode.GE: ">=",
                TACOpcode.EQ: "==",
                TACOpcode.NE: "!=",
                TACOpcode.AND: "&&",
                TACOpcode.OR: "||",
            }.get(self.opcode, str(self.opcode.value))
            
            return f"    {self.result} = {self.arg1} {op_str} {self.arg2}"
        
        return f"    {self.opcode.value} {self.result} {self.arg1} {self.arg2}"


class TACProgram:
    """
    Represents a complete TAC program
    
    Attributes:
        instructions: List of TAC instructions
        temp_count: Counter for temporary variables
        label_count: Counter for labels
    """
    
    def __init__(self):
        self.instructions: List[TACInstruction] = []
        self.temp_count = 0
        self.label_count = 0
    
    def new_temp(self) -> str:
        """
        Generate a new temporary variable
        
        Returns:
            Temporary variable name (e.g., 't0', 't1', ...)
        """
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp
    
    def new_label(self, prefix: str = "L") -> str:
        """
        Generate a new label
        
        Args:
            prefix: Label prefix (default: 'L')
            
        Returns:
            Label name (e.g., 'L0', 'L1', ...)
        """
        label = f"{prefix}{self.label_count}"
        self.label_count += 1
        return label
    
    def emit(self, opcode: TACOpcode, result: Optional[str] = None,
             arg1: Optional[str] = None, arg2: Optional[str] = None):
        """
        Emit a TAC instruction
        
        Args:
            opcode: Operation code
            result: Result operand
            arg1: First argument
            arg2: Second argument
        """
        instruction = TACInstruction(opcode, result, arg1, arg2)
        self.instructions.append(instruction)
    
    def emit_label(self, label: str):
        """
        Emit a label
        
        Args:
            label: Label name
        """
        self.emit(TACOpcode.LABEL, result=label)
    
    def emit_goto(self, label: str):
        """
        Emit an unconditional jump
        
        Args:
            label: Target label
        """
        self.emit(TACOpcode.GOTO, result=label)
    
    def emit_if_false(self, condition: str, label: str):
        """
        Emit a conditional jump (if false)
        
        Args:
            condition: Condition variable
            label: Target label
        """
        self.emit(TACOpcode.IF_FALSE, result=label, arg1=condition)
    
    def emit_if_true(self, condition: str, label: str):
        """
        Emit a conditional jump (if true)
        
        Args:
            condition: Condition variable
            label: Target label
        """
        self.emit(TACOpcode.IF_TRUE, result=label, arg1=condition)
    
    def emit_assign(self, dest: str, source: str):
        """
        Emit an assignment
        
        Args:
            dest: Destination variable
            source: Source variable
        """
        self.emit(TACOpcode.ASSIGN, result=dest, arg1=source)
    
    def emit_binary_op(self, opcode: TACOpcode, result: str, 
                       arg1: str, arg2: str):
        """
        Emit a binary operation
        
        Args:
            opcode: Operation code
            result: Result variable
            arg1: First operand
            arg2: Second operand
        """
        self.emit(opcode, result, arg1, arg2)
    
    def emit_unary_op(self, opcode: TACOpcode, result: str, arg: str):
        """
        Emit a unary operation
        
        Args:
            opcode: Operation code
            result: Result variable
            arg: Operand
        """
        self.emit(opcode, result, arg)
    
    def emit_return(self, value: Optional[str] = None):
        """
        Emit a return statement
        
        Args:
            value: Return value (None for void return)
        """
        if value:
            self.emit(TACOpcode.RETURN, arg1=value)
        else:
            self.emit(TACOpcode.RETURN_VOID)
    
    def emit_call(self, func_name: str, num_args: int, 
                  result: Optional[str] = None):
        """
        Emit a function call
        
        Args:
            func_name: Function name
            num_args: Number of arguments
            result: Variable to store result (None for void functions)
        """
        self.emit(TACOpcode.CALL, result=result, arg1=func_name, 
                 arg2=str(num_args))
    
    def emit_param(self, param: str):
        """
        Emit a parameter passing
        
        Args:
            param: Parameter variable
        """
        self.emit(TACOpcode.PARAM, arg1=param)
    
    def emit_read(self, var: str):
        """
        Emit a read operation
        
        Args:
            var: Variable to read into
        """
        self.emit(TACOpcode.READ, result=var)
    
    def emit_print(self, value: str):
        """
        Emit a print operation
        
        Args:
            value: Value to print
        """
        self.emit(TACOpcode.PRINT, arg1=value)
    
    def emit_begin_func(self, func_name: str):
        """
        Emit function begin marker
        
        Args:
            func_name: Function name
        """
        self.emit(TACOpcode.BEGIN_FUNC, result=func_name)
    
    def emit_end_func(self, func_name: str):
        """
        Emit function end marker
        
        Args:
            func_name: Function name
        """
        self.emit(TACOpcode.END_FUNC, result=func_name)
    
    def __str__(self) -> str:
        """String representation of the TAC program"""
        return "\n".join(str(instr) for instr in self.instructions)
    
    def to_list(self) -> List[str]:
        """
        Convert TAC program to list of strings
        
        Returns:
            List of instruction strings
        """
        return [str(instr) for instr in self.instructions]


def format_tac_output(program: TACProgram) -> str:
    """
    Format TAC program for pretty printing
    
    Args:
        program: TAC program
        
    Returns:
        Formatted string
    """
    output = ["=== THREE-ADDRESS CODE ===\n"]
    
    for instr in program.instructions:
        output.append(str(instr))
    
    output.append("\n" + "=" * 30)
    
    return "\n".join(output)
