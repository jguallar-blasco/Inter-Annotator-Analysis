import csv
from collections import defaultdict
import re
import json


prep_dict = defaultdict(list)

# Compile annotator answers according to HIT
csv_fh = open('pilot_data-Batch_863_results.csv', 'r', encoding='utf-8')
reader = csv.DictReader(csv_fh)

for row in reader:
    prep_dict[row['HITId']]
    argument_spans = json.loads(row['Answer.argument_spans'])
    for argument_span in argument_spans:
        #print(argument_span)
        prep_dict[row['HITId']].append(argument_span)
        #print()
    #print()
        

#print(prep_dict);

# Calculate matches
total_p = 0
total_m = 0
first = 0

for hit in prep_dict:
    cur_arguments = prep_dict[hit]
    for argument in cur_arguments:
        cur_argument = argument['argument']
        if (cur_argument[0] == 'arg1'):
            if (first == 0):
                check_startToken = argument['startToken']
                check_endToken = argument['endToken']
                total_p += 1
                first = 1
            else:
                startToken = argument['startToken']
                endToken = argument['endToken']
                total_p += 1
                if (check_startToken == startToken and check_endToken == endToken):
                    total_m += 1
    first = 0; 

# Calculate kappa

Po = total_m/total_p
Pe = ()

k = (Po-Pe)/(1-Pe)
print(k)

