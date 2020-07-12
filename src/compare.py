import numpy as np
import pandas as pd


def ITN(blank_matrix, sample_matrix):
    diff = np.subtract(sample_matrix.values, blank_matrix.values)
    diff = diff.clip(min=0)
    diff = np.around(diff, decimals=6)
    diff = pd.DataFrame(diff, index=blank_matrix.index, columns=blank_matrix.columns)

    return diff


def RU(blank_matrix, blank_sum, sample_matrix):
    diff = np.subtract(sample_matrix.values, blank_matrix.values)
    diff /= blank_sum
    diff = diff.clip(min=0)
    diff = np.around(diff, decimals=6)
    diff = pd.DataFrame(diff, index=blank_matrix.index, columns=blank_matrix.columns)

    return diff


def compare(blank_matrix, blank_sum, sample_matrix):

    res = {}

    df_itn = ITN(blank_matrix, sample_matrix)
    res["ITN"] = df_itn

    df_ru = RU(blank_matrix, blank_sum, sample_matrix)
    res["RU"] = df_ru

    return res
