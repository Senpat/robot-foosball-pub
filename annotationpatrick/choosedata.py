import glob, os
import sys
import random
from shutil import copyfile


current_dir = sys.argv[1];

final_dir = sys.argv[2];

numdata = 1000

total_size = len(os.listdir(current_dir))
'''
for path, dirs, files in os.walk(current_dir):
    for f in files:
        fp = os.path.join(path, f)
        total_size += os.path.getsize(fp)
'''
print("Directory size: " + str(total_size))

data = random.sample(range(0,total_size),numdata)

num = 0
for i in data:
	num+=1
	if(num % 100 == 0): print(num)
	copyfile(current_dir + "/"+ str(i) + ".jpg",final_dir + "/"+ str(i) + ".jpg")
