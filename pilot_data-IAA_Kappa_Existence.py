import csv
from collections import defaultdict
import re
import json
import sys
from sklearn.metrics import cohen_kappa_score
import statistics

# Sort_annotations function, organize data according to Turkle.Username
def sort_annotations(file, prep_dict, sentence_dict):  

    csv_fh = open(file, 'r', encoding='utf-8')
    reader = csv.DictReader(csv_fh)

    for row in reader:
        argument_spans = json.loads(row['Answer.argument_spans'])
        sentence_spans = json.loads(row['Input.json_data'])
        
        if not row['Turkle.Username'] in prep_dict:
            prep_dict['Turkle.Username'] = []

        #if not row['HITId'] in sentence_dict:
        #    sentence_dict['HITId'] = []
        
        for argument_span in argument_spans:
            argument_span['HITId'] = row['HITId']
            prep_dict[row['Turkle.Username']].append(argument_span)

        
        sentence_dict[row['HITId']].append(sentence_spans['sentences'])
        sentence_dict[row['HITId']].append(sentence_spans['bleachedGloss'])

    #print(sentence_dict)
    #print(prep_dict)    
    return(prep_dict, sentence_dict)

# Calcualte_matches function, calculate agreement between annotators
def calculate_IAA(prep_dict, agreement_dict, sentence_dict):

    results = open('existence_examples.txt', 'w')

    for username in prep_dict:

        total = 0
        agreement = 0
        agreements = []
        t1 = prep_dict[username]

        for compare_username in prep_dict:
            if username == compare_username:
                continue
            t2 = prep_dict[compare_username]
            answer_count = []
            compare_answer_count = []
            answer_dict = {'EXISTS': 0, 'DOES NOT EXIST': 0}
            compare_answer_dict = {'EXISTS': 0, 'DOES NOT EXIST': 0}
            
            for answers in t1:
                for compare_answers in t2:
                    if not compare_answers['HITId'] == answers['HITId']:
                        continue

                    if answers['argument'][0] == compare_answers['argument'][0]:
                        a1 = False
                        a2 = False

                        if (answers['startToken'] == -1 and answers['endToken'] == -1):
                            answer_count.append(0)
                        else:
                            answer_count.append(1)
                            a1 = True
                    
                        if (compare_answers['startToken'] == -1 and compare_answers['endToken'] == -1):
                            compare_answer_count.append(0)
                        else:
                            compare_answer_count.append(1)
                            a2 = True

                        if a1 != a2:
                            results.writelines('Annotator 1 says that the existence of ' +
                                    str(answers['argument'][1]) + ' is ' + str(a1) + 
                                    ' while Annotator 2 says that the existence of ' +
                                    str(compare_answers['argument'][1])
                                    + ' is ' + str(a2))

                            results.writelines('\n')
                            results.writelines('Looking for: ')
                            for items in sentence_dict[answers['HITId']][1]:
                                #results.writelines("Looking for: ")
                                results.writelines(items)
                            #results.writelines(sentence_dict[answers['HITId']][1])
                            results.writelines('\n')
                            results.writelines('Text: ')
                            for items in sentence_dict[answers['HITId']][0]:
                                for item in items:
                                    results.writelines(item)
                                    results.writelines(' ')
                            #results.writelines(sentence_dict[answers['HITId']][0])
                            results.writelines('\n')
                            results.writelines('\n')

                    else:
                        continue

            total += 1

            agreement += cohen_kappa_score(answer_count, compare_answer_count)
            agreements.append(cohen_kappa_score(answer_count, compare_answer_count))

        agreement_dict[username].append(agreement/total)
        agreement_dict[username].append(statistics.median(agreements))
        agreement_dict[username].append(agreements)
    #for key in agreement_dict:
        #print(key,': ', agreement_dict[key])



# Main function
def main():
    
    prep_dict = defaultdict(list)
    sentence_dict = defaultdict(list)
    agreement_dict = defaultdict(list)

    prep_dict, sentence_dict = sort_annotations(sys.argv[1], prep_dict, sentence_dict)
    del prep_dict['Turkle.Username']
    calculate_IAA(prep_dict, agreement_dict, sentence_dict) 

    #with open("pilot-Results.json", "w") as f1:
    #    json.dump(agreement_dict, f1)


if __name__=="__main__":
    main()
