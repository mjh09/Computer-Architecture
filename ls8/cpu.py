"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    instructions = {
        130 : 'LDI'
    }
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.register = [0]*8
        self.pc=0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        
        IR = self.pc

        #load 8 into register 0
        # print register 0
        #halt
        running = True
        while running:

            command = self.ram[IR]
            
            #number of instructions
            byte_string = f'{command:b}'
            slice_of_instructs = byte_string[:2]
            num_of_instructs = int(slice_of_instructs,2)
            
            if num_of_instructs == 2:
                operand_a = self.ram_read(IR+1)
                operand_b = self.ram_read(IR+2)

            if num_of_instructs == 1:
                operand_a = self.ram_read(IR+1)

            if command == 0b10000010: # load LDI
                
                load_reg = operand_a # register to load
                val = operand_b # value to insert

                self.register[load_reg] = val
                IR+=3
                continue
            
            elif command == 0b01000111: # print code
                reg_to_print = operand_a # register value is to be printed from
                val_to_print = self.register[reg_to_print] # value from register
                print(val_to_print) # 
                IR+=2
                continue

            elif command == 0b00000001: # halt
                running = False
