from glob import glob
from os import path
from src.data_process import do_process, construct_blank, construct_sample, get_names
from src.prog_config import TEST_INPUT_DATA_DIR, TEST_OUTPUT_DIR, SAMPLE, BLANK
import numpy as np
import pandas as pd


def test_get_names():

    exp_path = path.join(*TEST_INPUT_DATA_DIR, "test_exp1")
    names = get_names(exp_path, SAMPLE)
    ans = sorted(['0124 SCX3 230 123', '0124 SCX3 230 550'])

    assert ans == sorted(names)


def test_construct_sample():

    exp_path = path.join(*TEST_INPUT_DATA_DIR, "test_exp1")
    res_df = construct_sample(exp_path, "0124 SCX3 230 123")

    ans_path = path.join(*TEST_INPUT_DATA_DIR, "test_exp1", "20200711.xlsx")
    ans_df = pd.read_excel(ans_path, sheet_name='data', index_col=0)

    assert np.array_equal(np.around(res_df.values, 6), np.around(ans_df.values, 6))


def test_construct_blank():
    
    exp_path = path.join(*TEST_INPUT_DATA_DIR, "test_exp1")
    res_df, res_sum = construct_blank(exp_path)

    ans_sum = 2614.957
    ans_path = path.join(*TEST_INPUT_DATA_DIR, "test_exp1", "20200711.xlsx")
    ans_df = pd.read_excel(ans_path, sheet_name='blank', index_col=0)

    assert res_sum == ans_sum
    assert np.array_equal(np.around(res_df.values, 6), np.around(ans_df.values, 6))


def test_do_process():
    import shutil
    import os

    exps = glob(path.join(*TEST_INPUT_DATA_DIR, "*"))
    for exp in exps:
        do_process(exp, TEST_OUTPUT_DIR)

    res_num_exp = len(glob(path.join(*TEST_OUTPUT_DIR, "*")))
    res_num_csv = len(glob(path.join(*TEST_OUTPUT_DIR, "*", "*.csv")))
    res_num_config = len(glob(path.join(*TEST_OUTPUT_DIR, "*", "*.txt")))

    ans_num_config = ans_num_exp = 2
    ans_num_csv = 8

    # clean up
    test_output_dir = path.join(*TEST_OUTPUT_DIR)
    shutil.rmtree(test_output_dir)
    os.mkdir(test_output_dir)


    assert res_num_exp == ans_num_exp
    assert res_num_csv == ans_num_csv
    assert res_num_config == ans_num_config
