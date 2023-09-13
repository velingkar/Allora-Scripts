# Import os module
import os
import sys

def AddPrefix(path, files, fileExt, filter, prefix):
    if (prefix == "" or len(prefix) < 3 or len(prefix) > 7):
        print("Error: Prefix must be between 3 to 7 characters")
        return
    
    #append "_" to each filter element
    filter = list(map(lambda x: "_" + x, filter))
    
    # Loop through the files in the directory
    fileCount = 0
    for file in files:
        # get the file name without extension
        fileName = os.path.splitext(file)

        # skip if file name is not of supported extension
        if (fileName[1] != "."+fileExt):
            continue

        # only proceed if file name contains colors mentioned in the filter
        if any(word in fileName[0] for word in filter):
            fileCount += 1 #increment by 1
            # Get the old file name
            old_name = os.path.join(path, file)
            # Add the prefix to the file name
            new_name = os.path.join(path, prefix + file)
            # Rename the file
            os.rename(old_name, new_name)

    print("Done! ",fileCount," files renamed.")

def RemovePrefix(path, files, fileExt, prefix):
    if (prefix == "" or len(prefix) < 3 or len(prefix) > 7):
        print("Error: Prefix must be between 3 to 7 characters")
        return
    
    # Loop through the files in the directory
    skippedFileCount = 0
    for file in files:
        # get the file name without extension
        fileName = os.path.splitext(file)
        if (fileName[1] != "."+fileExt):
            skippedFileCount += 1 #increment by 1
            continue

        if (not fileName[0].startswith(prefix)):
            skippedFileCount += 1 #increment by 1
            continue

        # Get the old file name
        old_name = os.path.join(path, file)
        # Add the prefix to the file name
        new_name = os.path.join(path, file.removeprefix(prefix))
        # Rename the file
        os.rename(old_name, new_name)

    print("Done! ",len(files)-skippedFileCount," files renamed.")

def InputPrefixToRemove():
    prefix = input("Input prefix: ").strip()
    if(not (prefix.endswith("_") or prefix.endswith("-"))):
        prefix = prefix+"_" #add a separator if missing
    return prefix

def InputPrefixToAdd(sku_prefix):
    prefix = input("Input prefix (default - "+sku_prefix+"): ") or sku_prefix
    if(not (prefix.endswith("_") or prefix.endswith("-"))):
        prefix = prefix+"_" #add a separator if missing
    return prefix

# Define the prefix to add
prefix = ""

# Get the current working directory
folder = input("Enter the folder path in which you want to rename files: ")
if not os.path.isdir(folder):
    sys.exit("ERROR: Folder does not exist")

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
from settings import sku_product_type_prefix, sku_collection_prefix, image_colors

# Get the file extension for which you want to rename
fileExt = input("Enter the file extension for which you want to rename files (default: png): ") or "png"
if len(fileExt) != 3:
    sys.exit("ERROR: File Extension should be 3 characters long")

# Get the file names in the folder
files = os.listdir(folder)

# print some sample files
print("\n\nPrinting sample files from folder: ",folder)
print(files[:5])

# ask input
userAction = input("\n\nWhat do you want to do?\n\t(1) Add Prefix\n\t(2) Remove Prefix\n\t( ) Exit\nInput: ").strip()

if (userAction == "1"):
    # TODO - Loop
    for pIndex, product in enumerate(sku_product_type_prefix):
        # Add Extension
        sku_prefix = product.upper() + sku_collection_prefix.upper()
        prefix = InputPrefixToAdd(sku_prefix)
        print("\nAdding Prefix for ",product, image_colors[pIndex])
        AddPrefix(folder, files, fileExt, image_colors[pIndex], prefix)
elif (userAction == "2"):
    # Remove Extension
    prefix = InputPrefixToRemove()
    print("\nRemoving  Prefix ...")
    RemovePrefix(folder, files, fileExt, prefix)
else:
    # Quit
    print("\nBye")
