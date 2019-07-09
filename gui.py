import os

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class Board:
    """ GUI for image stitching """
    def __init__(self, width=None, height=None):
        """ Create root window

        """
        self.root = tk.Tk()
        
        # screen resolution
        if width == None:
            width = self.root.winfo_screenwidth() - 100
        if height == None:
            height = self.root.winfo_screenheight() - 100

        self.root.wm_geometry("{}x{}+{}+{}".format(width, height, 0, 0))
        self.root.wm_resizable(False, False)
        # path to images
        self.images_path = []

        # image (opened from ImageTk)
        self.images = []
        
        # maximum width of an image input showed up on window
        self.max_width = 150
        # number of image can show up
        self.maximum_images = int((width - 100)/200)
        # current input images on window
        self.current_image = 0
        # initial labels for set images
        self.images_label = [tk.Label(self.root) for _ in range(self.maximum_images)]



    def choose_image(self):
        """ Browsing Image files """
        image_file = filedialog.askopenfile()
        name = image_file.name
        
        # dir path use for showing image
        dir_path = os.getcwd()
        current_image_name = name[len(dir_path) + 1:]

        # Open image and resize with PIL
        img = Image.open(name)
        scale = self.max_width / img.width
        img = img.resize((int(scale*img.width), int(scale*img.height)))
        img = ImageTk.PhotoImage(img)
        self.images_path.append(name)
        self.images.append(img)
        # pack to root
        self.images_label[self.current_image].config(image=self.images[-1],
                text=current_image_name,
                compound="top")
        self.images_label[self.current_image].pack(anchor="nw", side="left")
        self.current_image += 1

    def show_output(self):
        """ Output function
        """
        pass

    def loop(self):
        
        # choose image button
        choose_button = tk.Button(self.root, text="CHOSE IMAGES",
                bg="red", fg="white", font=("Times", 20, "bold"), bd=3,
                command=self.choose_image)
        choose_button.pack(side="top")

        # output image button
        output_button = tk.Button(self.root, text="OUTPUT IMAGE",
                bg="red", fg="white", font=("Times", 20, "bold"), bd=3,
                command=self.show_output)
        output_button.pack(side="bottom")
        self.root.mainloop()

a = Board(800,600)
a.loop()



