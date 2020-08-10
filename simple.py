PRINT_ANIKA = 0b00000001
PRINT_NUM = 0b00000010
HALT = 0b00000011
SAVE = 0b00000100
PRINT_REGISTER = 0b00000101
ADD = 0b00000110


PRINT_ANIKA,
PRINT_ANIKA,
PRINT_NUM,
99,
SAVE,
# Save the number 42 into register 2
42,
# What arguments does SAVE require?
2,
SAVE,
42,
3,
ADD,
2,
3,
PRINT_REGISTER, # should print 84
2,
HALT

memory = []

running = True
program_counter = 0

#Registers
#R0 - R7
registers = [None] * 8

while running:
    command = memory[program_counter]

    if command == PRINT_ANIKA:
        print('Anika!')
        program_counter += 1

    elif command == PRINT_NUM:
        program_counter += 1
        print(memory[program_counter])
        program_counter += 1

    elif command == SAVE:
        program_counter += 1
        number = memory[program_counter]
        program_counter += 1
        registers[memory[program_counter]] = number
        program_counter += 1

    elif command == PRINT_REGISTER:
        program_counter += 1
        index = memory[program_counter]
        print(registers[index])
        program_counter += 1

    elif command == ADD:
        program_counter += 1
        reg1 = memory[program_counter]
        program_counter += 1
        reg2 = memory[program_counter]
        registers[reg1] += registers[reg2]
        program_counter += 1

    elif command == HALT:
        running = False

    else:
        print('Command not recognized!')
