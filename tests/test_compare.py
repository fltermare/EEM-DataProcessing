from glob import glob
from os import path
from src.data_process import construct_blank, construct_sample
from src.compare import compare
from src.prog_config import TEST_INPUT_DATA_DIR, TEST_OUTPUT_DIR, SAMPLE, BLANK
import numpy as np
import pandas as pd


def test_ITN_RU():
    exp_path = path.join(*TEST_INPUT_DATA_DIR, "test_exp1")

    sample_df = construct_sample(exp_path, "0124 SCX3 230 123")
    blank_df, blank_sum = construct_blank(exp_path)

    data = compare(blank_df, blank_sum, sample_df)

    ans_path = path.join(*TEST_INPUT_DATA_DIR, "test_exp1", "20200711.xlsx")
    itn_df = pd.read_excel(ans_path, sheet_name="result (ITN)", index_col=0)
    ru_df = pd.read_excel(ans_path, sheet_name="result (RU)", index_col=0)

    assert np.array_equal(np.around(itn_df.values, 6), np.around(data["ITN"].values, 6))
    assert np.array_equal(np.around(ru_df.values, 6), np.around(data["RU"].values, 6))
