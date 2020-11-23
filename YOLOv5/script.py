import json
import os
import random


fin1 = open("./custom_train/train_final.txt", "a+")
fin2 = open("./custom_train/valid_final.txt", "a+")

my_randoms = random.sample(range(0, 1000), 800)
for file in os.listdir("../yolov3/custom_data/deepfake/images/"):
	path = os.path.join("../yolov3/custom_data/deepfake/images/",file)
	split = file.split("_")
	if int(split[1]) in my_randoms:  
		fin1.write(path + "\n")
	else:
		fin2.write(path + "\n")

fin1.close()
fin2.close()