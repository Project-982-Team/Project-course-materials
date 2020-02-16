import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix,classification_report
import os
import re

#################
file_path = 'reference_text_files'
#reading text files names from the specified path 
ref_arr = os.listdir(file_path)

kmeans=KMeans(n_clusters=2)

results = {}

for text_name in ref_arr:
    f = open(file_path + '/' + text_name, "r", encoding = 'utf-8')
    lines = f.readlines()
    
    if len(lines) == 0:
        continue
    
    sentences = []
    
    for i in range(len(lines)):
        d = {}
        #1
        d['length'] = len(lines[i]) - lines[i].count(' ')
        
    
        #2
        if lines[i] == '\n' :
             d['Pattern_Num'] = 0
        else:
            # num. or num) or num-
            lines_split_dot = lines[i].split('.')
            lines_split_paran = lines[i].split(')')
            lines_split_dash = lines[i].split('-')
            if lines_split_dot[0].strip().isdigit() or lines_split_paran[0].strip().isdigit() or lines_split_dash[0].strip().isdigit():
                d['Pattern_Num'] = 1
            else:
                d['Pattern_Num'] = 0
        
        #3
        if i == 0:
            d['Pervious_end_with_dot'] = 1
        else:
            if lines[i-1][len(lines[i-1])-2] == '.':
                d['Pervious_end_with_dot'] = 1
            else:
                d['Pervious_end_with_dot'] = 0
            
        #4
        if lines[i] == '\n' :
             d['Pattern_dash'] = 0
        else:
            # -
            lines_split_dash = lines[i].split('-')
            if lines_split_dot[0].strip()=='':
                d['Pattern_dash'] = 1
            else:
                d['Pattern_dash'] = 0
        
        sentences.append(d)
    #################################
    
    df = pd.DataFrame.from_dict(sentences)
    print(df)
    kmeans.fit(df)
        
    print(df.head())

#################################
#################################
first_line = 0
not_first_line = 1

test_file_path = 'test_reference_text_files'
#reading text files names from the specified path 
test_ref_arr = os.listdir(test_file_path)

for text_name in test_ref_arr:

    print(text_name + ' : \n')
    f = open(test_file_path + '/' + text_name, "r", encoding = 'utf-8')
    lines = f.readlines()
    
    string_result = ""
    list_result = []
    
    if len(lines) == 0:
        list_result.append("No references !")
        results[text_name] = list_result
        continue
    
    sentences = []

    for i in range(len(lines)):
        d = {}
        #1
        d['length'] = len(lines[i]) - lines[i].count(' ')
        
    
    
        #2
        if lines[i] == '\n' :
             d['Pattern_Num'] = 0
        else:
            # num. or num) or num-
            lines_split_dot = lines[i].split('.')
            lines_split_paran = lines[i].split(')')
            lines_split_dash = lines[i].split('-')
            if lines_split_dot[0].strip().isdigit() or lines_split_paran[0].strip().isdigit() or lines_split_dash[0].strip().isdigit():
                d['Pattern_Num'] = 1
            else:
                d['Pattern_Num'] = 0
        
        #3
        if i == 0:
            d['Pervious_end_with_dot'] = 1
        else:
            if lines[i-1][len(lines[i-1])-2] == '.':
                d['Pervious_end_with_dot'] = 1
            else:
                d['Pervious_end_with_dot'] = 0
            
        #4
        if lines[i] == '\n' :
             d['Pattern_dash'] = 0
        else:
            # -
            lines_split_dash = lines[i].split('-')
            if lines_split_dot[0].strip()=='':
                d['Pattern_dash'] = 1
            else:
                d['Pattern_dash'] = 0
        
        sentences.append(d)
    
    df = pd.DataFrame.from_dict(sentences)
    print(df)
    listt = kmeans.predict(df)

    
    first_line = listt[0]
    not_first_line = listt[0] ^ 1
    
    #Reference body
    inside = 0
    for counter in range(len(lines)):
        string_result = re.sub("\n", "", string_result)
        if listt[counter] == first_line:
            if string_result != "":
                list_result.append(string_result)
            string_result = lines[counter]
        else:
            string_result += lines[counter]
    
    # for last refrence
    string_result = re.sub("\n", "", string_result)
    if string_result != "":
         list_result.append(string_result)
    
    results[text_name] = list_result

#test
print("\n check output...")
for value in results["paper86.txt"] :
    print(value)
    print("---------------------------------------------")