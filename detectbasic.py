import PIL
from PIL import Image
import urllib.request
import io
import sys
import time
import random
D = 3
W = -1
H = -1																		#dimensions

thresh = 25


if __name__ == "__main__":
	start_time = time.time()
	random.seed(200)

	#print(PIL.PILLOW_VERSION)

	K = -1
	f = io.BytesIO(urllib.request.urlopen('https://cf.geekdo-images.com/imagepage/img/5lvEWGGTqWDFmJq_MaZvVD3sPuM=/fit-in/900x600/filters:no_upscale()/pic260745.jpg?fbclid=IwAR2b1R0F-4ssT42HAak69tE8fqZjOah8BEfMgo70js0GcTTPSJBKBMo3C2s').read())
	for i in range(1,len(sys.argv)):
		if(sys.argv[i].isdigit()):
			K = int(sys.argv[i])
		elif('https' in sys.argv[i]):
			f = io.BytesIO(urllib.request.urlopen(sys.argv[i]).read())
		else:
			f = sys.argv[i]

	img = Image.open(f)
	pix = img.load()
	W = img.size[0]
	H = img.size[1]

	xtotal = 0
	xcount = 0
	ytotal = 0
	ycount = 0

	for x in range(W):
		for y in range(H):
			if(pix[x,y][0] < thresh and pix[x,y][1] < thresh and pix[x,y][2] < thresh):
				xtotal += x
				ytotal += y
				xcount += 1
				ycount += 1


	answerx = xtotal/xcount
	answery = ytotal/ycount
	print(str(answerx) + " " + str(answery))
