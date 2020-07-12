from glob import glob
from os import path
from src.data_process import do_process


def main():
    exps = glob(path.join(".", "input_data", "*"))

    for exp in exps:
        do_process(exp)
