## This is a script for automatically updating a list of .xml files. 
    # Original purpose: updating metadata for geodatabase improvement.
    # May be adaptable to loop through files for other purposes.

## Python version 3.8.3
## Date last updated: 08/03/2020
## Written by Paul Seibert

## Pre-requisites: 
    # Files to edit must be downloaded to local drive and stored where appropriate
    # Python must be up to date
    # 'Original' directory must be a newly created folder, with no files stored inside

import os
import shutil
import glob
import xml.etree.ElementTree as ET


########## Part 1: copy the extracted metadata files from their folders to new directories with corresponding names ##########
os.system('cls') # Clears terminal for every run 

# Declare folder for original metadata to be stored
######  Original metadata folder must be an empty folder created manually. At the moment this seems the easiest way to do it ######
originals = 'C:/Users/Paul/Documents/NOAA_Precip_Freq_Data/originals_est'


###### Define basepath ######
basepath = 'C:/Users/Paul/Documents/NOAA_Precip_Freq_Data/zip_to_here'

basepath_grab_xml = basepath + '/**/*.xml' # Add the grab xml files syntax
x = glob.glob(basepath_grab_xml, recursive = True)  # Grab every .xml file from basepath that contains needed files and create a list of path names (a one dimensional array of file paths)

# For loop to run through the list of file paths
# 'Original' directory must be empty
  
# Getting the list of directories 
directory_test = os.listdir(originals) 
if len(directory_test) == 0: ## Must test to make sure it is an empty directory ##
    for files in x:
            # file.split creates an array that splits apart the list where \\ exists in the file path, this is because the file path for the metadata   
            # when zip was extracted from google drive was 'C:/Users/Paul/Documents/NOAA_Precip_Freq_Data/metadata/ziptohere/NOAA_PF_and_UCL\\**\\'
        file_array = files.split('\\') 
        print(file_array) 
        name = file_array[-2] # Creates a variable to represent the pXyrYYhau or pXyrYYmau part of the path. May have to change the array integer to work
        if name[-1] == 'a': # Checks the second to last element of the name for a, since that is what we are interested in 
            os.makedirs(os.path.dirname(originals + '/' + name + '/metadata.xml')) # Creates a directory for each metadata file that corresponds to the name of the original folder
            shutil.copy2(files,originals + '/' + name + '/original_metadata.xml') # Copies metadata files into their corresponding folders in the new directory

elif len(directory_test) != 0: ## If the original folder already has files, the for loop will not run, and the files will not be copied ##
    print('Error: Not empty original folder')

########## Part 2: Edit metadata for corresponding files ##########

y = glob.glob(originals + '\**\*.xml', recursive = True) # Grab original xml files and create a list of them 

for files2 in y:
    file_array = files2.split('\\')  
    print(file_array)
    name = file_array[-2]      # Grab names in form of pXyrYYhau or pXyrYYmau
    tree = ET.parse(files2)    # Read file
    root = tree.getroot()      # Get root, in this case it is 'metadata'
    startyr = name.find('p') + len('p')     # These three lines split the name to extract the year storm for use later in the script
    endyr = name.find('yr')
    year = name[startyr:endyr]  
    
    if name.endswith('ha'):      # If the name ends with hau, separate to find the 'hour' storm, else it is a 'minute' storm
        startdur = name.find('yr') + len('yr')
        enddur = name.find('ha')
        duration = name[startdur:enddur] + ' hour'
    elif name.endswith('ma'):
        startdur = name.find('yr') + len('yr')
        enddur = name.find('ma')
        duration = name[startdur:enddur] + ' minute'

    trigger = root.findall('./dataIdInfo')     # Get parent node for creating subelements AKA children

    for trigger_elem in trigger:     # Loop though parent node to create new subelements
        purpose = ET.SubElement(trigger_elem,'idPurp')    # Make sure that the subelements being created have the same syntax that ArcMap uses
        purpose.text = 'For use in GISHydro (WinTR-20 model) ' + year + ' year, ' + duration  + ' Precipitation Frequency Estimates' # Concatenation of strings that unique to each file folder
        abstract = ET.SubElement(trigger_elem,'idAbs')
        abstract.text = '''Units: 1/1000 inch \nPrecipitation Frequency Estimates data obtained from NOAA Precipitation Frequency Data Server, GIS grids (https://hdsc.nws.noaa.gov/hdsc/pfds/pfds_gis.html), Ohio River Basin and Surrounding States. \nData downloaded June 2020. \nProjected to Maryland State Plane, 750 m grid size \nRegistration point: x = 0, y = 0 \nInterpolation method: bilinear \nClipped to GISHydro spatial extent \n\nAnalysis by K Brubaker, P Seibert, J Walsh, J Slattery, UMCP Civil and Environmental Engineering Dept. Contact: kbru@umd.edu'''              
        credit = ET.SubElement(trigger_elem,'idCredit')
        credit.text = 'NOAA Precipitation Frequency Data Server (https://hdsc.nws.noaa.gov/hdsc/pfds/)'
        search_keys = ET.SubElement(trigger_elem,'searchKeys')

    tree.write(basepath + '/NOAA_PF_and_UCL/' + name + '/metadata.xml', encoding = "UTF-8")

    trigger2 = root.findall('*/searchKeys')
    for trigger_elem2 in trigger2:
        keyword1 = ET.SubElement(search_keys,'keyword')
        keyword1.text = 'NOAA'
        keyword2 = ET.SubElement(search_keys,'keyword')
        keyword2.text = 'Precipitation'
        keyword3 = ET.SubElement(search_keys,'keyword')
        keyword3.text = 'Precipitation Frequency Estimates'

    tree.write(basepath + '/NOAA_PF_and_UCL/' + name + '/metadata.xml', encoding = "UTF-8")   # Overwrites the file created above, not sure why this is necessary but it works


print('done running :D')
