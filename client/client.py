# 0 - create room
# 1 - join room
# 2 - play
# 3 - pause
# 4 - play at

# TODO: Import the message queue list from utility.py in here and keep reading it

import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

from tkinter import filedialog 
import client_utility as cu


class Home:
    
    def __init__(self, window, window_title):

        self.window = window
        self.window.title(window_title)
         
        
        self.textExample = tkinter.Text(window, height=4)
        self.textExample.pack()
 

          # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = 10, height = 10)
        self.canvas.pack()
        
          # Button that lets the user take a snapshot
        self.btn_submit=tkinter.Button(window, text="Submit", width=30,command = self.home ) 
        self.btn_submit.pack(anchor=tkinter.CENTER, expand=True)
        
        # self.btn_browse=tkinter.Button(window, text="UserPage", width=30,command = self.browse ) 
        # self.btn_browse.pack(anchor=tkinter.CENTER, expand=True)
        
        self.window.mainloop()
        
    
    def browse(self):
        
        def browseFiles():
          
            filename = filedialog.askopenfilename(initialdir = "/", 
        										title = "Select a File", 
        										filetypes = (("Text files", 
        														"*.txt*"), 
        													("all files", 
        														"*.*"))) 
        	
 
            label_file_explorer.configure(text="File Opened: "+filename) 
 
        self.window = tkinter.Tk()  
 
        self.window.title('File Explorer') 
 
        self.window.geometry("500x500") 
 
        self.window.config(background = "white") 
 
        label_file_explorer = tkinter.Label(self.window, 
        							text = "File Explorer using Tkinter", 
        							width = 100, height = 4, 
        							fg = "blue") 
        
        	
        button_explore = tkinter.Button(self.window, 
        						text = "Browse Files", 
        						command = browseFiles,width=10) 
        
        button_exit = tkinter.Button(self.window, 
        					text = "Exit", 
        					command = exit,width=10) 
        
        # get username from receive message
        btn_create = tkinter.Button(self.window, 
        						text = "Create Room", 
        						command = cu.create_room("Aravind"),width=10) 
        code = tkinter.Text(self.window, height=2)
        btn_join = tkinter.Button(self.window, 
        						text = "Join Room", 
        						command =cu.join_room("aravind",1),width=10) 
        
 
        label_file_explorer.grid(column = 1, row = 1) 
        code.grid(column=1,row = 3)
        button_explore.grid(column = 1, row = 4) 
        btn_create.grid(column = 1,row = 5)
       
        btn_join.grid(column = 1,row = 6) 
        button_exit.grid(column = 1,row = 7) 
        
        # Let the window wait for any events 
        self.window.mainloop() 

    
    
    
        
    def home(self):
        App(tkinter.Tk(), "Home Page")
    
    

class App:

    def __init__(self, window, window_title, video_source=0):

        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        
        self.textExample = tkinter.Text(window, height=10)
        self.textExample.pack()
        
          # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

          # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
        
          # Button that lets the user take a snapshot
        self.btn_pause=tkinter.Button(window, text="Pause", width=50, command=self.pause)
        self.btn_play = tkinter.Button(window, text="Play", width=50, command=self.play)
        self.btn_pause.pack(anchor=tkinter.CENTER, expand=True)
        self.btn_play.pack(anchor=tkinter.CENTER, expand=True)

          # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def pause(self):
        print("pause button pressed")
          # Get a frame from the video source
#          ret, frame = self.vid.get_frame()
#
#          if ret:
#
#              cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def play(self):
        
        print("play button pressed")

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

#
#
#class UserPage:
#    
#    def __init__(self):
#        
#        
#        

  # Create a window and pass it to the Application object
Home(tkinter.Tk(), "Tkinter and OpenCV")


