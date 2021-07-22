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
def calculate_matches(prep_dict, agreement_dict):
    #file = open("results.txt", "w+")

    total = 0
    agreement = 0

    for username in prep_dict:
        total = 0
        agreement = 0
        t1 = prep_dict[username]
        agreement_dict[username] = []
        for compare_username in prep_dict:
            t2 = prep_dict[compare_username]
            if not username == compare_username:
                for answers in t1:
                    #print(answers['HITId'])
                    #print(answers['argument'])
                    #print(answers)
                    for compare_answers in t2:
                        #print(compare_answers)
                        if (answers['HITId'] == compare_answers['HITId'] and answers['argument'][0] == compare_answers['argument'][0]):
                            #file.write(username)
                            #file.write(compare_username)
                            #file.write(answers['HITId'])
                            #file.write(compare_answers['HITId'])
                            #file.write("")
                            total += 1

                            if (answers['startToken'] == compare_answers['startToken'] and answers['endToken'] == compare_answers['endToken']):
                                agreement += 1

        if (total == 0):
            pass
        else:
            agreement_dict[username].append(agreement/total)
    print(agreement_dict)
    return agreement_dict



# Calculate kappa

def main():
    #total_m = 0;
    prep_dict = defaultdict(list)
    agreement_dict = defaultdict(list)
    prep_dict = sort_annotations(sys.argv[1], prep_dict)
    agreement_dict = calculate_matches(prep_dict, agreement_dict)

    total = 0
    turkers = 0
    del agreement_dict['Turkle.Username']
    for averages in agreement_dict:
        total += agreement_dict[averages][0]
        turkers += 1

    print(total/turkers)


if __name__=="__main__":
    main()


