import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
#import image_stitching
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
        # path to images
        self.images_path = []
        # LIST IMAGE
        self.image_list = []
        # label Image name
        self.images_label = []
        # output image
        self.output_label = tk.Label(self.root)

    def choose_image(self):
        """ Browsing Image files """
        image_file = filedialog.askopenfile()
        name = image_file.name
        self.images_path.append(name)
        # images to stich list
        image = cv2.imread(name)
        self.image_list.append(image)
        
        # pack to root
        new_label = tk.Label(self.root, text=name)
        self.images_label.append(new_label)
        self.images_label[-1].pack(side="top")
    

    def stitching(self):
        print("[INFO] stitching images...")
        
        stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
        (status, stitched) = stitcher.stitch(self.image_list)
        #
        if status == 0:
    # check crop out the largest rectangular
    # region from the stitched image
            print("[INFO] cropping...")
            stitched = cv2.copyMakeBorder(stitched, 5, 5, 5, 5,
            cv2.BORDER_CONSTANT, (0, 0, 0))

        # convert the stitched image to grayscale and threshold it
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

    # write the output stitched image to disk
            cv2.imwrite("output11.jpg", stitched)

    # display the output stitched image to our screen
            cv2.imshow("Stitched", stitched)
            cv2.waitKey(0)

    # being detected
        else:
            print("[INFO] image stitching failed ({})".format(status))
        
        self.output_label.destroy()
        self.output_label = tk.Label(self.root, text="IMAGE ARE STITCHED")
        self.output_label.pack(side="bottom")
        
    def loop(self):
        
        # choose image button
        choose_button = tk.Button(self.root, text="CHOSE IMAGES",
                font=("Times", 14, "bold"), bd=2,
                command=self.choose_image)
        choose_button.pack(side="top")

        # output image button
        output_button = tk.Button(self.root, text="STITCH",
                font=("Times", 14, "bold"), bd=2,
                command=self.stitching)
        output_button.pack(side="bottom")
        self.root.mainloop()

a = Board(400,300)
a.loop()
