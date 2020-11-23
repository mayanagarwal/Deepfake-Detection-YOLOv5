import json
import os

dict = {}

def changeline(path,filename):
    path = path[:-3] + "txt"
    new1 = "fake"
    try:
        fin = open(path, "rt")
        for line in fin: 
            if line[0] == '0':
                new1 = "real"
        fin.close()
    except:
        print("default")

    dict[filename] = new1

for file in os.listdir("./"):
	if file.endswith(".png"):
		path = os.path.join("./",file)
		changeline(path,file)
    
print(dict)
