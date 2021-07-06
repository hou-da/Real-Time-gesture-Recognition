# import the necessary packages
from __future__ import print_function
import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import datetime

class Application(tk.Frame):

    def __init__(self, master=None, video_source=0):
        tk.Frame.__init__(self, master)
        self.size = 500
        self.pack()
        self.video_source = video_source
        self.vid = MyVideoCapture(self.video_source)

        self.canv = tk.Canvas(self, bg="gray", height=self.size, width=self.size)
        self.canv.pack()

        # create a button, that when pressed, will take the current frame and save it to file

        self.snapshotButton = tk.Button(self, text="Snapshot", command=self.snapshot)
        self.snapshotButton.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

        self.delay = 15
        self.update()
        self.master.mainloop()

    def snapshot(self):
        #
        ret, frame = self.vid.get_frame()
        # grab the current timestamp and use it to construct the file name
        ts = datetime.datetime.now()
        name = '.\\image\\nothing' + '\\frame' + '{}.jpg'.format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        print('Creating...' + name)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # save the file
        cv2.imwrite(name, frame.copy())

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canv.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.after(self.delay, self.update)

class MyVideoCapture:
    """docstring for  MyVideoCapture"""
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("unable open video source", video_source)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

if __name__ == "__main__":
    app = tk.Tk()
    app.title('Video Capture')
    display = Application(app)
    app.mainloop()
