#!/usr/bin/env python 

import os
path= "c:\\MyStuff\\JustCurious\\src\\Travel\\Croatia2023\\Venice\\pictures\\"
print(f"List of all the files in the directory {path}")
files=os.listdir(path)
#Filtering only the files
files=[f for f in files if os.path.isfile(path+'/'+f)]

print(*files, sep="\n")

pictlistfile = path + "piclistfile.js"
print(path)
#Open the file
fo =  open("pictlistfile", "x")
#Write the file
line = fo.writelines(files)
#Close the file
fo.close()



