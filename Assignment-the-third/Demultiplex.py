# Cameron Kunstadt
import bioinfo
import argparse
import gzip

parser = argparse.ArgumentParser()
parser.add_argument('--input_1', '-1')
parser.add_argument('--input_2', '-2')
parser.add_argument('--input_3', '-3')
parser.add_argument('--input_4', '-4')
args = parser.parse_args()

# 30 is a good cutoff for reasonably good data
quality_threshold = 30
unknown_count = 0
index_hopped_count = 0
matched_count_dict = {}

# Open all output files at the beginning
unknown_R1_file = gzip.open("unknown_R1.fq.gz", 'wt+')
unknown_R2_file = gzip.open("unknown_R2.fq.gz", 'wt+')
index_hopped_R1_file = gzip.open("index_hopped_R1.fq.gz", 'wt+')
index_hopped_R2_file = gzip.open("index_hopped_R2.fq.gz", 'wt+')

# Dict for the opened index-matched files
matched_files = {}


def write_out_record(R1, R2, type, index1, index2):
    '''Writes out formatted headers to output fq files'''
    if type == "unknown":
        output_formatted_record(R1, unknown_R1_file, index1, index2)
        output_formatted_record(R2, unknown_R2_file, index1, index2)

    elif type == "index_hopped":
        output_formatted_record(R1, index_hopped_R1_file, index1, index2)
        output_formatted_record(R2, index_hopped_R2_file, index1, index2)

    elif type == "matched":
        if (index1, index2) not in matched_files:
            matched_files[(index1, index2)] = (
                gzip.open(f"{index1}_{index2}_R1.fq.gz", 'wt+'),
                gzip.open(f"{index1}_{index2}_R2.fq.gz", 'wt+')
            )
        matched_R1_file, matched_R2_file = matched_files[(index1, index2)]
        output_formatted_record(R1, matched_R1_file, index1, index2)
        output_formatted_record(R2, matched_R2_file, index1, index2)


def output_formatted_record(strings, infile, index1, index2):
    firstline = True
    for line in strings:
        # For the first line of the record we want to append the indexes
        if firstline:
            infile.write(line + " " + index1 + ":" + index2)
            infile.write('\n')
            firstline = False
        else:
            infile.write(line)
            infile.write('\n')

forward_barcodes = {
    "GTAGCGTA", "CGATCGAT", "GATCAAGG", 
    "AACAGCGA", "TAGCCATG", "CGGTAATC",
    "CTCTGGAT", "TACCGGAT", "CTAGCTCA", 
    "CACTTCAC", "GCTACTCT", "ACGATCAG",
    "TATGGCAC", "TGTTCCGT", "GTCCTAAG", 
    "TCGACAAG", "TCTTCGAC", "ATCATGCG",
    "ATCGTGGT", "TCGAGAGT", "TCGGATTC", 
    "GATCTTGC", "AGAGTCCA", "AGGATAGC"
}

reverse_barcodes = set()

for barcode in forward_barcodes:
    reverse_barcodes.add(bioinfo.rev_comp(barcode))
    
# Open all 4 input files
with gzip.open(args.input_1, 'rt') as R1, gzip.open(args.input_2, 'rt') as R2, \
     gzip.open(args.input_3, 'rt') as R3, gzip.open(args.input_4, 'rt') as R4:
    while True:
        # Hold each record of 4 lines
        R1_record = []
        R2_record = []
        R3_record = []
        R4_record = []

        # Read blocks of 4 lines and save to record
        for i in range(4):
            R1_line = R1.readline()
            R4_line = R4.readline()
            R2_line = R2.readline()
            R3_line = R3.readline()
            if not R1_line or not R4_line or not R2_line or not R3_line:
                break
            R1_record.append(R1_line.strip())
            R2_record.append(R2_line.strip())
            R3_record.append(R3_line.strip())
            R4_record.append(R4_line.strip())
        if not R1_record or not R2_record or not R3_record or not R4_record:
            break

        #Now all the logic stuff of each record should happen here
        sequence = R1_record[1]
        rev_sequence = R4_record[1]
        index1 = R2_record[1]
        index2 = R3_record[1]

        index1_qscore = bioinfo.qual_score(R2_record[3])
        index2_qscore = bioinfo.qual_score(R3_record[3])

        if index1 not in forward_barcodes or index2 not in reverse_barcodes \
            or index1_qscore < quality_threshold or index2_qscore < quality_threshold:
            write_out_record(R1_record, R4_record, "unknown", index1, index2)
            unknown_count += 1
        elif index1 == bioinfo.rev_comp(index2):
            write_out_record(R1_record, R4_record, "matched", index1, index2)
            if index1 not in matched_count_dict:
                matched_count_dict[index1] = 1
            else:
                matched_count_dict[index1] += 1
        else:
            write_out_record(R1_record, R4_record, "index_hopped", index1, index2)
            index_hopped_count += 1

# Close all open output files
unknown_R1_file.close()
unknown_R2_file.close()
index_hopped_R1_file.close()
index_hopped_R2_file.close()
for R1_file, R2_file in matched_files.values():
    R1_file.close()
    R2_file.close()

print(f"Number of unknown records: {unknown_count}")
print(f"Number of index hopped records: {index_hopped_count}")

for key in matched_count_dict:
    print(f"Number of {key} records: {matched_count_dict[key]}")


