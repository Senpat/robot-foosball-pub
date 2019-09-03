
#Constants
#(0,0) is top left corner, (W,H) is bottom right
YU = 100
YD = 260
LEVERS = {40,80,160,240}



prev = []

#takes in a point (px,py) which is the latest coordinate of the ball.
#uses list of past points
#return list that contains the y coordinate of ball at each of the levers
def calc(px,py):
	global prev

	#prev is empty
	if(not prev):
		prev = {(px,py)}
		return

	#ball is going forward - check px > x of last point
	if(px >= prev[-1][0]):
		prev = {(px,py)}
		return

	prev.append((px,py))

	#list that contains the y coordinate of ball at each of the levers
	#-1 means ball is in front of lever, so don't move it
	ret = {-1,-1,-1,-1}

	#for brevity - (x1,y1) is current point of ball, (x2,y2) is previous point of ball
	x1=px
	y1=py
	x2=prev[-1][0]
	y2=prev[-1][1]

	#ball is going up
	if(y1<=y2):
		#x coordinate when the ball bounces off of YU
		#-99 means it never intersects YU, so when py == prev[-1][1]
		intersect = -99
		if(y1 != y2):
			intersect = (YU-y1)*(x1-x2)/(y1-y2) + x1				#FORMULA #1: Intersection Formula

		for i in range(len(LEVERS)):
			#find y coordinate when ball crosses LEVERS[i]

			y = (y1-y2)*(LEVERS[i]-x1)/(x1-x2)+y1

			#check if ball will bounce before reaching LEVERS[i]
			if(y < YU):
				y += 2*(YU-y)

			ret[i] = y

	#ball is going down
	else:


		intersect = (YD-y1)*(x1-x2)/(y1-y2) + x1

		for i in range(len(LEVERS)):
			#find y coordinate when ball crosses LEVERS[i]

			y = (y1-y2)*(LEVERS[i]-x1)/(x1-x2)+y1

			#check if ball will bounce before reaching LEVERS[i]
			if(y > YD):
				y -= 2*(y-YD)

			ret[i] = y

	return ret







if __name__ == "__main__":
	pass
