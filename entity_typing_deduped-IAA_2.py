import csv
from collections import defaultdict
import re
import json
import sys

# Sort_annotatons functions, organized data according to Turkle.Username
def sort_annotations(file, prep_dict):  

    csv_fh = open(file, 'r', encoding='utf-8')
    reader = csv.DictReader(csv_fh)

    for row in reader:
        argument_spans = json.loads(row['Answer.entity_typing'])
        
        if not row['Turkle.Username'] in prep_dict:
            prep_dict['Turkle.Username'] = []
        
        for argument_span in argument_spans:
            argument_span['HITId'] = row['HITId']
            prep_dict[row['Turkle.Username']].append(argument_span)
       
    for user in prep_dict:
        print(user)
        print()
    return(prep_dict)

# Calculate_matches function, calculate agreement between annotators
def calculate_matches(prep_dict, agreement_dict):

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
                    
                    for compare_answers in t2:
                        
                        if (answers['HITId'] == compare_answers['HITId'] 
                                and answers['argument'][0] == compare_answers['argument'][0]):
                            total += 1

                            if (answers['type'] == compare_answers['type'] 
                                    and answers['subtype'] == compare_answers['subtype'] 
                                    and answers['subsubtype'] == compare_answers['subsubtype']):
                                agreement += 1

        if (total == 0):
            pass
        else:
            # Calculate observed agreement for annotator
            agreement_dict[username].append(agreement/total)
    
    #print(agreement_dictt)
    return agreement_dict



# Main function
def main():

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

    # Calculate average observed agreement between annotators
    print(round((total/turkers),2))

    with open("entity_typing_deduped-Results.json", "w") as f1:
        json.dump(agreement_dict, f1)


if __name__=="__main__":
    main()


