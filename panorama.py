#import package
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import imutils
import argparse
import numpy as np

class Board:
    """ GUI for image stitching """
    def __init__(self, width=None, height=None):
        """ Create root window
        """
        self.root = tk.Tk()
        self.width = width
        self.height = height

        # screen resolution
        if width == None:
            self.width = self.root.winfo_screenwidth() - 100
        if height == None:
            self.height = self.root.winfo_screenheight() - 100

        self.root.wm_geometry("{}x{}+{}+{}".format(self.width, self.height, 0, 0))
        self.root.wm_resizable(False, False)

        #
        # path to images
        self.images_path = []
        # LIST IMAGE
        self.image_list = []
        # label Image name
        self.images_label = []
        # output image
        self.output_label = tk.Label(self.root)
        self.quit_button = tk.Button(self.root)
        #
        self.create_widgets()
    
    
    #create widget
    def create_widgets(self):
        self.label = tk.Label(text = "Panorama App",font="Consalas 35", fg="blue")
        self.label.pack(pady=10)


    def choose_image(self):
        """ Browsing Image files """
        image_file = filedialog.askopenfile()
        name = image_file.name
        self.images_path.append(name)
        # images to stich list
        image = cv2.imread(name)
        self.image_list.append(image)
        #im = image.subsample(3,3)
        #cv2.imshow("Input",im)
        
        # pack to root
        new_label = tk.Label(self.root, text=name)
        self.images_label.append(new_label)
        self.images_label[-1].pack(side="top")
    

    def stitching(self):
        #create oject for sticher
        stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
        (status, stitched) = stitcher.stitch(self.image_list)
        if status == 0:

        #crop out the image with 5 pixcel
            stitched = cv2.copyMakeBorder(stitched, 5, 5, 5, 5,
            cv2.BORDER_CONSTANT, (0, 0, 0))

        # convert to grayscale and threshold it
            gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

        # the stitched image
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            c = max(cnts, key=cv2.contourArea)

        # rectangular bounding box of the stitched image region
            mask = np.zeros(thresh.shape, dtype="uint8")
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

        # create two copies of the mask: one to serve as our actual
            minRect = mask.copy()
            sub = mask.copy()

            while cv2.countNonZero(sub) > 0:
            # erode the minimum rectangular mask and then subtract
            # the thresholded image from the minimum rectangular mask
                minRect = cv2.erode(minRect, None)
                sub = cv2.subtract(minRect, thresh)

            cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            c = max(cnts, key=cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(c)

        # stitched image
            stitched = stitched[y:y + h, x:x + w]

    # write output to disk
            cv2.imwrite("output.jpg", stitched)

    # display to screen
            newimg = cv2.resize(stitched,(1366,768))
            cv2.imshow("Stitched", newimg)
            cv2.waitKey(0)
            self.output_label.destroy()
            self.output_label = tk.Label(self.root, text="IMAGE ARE STITCHED", fg="red")
            self.output_label.pack(side="bottom")
    # Not stitching
        else:
            print("Image stitching failed ")
        
        
        
    def loop(self):
        
        # choose image button
        choose_button = tk.Button(self.root, text="CHOSE IMAGES",
                font=("Consalas", 14, "bold"), bd=4,
                command=self.choose_image)
        choose_button.pack(side="top")

        #Quit button
        quit_button = tk.Button(self.root, text="QUIT",
               font=("Consalas", 14,"bold"),fg ="red", bd=4,
              command=self.root.destroy)
        quit_button.pack(side="bottom")

        
        # output image button
        output_button = tk.Button(self.root, text="STITCH",
                font=("Consalas", 14, "bold"), bd=4,
                command=self.stitching)
        output_button.pack(side="bottom")

        
        self.root.mainloop()
#Create board
a = Board(500,400)
a.loop()

