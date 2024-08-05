#!/usr/bin/env python 
import os
import glob
import operator
import time
from datetime import datetime
# pip install image
# https://pypi.org/project/pillow/
from PIL import Image
from PIL.ExifTags import TAGS

DEBUG = False;

#This is the path that the program will start looking at and then iterate through the directory structure to fine the "target_dir" folders
root_path = "c:\\mystuff\\JustCurious\\src\\Travel\\"  # Root to start at
#If this folder name is found, it will be added to the list that contains the folders with pictures.
target_dir = "pictures"  

# https://justcuriousbugs.atlassian.net/browse/JCWSD-76 - The configuration of the SlideShow for all travel pages currently involves manually importing the  pictures into a .js file and setting up a data structure in the appropriate file, that allows the Slideshow to process them.  I would like to semi-automate this procedure and just use all pictures that are in the pictures folder in the slideshow.

# This program will be used in the JustCurious website build.  I have been able to use PhotoGallery in the travel section of the website to provide a icon list of the photos and then a gallery list if someone clicks on any photo.  What I want to do to make the process more generic is to dump the files that I want to use into a ./pictures folder in the working folder of the particular trip, and then generate an array that contains the picture name, the height and width of the photo, a caption and a title for the photo.  This data will then be stored in a file in the ./picture directory called pictlistfile.js.  This file can then be imported to the .js file of the appropriate trip page (ex Venice)
#import { photoAlbumList } from "./pictures/piclistfile";

#This is the data that is stored in the dictionary for each picture
# "asset" - This is the full file name including the file extension.  This also included the  path relative to the base directory of the travel page and the
# "width": - This is retrieved from the picture file
# "height": - This is rerieved from the picture file
# "title":  - This is the first part of the file name
# "description": This is the text that is included in the picture file
# "file_name": This is the filename without the file path.

# The list of folders to be processed will be determined by the program.  The root of the travel folder is provided as an input and the program will iterate through the directory structure and append any folder that has a ./pictures folder to the list

#ToDo
#1) Add a command line option to just do one directory
#2) List the photos in date order

#***************************************************************************
  #Starting at the root_path, iterate through all the folders.  If any of the folders have a "target_dir" folder then append that to the dir_list

  #Search for directories with the name `target_dir` within `root_path`.

  #Parameters:
  #root_path (str): The root directory path to start the search.
  #target_dir (str): The name of the directory to search for.

  #Returns:
  #list: A list of full paths to directories named `target_dir`.
def find_directory(root_path, target_dir):
  # Initialize an empty list to store the paths of found directories

  dir_list = []

  # Walk through the directory tree starting from `root_path`
  for root, dirs, files in os.walk(root_path):
    # Check if `target_dir` is in the list of directories for the current root
    if target_dir in dirs:
    # Construct the full path to the target directory and add it to the list
      dir_list.append(os.path.join(root, target_dir))
    
  # Return the list of found directory paths
  return dir_list

#***************************************************************************
#This method will creat a list of all of the directories that contain pictures and need to be processed.
def get_directory_list():
  # Directory to start at
  dir_list = find_directory(root_path,target_dir)

  # This was test code before I implemented the find_directory function 
  # dir_list= ["c:" + "\\"+ "MyStuff" + "\\" + "JustCurious" + "\\" + "src"+ "\\" + "Travel"+ "\\" + "Italy2009"+ "\\" + "Rome"+ "\\" + "pictures"]

  if DEBUG:
   if dir_list:
     print("Found directory:", dir_list)
   else:
     print("Directory not found.")

  if DEBUG:
    print("dir_list = " )
    print( dir_list)

  return dir_list
#***************************************************************************
def get_file_list(path1):
    # Initialize an empty list to store the names of .jpg files
    clean_file_list = []
    path1=path1 + "\\"
    if DEBUG:
      print("path=", path1)
    files = glob.glob(path1  + "*.jpg")
    # print("file=", files, sep="\n")
    files.sort(key= os.path.getctime)
    # Iterate through each file in the directory specified by 'path'
    for file in files:
            file1 = os.path.basename(file)
            # If the file name ends with '.jpg', append it to clean_file_list
            clean_file_list.append(file1)
    
    # Optionally, print the list of files 
    # print(f"List of all the files in the directory {path1}")
    # print(*clean_file_list, sep="\n")
    
    # Return the list of .jpg files found in the directory
    return clean_file_list

#***************************************************************************
def build_picture_dictionary(full_path_name, file):

  im = Image.open(full_path_name)
  #Retrieve just the first part of the file name without the file extension
  file_name = os.path.splitext(file)
  # print(file_name[0])
  title = file_name[0] 

  exif_data = im._getexif()
  if exif_data:
    # looping through all the tags present in exifdata
    for tagid in exif_data:
      # getting the tag name instead of tag id
      tagname = TAGS.get(tagid, tagid)
      # passing the tagid to get its respective value
      value = exif_data.get(tagid)  
      
      #The description is stored in the picture EXIF data
      description = str(exif_data.get(0x010e))
      #The time that the picture was taken.
      TimePict = exif_data.get(0x9003)
      # TimePict = os.path.getctime()
      # print("Time = ", TimePict)
