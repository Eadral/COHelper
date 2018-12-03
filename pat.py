from config import cfg
import os
import shutil


def pat(filename):
    os.system("@echo off")

    os.system("rm isim_output.txt")

    os.system("call mars_code.cmd {}".format(filename))
    shutil.copy("code.txt", cfg.isim_code_dir)
    os.system("call {}".format(cfg.isim_test_cmd))
    shutil.copy(cfg.isim_output, "isim_output.txt")
    os.system("call {} {}".format(cfg.mars_test_cmd, filename))
    return compare("mars_output.txt", "isim_output.txt")

def compare(fileA, fileB):
    A = open(fileA).readlines()
    B = open(fileB).readlines()

    A = list(filter(lambda l: l.find("@") >= 0, A))
    B = list(filter(lambda l: l.find("@") >= 0, B))

    A = list(map(lambda l: l[l.find("@"):-1], A))
    B = list(map(lambda l: l[l.find("@"):-1], B))

    if len(A) != len(B):
        return -1, "different line number: except {} lines while found {} lines".format(len(A), len(B))

    for i in range(len(A)):
        if A[i] != B[i]:
            return -1, "except '{}' while found '{}'".format(A[i], B[i])

    return 0, "Accepted"


if __name__ == "__main__":
    # print(pat(r"C:\Users\Eadral\Desktop\学习\6系\计组\P5_P6\control_test_cases_1\sb.asm"))
    # print(pat(r"C:\Users\Eadral\Desktop\学习\6系\计组\P5_P6\auto_test_cases_1\auto_test_2018-12-03-10-48-57.asm"))

    print(pat(r"C:\Users\Eadral\Desktop\学习\6系\计组\P5_P6\weak.asm"))
