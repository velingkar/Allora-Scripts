# Import os module
import os
import sys

def AddPrefix(path, files, fileExt, prefix):
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

        # Get the old file name
        old_name = os.path.join(path, file)
        # Add the prefix to the file name
        new_name = os.path.join(path, prefix + file)
        # Rename the file
        os.rename(old_name, new_name)

    print("Done! ",len(files)-skippedFileCount," files renamed.")

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

def InputPrefix():
    prefix = input("Input prefix: ").strip()
    if(not (prefix.endswith("_") or prefix.endswith("-"))):
        prefix = prefix+"_" #add a separator if missing
    return prefix

# Define the prefix to add
prefix = ""

# Get the current working directory
folder = input("Enter the folder path in which you want to rename files: ")
if not os.path.isdir(folder):
    sys.exit("ERROR: Folder does not exist")

# Get the file extension for which you want to rename
fileExt = input("Enter the file extension for which you want to rename files (default: png): ") or "png"
if len(fileExt) != 3:
    sys.exit("ERROR: File Extension should be 3 characters long")

# Get the file names in the folder
files = os.listdir(folder)

# print some sample files
print("\n\nPrinting sample files from folder: "+folder)
print(files[:5])

# ask input
userAction = input("\n\nWhat do you want to do?\n\t(1) Add Prefix\n\t(2) Remove Prefix\n\t( ) Exit\nInput: ").strip()

if (userAction == "1"):
    # Add Extension
    prefix = InputPrefix()
    print("\nAdding  Prefix ...")
    AddPrefix(folder, files, fileExt, prefix)
elif (userAction == "2"):
    # Remove Extension
    prefix = InputPrefix()
    print("\nRemoving  Prefix ...")
    RemovePrefix(folder, files, fileExt, prefix)
else:
    # Quit
    print("\nBye")
