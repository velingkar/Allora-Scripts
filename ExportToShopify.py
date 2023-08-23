# import modules
import csv
import os
import sys
import random
from colorama import Fore, Back, Style

def GetSKUImageName(mediaFiles, fileName, sku_prefix, colorIndex):
    imageColors = ["Red", "Blue", "LightBlue", "Pink", "Yellow", "Navy"]

    # check if file exists with required name
    mediaName = sku_prefix+"_"+fileName+"_"+imageColors[colorIndex]+".png"
    if (sku_prefix+"_"+fileName+"_"+imageColors[colorIndex]+".png") in mediaFiles:
        return mediaName
    else:
        print (Fore.LIGHTMAGENTA_EX+"WARNING: SKU Media File Not Found "+ mediaName)
        return ""

# initialise key swatches
sizes = ["2-3 Years", "4-5 Years","6-7 Years","7-8 Years","9-10 Years","11-12 Years"]
colors = ["Red", "Blue", "Light Blue", "Pink", "Yellow", "Navy"]

# initialise key arrays
category = "Medieval Wonders"
sku_prefix = "KTMDW"
handle_prefix	= "medieval-wonders-"
tags = "Medieval Wonders"
weight = 250
cost =	400
price =	899
compare_price =	899
variant_qty = 0
image_path = "https://cdn.shopify.com/s/files/1/0801/1258/2976/files/"


# constants
product = "Premium Kids's T-Shirt"
body = "<ul>\
        <li>4-5 working days dispatch time.</li>\
        <li>100% Organic Cotton Biowash preshrunk T-shirt.</li>\
        <li>8 colors in premium organic cotton fabric.</li>\
        <li>5 size wide range, relaxed fit.</li>\
        <li>Eco-friendly printing as well as not harmful to the nature.</li>\
        <li>Regular Fit best for casual wear.</li>\
        <li>180 GSM fabric which is breathable and lightweight.</li>\
        <li>100% eco-friendly packaging with seed paper hang tag.</li>\
    </ul>"
vendor = "My Store"
product_category = "Apparel & Accessories > Clothing > Shirts & Tops"
Product_type = "kids causual tshirts"
headers = ["Handle","Title","Body (HTML)","Vendor","Product Category","Type","Tags","Published","Option1 Name","Option1 Value","Option2 Name","Option2 Value","Option3 Name","Option3 Value","Variant SKU","Variant Grams","Variant Inventory Tracker","Variant Inventory Qty","Variant Inventory Policy","Variant Fulfillment Service","Variant Price","Variant Compare At Price","Variant Requires Shipping","Variant Taxable","Variant Barcode","Image Src","Image Position","Image Alt Text","Gift Card","SEO Title","SEO Description","Google Shopping / Google Product Category","Google Shopping / Gender","Google Shopping / Age Group","Google Shopping / MPN","Google Shopping / Condition","Google Shopping / Custom Product","Google Shopping / Custom Label 0","Google Shopping / Custom Label 1","Google Shopping / Custom Label 2","Google Shopping / Custom Label 3","Google Shopping / Custom Label 4","Variant Image","Variant Weight Unit","Variant Tax Code","Cost per item","Included / India","Included / International","Price / International","Compare At Price / International","Status"]
numColumns = len(headers)

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

    # Get the file names in the design folder
    files = os.listdir(folder+"\designs")

    # Get the file names in the media folder
    mediaFiles = os.listdir(folder+"\designs\media")

    # print some info
    print(Fore.BLACK+"\nColumns in CSV File: ", numColumns)
    print(Fore.BLACK+"Files in dir: ", len(files))

    # confirm with user
    print(Fore.BLACK+"\nGenerating ",len(files)," Products. Total of ",len(files)*len(colors)*len(sizes)," SKUs.")
    print(Fore.BLACK+"")
    print(Fore.BLACK+"\tFolder Name:\t" + folder)
    print(Fore.BLACK+"\tCategory Name:\t" + category)
    print(Fore.BLACK+"\tSKU PREFIX:\t" + sku_prefix)
    goAhead = input(Fore.BLACK + "\nShould I Proceed? (Y/N): ")
    goAhead = goAhead.strip().lower(); # trim and lower case

    if (goAhead != "yes" and goAhead != "y"):
        print(Fore.BLACK + "\nAs you wish. If Catgeory & SKU did not match, please change variables in python script")
        print(Fore.BLACK + "\nExiting...")
        sys.exit()
    
    # array to randomise color positions
    colorPosition = list(range(len(colors))) # [0,1,2,3,...]
    skippedFileCount = 0 #keep count of skipped files 

    # Open the CSV file in write mode
    with open(folder+"\ExportToShopify.csv", "w", newline='') as f:
        # Create a csv writer object
        writer = csv.writer(f)

        # write CSV header
        writer.writerow(headers)

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
            handle = handle_prefix + fileName[0].strip().lower()

            # start creating swatches using size and color combinations
            for sizeIndex, size in enumerate(sizes):
                for colorIndex, color in enumerate(colors):
                    row = [""] * numColumns

                    # get SKU Image path
                    skuImageFile = ""
                    imageFileName = GetSKUImageName(mediaFiles, fileName[0], sku_prefix, colorIndex)
                    if (imageFileName != ""):
                        skuImageFile = image_path + imageFileName

                    # fill below information for main product only
                    if colorIndex == 0 and sizeIndex == 0:
                        row[1] = fileName[0] + " - " + category + " - " + product
                        row[2] = body
                        row[3] = vendor
                        row[4] = product_category
                        row[5] = Product_type
                        row[6] = tags
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
                    row[14] = sku_prefix + f'{(fileIndex+1-skippedFileCount):03}' + f'{(colorIndex+1):02}' + f'{(sizeIndex+1):02}'    
                    row[15] = weight
                    row[17] = variant_qty
                    row[18] = "deny" #variant policy
                    row[19] = "manual" #fullfillment
                    row[20] = price
                    row[21] = compare_price
                    row[22] = "TRUE" # requires shipping
                    row[23] = "TRUE" # is taxable
                    row[45] = cost
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
    print(Fore.BLUE+"Total SKUs Generated: ",(len(files) - skippedFileCount)*len(colors)*len(sizes))
    print(Fore.BLUE+"Export File Path: "+ folder+"\ExportToShopify.csv")
    print(Fore.BLUE+'##################################################')

finally:
    print(Style.RESET_ALL)
