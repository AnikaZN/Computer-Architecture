"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [None] * 256
        self.pc = 0
        self.reg = [None] * 8
        self.reg[7] = 0xF4
        self.running = True

    def ram_read(self, ignore, address):
        return self.ram[address]

    def ram_write(self, ignore, value, address):
        self.ram[address] = value

    def HLT(self, ignore, ignore2, ignore3):
        self.running = False

    def LDI(self, ignore, regnum, value):
        self.reg[regnum] = value
        self.pc += 3

    def PRN(self, ignore, regnum, ignore2):
        print(self.reg[regnum])
        self.pc += 2

    def PUSH(self, ignore, ignore2, ignore3):
        self.reg[7] -= 1
        reg_idx = self.ram[self.pc + 1]
        push_value = self.reg[reg_idx]
        sp = self.reg[7]
        self.ram[sp] = push_value
        self.pc += 2

    def POP(self, ignore, ignore2, ignore3):
        sp = self.reg[7]
        pop_value = self.ram[sp]
        reg_idx = self.ram[self.pc + 1]
        self.reg[reg_idx] = pop_value
        self.reg[7] += 1
        self.pc += 2

    def load(self):
        """Load a program into memory."""

        address = 0

        try:
            with open(sys.argv[1], 'r') as file:
                for line in file:
                    comment_split = line.split('#')

                    possible_num = comment_split[0]

                    if possible_num == '':
                        continue

                    if possible_num[0] == '1' or possible_num[0] == '0':
                        num = possible_num[:8]
                        #print(f'{num}: {int(num, 2)}')

                        self.ram[address] = int(num, 2)
                        address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} not found')

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        command_dict = {1 : self.HLT,
                        69 : self.PUSH,
                        70 : self.POP,
                        71 : self.PRN,
                        130 : self.LDI,
                        162 : self.alu}

        while self.running:

            ir = self.ram[self.pc]

            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]

            if ir == 162:
                program = ir
                op = "MUL"
            else:
                program = ir
                op = None

            command_dict[program](op, operand_a, operand_b)
