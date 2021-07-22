import csv
from collections import defaultdict
import re
import json
import sys

total_m = 0;

def sort_annotations(file, prep_dict):  

    #prep_dict = defaultdict(list)

    # Compile annotator answers according to Turkle.Username
    csv_fh = open(file, 'r', encoding='utf-8')
    reader = csv.DictReader(csv_fh)

    for row in reader:
        argument_spans = json.loads(row['Answer.argument_spans'])
        
        if not row['Turkle.Username'] in prep_dict:
            prep_dict['Turkle.Username'] = []
        
        for argument_span in argument_spans:
            argument_span['HITId'] = row['HITId']
            prep_dict[row['Turkle.Username']].append(argument_span)
        

    #print(prep_dict['jgualla1']);
    #print(prep_dict)
    return(prep_dict)

# Calculate matches
def calculate_matches(prep_dict, total_m):
    for username in prep_dict:
        for compare_username in prep_dict:
            if not username == compare_username:
                for answers in username:
                    print(answers)
                    for compare_answers in compare_username:
                        print(compare_answers)
                        #if (answers['HITTid'] == compare_answers['HITTid']):
                            #print(compare_answers)
                            #print(answers)



# Calculate kappa

def main():
    #total_m = 0;
    prep_dict = defaultdict(list)
    prep_dict = sort_annotations(sys.argv[1], prep_dict)
    calculate_matches(prep_dict, total_m)

    #print(total_m)
    #Po = total_m/total_p
    #Pe = 0


if __name__=="__main__":
    main()


