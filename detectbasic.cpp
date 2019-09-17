#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/calib3d/calib3d.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <stdio.h>
using namespace std;
using namespace cv;
int main()
{
	VideoCapture cp("test.mov");
	int frame_width = cp.get(CAP_PROP_FRAME_WIDTH);
	int frame_height = cp.get(CAP_PROP_FRAME_HEIGHT);
	VideoWriter video("out.avi", VideoWriter::fourcc('M', 'J', 'P', 'G'),30, Size(frame_width, frame_height));
   while (1)
   {
      Mat src;
		cap >> src;
		if (src.empty())
			break;
      int x_accum=0;
      int y_accum=0;
      int ctpix=0;
      for (int x=0;x<frame_width;x++)
      {
         for (int y=0;y<frame_height;y++)
         {
            Vec3b colour=src.at<Vec3b>(Point(x,y));
            if(200<colour.val[0]&&colour.val[0]<255 && 200<colour.val[1]&&colour.val[1]<255 && 200<colour.val[2]&&colour.val[2]<255)
            {
               x_accum+=x;
               y_accum+=y;
               ctpix++;
            }
         }
      }
      Point2i ball_loc(x_accum/ctpix,y_accum/ctpix);
      circle(src,ball_loc,3,(255,0,0),3);
      video.write(src);
   }
	// When everything done, release the video capture and write object
	cap.release();
	video.release();

	// Closes all the windows
	destroyAllWindows();
	//////
	
	waitKey(0);
	return 0;
}