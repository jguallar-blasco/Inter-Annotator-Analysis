import csv
from collections import defaultdict
import re
import json
import sys

total_m = 0;

def sort_annotations(file):

    prep_dict = defaultdict(list)

    # Compile annotator answers according to HIT
    csv_fh = open(file, 'r', encoding='utf-8')
    reader = csv.DictReader(csv_fh)

    for row in reader:
        prep_dict[row['HITId']]
        argument_spans = json.loads(row['Answer.argument_spans'])
        for argument_span in argument_spans:
            #print(argument_span)
            prep_dict[row['HITId']].append(argument_span)
            #print()

    return prep_dict
        

#print(prep_dict);

# Calculate matches
def calculate_matches(prep_dict, total_m):
    first = 0;
    for hit in prep_dict:
        cur_arguments = prep_dict[hit]
        for argument in cur_arguments:
            cur_argument = argument['argument']
            if (cur_argument[0] == 'arg1'):
                if (first == 0):
                    check_startToken = argument['startToken']
                    check_endToken = argument['endToken']
                    #total_p += 1
                    first = 1
                else:
                    startToken = argument['startToken']
                    endToken = argument['endToken']
                    #total_p += 1
                    if (check_startToken == startToken and check_endToken == endToken):
                        total_m += 1
        first = 0;

    return(total_m)

# Calculate kappa

def main():
    total_m = 0;
    prep_dict = sort_annotations(sys.argv[1])
    total_m = calculate_matches(prep_dict, total_m)

    print(total_m)
    #Po = total_m/total_p
    Pe = 0


if __name__=="__main__":
    main()


