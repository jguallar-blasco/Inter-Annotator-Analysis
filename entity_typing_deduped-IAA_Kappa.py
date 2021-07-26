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
        agreement_dict[username] = []
        for compare_username in prep_dict:
            t2 = prep_dict[compare_username]
            
            username_dict = {'LOC': 0, 'MON': 0, 'ORG': 0, 'PER': 0, 
                    'RES': 0, 'SID': 0, 'TTL': 0, 'VAL': 0, 'VEH': 0, 
                    'WEA': 0, 'BAL': 0, 'COM': 0, 'CRM': 0, 'FAC': 0, 
                    'GPE': 0, 'LAW': 0}
            compare_username_dict = {'LOC': 0, 'MON': 0, 'ORG': 0, 'PER': 0,
                    'RES': 0, 'SID': 0, 'TTL': 0, 'VAL': 0, 'VEH': 0, 
                    'WEA': 0, 'BAL': 0, 'COM': 0, 'CRM': 0, 'FAC': 0, 
                    'GPE': 0, 'LAW': 0}

            if not username == compare_username:
                print(t1)
                for answers in t1:
                    answer_type = answers['type']
                    print(answer_type)
                    print('HIIIIIIIII')
                    username_dict[answer_type] += 1
                print(username_dict)
                    
                for compare_answers in t2:
                    answer_type = compare_answers['type']
                    compare_username_dict[answer_type] += 1
                print(username_dict)

                user_count = []
                for count in username_dict:
                    user_count.append(username_dict[count])

                compareuser_count = []
                for count in compare_username_dict:
                    compareuser_count.append(compare_username_dict[count])

                print(username)
                print(compare_username)
                print(cohen_kappa_score(user_count, compareuser_count))
                        

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


