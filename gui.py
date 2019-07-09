import os

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

""" M down ve, sua lai show_output
    
"""
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
        # label Image name
        self.images_label = []
        # output image
        self.output_label = tk.Label(self.root)

    def choose_image(self):
        """ Browsing Image files """
        image_file = filedialog.askopenfile()
        name = image_file.name
        self.images_path.append(name)
        # pack to root
        new_label = tk.Label(self.root, text=name)
        self.images_label.append(new_label)
        self.images_label[-1].pack(side="top")
    
    def stitching(self):
        """ Ham cua m de o day :)
        """




        ### cai nay show output chu k lam gi het
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



