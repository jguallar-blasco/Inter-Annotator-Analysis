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
            
            username_dict = {'BallotSlate': 0, 'PaperBallot': 0, 
                    'Document': 0, 'Equipment': 0, 'Flag': 0, 'Wreckage': 0, 
                    'BehaviorCrime': 0, 'FinanaicalCrime': 0, 'PoliticalCrime': 0, 'ViolentCrime': 0, 
                    'Building': 0, 'GeographicalArea': 0, 
                    'Installation': 0, 'Structure': 0, 'Way': 0, 
                    'Country': 0, 'OrganizationOfCountries': 0, 'ProvinceState': 0, 'UrbanArea': 0, 
                        'GeographicPoint': 0, 'Land': 0, 'Position': 0, 
                    'Assests': 0, 'Cash': 0, 
                    'Association': 0, 'CommericalOrganization': 0, 'CriminalOrganization': 0, 
                        'Government': 0, 'International': 0, 'MilitaryOrganization': 0, 
                        'PoliticalOrganization': 0, 
                    'Combatant': 0, 'Fan': 0, 'MilitaryPersonnel': 0, 'Police': 0, 
                        'ProfessionalPosition': 0, 'Protester': 0, 'Politician': 0, 
                    'Political': 0,     
                    'NumberPercentageVotes': 0, 'TurnoutVoters': 0, 
                    'Cultural': 0, 'Ideological': 0, 'Poltical': 0, 'Religious': 0, 'Sports': 0, 
                    'Number': 0, 
                    'Aircraft': 0, 'MilitaryVehicle': 0, 'Tocket': 0, 'Watercraft': 0, 
                        'WheeledVehicle': 0, 
                    'Bomb': 0, 'Bullets': 0, 'Cannon': 0, 'Club': 0, 'DaggerKnifeSword': 0, 'Gas': 0, 
                        'GrenadeLauncher': 0, 'Gun': 0, 'MissileSystem': 0, 'ThrownProjectile': 0, 
                    'LOC': 0, 'MON': 0, 'ORG': 0, 'PER': 0,
                        'RES': 0, 'SID': 0, 'TTL': 0, 'VAL': 0, 'VEH': 0, 
                        'WEA': 0, 'BAL': 0, 'COM': 0, 'CRM': 0, 'FAC': 0, 
                        'GPE': 0, 'LAW': 0, -1: 0, 'n/a': 0}

            compare_username_dict = {'HERE': 0, 'BallotSlate': 0, 'PaperBallot': 0,
                    'Document': 0, 'Equipment': 0, 'Flag': 0, 'Wreckage': 0, 
                    'BehaviorCrime': 0, 'FinancialCrime': 0, 'PoliticalCrime': 0, 'ViolentCrime': 0,
                    'Building': 0, 'GeographicalArea': 0,
                    'Installation': 0, 'Structure': 0, 'Way': 0, 
                    'Country': 0, 'OrganizationOfCountries': 0, 'ProvinceState': 0, 'UrbanArea': 0, 
                        'GeographicPoint': 0, 'Land': 0, 'Position': 0, 
                    'Assests': 0, 'Cash': 0,
                    'Association': 0, 'CommericalOrganization': 0, 'CriminalOrganization': 0, 
                        'Government':0, 'International': 0, 'MilitaryOrganization': 0, 
                        'PoliticalOrganization': 0,
                    'Combatant': 0, 'Fan': 0, 'MilitaryPersonnel': 0, 'Police': 0,
                        'ProfessionalPosition': 0, 'Protester': 0, 'Politician': 0,
                    'Political': 0,
                    'NumberPercemtageVotes': 0, 'TurnoutVoters': 0, 
                    'Cultural': 0, 'Ideological': 0, 'Political': 0, 'Religious': 0, 'Sports': 0,
                    'Number': 0,
                    'Aircraft': 0, 'MilitaryVehicle': 0, 'Rocket': 0, 'Watercraft': 0, 
                        'WheeledVehicle': 0, 
                    'Bomb': 0, 'Bullets': 0, 'Cannon': 0, 'Club': 0, 'DagerKnifeSword': 0, 
                        'Gas': 0, 'GrenadeLauncher': 0, 'Gun': 0, 'MissileSystem': 0,
                        'ThrownProjectile': 0, 
                    'LOC': 0, 'MON': 0, 'ORG': 0, 'PER': 0, 'RES': 0, 'SID': 0, 'TTL': 0, 'VAL':0,
                        'VEH': 0, 'WEA': 0, 'BAL': 0, 'COM': 0, 'CRM': 0, 'FAC': 0, 'GPE': 0,
                        'LAW': 0, -1: 0, 'n/a': 0}
            

            for answers in t1:
                    
                for compare_answers in t2:
                    if not compare_answers['HITId'] == answers['HITId']:
                        continue

                    #print(username)
                    #print(compare_username)
                    answer_type = answers['subtype']
                    #if answer_type == 'n/a':
                       # username_dict[answers['type']] += 1
                    #else:
                    username_dict[answer_type] += 1

                    answer_type = compare_answers['subtype']
                    #if answer_type == 'n/a':
                    #    compare_username_dict[compare_answers['type']] += 1
                    #else:
                    compare_username_dict[answer_type] += 1
            
            total += 1

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
            #print(username)
            #print(compare_username)
            print(cohen_kappa_score(user_count, compareuser_count))
            agreement += cohen_kappa_score(user_count, compareuser_count)

        agreement_dict[username].append(agreement/total)
    print(agreement_dict)
    return agreement_dict
                       



# Main function
def main():

    prep_dict = defaultdict(list)
    agreement_dict = defaultdict(list)
    prep_dict = sort_annotations(sys.argv[1], prep_dict)
    del prep_dict['Turkle.Username']
    #del prep_dict['jgualla1']
    agreement_dict = calculate_matches(prep_dict, agreement_dict)

    # Calculate average observed agreement between annotators

    with open("entity_typing_deduped-Results_Kappa_SecondLayer.json", "w") as f1:
        json.dump(agreement_dict, f1)


if __name__=="__main__":
    main()


