import csv
from collections import defaultdict
import re
import json
import sys
from sklearn.metrics import cohen_kappa_score
import statistics

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
        agreements = []
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
                    'PoliceMisconduct': 0, 'Terrorism': 0,
                    'Building': 0, 'GeographicalArea': 0, 'Installation': 0, 'Structure': 0, 'Way': 0,
                        'ApartmentBuilding': 0, 'GovernmentBuilding': 0, 'House': 0, 'OfficeBuilding': 0,
                        'School': 0, 'StoreShop': 0, 'VotingFacility': 0, 'Border': 0, 'CheckPoint': 0,
                        'Airport': 0, 'MilitaryInstallation': 0, 'TrainStation': 0, 'TrainStation': 0,
                        'Barricade': 0, 'Bridge': 0, 'Plaza': 0, 'Tower': 0, 'Highway': 0, 'Street': 0,
                    'Country': 0, 'OrganizationOfCountries': 0, 'ProvinceState': 0, 'UrbanArea': 0,
                        'City': 0, 'Village': 0,
                    'GeographicPoint': 0, 'Land': 0, 'Position': 0, 'Address': 0, 'Continent': 0, 
                        'AirSpace': 0, 'CrimeScene': 0, 'Neighborhood': 0, 'Region': 0,
                    'Assests': 0, 'Cash': 0, 
                    'Association': 0, 'CommericalOrganization': 0, 'CriminalOrganization': 0, 
                        'Government': 0, 'International': 0, 'MilitaryOrganization': 0, 
                        'PoliticalOrganization': 0, 'Club': 0, 'Team': 0, 'BroadcastingCompany': 0,
                        'Corportation': 0, 'Manufacturer': 0, 'NewsAgency': 0, 'CriminalOrganization': 0,
                        'Agency': 0, 'Council': 0, 'FireDepartment': 0, 'LawEnforcementAgency': 0,
                        'LegislativeBody': 0, 'ProsecutorOffice': 0, 'Railway': 0, 'Commission': 0,
                        'MonitoringGroup': 0, 'GovernmentArmedForces': 0, 'Intelligence': 0, 
                        'NonGovernmentMilitia': 0, 'Court': 0, 'Party': 0,
                    'Combatant': 0, 'Fan': 0, 'MilitaryPersonnel': 0, 'Police': 0, 
                        'ProfessionalPosition': 0, 'Protester': 0, 'Politician': 0, 
                        'Political': 0, 'Mercenary': 0, 'Sniper': 0, 'SportsFan': 0, 'ChiefOfPolice': 0,
                        'Govenor': 0, 'HeadOfGovernment': 0, 'Mayor': 0, 'Ambassador': 0, 
                        'Firefighter': 0, 'Journalist': 0, 'Minister': 0, 'MedicalPersonnel': 0, 
                        'Scientist': 0, 'Spy': 0, 'ProtestLeader': 0, 'Spokesperson': 0,
                        'MilitaryOfficer': 0,
                    'NumberPercentageVotes': 0, 'TurnoutVoters': 0, 
                    'Cultural': 0, 'Ideological': 0, 'Poltical': 0, 'Religious': 0, 'Sports': 0,
                        'Opposition': 0,
                    'Number': 0, 
                    'Aircraft': 0, 'MilitaryVehicle': 0, 'Tocket': 0, 'Watercraft': 0, 
                        'WheeledVehicle': 0, 'Aircraft': 0, 'CargoAircraft': 0, 'Drone': 0, 
                        'Helicopter': 0, 'FighterAircraft': 0, 'MilitaryBoat': 0,
                        'MilitaryTransportAircraft': 0, 'Tank': 0, 'Boat': 0, 'Yacht': 0, 'Bus': 0,
                        'Car': 0, 'FireApparatus': 0, 'Train': 0, 'Truck': 0,
                    'Bomb': 0, 'Bullets': 0, 'Cannon': 0, 'Club': 0, 'DaggerKnifeSword': 0, 'Gas': 0, 
                        'GrenadeLauncher': 0, 'Gun': 0, 'MissileSystem': 0, 'ThrownProjectile': 0,
                        'Grenade': 0, 'MolotivCocktail': 0, 'Ammunition': 0, 'LiveRounds': 0, 
                        'RubberBullets': 0, 'Cannon': 0, 'Bat': 0, 'Hatchet': 0, 'PoisonGas': 0,
                        'TearGas': 0, 'Artillery': 0, 'Firearm': 0, 'AirToMissile': 0,
                        'MissileLauncher': 0, 'Missile': 0, 'SurfaceToAirMissile': 0, 
                        'Rock': 0, 'AntiAircraftMissle': 0, 'MilitaryEquipment': 0,  
                    'LOC': 0, 'MON': 0, 'ORG': 0, 'PER': 0,
                        'RES': 0, 'SID': 0, 'TTL': 0, 'VAL': 0, 'VEH': 0, 
                        'WEA': 0, 'BAL': 0, 'COM': 0, 'CRM': 0, 'FAC': 0, 
                        'GPE': 0, 'LAW': 0, -1: 0}

            compare_username_dict = {'BallotSlate': 0, 'PaperBallot': 0, 
                    'Document': 0, 'Equipment': 0, 'Flag': 0, 'Wreckage': 0, 
                    'BehaviorCrime': 0, 'FinanaicalCrime': 0, 'PoliticalCrime': 0, 'ViolentCrime': 0,
                        'PoliceMisconduct': 0, 'Terrorism': 0,
                    'Building': 0, 'GeographicalArea': 0, 'Installation': 0, 'Structure': 0, 'Way': 0,
                        'ApartmentBuilding': 0, 'GovernmentBuilding': 0, 'House': 0, 'OfficeBuilding': 0,
                        'School': 0, 'StoreShop': 0, 'VotingFacility': 0, 'Border': 0, 'CheckPoint': 0,
                        'Airport': 0, 'MilitaryInstallation': 0, 'TrainStation': 0, 'TrainStation': 0,
                        'Barricade': 0, 'Bridge': 0, 'Plaza': 0, 'Tower': 0, 'Highway': 0, 'Street': 0,
                    'Country': 0, 'OrganizationOfCountries': 0, 'ProvinceState': 0, 'UrbanArea': 0,
                        'City': 0, 'Village': 0,
                    'GeographicPoint': 0, 'Land': 0, 'Position': 0, 'Address': 0, 'Continent': 0, 
                        'AirSpace': 0, 'CrimeScene': 0, 'Neighborhood': 0, 'Region': 0,
                    'Assests': 0, 'Cash': 0, 
                    'Association': 0, 'CommericalOrganization': 0, 'CriminalOrganization': 0, 
                        'Government': 0, 'International': 0, 'MilitaryOrganization': 0, 
                        'PoliticalOrganization': 0, 'Club': 0, 'Team': 0, 'BroadcastingCompany': 0,
                        'Corportation': 0, 'Manufacturer': 0, 'NewsAgency': 0, 'CriminalOrganization': 0,
                        'Agency': 0, 'Council': 0, 'FireDepartment': 0, 'LawEnforcementAgency': 0,
                        'LegislativeBody': 0, 'ProsecutorOffice': 0, 'Railway': 0, 'Commission': 0,
                        'MonitoringGroup': 0, 'GovernmentArmedForces': 0, 'Intelligence': 0, 
                        'NonGovernmentMilitia': 0, 'Court': 0, 'Party': 0,
                    'Combatant': 0, 'Fan': 0, 'MilitaryPersonnel': 0, 'Police': 0, 
                        'ProfessionalPosition': 0, 'Protester': 0, 'Politician': 0, 
                        'Political': 0, 'Mercenary': 0, 'Sniper': 0, 'SportsFan': 0, 'ChiefOfPolice': 0,
                        'Govenor': 0, 'HeadOfGovernment': 0, 'Mayor': 0, 'Ambassador': 0, 
                        'Firefighter': 0, 'Journalist': 0, 'Minister': 0, 'MedicalPersonnel': 0, 
                        'Scientist': 0, 'Spy': 0, 'ProtestLeader': 0, 'Spokesperson': 0,
                        'MilitaryOfficer': 0,
                    'NumberPercentageVotes': 0, 'TurnoutVoters': 0, 
                    'Cultural': 0, 'Ideological': 0, 'Poltical': 0, 'Religious': 0, 'Sports': 0,
                        'Opposition': 0,
                    'Number': 0, 
                    'Aircraft': 0, 'MilitaryVehicle': 0, 'Tocket': 0, 'Watercraft': 0, 
                        'WheeledVehicle': 0, 'Aircraft': 0, 'CargoAircraft': 0, 'Drone': 0, 
                        'Helicopter': 0, 'FighterAircraft': 0, 'MilitaryBoat': 0,
                        'MilitaryTransportAircraft': 0, 'Tank': 0, 'Boat': 0, 'Yacht': 0, 'Bus': 0,
                        'Car': 0, 'FireApparatus': 0, 'Train': 0, 'Truck': 0,
                    'Bomb': 0, 'Bullets': 0, 'Cannon': 0, 'Club': 0, 'DaggerKnifeSword': 0, 'Gas': 0, 
                        'GrenadeLauncher': 0, 'Gun': 0, 'MissileSystem': 0, 'ThrownProjectile': 0,
                        'Grenade': 0, 'MolotivCocktail': 0, 'Ammunition': 0, 'LiveRounds': 0, 
                        'RubberBullets': 0, 'Cannon': 0, 'Bat': 0, 'Hatchet': 0, 'PoisonGas': 0,
                        'TearGas': 0, 'Artillery': 0, 'Firearm': 0, 'AirToMissile': 0,
                        'MissileLauncher': 0, 'Missile': 0, 'SurfaceToAirMissile': 0, 
                        'Rock': 0, 'AntiAircraftMissle': 0, 'MilitaryEquipment': 0,  
                    'LOC': 0, 'MON': 0, 'ORG': 0, 'PER': 0,
                        'RES': 0, 'SID': 0, 'TTL': 0, 'VAL': 0, 'VEH': 0, 
                        'WEA': 0, 'BAL': 0, 'COM': 0, 'CRM': 0, 'FAC': 0, 
                        'GPE': 0, 'LAW': 0, -1: 0}
            

            for answers in t1:
                    
                for compare_answers in t2:
                    if not compare_answers['HITId'] == answers['HITId']:
                        continue

                    #print(username)
                    #print(compare_username)
                    answer_type = answers['subsubtype']
                    if answer_type == 'n/a':
                       answer_type = answers['subtype']
                       if answer_type == 'n/a':
                           username_dict[answers['type']] += 1
                       else: 
                           username_dict[answer_type] += 1
                    else:
                        username_dict[answer_type] += 1

                    answer_type = compare_answers['subsubtype']
                    if answer_type == 'n/a':
                        answer_type = compare_answers['subtype']
                        if answer_type == 'n/a':
                            compare_username_dict[compare_answers['type']] += 1
                        else:
                            compare_username_dict[answer_type] +1
                    else:
                        compare_username_dict[answer_type] += 1
            
            total += 1

            user_count = []
            for count in username_dict:
                user_count.append(username_dict[count])
            
            #print(user_count)

            compareuser_count = []
            for count2 in compare_username_dict:
                compareuser_count.append(compare_username_dict[count2])

            #print(compareuser_count)


                #print(username)
                #print(compare_username)
            #print(username)
            #print(compare_username)
            #print(cohen_kappa_score(user_count, compareuser_count))

            agreements.append(cohen_kappa_score(user_count, compareuser_count))
            agreement += cohen_kappa_score(user_count, compareuser_count)

        agreement_dict[username].append(agreement/total)
        agreement_dict[username].append(statistics.median(agreements))
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

    with open("entity_typing_deduped-Results_Kappa_ThirdLayer.json", "w") as f1:
        json.dump(agreement_dict, f1)


if __name__=="__main__":
    main()


