import random
from copy import copy
import datetime
import os
from pat import pat

n_reg = 5
n_line = 100
n_address = 10
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
    "slt $r, $r, $r",
    "sltu $r, $r, $r",

    "lw $m, *($0)",
    "lh $m, *($0)",
    "lhu $m, *($0)",
    "lb $m, *($0)",
    "lbu $m, *($0)",
    "sw $m, *($0)",
    "sb $m, *($0)",
    "sh $m, *($0)",

    # "addi $i, $i, *",
    "addiu $i, $i, *",
    "andi $i, $i, *",
    "ori $i, $i, *",
    "xori $i, $i, *",
    "lui $i, *",
    "slti $i, $i, *",
    "sltiu $i, $i, *",

    "sll $w, $w, *",
    "srl $w, $w, *",
    "sra $w, $w, *",

    "mult $x, $x",
    "multu $x, $x",
    "div $x, $x",
    "divu $x, $x",
    "mfhi $x",
    "mflo $x",
    "mthi $x",
    "mtlo $x",

    "beq $b, $b, label@",
    "bne $b, $b, label@",
    "blez $b, label@",
    "bgtz $b, label@",
    "bltz $b, label@",
    "bgez $b, label@",

    "j label@",
    "jal label@",
    "jalr $j, $j",
    "jr $j",
]

registers = ["$0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7", ]
address = ["$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7", "$t8", "$t9", ]


def generate_init():
    init = [
        "li $s0, *",
        "li $s1, *",
        "li $s2, *",
        "li $s3, *",
        "li $s4, *",
        "li $s5, *",
        "li $s6, *",
        "li $s7, *",
    ]
    program = []
    for i in range(n_reg):
        program.append(init[i].replace("*", str(random.randint(-num_range, num_range))))
    return program


def generate_address():
    init = [
        "la $t0, *",
        "la $t1, *",
        "la $t2, *",
        "la $t3, *",
        "la $t4, *",
        "la $t5, *",
        "la $t6, *",
        "la $t7, *",
        "la $t8, *",
        "la $t9, *",
    ]
    program = []
    for i in range(n_address-1):
        program.append(init[i].replace("*", "label{}".format(random.randint(10*(i+1), 10*(i+2)))))
    program.append(init[n_address-1].replace("*", "label{}".format(n_line)))
    return program


def choice_reg(num_reg=n_reg):
    return random.choice(registers[:num_reg+1])


def choice_address(i):
    return "$t{}".format(i // 10)


def replace(instr, template, target):
    return instr.replace(template, str(target), 1)


def generate_r(instr):
    instr = copy(instr)
    for i in range(3):
        instr = replace(instr, "$r", choice_reg())
    return instr


def generate_m(instr):
    instr = copy(instr)
    instr = replace(instr, "$m", choice_reg())
    if instr.find("b") >= 0:
        instr = replace(instr, "*", random.randint(0, num_range))
    elif instr.find("h") >= 0:
        instr = replace(instr, "*", random.randint(0, num_range) >> 1 << 1)
    elif instr.find("w") >= 0:
        instr = replace(instr, "*", random.randint(0, num_range) >> 2 << 2)
    else:
        raise NameError("Unexpected Instruction: {}".format(instr))
    return instr


def generate_i(instr):
    instr = copy(instr)
    instr = replace(instr, "$i", choice_reg())
    instr = replace(instr, "$i", choice_reg())
    if instr.find("lui") >= 0:
        instr = replace(instr, "*", random.randint(0, 0xff))
    else:
        instr = replace(instr, "*", random.randint(-num_range, num_range))
    return instr


def generate_x(instr):
    instr = copy(instr)
    instr = replace(instr, "$x", choice_reg())
    instr = replace(instr, "$x", choice_reg())
    return instr


def generate_w(instr):
    # shift
    instr = copy(instr)
    instr = replace(instr, "$w", choice_reg())
    instr = replace(instr, "$w", choice_reg())
    instr = replace(instr, "*", random.randint(0, 0b11111))
    return instr

def choice_label(i):
    label = random.randint(i+1, i+10)
    if label > 100:
        label = 100
    return label

def generate_b(instr, i):
    instr = copy(instr)
    instr = replace(instr, "$b", choice_reg())
    instr = replace(instr, "$b", choice_reg())
    instr = replace(instr, "@", choice_label(i))
    return instr


def generate_j(instr, i):
    instr = copy(instr)
    instr = replace(instr, "@", choice_label(i))
    if instr.find("jr") >= 0:
        instr = replace(instr, "$j", choice_address(i))
    elif instr.find("jalr") >= 0:
        instr = replace(instr, "$j", choice_reg())
        instr = replace(instr, "$j", choice_address(i))
    return instr

def generate_statement(instr, i):
    if instr.find("$r") >= 0:
        return generate_r(instr)
    elif instr.find("$m") >= 0:
        return generate_m(instr)
    elif instr.find("$i") >= 0:
        return generate_i(instr)
    elif instr.find("$x") >= 0:
        return generate_x(instr)
    elif instr.find("$w") >= 0:
        return generate_w(instr)
    elif instr.find("$b") >= 0:
        return generate_b(instr, i)
    elif instr.find("j") >= 0:
        return generate_j(instr, i)
    else:
        raise NotImplementedError("Not Implemented Instruction: {}".format(instr))


def find_delayed_unpredictable(instr):
    return instr.find("$b") >= 0 or instr.find("$j") >= 0 or instr.find("j") >= 0


def choice_instr(last_instr):
    delayed = find_delayed_unpredictable(last_instr)
    if delayed:
        instr = random.choice(instrs)
        while find_delayed_unpredictable(instr):
            instr = random.choice(instrs)
        return instr
    else:
        return random.choice(instrs)


def generate():
    program = []
    program += generate_init()
    program += generate_address()
    last_instr = ""
    for i in range(n_line):
        instr = choice_instr(last_instr)
        program.append("label{}: ".format(i) + generate_statement(instr, i))
        last_instr = instr
    program.append("label{}:".format(n_line))
    return program


def write_file(program, file_dir):
    program = list(map(lambda x: x + "\n", program))
    open(file_dir, "w").writelines(program)


def autotest(dir, times=0xffffffff):
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
    print(autotest(r"C:\Users\Eadral\Desktop\学习\6系\计组\P5_P6\auto_test_cases_1"))

