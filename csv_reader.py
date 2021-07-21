import csv
from collections import defaultdict
import re

#def parse_csv(args):
prep_dict = defaultdict(list)
count = 1; 
with open('pilot_data-Batch_863_results.csv', 'rt') as f1:
    reader = csv.reader(f1, skipinitialspace=True);
    for line in reader:

        if line[0] in prep_dict:
            for thing in line[12]:
                print(thing)
            prep_dict[line[0]].append(line[12]);
        else:
            prep_dict[line[0]].append(line[12]);
        

#print(prep_dict);

for key in prep_dict:
    dict = prep_dict[key]
    #print(dict)

#def main(args):
    #print(parse_csv(args.csv));
