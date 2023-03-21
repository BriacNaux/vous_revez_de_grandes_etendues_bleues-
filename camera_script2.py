
import tkinter as tk
from tkinter import *
import os
import cv2
import sys
from PIL import Image, ImageTk
from datetime import datetime
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import keyboard
import random
from playsound import playsound
import pygame

from print_script import print_photo
from name_script import saveName



class Application(tk.Frame) :   
    def __init__(self, image, master = None) :
        
        super().__init__(master)
        self.master = master

        self.pack()

        self.createImage(image)

        self.createButton()

    def createImage(self, image) :

        # Créer un cadre pour contenir l'image
        self.image_frame = tk.Frame(self)
        self.image_frame.pack(side="left")

        # Charger l'image et créer un widget pour l'afficher
        self.image = Image.open(image)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(self.image_frame, image=self.photo)
        self.image_label.pack()

    def createButton(self) :
        global Capturebutton

        self.Capturebutton = tk.Button(root, text="Prendre la photo", bg='#dbb184', command=choice)
        self.Capturebutton.place(bordermode=tk.OUTSIDE, x = 530, y = 570, anchor=tk.CENTER, width=300, height=50)
        self.Capturebutton.focus()
   
    def choice(event = 0) : 
        global pause, button, acceptButton, TryAgainButton
        pause = True


        Capturebutton.place_forget()
        acceptButton = tk.Button(root, text="J'aime bien cette image", command=saveAndPrint)
        TryAgainButton = tk.Button(root, text="Non horrible je recommence", command=resume)
        acceptButton.place(anchor=tk.CENTER, x = 425, y = 570, width=200, height=50)
        TryAgainButton.place(anchor=tk.CENTER, x = 660, y = 570, width=200, height=50)

        acceptButton.focus()
        TryAgainButton.focus()
        playsound("music/appareil_photo.wav")

    def saveAnPrint(self) : 
        pass
    def resume(self) :
        pass
if __name__ == "__main__":

    root = tk.Tk()
    root.geometry("1520x1080+0+0")
    root.configure(bg='#fa07fa')

    mainWindow = Application("mainWindow_image.png", master=root)


    mainWindow.mainloop()