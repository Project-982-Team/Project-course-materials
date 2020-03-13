import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score
import os
import re

#################
file_path = 'reference_text_files'
#reading text files names from the specified path 
ref_arr = os.listdir(file_path)

kmeans=KMeans(n_clusters=2)

results = {}
real_results = {}
train_ref_num = 0;

for text_name in ref_arr:
    f = open(file_path + '/' + text_name, "r", encoding = 'utf-8')
    lines = f.readlines()
    f.close()
    
    train_ref_num += 1
    
    if len(lines) == 0:
        continue
    
    sentences = []
    
    for i in range(len(lines)):
        d = {}
        #1
#        d['length'] = len(lines[i]) - lines[i].count(' ')
        
    
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
        
        #5
        y = re.sub(" ", "", lines[i])
        x = re.search("\.\(\d+\)\.", y)
        if x == None:
            d['year'] = 0
        else:
            #print("Here --> "+ y)
            d['year'] = 1
        
        #6
       
          
        sentences.append(d)
    #################################
    
    df = pd.DataFrame.from_dict(sentences)
   # print(df)
    kmeans.fit(df)
        
  #  print(df.head())

#################################
#################################
first_line = 0
not_first_line = 1

test_file_path = 'test_reference_text_files'
sep_test_file_path = 'separated_test_reference_text_files'
#reading text files names from the specified path 
test_ref_arr = os.listdir(test_file_path)
test_ref_num = 0;
ref_lines_accuracy = 0;
ref_text_accuracy = 0;
#ref_accuracy = 0;
#ref_precision_positive = 0;
#ref_recall_positive = 0;
#ref_precision_negative = 0;
#ref_recall_negative = 0;

for text_name in test_ref_arr:

#    print('\n' + text_name + ' : ')
    f = open(test_file_path + '/' + text_name, "r", encoding = 'utf-8')
    lines = f.readlines()
    f.close()
    
    f = open(sep_test_file_path + '/' + text_name, "r", encoding = 'utf-8')
    sep_lines = f.readlines()
    f.close()
    
    sep_listt = []
    
    string_result = ""
    list_result = []
    sep_list_result = []
    
    if len(lines) == 0:
        list_result.append("No references !")
        results[text_name] = list_result
        continue
    
    sentences = []

    for i in range(len(lines)):
        d = {}
        #1
#        d['length'] = len(lines[i]) - lines[i].count(' ')
        
    
    
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
        
        #5
        y = re.sub(" ", "", lines[i])
        x = re.search("\.\(\d+\)\.", y)
        if x == None:
            d['year'] = 0
        else:
            #print("Here --> "+ y)
            d['year'] = 1
        
        #6
            
        sentences.append(d)
    
    
    df = pd.DataFrame.from_dict(sentences)
    listt = kmeans.predict(df)

    
    first_line = listt[0]
    not_first_line = listt[0] ^ 1
    
    for i in range(len(sep_lines)):
        if i == 0:
            sep_listt.append(first_line)
            string_result = re.sub("\n", "", sep_lines[i])
        else:
            if sep_lines[i] == '\n':
                sep_list_result.append(re.sub("\n", "", string_result))
                string_result = ""
                if i == len(sep_lines) - 2:
                    break
                    
            else:
                if sep_lines[i-1] == '\n':
                    sep_listt.append(first_line)
                    string_result = sep_lines[i]
                else:
                    sep_listt.append(not_first_line)
                    string_result += sep_lines[i]

    real_results[text_name] = sep_list_result
    corrects = 0
    text_corrects = 0


    
    #Reference body
    inside = 0
    for counter in range(len(lines)):
        #lines accuracy
        if listt[counter] == sep_listt[counter]:
            corrects += 1
        
        #text accuracy
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
    
    for r in list_result:
        if r in real_results[text_name]:
            text_corrects += 1
     
    
    print("________________________________________________________________________")
    print('\nResults for {} :: '.format(text_name))
    target_names = ['first line', 'not first line']
    print("\n",classification_report(sep_listt, listt, target_names = target_names))
    print('Accuracy is {} % '.format(100 * accuracy_score(sep_listt, listt)))
#    print('Lines Accuracy : {} %'.format(100*corrects / len(lines)))
#    print('Reference text Accuracy : {} %\n'.format(100*text_corrects / len(real_results[text_name])))
    

    

#print("\nlines accuracy \t\t", round(ref_lines_accuracy/test_ref_num , 2) , "%")
#print("text accuracy \t\t", round(ref_text_accuracy/test_ref_num , 2) ,"%")
#print("accuracy \t\t", round(100*ref_accuracy/test_ref_num , 2) ,"%")
#print("precision positive \t", round(100*ref_precision_positive/test_ref_num , 2) , "%")
#print("precision negative \t", round(100*ref_precision_negative/test_ref_num , 2) ,"%")
#print("recall positive \t", round(100*ref_recall_positive/test_ref_num , 2) , "%")
#print("recall negative \t", round(100*ref_recall_negative/test_ref_num , 2) ,"%")


#test
#test_str = "paper310.txt"
#print("\n check output for " + test_str + " ...")
#for value in results[test_str] :
#    print(value)
#    print("---------------------------------------------")