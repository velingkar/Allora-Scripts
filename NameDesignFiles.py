# Import os module
import os
import sys

def RenameFiles(path, fileExt, prefix, postfix):
    if not os.path.isdir(path):
        print("Error: folder is missing... ", path)
        return
    
    # Get the file names in the folder
    files = os.listdir(path)

    # print some sample files
    print("\n\nPrinting sample files from folder: ",path)
    print(files[:5])

    goAhead = input("\nShould I Proceed? (Y/N): ")
    goAhead = goAhead.strip().lower(); # trim and lower case

    if (goAhead != "yes" and goAhead != "y"):
        print("\nSkipping this folder...")
        return
    
    if (prefix == "" or len(prefix) < 3 or len(prefix) > 7):
        print("Error: Prefix must be between 3 to 7 characters")
        return
    
    # Loop through the files in the directory
    fileCount = 0
    for file in files:
        # get the file name without extension
        fileName = os.path.splitext(file)

        # skip if file name is not of supported extension
        if (fileName[1] != "."+fileExt):
            continue

        fileCount += 1 #increment by 1
        # Get the old file name
        old_name = os.path.join(path, file)

        # TODO - add checks if prefix or postfix is already present 
        
        # Add the prefix to the file name
        new_name = os.path.join(path, prefix + fileName[0] + postfix + fileName[1])
        
        # Rename the file
        os.rename(old_name, new_name)

    print("Done! ",fileCount," files renamed in ",path)

def InputPrefixToAdd(sku_prefix):
    prefix = input("Input prefix (default - "+sku_prefix+"): ") or sku_prefix
    if(not (prefix.endswith("_") or prefix.endswith("-"))):
        prefix = prefix+"_" #add a separator if missing
    return prefix

# Get the current working directory
settingsFolder = input("Enter the folder path with settings.py: ")
if not os.path.isdir(settingsFolder):
    sys.exit("ERROR: Folder does not exist")

# check if settings file exists
if (not os.path.isfile(settingsFolder+"\settings.py")):
    print("\nERROR: settings.py file was not found. Please create config.py file in directory.")
    print("For example template: https://github.com/velingkar/Allora-Scripts/blob/main/settings_template.py")
    sys.exit()

# import key variables
sys.path.append(settingsFolder) #temporarily adds folder to system path
from settings import sku_collection_prefix

prefix = InputPrefixToAdd(sku_collection_prefix.upper())

#1. Rename the Design Files
highresFolder = settingsFolder+"\HighRes"
RenameFiles(highresFolder,"png",prefix,"")

#2. Rename files in designs folder
RenameFiles(highresFolder+"\designs\Light","psd",prefix,"_light")
RenameFiles(highresFolder+"\designs\Dark","psd",prefix,"_dark")

#3. Rename files in designs_png folder
RenameFiles(highresFolder+"\designs_png\Light","png",prefix,"_light")
RenameFiles(highresFolder+"\designs_png\Dark","png",prefix,"_dark")

print("Done!")