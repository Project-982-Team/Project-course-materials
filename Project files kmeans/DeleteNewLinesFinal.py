#################
#delete new lines for reference texts
import os
file_path = 'reference_text_files'
#reading text files names from the specified path 
ref_arr = os.listdir(file_path)

for text_name in ref_arr:    

    f = open(file_path + '/' + text_name, 'r', encoding = 'utf-8')
    lines = f.readlines()
    f.close()
    update_lines = {}
    j = 0
    
    #delete newlines
    for i in range(len(lines)):
        if len(lines[i]) - lines[i].count(' ') != 1:
            update_lines[j] = lines[i]
            j += 1
    
    #save changs
    f = open(file_path + '/' + text_name, 'w', encoding = 'utf-8')
    for i in range(len(update_lines)):
        f.writelines("%s" % update_lines[i])
    f.close()
    
#############################
#delete new lines for test reference texts
test_file_path = 'test_reference_text_files'
#reading text files names from the specified path 
test_ref_arr = os.listdir(test_file_path)

for text_name in test_ref_arr:    

    f = open(test_file_path + '/' + text_name, 'r', encoding = 'utf-8')
    lines = f.readlines()
    update_lines = {}
    j = 0
    f.close()
    
    #delete newlines
    for i in range(len(lines)):
        if len(lines[i]) - lines[i].count(' ') != 1:
            update_lines[j] = lines[i]
            j += 1
    
    #save changs
    f = open(test_file_path + '/' + text_name, 'w', encoding = 'utf-8')
    for i in range(len(update_lines)):
        f.writelines("%s" % update_lines[i])
    f.close()