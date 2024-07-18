#!/usr/bin/env python 

import os
#from PIL import Image

# https://justcuriousbugs.atlassian.net/browse/JCWSD-76 - SlideShow for all travel pages currently imports pictures.  I would like to just use all pictures that are in the pictures folder in the slideshow.

# This program will be used in the JustCurious website build.  I have been able to use PhotoGallery in the travel section 
# of the website to provide a icon list of the photos and then a gallery list if someone clicks on any photo.  What I want to 
# do to make the process more generic is to dump the files that I want to use into a folder, and then generate an array that 
# contains the picture name, the height and width of the photo, a caption and a title for the photo

# I would like the list of folders to be processed to be provided in a files
# I would like the array data for each folder to be stored in a file in the folder


# I used this to help me get the list of files
# https://www.geeksforgeeks.org/python-list-files-in-a-directory/

# This helped me store the list to a file
# https://stackoverflow.com/questions/899103/writing-a-list-to-a-file-with-python-with-newlines

# Next Steps.  
# 1) I need to setup a new dictionary list that has:
# a) The file name, 
# b) The picture width
# c) The picture height




path= "c:\MyStuff\JustCurious\src\Travel\Croatia2023\Venice\pictures"
# path= "c:\\MyStuff\\JustCurious\\src\\Travel\\Croatia2023\\Venice\\pictures\\"
print(f"List of all the files in the directory {path}")
files=os.listdir(path)

#Filtering only the files
files=[f for f in files if os.path.isfile(path+'/'+f)]

# print(*files, sep="\n")
pict_list=[]
for list in files:
  picture_dictionary = {"asset":list, "width": "1", "height": "2"}
  pict_list.append(picture_dictionary)


for item in pict_list:
  print("asset:" + "\t" + item["asset"] + "width:" + "\t" + item["width"] + "\t" + item["height"])
    # for client in result_list:
    #     print(client["ip"] + "\t\t" + client["mac"])


#Write the list to a file
pictlistfile = path + "\piclistfile.js"

# print(pictlistfile)
#Open the file
fo =  open(pictlistfile, "w+")




#Write the file
line = fo.writelines(files)
#Close the file
fo.close()



