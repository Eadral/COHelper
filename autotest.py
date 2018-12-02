import random
from copy import copy
import datetime
import os
from pat import pat

n_reg = 5
n_line = 100
num_range = 10


instrs = [
    # "add $r, $r, $r",
    "addu $r, $r, $r",
    # "sub $r, $r, $r",
    "subu $r, $r, $r",
    "sllv $r, $r, $r",
    "srlv $r, $r, $r",
    "srav $r, $r, $r",
    "and $r, $r, $r",
    "or $r, $r, $r",
    "xor $r, $r, $r",
    "nor $r, $r, $r",
]

registers = ["$0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7", "$t8", "$t9", ]

def generate_init():
    init = [
        "li $t0, *",
        "li $t1, *",
        "li $t2, *",
        "li $t3, *",
        "li $t4, *",
        "li $t5, *",
        "li $t6, *",
        "li $t7, *",
        "li $t8, *",
        "li $t9, *",
    ]
    program = []
    for i in range(n_reg):
        program.append(init[i].replace("*", str(random.randint(-num_range, num_range))))
    return program

def generate_r(instr):
    instr = copy(instr)
    for i in range(3):
        instr = instr.replace("$r", random.choice(registers[:n_reg+1]), 1)
    return instr

def generate_statement(instr):
    if instr.find("$r") > 0:
        return generate_r(instr)
    else:
        raise NotImplementedError("Not Implemented Instruction: {}".format(instr))

def generate():
    program = []
    program += generate_init()
    for i in range(n_line):
        program.append(generate_statement(random.choice(instrs)))
    return program

def write_file(program, file_dir):
    program = list(map(lambda x: x + "\n", program))
    open(file_dir, "w").writelines(program)

def autotest(dir, times):
    for i in range(times):
        filename = "{}_{}.asm".format("auto_test", datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        file_dir = os.path.join(dir, filename)
        program = generate()
        write_file(program, file_dir)
        ac, error = pat(file_dir)
        if ac != 0:
            return ac, error
    return 0, "Accepted"


if __name__ == "__main__":
    # print(generate())
    print(autotest(r"C:\Users\Eadral\Desktop\学习\6系\计组\P5_P6\auto_test_cases_1", 10))

