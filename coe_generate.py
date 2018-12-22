import os
from config import cfg
import shutil

def coe_generate(main, handler, coe):
    header = [
        "memory_initialization_radix=16;",
        "memory_initialization_vector="
    ]
    code = open(main).readlines()
    handler = open(handler).readlines()

    code = list(map(lambda line: line[:-1] + ",", code))
    handler = list(map(lambda line: line[:-1] + ",", handler))
    pad = ["00000000," for i in range((0x4180 - len(code) - 0x3000) // 4)]

    coe_file = header + code + pad + handler + ["00000000;"]


    write_file(coe_file, coe)

def write_file(program, file_dir):
    program = list(map(lambda x: x + "\n", program))
    open(file_dir, "w").writelines(program)

def code_gen(filename):
    os.system("call mars_code.cmd {}".format(filename))
    shutil.copy("code.txt", cfg.isim_code_dir)
    shutil.copy("code_handler.txt", cfg.isim_code_dir)

if __name__=="__main__":
    code_gen(r"C:\Users\Eadral\Desktop\学习\6系\计组\P8\mips_program\simple.asm")

    path = cfg.isim_code_dir
    coe_generate(os.path.join(path, "code.txt"), os.path.join(path, "code_handler.txt"), os.path.join(path, "code.coe"))
