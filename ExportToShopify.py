# import modules
import csv
import os
import sys
from turtle import window_height

# initialise key swatches
sizes = ["2-3 Years", "4-5 Years","6-7 Years","7-8 Years","9-10 Years","11-12 Years"]
colors = ["Red", "Blue", "Light Blue", "Pink", "Yellow", "Navy"]

# initialise key arrays
category = "Sweeth Tooth"
sku_prefix = "KTSWT"
handle_postfix	= "sweeth-tooth"
tags = "Sweeth Tooth"
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
headers = ["Title","Body (HTML)","Vendor","Product Category","Type","Tags","Published","Option1 Name","Option1 Value","Option2 Name","Option2 Value","Option3 Name","Option3 Value","Variant SKU","Variant Grams","Variant Inventory Tracker","Variant Inventory Qty","Variant Inventory Policy","Variant Fulfillment Service","Variant Price","Variant Compare At Price","Variant Requires Shipping","Variant Taxable","Variant Barcode","Image Src","Image Position","Image Alt Text","Gift Card","SEO Title","SEO Description","Google Shopping / Google Product Category","Google Shopping / Gender","Google Shopping / Age Group","Google Shopping / MPN","Google Shopping / Condition","Google Shopping / Custom Product","Google Shopping / Custom Label 0","Google Shopping / Custom Label 1","Google Shopping / Custom Label 2","Google Shopping / Custom Label 3","Google Shopping / Custom Label 4","Variant Image","Variant Weight Unit","Variant Tax Code","Cost per item","Included / India","Included / International","Price / International","Compare At Price / International","Status"]
numColumns = len(headers)

# Ask for a folder path
folder = input("Enter the parent folder path (should have design sub-folder): ")

# check if design sub-folder exists
if (not os.path.isdir(folder+"\designs")):
    sys.exit("ERROR: Design Folder is not found. Create designs with text first.")

# check if media sub-folder exists
if (not os.path.isdir(folder+"\designs\media")):
    sys.exit("ERROR: Media Sub-Folder is not found. Create t-shirt mockups first.")

# Get the file names in the folder
files = os.listdir(folder+"\designs")

# print some info
print("Columns in CSV File: ", numColumns)
print("Files in dir: ", len(files))

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
            print ("WARNING: Ignoring Unexpected File. Was expecting .png. Found "+fileName[0]+fileName[1])
            break

        # start creating swatches using size and color combinations
        for colorIndex, color in enumerate(colors):
            for sizeIndex, size in enumerate(sizes):
                row = [""] * numColumns
                # TODO - how to randomize color image for main product

                # fill below information for main product only
                if colorIndex == 0 and sizeIndex == 0:
                    row[0] = fileName[0] + " - " + category + " - " + product
                    # TODO REMOVE COMMENT BELOW, added to reduce noise for testing
                    # row[1] = body
                    row[2] = vendor
                    row[3] = product_category
                    row[4] = Product_type
                    row[5] = tags
                    row[6] = "TRUE" # Published
                    row[7] = "Color" # Option1 Name
                    row[9] = "Size" #Option 2 Name
                    # create SKU Name (prefix(5) + design(3) + color(2) + size(2) )
                    row[13] = sku_prefix + f'{fileIndex:03}' + f'{colorIndex:02}' + f'{sizeIndex:02}'
                    row[27] = "FALSE" #GIFT CARD
                    row[28] = "" # TODO SEO Title
                    row[29] = "" # TODO SEO Description
                    row[45] = "TRUE" # for India
                    row[46] = "FALSE" # not for international (yet)

                # fill information for SKUs
                row[8] = color
                row[10] = size
                row[14] = weight
                row[16] = variant_qty
                row[17] = "deny" #variant policy
                row[18] = "manual" #fullfillment
                row[19] = price
                row[20] = compare_price
                row[21] = "TRUE" # requires shipping
                row[22] = "TRUE" # is taxable
                row[24] = image_path #TODO Product Image - need to randomise this
                # TODO Product Image position
                row[41] = image_path #TODO write a function to give proper path, rename, check file etc.
                row[44] = cost
                row[49] = "draft" # do not publish as active

                # write to CSV 
                writer.writerow(row)

print("Done! CSV created at "+ folder+"\ExportToShopify.csv")
