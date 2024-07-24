#!/usr/bin/env python 
import os
# pip install image
# https://pypi.org/project/pillow/
from PIL import Image
from PIL.ExifTags import TAGS

# https://justcuriousbugs.atlassian.net/browse/JCWSD-76 - The configuration of the SlideShow for all travel pages currently involves manually importing the  pictures into a .js file and setting up a data structure in the appropriate file, that allows the Slideshow to process them.  I would like to semi-automate this procedure and just use all pictures that are in the pictures folder in the slideshow.

# This program will be used in the JustCurious website build.  I have been able to use PhotoGallery in the travel section of the website to provide a icon list of the photos and then a gallery list if someone clicks on any photo.  What I want to do to make the process more generic is to dump the files that I want to use into a ./pictures folder in the working folder of the particular trip, and then generate an array that contains the picture name, the height and width of the photo, a caption and a title for the photo.  This data will then be stored in a file in the ./picture directory called pictlistfile.js.  This file can then be imported to the .js file of the appropriate trip page (ex Venice) as
#import { photoAlbumList } from "./pictures/piclistfile";
#This is the data that is stored in the dictionary for each picture
# "asset" - This is the full file name including the file extension.  This also included the  path relative to the base directory of the travel page and the
# "width": - This is retrieved from the picture file
# "height": - This is rerieved from the picture file
# "title":  - This is the first part of the file name
# "description": This is the text that is included in the picture file
# "file_name": This is the filename withtout the file path.

# The list of folders to be processed to be provided in a file.  I would like the array data for each folder to be stored in a file in the folder


#This method will read a file that contains a list of all of the directories that contain pictures and need to be processed.
def get_directory_list():
  #Create a list
  dir_list=[]
  #Todo: Create and read file
  dir_list= ["c:" + "\\"+ "MyStuff" + "\\" + "JustCurious" + "\\" + "src"+ "\\" + "Travel"+ "\\" + "Croatia2023"+ "\\" + "Venice"+ "\\" + "pictures"]
  # dir_list= ["c:" + "\\"+ "MyStuff" + "\\" + "WebDevCourse" + "\\" + "Slider"+ "\\" + "imageslider"+ "\\" + "src"+ "\\" + "\\" + "pictures"]

# C:\MyStuff\WebDevCourse\Slider\imageslider\src\pictures


  return dir_list

def get_file_list(path):
    # Initialize an empty list to store the names of .jpg files
    clean_file_list = []
    
    # Iterate through each file in the directory specified by 'path'
    for file in os.listdir(path):
        # Check if the file name ends with '.jpg'
        if file.endswith(".jpg"):
            # If the file name ends with '.jpg', append it to clean_file_list
            clean_file_list.append(file)
    
    # Optionally, print the list of files (commented out in original code)
    # print(f"List of all the files in the directory {path}")
    # print(*clean_file_list, sep="\n")
    
    # Return the list of .jpg files found in the directory
    return clean_file_list

def build_picture_dictionary(path, file):
  im = Image.open(path)
  exif_data = im._getexif()
  if exif_data:
    # looping through all the tags present in exifdata
    for tagid in exif_data:
      # getting the tag name instead of tag id
      tagname = TAGS.get(tagid, tagid)
      # passing the tagid to get its respective value
      value = exif_data.get(tagid)    

      # printing the final result
      #print(f"{tagname:25}: {value}")

    camera_make = exif_data.get(0x010e)
    # camera_model = exif_data.get(272)
    #print("Camera Make:", camera_make)
    # print("Camera Model:", camera_model)
  else:
    print("No EXIF data found.")
    exif_data = im._getexif()

  #Retrieve just the first part of the file name without the file extension
  file_name = os.path.splitext(file)
  print(file_name[0])
  title = file_name[0] 
  #The description is stored in the picture EXIF data
  description = str(exif_data.get(0x010e))
  # Add this file information to the dictionary
  picture_dictionary = {"asset":file, "width": im.size[0] , "height": im.size[1], "title": title, "description": description , "file_name": file}
 
  return picture_dictionary

def write_to_file(path, pict_list):
  #Write the list to a file
  pictlistfile = path + "\\" + "piclistfile.js"
  print(pictlistfile)
  #Open the file
  fo =  open(pictlistfile, "w+")

  #Write the header of the file to import the pictures in the folder
  # ex import image0 from "./AlltheDoges.jpg";
  i = 0
  for picture in pict_list:
    line = fo.writelines("import " + "image" + str(i) + " from \"./" + picture["file_name"] +"\";\n")
    i +=1

  #Write the data structure to the file
  line = fo.writelines("\nexport const photoAlbumList = [ \n")

  i =0
  for picture in pict_list:
    width = str(picture["width"])
    heigth = str(picture["height"])

    line = fo.writelines("{ " + "src:" + "image"+ str(i) +  ",\t" + 
                         "width:" +  width + ",\t" +
                         "height:" + heigth + ",\t" + 
                         "title:" + "\"" + picture["title"] + "\"" + ",\t"+ 
                         "description:" + "\"" + picture["description"] + "\""  +" }," "\n")
    i +=1
#    line = fo.writelines("{ " + "src:" + "\"" +picture["asset"] + "\""+ ",\t" + "width:" +  width + ",#\t" +"height:" + heigth + ",\t" + "title:" + "\"" + picture["title"] + "\"" +" }," "\n")



  line = fo.writelines("]")

  # line = fo.writelines(".map(({ asset, width, height }) => ({ \n" + 
  #                      "\tsrc: assetLink(asset, width),\n" +
  #                      "\twidth,\n" +
  #                      "\theight,\n" +
  #                      "\tsrcSet: breakpoints.map((breakpoint) => ({\n" +
  #                      "\t\tsrc: assetLink(asset, breakpoint),\n" +
  #                      "\t\twidth: breakpoint,\n" +
  #                      "\t\theight: Math.round((height / width) * breakpoint),\n"+
  #                      "\t})),\n"
  #                      "}));\n")

  #Close the file
  fo.close()

# im = Image.open("c:\MyStuff\JustCurious\src\Travel\Croatia2023\Venice\pictures\\AnnInTheBigHouse.jpg")
# print(im.size)
# print(type(im.size))

#Main Program
#This List will store the individual picture dictionaries  
pict_list=[]

dir_list = get_directory_list()
# print("dir_list = " )
# print( dir_list)
for dir in dir_list:
  #print("dir= " + dir)
  file_list = get_file_list(dir)
  for file in file_list:
    #print("file=" + file)
    pict_path = dir + "\\" + file
    picture_dictionary = build_picture_dictionary(pict_path, file)
    pict_list.append(picture_dictionary)

  write_to_file(dir, pict_list)


  



