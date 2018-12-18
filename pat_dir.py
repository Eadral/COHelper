import os
from pat import pat
import random

def pat_dir(dir):

    filenames = os.listdir(dir)
    random.shuffle(filenames)
    for filename in filenames:
        if filename.split(".")[-1] != "asm":
            continue
        ac, error = pat(os.path.join(dir, filename))
        if ac != 0:
            return -1, "Error in {}".format(filename) + ": " + error

    return 0, "Accepted"

def pat_dirs(dirs):
    for dir in dirs:
        ac, error = pat_dir(dir)
        if ac != 0:
            return error
    return "Accepted"


if __name__ == "__main__":
    print(pat_dir(r"C:\Users\Eadral\Desktop\学习\6系\计组\P5_P6\modified_auto_test_cases_1"))
