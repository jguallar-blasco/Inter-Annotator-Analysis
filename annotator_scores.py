import csv
import json
from collections import defaultdict

# RESULTS
with open('pilot-Results.json') as f1:
    data_1 = json.load(f1)

with open('pilot-Results_IgnoreExistence.json') as f2:
    data_3 = json.load(f2)

with open('entity_typing_deduped-Results_Kappa.json') as f3:
    data_2 = json.load(f3)

with open('entity_typing_deduped-Results_Kappa_SecondLayer.json') as f4:
    data_4 = json.load(f4)

with open('entity_typing_deduped-Results_Kappa_SecondLayer.json') as f5:
    data_5 = json.load(f5)


# STATS
time_dict = defaultdict(list)

csv_fh = open('pilot_data-Batch_863_stats.csv', 'r', encoding='utf-8')
reader = csv.DictReader(csv_fh)

for row in reader:
    time_dict[row['\ufeffUsername']] = []
    time_dict[row['\ufeffUsername']].append(row['Median Time'])

csv_fh = open('entity_typing_deduped-Batch_866_stats.csv', 'r', encoding='utf-8')
reader = csv.DictReader(csv_fh)

for row in reader:
    time_dict[row['\ufeffUsername']].append(row['Mean Time'])


#print(time_dict)


# Calculate annoator score and compile all stats
compiled_dict = defaultdict(list)

for user in time_dict:

    # DATA FOR PILOT
    compiled_dict[user] = []
    compiled_dict[user].append(data_1[user][0])
    
    # DATA FOR PILOT IGNORING EXISTENCE
    try:
        compiled_dict[user].append(data_3[user][0])
    except KeyError:
        compiled_dict[user].append("No IAA for pilot_data ignoring existence")


    # DATA FOR ENTITY_TYPING KAPPA MEAN
    try:
        compiled_dict[user].append(data_2[user][0])
    except KeyError:
        compiled_dict[user].append("No IAA for entity_typing")
    
    # DATA FOR ENTITY_TYPING MEDIAN
    try: 
        compiled_dict[user].append(data_2[user][1])
    except KeyError:
        compiled_dict[user].append("No Median IAA for entity_typing")


    # DATA FOR PILOT MEDIAN TIME
    compiled_dict[user].append(time_dict[user][0])
    
    # DATA FOR ENTITY_TYPING MEDIAN TIME
    try:
        compiled_dict[user].append(time_dict[user][1])
    except IndexError:
        compiled_dict[user].append("No average time for entity_typing")

    #Compute global score
    lambda1 = 1
    lambda2 = 1

    try:
        globalscore = 1000 * float(compiled_dict[user][0]) * float(lambda1) * (1/float(compiled_dict[user][2]))
    except Exception:
        globalscore = None
        globalscore = 'No global score'
    try:
        globalscore += 1000 * float(compiled_dict[user][1]) * float(lambda2) * (1/float(compiled_dict[user][3]))
    except Exception:
        globalscore = None
        globalscore = 'No global score'

    compiled_dict[user].append(globalscore)


#print(compiled_dict)

# Outputting to csv file
csv_format_list = []

for user in compiled_dict:
    cur_dict = {}
    cur_dict['Turkle Username'] = user
    cur_dict['Pilot Data Agreement (Raw)'] = compiled_dict[user][0]
    cur_dict['Pilot Data Agreement Ignoring Existence (Raw)'] = compiled_dict[user][1]
    cur_dict['Pilot Data Average Time'] = compiled_dict[user][4]
    cur_dict['Entity Typing Agreement'] = compiled_dict[user][2]
    cur_dict['Entity Typing Agreement Median'] = compiled_dict[user][3]
    cur_dict['Entity Typing Average Time'] = compiled_dict[user][5]
    cur_dict['Annotator Score'] = compiled_dict[user][6]
    csv_format_list.append(cur_dict)

print(csv_format_list)

csv_format_list_filtered = filter(None, csv_format_list)

with open('annotator_scores-Results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Turkle Username', 'Pilot Data Agreement (Raw)', 'Pilot Data Agreement Ignoring Existence (Raw)', 'Pilot Data Average Time', 
            'Entity Typing Agreement', 'Entity Typing Agreement Median', 'Entity Typing Average Time', 'Annotator Score']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for item in csv_format_list_filtered:
        writer.writerow(item)

