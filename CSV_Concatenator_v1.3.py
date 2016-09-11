'''
CSV-file Concatenator v1.3
Created by Ryan Thorpe 09/04/2016
This tool is designed specifically for use with datasets from BASS
'''


import pandas as pd
import sys, os


#Function where user enters folder path
def enter_folder():
    
    try:
        folder = raw_input("\nEnter the complete folder pathway which contains the files you wish to concatenate (all files in this folder will be concatenated, so be sure they are all homogeneously formatted): ")
    except:
        print "\n\tInvalid entry! Try again."
        enter_folder()
    return folder

#Function where user enters csv delimiter
def enter_delimiter():
    
    try:
        sep = raw_input("\nDelimiter: ")
    except:
        print "\n\tInvalid entry! Try again."
        enter_delimiter()
    return sep    

#Function where user enters which axis long which to combine dataframes
def enter_axis():
    
    axis = raw_input("\nCombine rows or columns (r/c)? ").lower()
    
    #User error control
    if axis == 'rows':
        axis = 'r'
    elif axis == 'columns':
        axis = 'c'
    elif (axis != 'r') & (axis != 'c'):
        print "\n\tInvalid entry! Try again."
        enter_axis()
    return axis

#Function where user chooses columns to exclude when combining columns or rows to exclude when combining rows
def enter_exclude_columns_or_rows(c_or_r):
    
    #User error control
    valid_input = False    
    while valid_input == False:
        choice = raw_input("\nDo you wish to exclude any %s (y/n)? " % c_or_r).lower()

        if choice == 'yes':
            choice = 'y'
        elif choice == 'no':
            choice = 'n'
        if (choice != 'y') & (choice != 'n'):
            print "\n\tInvalid entry! Try again."
            valid_input = False
        valid_input = True
    
    #Enter columns or rows to exclude
    if choice == 'y':
        
        #User error control
        valid_input = False
        while valid_input == False:
            try:
                del_c = eval(raw_input("\nEnter the indices of the %s you wish to exclude (comma separated): " % c_or_r))
                try:
                    del_c = list(del_c)
                except:
                    del_c = [int(del_c)]
                valid_input = True

            except:
                print "\n\tInvalid entry! Try again."
                continue

    elif choice == 'n':
        del_c = None
    return del_c

#User enters the index of the column or row that contains the indices for all rows or colunms, respectively
def enter_index_column_or_row(c_or_r):

    #User error control
    valid_input = False
    while valid_input == False:
        try:
            indices = eval(raw_input("\nWhich %s determines the indices parallel to the concatenation axis (enter %s index or \"None\" for arbitrary indices)? " % (c_or_r, c_or_r)))
            valid_input = True
        except:
            print "\n\tInvalid entry! Try again."
            continue

    return indices
    
def concat_wrapper(files):
            
    delimiter = enter_delimiter()
    axis = enter_axis()

    if axis == 'r':

        del_r = enter_exclude_columns_or_rows('rows')
        ind_r = enter_index_column_or_row('row')

        #Initialize lists
        df_list = []
        df_key = []

        #Add data files to list
        for f in files:
            try:
                data = pd.read_csv(f, header=ind_r, index_col=0, sep=delimiter)

            except:
                data = pd.read_csv(f, header=ind_r, index_col=0, sep=delimiter)
            
            #Delete excluded rows
            if del_r != None:
                labels = []
                for i in del_r:
                    labels.append(data.axes[0][i])
                data = data.drop(labels, axis=0)

            df_list.append(data)
            df_key.append(f)

        combined_data = pd.concat(df_list, axis=0, keys = df_key, ignore_index=False)

    elif axis == 'c':

        del_c = enter_exclude_columns_or_rows('columns')
        ind_c = enter_index_column_or_row('column')

        #Initialize lists
        df_list = []
        df_key = []

        #Add data files to list
        for f in files:
            try:
                data = pd.read_csv(f, header=0, index_col=ind_c, sep=delimiter)

            except:
                data = pd.read_csv(f, header=0, index_col=ind_c, sep=delimiter)
            
            #Delete excluded columns
            if del_c != None:
                labels = []
                for i in del_c:
                    labels.append(data.axes[1][i])
                data = data.drop(labels, axis=1)

            df_list.append(data)
            df_key.append(f)

        combined_data = pd.concat(df_list, axis=1, keys = df_key, ignore_index=False)
        
    return combined_data
        

#//////////Main////////////
#Clear screen
try:
    os.system('cls') #Windows
except:
    os.system('clear') #Linux/OSX

print "\n\n/////////////////Welcome to the CSV-File Concatenator!!!/////////////////"

#Loop program as long as user enters 'y' after each session
cont = 'y'
while cont == 'y':
	#Enter and check folder path
    valid_path = False
    while valid_path == False:
        folder = enter_folder()
        try:
            os.chdir(folder) #Change working directory
            valid_path = True
        except:
            print "\n\tInvalid path! Try again."
            continue
    
    folder = os.getcwd() #Makes 'folder' format consistent: allows user to input folder with a slash at the end
    files = os.listdir(folder) #List of files in folder    
    
    #Enter settings, upload files, and run concatenation
    successful_concat = False
    while successful_concat == False:
    	try:
			combined_data = concat_wrapper(files)
			successful_concat = True
        except:
			print "\nError: a problem occured during the CSV file reading and merging process!! Check settings and try again."
			continue
	
    combined_data.to_csv('Concatenated_File.csv')
    print "\nProcess Complete!! Combined file has been saved as \"Concatenated_File.csv\"."
    
    cont = raw_input("Continue (y/n)? ")

    #User error control
    cont = cont.lower()
    if cont == 'yes':
        cont = 'y'
	