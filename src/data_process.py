import config
import os
import shutil
import pandas as pd

from datetime import datetime
from glob import glob
from os import path

from src.compare import compare
from src.prog_config import BLANK, SAMPLE


def to_matrix(exp_path, data_type, prefix):
    """Load data and convert to dataframe from a file

    Args:
        exp_path: path to experiment
        data_type: blank or sample
        prefix: file prefix
    Return:
        df: dataframe
    """

    tmp = []
    for i in range(config.n):
        filename = path.join(exp_path, data_type, prefix + "#%02d.sp" % (i + 1))

        flag_LS45 = flag_data = False
        col_idx = None
        row_idx = []
        vals = []

        with open(filename, "r") as fp:
            for row in fp:
                row = row.strip()
                if not flag_LS45 and row == "LS45":
                    flag_LS45 = True
                    continue
                if not flag_data and row == "#DATA":
                    flag_data = True
                    continue

                if flag_LS45:
                    col_idx = float(row)
                    flag_LS45 = False

                if flag_data and row:
                    idx, val = row.split()
                    row_idx.append(float(idx))
                    vals.append(float(val))

        s = pd.Series(vals, name=col_idx, index=row_idx)
        tmp.append(s)

    df = pd.concat(tmp, axis=1)
    assert df.shape == (config.m, config.n)

    return df


def get_names(exp_path, data_type):
    """Get list of name from given directory

    Args:
        exp_path: path to experiment
        data_type: blank or sample
    Return:
        names: list of name
    """

    path2dir = path.join(exp_path, data_type, "*.sp")
    names = set()
    for x in glob(path2dir):
        basename = path.basename(x).split("#")[0]
        names.add(basename)

    if data_type == BLANK:
        assert len(names) == 1, "Detect Multiple blanks in [%s]" % exp_path

    return list(names)


def construct_blank(exp_path):
    names = get_names(exp_path, BLANK)
    df = to_matrix(exp_path, BLANK, names[0])

    blank_sum = 0

    # calculate sum
    for idx, value in df[float(config.sum_col)].iteritems():
        if float(idx) < float(config.sum_row_start):
            continue
        elif float(config.sum_row_end) < float(idx):
            break
        else:
            blank_sum += float(value)

    blank_sum = round(blank_sum, 6)

    return df, blank_sum


def construct_sample(exp_path, name):
    df = to_matrix(exp_path, SAMPLE, name)
    return df


def prepare_output_env(exp_name_date, base_output_dir):

    try:
        output_dir = path.join(*base_output_dir, exp_name_date)
        os.mkdir(output_dir)
    except OSError:
        print("Creation of the directory %s failed" % output_dir)
    else:
        print("Successfully created the directory %s" % output_dir)

    config_path = path.join(*base_output_dir, exp_name_date, "config.txt")
    shutil.copyfile(path.join(".", "config.py"), config_path)


def do_process(exp_path, base_output_dir):
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M_%S")

    exp_name = path.basename(exp_path)
    exp_name_date = "_".join([dt_string, exp_name])

    if exp_name == "sample_exp":
        return

    # check env
    prepare_output_env(exp_name_date, base_output_dir)

    blank_matrix, blank_sum = construct_blank(exp_path)

    names = get_names(exp_path, SAMPLE)
    for name in names:
        sample_matrix = construct_sample(exp_path, name)
        data = compare(blank_matrix, blank_sum, sample_matrix)

        # output ITN
        filename = "_".join([name, "ITN", dt_string]) + ".csv"
        path_itn = path.join(*base_output_dir, exp_name_date, filename)
        data["ITN"].to_csv(path_itn)
        print("[Done]", path_itn)

        # output RU
        filename = "_".join([name, "RU", dt_string]) + ".csv"
        path_ru = path.join(*base_output_dir, exp_name_date, filename)
        data["RU"].to_csv(path_ru)
        print("[Done]", path_ru)
