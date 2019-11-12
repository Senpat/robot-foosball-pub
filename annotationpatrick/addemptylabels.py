import glob, os

# Current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

print(current_dir)

current_dir = 'C:/Users/zz198/Desktop/Senior Research/robot-foosball/annotationpatrick/Patrick/Images'


for pathAndFilename in glob.iglob(os.path.join(current_dir, "*.jpg")):
	title, ext = os.path.splitext(os.path.basename(pathAndFilename))

	if(not os.path.isfile(current_dir + "/" + title + ".txt")):
		print(title)
		open(current_dir + "/" + title + ".txt",'a').close()
