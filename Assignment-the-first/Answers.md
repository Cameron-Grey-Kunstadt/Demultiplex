# Assignment the First

## Part 1
1. Be sure to upload your Python script. Provide a link to it here:

[perbase_dist.py](perbase_dist.py)


| File name                    | label  | Read length | Phred encoding |
| ---------------------------- | ------ | ----------- | -------------- |
| 1294_S1_L008_R1_001.fastq.gz | Read1  | 101         | 33             |
| 1294_S1_L008_R2_001.fastq.gz | Index1 | 8           | 33             |
| 1294_S1_L008_R3_001.fastq.gz | Index2 | 8           | 33             |
| 1294_S1_L008_R4_001.fastq.gz | Read2  | 101         | 33             |
2. Per-base NT distribution
    1. Use markdown to insert your 4 histograms here.

    R1:
    
    ![R1](R1_graph.png)
    

    R2:
    
    ![R2](R2_graph.png)

    R3:
    
    ![R3](R3_graph.png)

    R4:
    
    ![R4](R4_graph.png)

    2. What is a good quality score cutoff for index reads and biological read pairs to utilize for sample identification and downstream analysis, respectively? Justify your answer.


	I would think that for our index reads, our Qscores should have a higher cutoff, as low quality indexes will have a high likelyhood of messing up the identification of a specific sequence, and there are only 8 basepairs to work with, so they should be of high quality and held to a higher standard. I suggest atleast Q30, so errors are 1 in 1000.

	The biological reads I think can be a bit more lenient (depending on what our actually purposes of the research are), and there are 101 basepairs on each read to work with, so each single basepair is likely not quite as important. I think somewhere around Q20 to Q25 would be an appropriate cutoff point. 


 
     3. How many indexes have undetermined (N) base calls? (Utilize your command line tool knowledge. Submit the command(s) you used. CHALLENGE: use a one-line command)

```
zcat 1294_S1_L008_R2_001.fastq.gz | sed -n '2~4p' | grep -c "N"
3976613

zcat 1294_S1_L008_R3_001.fastq.gz | sed -n '2~4p' | grep -c "N"
3328051
```
    
## Part 2
1. Define the problem

The problem is that we have dual-matched sequencing data where index hopping occurred. So we have some of our sequenced with incorrect indexes, and some with indexes with low quality scores.


2. Describe output

```
    1. Reads that have indexes that are matching (reverse compliments of each other), that are both in our set of barcodes, and are of good quality.
    2. Reads that have indexes that are in our sets of barcodes, are of good quality, but are NOT matching.
    3. Reads where one or both of the indexes are not in our set of barcodes, or where one or both of them have too low of a Q score. 
```

3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
4. Pseudocode

[Pseudocode](First_assignment_Part2_Psuedocode.pdf)

5. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement

```
def rev_comp(input_string):
''' returns reverse compliment of input_string'''
	returns rev_comp

x = rev_comp(ATC)
print("x is:",x)
```
x is GAT
```

def add_index_to_header(header, index1, index2)
'''returns the header with the indexes added appropriately, I'm not sure exactly how i'm going to format the headers yet'''
	returns new_header

index1, index2 = 'AAA', 'TTT'
old_header = "NUM12300000:123:123:1::453; 213 23"
new_header = add_index_to_header(old_header, index1, index2)
print(new_header)
```
NUM12300000:123:123:1::453; 213 23 AAA TTT
```


def qual_score(phred_score: str) -> float:
    '''Calculates average phred score for a string of character phred scores'''
    sum_score = 0
    for letter in phred_score:
        score = convert_phred(letter)
        sum_score += score
    return sum_score / len(phred_score)
```
This is already in bioinfo and it has been unit tested.
```
def write_out_record(strings, file, perm)
	'''all the code to write out our formatted headers to a specific file, given the permissions of write, or append'''

Function does not return anything, just writes the given strings out to a given file.
```
