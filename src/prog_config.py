import configparser
from os import path


TEST_INPUT_DATA_DIR = [".", "tests", "data", "input_data"]
TEST_OUTPUT_DIR = [".", "tests", "data", "output"]

INPUT_DATA_DIR = [".", "input_data"]
OUTPUT_DIR = [".", "output"]

BLANK = "blank"
SAMPLE = "samples"

# load configuration from config.ini
config = configparser.ConfigParser()
config.read(path.join(".", "config.ini"))

m = int(config['parameter']['m'])
n = int(config['parameter']['n'])
sum_col = float(config['parameter']['sum_col'])
sum_row_start = float(config['parameter']['sum_row_start'])
sum_row_end = float(config['parameter']['sum_row_end'])
