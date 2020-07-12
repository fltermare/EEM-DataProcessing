from glob import glob
from os import path
from src.data_process import do_process
from src.prog_config import INPUT_DATA_DIR, OUTPUT_DIR


def main():
    exps = glob(path.join(*INPUT_DATA_DIR, "*"))

    for exp in exps:
        do_process(exp, OUTPUT_DIR)
