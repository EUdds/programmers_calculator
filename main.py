import sys
import tty
import termios
import os

from time import sleep

DEBUG = False

class Interface:
    
    options = ["DEC", "BIN", "HEX", "OCT"]
    option_bases = [10, 2, 16, 8]
    
    def __init__(self):
        self.curr_char = ""
        self.curr_mode = 0
        self.operands = []
        self.curr_base = self.option_bases[self.curr_mode]
        self.prev_base = self.curr_base

    def show_interface(self):
        os.system('clear')
        for idx, option in enumerate(self.options):
            base = self.option_bases[idx]
            if idx == self.curr_mode:
                print("[%s]:" % option, end="\t")
            else:
                print("%s:" % option, end="\t")
            for op_idx, operand in enumerate(self.operands):
                if len(operand) == 0:
                    print(" ", end="\t")
                else:
                    if op_idx % 2 == 0:
                        print("%s" %  self.to_base(operand, self.curr_base, base), end=" ")
                    else:
                        print("%s" % self.operands[op_idx], end=" ")
            print("")
        print("-"*20) 
        print("q: quit, k: previous, j: next")
        debug("%s" % self.operands)
        debug("%s" % self.curr_mode)
        debug("%s" % self.curr_base)
        debug("%s" % self.prev_base)
        debug("Ready to solve? %s" % self.ready_to_solve())
    
    def get_valid_op_inputs(self):
        if self.curr_mode == 0: # DEC
            return [str(i) for i in range(10)]
        elif self.curr_mode == 1: # BIN
            return ["0", "1"]
        elif self.curr_mode == 2: # HEX
            return [str(i) for i in range(10)] + ["A", "B", "C", "D", "E", "F"]
        elif self.curr_mode == 3: # OCT
            return [str(i) for i in range(8)]
    
    def get_valid_operations(self):
        return ["+", "-", "*", "/", ""]
    
    def interact(self, ch):
        if ch == "q":
            sys.exit(1)
        elif ch == "k":
            self.change_mode(self.curr_mode - 1)
        elif ch == "j":
            self.change_mode(self.curr_mode + 1)
        elif ord(ch) == 127:
            if len(self.operands) > 0:
                if len(self.operands[-1]) > 0:
                    self.operands[-1] = self.operands[-1][:-1]
                else:
                    self.operands.pop()
        elif ord(ch) == 10 or ord(ch) == 13:
            self.solve()
        else:
            debug("%s" % ch)
        
    def change_mode(self, mode):
        self.prev_base = self.curr_base
        self.curr_mode = mode % len(self.options)
        self.curr_base = self.option_bases[self.curr_mode]
        self.convert_operands(self.prev_base, self.curr_base)
    

    def convert_operands(self, prev_base, next_base):
        for idx, operand in enumerate(self.operands):
            if len(operand) == 0:
                return
            if idx % 2 == 0:
                self.operands[idx] = self.to_base(operand, prev_base, next_base)

            

    
    def input_operand(self, number):
        if len(self.operands) == 0:
            self.operands.append(number)
        else:
            self.operands[-1] += number



    def get_input(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    
    def can_get_operation(self):
        return len(self.operands) > 0 and len(self.operands[-1]) > 0 and len(self.operands) % 2 == 1
    
    def ready_to_solve(self):
        if len(self.operands) < 3: # Needs to be at least 2 operands and an operation
            return False
        
        if self.operands[-1] in self.get_valid_operations(): # The last operand can't be an operation
            return False
        
        if len(self.operands[-1]) == 0: # The last operand can't be empty
            return False
        
        return True
    
    def solve(self):
        if not self.ready_to_solve():
            raise Exception("Not ready to solve")
        
        # PEMDAS
        PEMDAS = ["*", "/", "+", "-"]

        for operator in PEMDAS:
            while operator in self.operands:
                self.complete_equation(operator)
        




    def complete_equation(self, operation):
        idx = self.operands.index(operation)
        A = self.operands[idx - 1]
        B = self.operands[idx + 1]
        dec_A = self.to_decimal(A)
        dec_B = self.to_decimal(B)
        if operation == "+":
            result = dec_A + dec_B
        elif operation == "-":
            result = dec_A - dec_B
        elif operation == "*":
            result = dec_A * dec_B
        elif operation == "/":
            result = dec_A // dec_B
        self.operands[idx] = self.to_base(str(result), 10, self.curr_base)
        self.operands.pop(idx + 1)
        self.operands.pop(idx - 1)



    def run(self):
        while True:
            self.show_interface()
            ch = self.get_input()
            if ch.upper() in self.get_valid_op_inputs():
                self.input_operand(ch)
            elif (ch in self.get_valid_operations()) and self.can_get_operation():
                self.operands.append(ch)
                self.operands.append("")
            else:
                self.interact(ch)
    
    def to_binary(self, number):
        bin_num = ""
        if int(number) >= 0:
            bin_num = bin(int(number))[2:]
        else:
            bin_num = bin(int(number))[3:]

        # Split into bytes 
        if len(bin_num) > 4: # Only run this if the number is greater than 4 bits
            return self.format_binary_number(bin_num)
        else:
            return bin_num
        
    def format_binary_number(self, bin_num):
        bin_num = bin_num[::-1]
        bytes_inv_le = [bin_num[i:i+4] for i in range(0, len(bin_num), 4)]
        bytes_le = [byte[::-1] for byte in bytes_inv_le]
        bytes_lst = bytes_le[::-1]
        if (len(bytes_lst[0]) < 4): # If the last byte is not full
            padding_amt = 4 - len(bytes_lst[0])
            ext = bytes_lst[0][0] if int(bin_num, 2) < 0 else "0"
            bytes_lst[0] = str(ext * padding_amt) + bytes_lst[0]
        bytes_str = " ".join(bytes_lst)
        return bytes_str
    
    def to_decimal(self, number):
        return int(number, self.curr_base)
    
    def to_hex(self, number):
        return hex(int(number))[2:]
    
    def to_octal(self, number):
        return oct(int(number))[2:]
    
    def to_base(self, number, from_base, base):
        dec_num = str(int(number, from_base))
        if base == 10:
            return dec_num
        elif base == 2:
            return self.to_binary(dec_num)
        elif base == 16:
            return self.to_hex(dec_num)
        elif base == 8:
            return self.to_octal(dec_num)
        else:
            raise ValueError("Invalid base")
    


            

def debug(msg, *args):
    if DEBUG:
        if args:
            print(msg % args)
        else:
            print(msg)

if __name__ == "__main__":
    interface = Interface()
    interface.run()
