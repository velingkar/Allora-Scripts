# import modules
import csv
from logging import config
import os
import sys
import random
from colorama import Fore, Back, Style

def GetSKUImageName(mediaFiles, fileName, sku_prefix, imageColors, colorIndex):
    # check if file exists with required name
    mediaName = sku_prefix+"_"+fileName+"_"+imageColors[colorIndex]+".png"
    if (sku_prefix+"_"+fileName+"_"+imageColors[colorIndex]+".png") in mediaFiles:
        return mediaName
    else:
        print (Fore.LIGHTMAGENTA_EX+"WARNING: SKU Media File Not Found "+ mediaName)
        return ""

# Start Prompt
Style.RESET_ALL
print(Back.YELLOW)
print(Fore.BLUE+'##################################################')
print(Fore.BLUE+'Welcome to Allorio Shopify CSV Creator')
print(Fore.BLUE+'##################################################')

try:
    # Ask for a folder path
    folder = input(Fore.BLACK + "\nEnter the parent folder path (should have design sub-folder): ")

    # check if design sub-folder exists
    if (not os.path.isdir(folder+"\designs")):
        print(Fore.RED + "\nERROR: Design Folder is not found. Create designs with text first.")
        sys.exit()

    # check if media sub-folder exists
    if (not os.path.isdir(folder+"\designs\media")):
        print(Fore.RED + "\nERROR: Media Sub-Folder is not found. Create t-shirt mockups first.")
        sys.exit()
    
    # check if media sub-folder exists
    if (not os.path.isfile(folder+"\settings.py")):
        print(Fore.RED + "\nERROR: settings.py file was not found. Please create config.py file in directory.")
        print(Fore.RED + "\nFor example template: https://github.com/velingkar/Allora-Scripts/blob/main/settings_template.py")
        sys.exit()

    # import key variables
    sys.path.append(folder) #temporarily adds folder to system path
    import settings
    numColumns = len(settings.headers)

    # Get the file names in the design folder
    files = os.listdir(folder+"\designs")

    # Get the file names in the media folder
    mediaFiles = os.listdir(folder+"\designs\media")

    # print some info
    print(Fore.BLACK+"\nColumns in CSV File: ", numColumns)
    print(Fore.BLACK+"Files in dir: ", len(files))

    # confirm with user
    print(Fore.BLACK+"\nGenerating ",len(files)," Products. Total of ",len(files)*len(settings.colors)*len(settings.sizes)," SKUs.")
    print(Fore.BLACK+"")
    print(Fore.BLACK+"\tFolder Name:\t" + folder)
    print(Fore.BLACK+"\tCategory Name:\t" + settings.category)
    print(Fore.BLACK+"\tSKU PREFIX:\t" + settings.sku_prefix)
    goAhead = input(Fore.BLACK + "\nShould I Proceed? (Y/N): ")
    goAhead = goAhead.strip().lower(); # trim and lower case

    if (goAhead != "yes" and goAhead != "y"):
        print(Fore.BLACK + "\nAs you wish. If Catgeory & SKU did not match, please change variables in python script")
        print(Fore.BLACK + "\nExiting...")
        sys.exit()
    
    # array to randomise color positions
    colorPosition = list(range(len(settings.colors))) # [0,1,2,3,...]
    skippedFileCount = 0 #keep count of skipped files 

    # Open the CSV file in write mode
    with open(folder+"\ExportToShopify.csv", "w", newline='') as f:
        # Create a csv writer object
        writer = csv.writer(f)

        # write CSV header
        writer.writerow(settings.headers)

        # Loop through the files and add the prefix
        for fileIndex, file in enumerate(files):
            # get the file name without extension
            fileName = os.path.splitext(file)
            if (fileName[1] != ".png"):
                skippedFileCount += 1 #increment by 1
                print (Fore.LIGHTMAGENTA_EX+"WARNING: Ignoring Unexpected File. Was expecting .png. Found "+fileName[0]+fileName[1]+" : index "+str(fileIndex))
                continue

            # for every design, shuffle the image position index (variety of colors will be shown)
            # TODO This did not work - need to get this ahead of time 
            random.shuffle(colorPosition)

            #make unique handle
            # TODO replace spaces with -
            handle = settings.handle_prefix + fileName[0].strip().lower()

            # start creating swatches using size and color combinations
            for sizeIndex, size in enumerate(settings.sizes):
                for colorIndex, color in enumerate(settings.colors):
                    row = [""] * numColumns

                    # get SKU Image path
                    skuImageFile = ""
                    imageFileName = GetSKUImageName(mediaFiles, fileName[0], settings.sku_prefix, settings.imageColors, colorIndex)
                    if (imageFileName != ""):
                        skuImageFile = settings.image_path + imageFileName

                    # fill below information for main product only
                    if colorIndex == 0 and sizeIndex == 0:
                        row[1] = fileName[0] + " - " + settings.category + " - " + settings.product
                        row[2] = settings.body
                        row[3] = settings.vendor
                        row[4] = settings.product_category
                        row[5] = settings.Product_type
                        row[6] = settings.tags
                        row[7] = "TRUE" # Published
                        row[8] = "Color" # Option1 Name
                        row[10] = "Size" #Option 2 Name
                        row[28] = "FALSE" #GIFT CARD
                        row[29] = "" # TODO SEO Title
                        row[30] = "" # TODO SEO Description
                        row[46] = "TRUE" # for India
                        row[47] = "FALSE" # not for international (yet)

                    # add image path for main product for each color, randomise color positions
                    if sizeIndex == 0:
                        row[25] = skuImageFile
                        row[26] = colorPosition[colorIndex] # randomised image position

                    # fill information for SKUs
                    row[0] = handle
                    row[9] = color
                    row[11] = size
                    # create SKU Name (prefix(5) + design(3) + color(2) + size(2) )
                    row[14] = settings.sku_prefix + f'{(fileIndex+1-skippedFileCount):03}' + f'{(colorIndex+1):02}' + f'{(sizeIndex+1):02}'    
                    row[15] = settings.weight
                    row[17] = settings.variant_qty
                    row[18] = "deny" #variant policy
                    row[19] = "manual" #fullfillment
                    row[20] = settings.price
                    row[21] = settings.compare_price
                    row[22] = "TRUE" # requires shipping
                    row[23] = "TRUE" # is taxable
                    row[45] = settings.cost
                    row[50] = "draft" # do not publish as active

                    # add variant image path
                    row[42] = skuImageFile

                    # write to CSV 
                    writer.writerow(row)
        
        # close the CSV file
        f.close()

    # Write Export Summary
    print(Fore.BLUE+'##################################################')
    print(Fore.BLUE+'Export CSV SUCCESSFUL:')
    print(Fore.BLUE+"Files Processed: ",(len(files) - skippedFileCount))
    print(Fore.BLUE+"Files Skipped: ",skippedFileCount)
    print(Fore.BLUE+"Total SKUs Generated: ",(len(files) - skippedFileCount)*len(settings.colors)*len(settings.sizes))
    print(Fore.BLUE+"Export File Path: "+ folder+"\ExportToShopify.csv")
    print(Fore.BLUE+'##################################################')

finally:
    print(Style.RESET_ALL)