# 2009:04:07 16:09:48
      if(None == TimePict):
          TimePict = datetime.strptime("2000/01/01 12:00:00", '%Y/%m/%d %H:%M:%S')
          #  TimePict="01/01/00"
      else:
        try: 
          TimePict = datetime.strptime(TimePict, '%Y:%m:%d %H:%M:%S')
        except ValueError as ve1: 
          try:
            TimePict = datetime.strptime(TimePict, '%Y-%m-%d %H:%M:%S')
          except ValueError as ve1:
            print("Error - TimePict=", TimePict)
  else:
    print("No EXIF data found.")
    exif_data = im._getexif()
    #The description is stored in the picture EXIF data
    description = "No Description"

 
  # Add this file information to the dictionary
  picture_dictionary = {"asset":file, "width": im.size[0] , "height": im.size[1], "title": title, "description": description , "file_name": file, "dateTime": TimePict }
 
  print("picture_dictionary", picture_dictionary)

  return picture_dictionary

#***************************************************************************
def build_picture_dictionary1(full_path_name, file):

  im = Image.open(full_path_name)
  #Retrieve just the first part of the file name without the file extension
  file_name = os.path.splitext(file)
  # print(file_name[0])
  #We will use the filename as the title of the photo
  title = file_name[0] 

  # c_time = os.path.getctime(full_path_name)
  # TimePict = time.ctime(c_time)



  #exif_data is special information that is encoded in the photo file.  Using 
  #Microsoft Picture I added a description to each file and this will be the 
  #description information for the file.
  exif_data = im._getexif()

  if exif_data:

    # looping through all the tags present in exif_data
    for tagid in exif_data:
      # getting the tag name instead of tag id
      tagname = TAGS.get(tagid, tagid)
      # passing the tagid to get its respective value
      value = exif_data.get(tagid)  
      
      #The description is stored in the picture EXIF data
      description = str(exif_data.get(0x010e))
      #The time that the picture was taken.
      PictTime = exif_data.get(0x9003)
      # TimePict = os.path.getctime()
      # TimePict = time.ctime(PictTime)
      print("Time = ", PictTime)
# 2009:04:07 16:09:48
      # if(None == TimePict):
      #     TimePict = datetime.strptime("2000/01/01 12:00:00", '%Y/%m/%d %H:%M:%S')
      #     #  TimePict="01/01/00"
      # else:
      #   try: 
      #     TimePict = datetime.strptime(TimePict, '%Y:%m:%d %H:%M:%S')
      #   except ValueError as ve1:    
  else:
    print("No EXIF data found.")
    exif_data = im._getexif()
    #The description is stored in the picture EXIF data
    description = "No Description"

 
  # Add this file information to the dictionary
  picture_dictionary = {"asset":file, "width": im.size[0] , "height": im.size[1], "title": title, "description": description , "file_name": file, "dateTime": PictTime }
 
  print("picture_dictionary", picture_dictionary)

  return picture_dictionary



#***************************************************************************
def write_to_file(path, pict_list):
  #Write the list to a file
  pictlistfile = path + "\\" + "piclistfile.js"
  # print(pictlistfile)
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

    line = fo.writelines("{ " + "src:" + "image"+ str(i) +  ",\n\t" + 
                         "width:" +  width + ",\n\t" +
                         "height:" + heigth + ",\n\t" + 
                         "title:" + "\"" + picture["title"] + "\"" + ",\n\t"+ 
                         "description:" + "\"" + picture["description"] + "\""  +"\n }," "\n\n")
    i +=1
#    line = fo.writelines("{ " + "src:" + "\"" +picture["asset"] + "\""+ ",\t" + "width:" +  width + ",#\t" +"height:" + heigth + ",\t" + "title:" + "\"" + picture["title"] + "\"" +" }," "\n")

  line = fo.writelines("]")

  #Close the file
  fo.close()

#***************************************************************************
#Main Program
#This List will store the individual picture dictionaries  
pict_list=[]
#Get the list of the directories to process
dir_list = get_directory_list()
#Loop through each directory
for dir in dir_list:
  if DEBUG:
    print("dir= " + dir)
    
  print("dir= " + dir)
  file_list = get_file_list(dir)

  for file in file_list:
    if DEBUG:
      print("file=" + file)
    full_path_name = dir + "\\" + file
    picture_dictionary = build_picture_dictionary(full_path_name, file)
    pict_list.append(picture_dictionary)

  pict_list.sort(key=operator.itemgetter('dateTime'))

  write_to_file(dir, pict_list)
  file_list.clear()
  pict_list.clear()


  



