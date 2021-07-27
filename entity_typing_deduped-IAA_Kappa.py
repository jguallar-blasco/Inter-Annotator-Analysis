import csv
from collections import defaultdict
import re
import json
import sys
from sklearn.metrics import cohen_kappa_score

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
        
    return(prep_dict)

# Calculate_matches function, calculate agreement between annotators
def calculate_matches(prep_dict, agreement_dict):

    total = 0 #
    agreement = 0 # 

    for username in prep_dict:
        total = 0
        agreement = 0
        t1 = prep_dict[username]

        #print(username)
        #print(t1)
        agreement_dict[username] = []
        for compare_username in prep_dict:
            if username == compare_username:
                continue
            t2 = prep_dict[compare_username]
            
            username_dict = {'LOC': 0, 'MON': 0, 'ORG': 0, 'PER': 0, 
                    'RES': 0, 'SID': 0, 'TTL': 0, 'VAL': 0, 'VEH': 0, 
                    'WEA': 0, 'BAL': 0, 'COM': 0, 'CRM': 0, 'FAC': 0, 
                    'GPE': 0, 'LAW': 0, -1: 0}
            compare_username_dict = {'LOC': 0, 'MON': 0, 'ORG': 0, 'PER': 0,
                    'RES': 0, 'SID': 0, 'TTL': 0, 'VAL': 0, 'VEH': 0, 
                    'WEA': 0, 'BAL': 0, 'COM': 0, 'CRM': 0, 'FAC': 0, 
                    'GPE': 0, 'LAW': 0, -1: 0}

            for answers in t1:
                    
                for compare_answers in t2:
                    if not compare_answers['HITId'] == answers['HITId']:
                        continue

                    #print(username)
                    #print(compare_username)
                    answer_type = answers['type']
                    username_dict[answer_type] += 1

                    answer_type = compare_answers['type']
                    compare_username_dict[answer_type] += 1

            user_count = []
            for count in username_dict:
                user_count.append(username_dict[count])
            
            print(user_count)

            compareuser_count = []
            for count2 in compare_username_dict:
                compareuser_count.append(compare_username_dict[count2])

            print(compareuser_count)


                #print(username)
                #print(compare_username)
            print(username)
            print(compare_username)
            print(cohen_kappa_score(user_count, compareuser_count))
                       



# Main function
def main():

    prep_dict = defaultdict(list)
    agreement_dict = defaultdict(list)
    prep_dict = sort_annotations(sys.argv[1], prep_dict)
    del prep_dict['Turkle.Username']
    del prep_dict['jgualla1']
    calculate_matches(prep_dict, agreement_dict)

    # Calculate average observed agreement between annotators

    with open("entity_typing_deduped-Results.json", "w") as f1:
        json.dump(agreement_dict, f1)


if __name__=="__main__":
    main()


