#!/usr/bin/env python 
import bioinfo
import argparse
import gzip as gz
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
parser.add_argument('-l', '--length')
parser.add_argument('-g', '--graph_out', default="graph.png")
args = parser.parse_args()



def init_list(lst: list, length: int, value: float=0.0):
    '''This function takes an empty list and will populate it with
    the value passed in "value". If no value is passed, initializes list
    with length num values of 0.0.'''
    lst = [value] * int(length)
    return lst
    

def populate_list(file: str, seq_length: int):
    """This function will take in a fastq file, read each 4th line for the PHRED score,
        and return a list of the average scores in that position"""
    # Keep track of # of lines and every fourth line
    num_lines: int = 0
    fourth_line: int = 3

    # Init list of our phred scores using our previous function
    phred_score_list: list = []
    phred_score_list = init_list(phred_score_list, seq_length)

    with gz.open(f'{file}', "rt") as fh:
        for i, ASCII_line in enumerate(fh):
            num_lines += 1
            numerical_phred_line = []
            numerical_phred_line = init_list(numerical_phred_line, seq_length)

            if i == fourth_line:
                fourth_line += 4
                
                for j in range(len(ASCII_line)-1):
                    numerical_phred_line[j] = bioinfo.convert_phred(ASCII_line[j])

                for q, score in enumerate(phred_score_list):
                    phred_score_list[q] += numerical_phred_line[q]
                
    return phred_score_list, num_lines

my_list, num_lines = populate_list(args.file, args.length)
QC_score_lines = num_lines/4

for i, ave in enumerate(my_list):
    my_list[i] = my_list[i] / QC_score_lines

# Set the figure size
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

# Plot bar chart with data points
plt.bar(range(1,len(my_list)+1), my_list, color='lightcoral')
plt.title(f"Ave PHRED Score of position in sequences")
plt.xlabel("Sequence Position")
plt.ylabel("Average PHRED Score")

# Display the plot
plt.savefig(args.graph_out)