import csv
from collections import defaultdict
import re
import json
import sys
from sklearn.metrics import cohen_kappa_score

# Sort_annotations function, organize data according to Turkle.Username
def sort_annotations(file, prep_dict):  

    csv_fh = open(file, 'r', encoding='utf-8')
    reader = csv.DictReader(csv_fh)

    for row in reader:
        argument_spans = json.loads(row['Answer.argument_spans'])
        
        if not row['HITId'] in prep_dict:
            prep_dict['HITId'] = []
        
        for argument_span in argument_spans:
            prep_dict[row['HITId']].append(argument_span)
        
    #print(prep_dict)    
    return(prep_dict)

# Calcualte_matches function, calculate agreement between annotators
def calculate_IAA(prep_dict, agreement_dict):

    for hit in prep_dict:
        cur_answers = prep_dict[hit] 

        total = 0
        agreement = 0
        answer_dict = {'MATCH': 0, 'NOT MATCH': 0}
        compare_answer_dict = {'MATCH': 0, 'NOT MATCH': 0}

        for answer in cur_answers:
            for compare_answer in cur_answers:
                if answer['argument'][0] == compare_answer['argument'][0]:
                    #print(hit)
                    #print(answer)
                    #print(compare_answer)
                    #print()

                    if (answer['startToken'] == compare_answer['startToken'] and
                            answer['endToken'] == compare_answer['endToken']):
                        answer_dict['MATCH'] += 1
                        compare_answer_dict['MATCH'] += 1
                    else:
                        answer_dict['MATCH'] += 1
                        compare_answer_dict['NOT MATCH'] += 1

            total += 1

            answer_count = []
            answer_count.append(answer_dict['MATCH'])
            answer_count.append(0)

            compare_answer_count = []
            compare_answer_count.append(compare_answer_dict['MATCH'])
            compare_answer_count.append(compare_answer_dict['NOT MATCH'])
            
            print(answer_count)
            print(compare_answer_count)
            print(cohen_kappa_score(answer_count, compare_answer_count))
            agreement += cohen_kappa_score(answer_count, compare_answer_count)

        agreement_dict[hit].append(agreement/total)
    print(agreement_dict)



# Main function
def main():
    
    prep_dict = defaultdict(list)
    agreement_dict = defaultdict(list)

    prep_dict = sort_annotations(sys.argv[1], prep_dict)
    del prep_dict['HITId']
    calculate_IAA(prep_dict, agreement_dict) 

    #with open("pilot-Results.json", "w") as f1:
    #    json.dump(agreement_dict, f1)


if __name__=="__main__":
    main()
