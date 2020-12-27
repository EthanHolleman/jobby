import argparse
import pathlib

JOBBY_PATH = pathlib.Path(__file__).parent.absolute()
TEMPLATES_PATH = JOBBY_PATH.joinpath('templates')
SBATCH_SIGNATURE = '''
# This batch file was created using Jobby, a scrappy
# Python program built to make Ethan Holleman's life
# a bit easier.
'''

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def sbatch_from_template_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--template', help='Path to sbatch template')
    parser.add_argument('-w', '--working_dir', help='Path to run job from')
    parser.add_argument('-n', '--name', help='Name of the job')
    return parser