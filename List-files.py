import os

for root, dirs, files in os.walk("."):  
    for filename in files:
        if (len(root) <= 1):
            print(dirs , " \ " , filename)
        elif (len(root) > 1):
            print(root , " \ " , filename)