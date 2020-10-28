#import sys
#sys.setrecursionlimit(5000)
#
#from tkinter import *
#import imageio
#from PIL import Image, ImageTk
##def stream():
##    try:
##        image = video.get_next_data()
##        frame_image = Image.fromarray(image)
##        frame_image=ImageTk.PhotoImage(frame_image)
##        l1.config(image=frame_image)
##        l1.image = frame_image
##        l1.after(delay, lambda: stream())
##    except:
##        video.close()
##        return   
## 
##
#root = Tk()
###root.title('Video in a Frame')
##f1=Frame()
##l1 = Label(f1)
##l1.pack()
##f1.pack()
##video_name = "Alexa intro.mp4"   #Image-path
##video = imageio.get_reader(video_name)
##delay = int(1000 / video.get_meta_data()['fps'])
##stream()
###root.mainloop()
#
##
#
#
#import numpy as np
#import cv2
#
#
##capture=cv2.VideoCapture("Alexa intro.mp4")
##red=255;
##green=255;
##blue=255;
##while(1):
##    #read frame by frame
##    ret,frame1=capture.read()
##
###    show=cv2.cvtColor(frame1,cv2.COLOR_BGR2HSV)        #convert to greyscale video
###    lowerlimit=np.array([110,50,50])
###    upperlimit=np.array([130,255,255])
###    mask=cv2.inRange(frame1,lowerlimit,upperlimit)
###    res = cv2.bitwise_and(frame1,frame1, mask= mask)
###    cv2.imshow('original',frame1)
##     
###    if cv2.waitKey(1)&0xFF==ord('r'):
###        red-=20;
###    if cv2.waitKey(1)&0xFF==ord('g'):
###        green-=20;
###    if cv2.waitKey(1)&0xFF==ord('b'):
###        blue-=20;    
###    if cv2.waitKey(1)&0xFF==ord('q'):
###        break
##
##
##capture.release()
###cv2.destroyAllWindows()
##
#
#
##from tkinter import *
#def play(event):
#    print("Play") 
#def pause(event):                           
#    print("Pause ") 
#    
#     
#
#play_btn = Button(None, text='Play')
#play_btn.pack()
#play_btn.bind('<Button-1>', play)
#
#
#pause_btn = Button(None, text='Pause')
#pause_btn.pack()
#pause_btn.bind('<Button-1>', pause) 
#
#play_btn.mainloop()


import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
 
class App:
    
    def __init__(self, window, window_title, video_source=0):
        
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
  
          # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
  
          # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
  
          # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
  
          # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
  
        self.window.mainloop()
  
    def snapshot(self):
          # Get a frame from the video source
          ret, frame = self.vid.get_frame()
  
          if ret:
              
              cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
  
    def update(self):
        
          # Get a frame from the video source
        ret, frame = self.vid.get_frame()
  
        if ret:
            
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
  
        self.window.after(self.delay, self.update)
  
  
class MyVideoCapture:
    
    def __init__(self, video_source="Alexa intro.mp4"):
          # Open the video source
          self.vid = cv2.VideoCapture(video_source)
          if not self.vid.isOpened():
              raise ValueError("Unable to open video source", video_source)
  
          # Get video source width and height
          self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
          self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
  
    def get_frame(self):
        
        if self.vid.isOpened():
            
            ret, frame = self.vid.read()
            if ret:
                
                  # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                
                return (ret, None)
        else:
            return (ret, None)
  
      # Release the video source when the object is destroyed
    def __del__(self):
        
        if self.vid.isOpened():
            
            self.vid.release()
  
  # Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")





