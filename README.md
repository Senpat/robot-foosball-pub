# robot-foosball

### Explanation of files

#### calc.py
* Inputs last coordinate of the ball, calculates trajectory of ball using previous coordinate, and returns y coordinate of ball at the x coordinate of each lever
* __Derivation of Formulas:__
 1. Intersection Formula
    * ![equation](http://www.sciweavers.org/tex2img.php?eq=y-y_1%20%3D%20%5Cfrac%7By_1-y_2%7D%7Bx_1-x_2%7D%5Ccdot%20%28x-x_1%29&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)
	* ![equation](http://www.sciweavers.org/tex2img.php?eq=%28y-y_1%29%5Ccdot%28%5Cfrac%7Bx_1-x_2%7D%7By_1-y_2%7D%29%2Bx_1%3Dx&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)




#### detectbasic.py
* Given url of image, return the coordinate of the ball
* Assumes ball is only white object in image
* Finds center of mass of all white points
