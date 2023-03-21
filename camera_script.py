
import tkinter
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

# initiations
fileName = os.environ['ALLUSERSPROFILE'] + "\WebcamCap.txt"
pause = False
pygame.mixer.init()

#functions :
# choice function after capture :
def play(music = "") :
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(loops= 100)

def stop_music() :
    pygame.mixer.music.stop()




def choice(event = 0):
    global pause, button, acceptButton, TryAgainButton
    pause = True


    Capturebutton.place_forget()
    acceptButton = tkinter.Button(mainWindow, text="J'aime bien cette image", command=saveAndPrint)
    TryAgainButton = tkinter.Button(mainWindow, text="Non horrible je recommence", command=resume)
    acceptButton.place(anchor=tkinter.CENTER, x = 425, y = 570, width=200, height=50)
    TryAgainButton.place(anchor=tkinter.CENTER, x = 660, y = 570, width=200, height=50)


    playsound("music/appareil_photo.wav")


def saveAndPrint(event = 0):
    global prevImg, filepath
    current_time = datetime.now().strftime("%H_%M_%S")
    
    
    
    if (len(sys.argv) < 2):
        filepath = f'savedImages/{current_time}.png'
    else:
        filepath = sys.argv[1]

    print ("Output file to: " + filepath)
    prevImg.save(filepath)

    messageBox(filepath)



def messageBox(photo_to_print) :
    global entree
    
    acceptButton.place_forget()
    TryAgainButton.place_forget()

    nameTaker= tkinter.Toplevel(mainWindow)
    nameTaker.geometry("350x120+500+250")
    nameTaker.configure(bg='#f314ff')
    label = Label(nameTaker, text="Rentrer votre prénom \n ou votre psuedoyme :", font=("Arial", 15), bg='#03e8fc' )
    label.pack(side=TOP)
    
    
    entree = Entry(nameTaker, width=60)
    entree.insert(0, "Ecrivez ici")
    entree.pack(side= TOP)  

    btn =Button(nameTaker, text='Confirmation',bg='#03e8fc', command=lambda:[getEntry(),nameTaker.destroy(), AcceptBox(photo_to_print)])
    btn.pack()

    nameTaker.grab_set()
    
def AcceptBox(photo_to_print) :

    acceptTaker= tkinter.Toplevel(mainWindow)
    acceptTaker.geometry("650x120+500+250")

    label = Label(acceptTaker, text="Etes-vous sûr de vouloir fournir vos infromations personnelles \n à Enzo Pernet ?", font=("Arial", 15))
    label.pack(side=TOP)
    Accepterbouton=Button(acceptTaker, text="Oui, sans aucune hésitation",
                           command=lambda: [acceptTaker.destroy(), printingScreen(), print_photo(photo_to_print), saveName(name, photo_to_print)], width=50, height=4, bg='#03e8fc')
    Accepterbouton.pack()

    acceptTaker.grab_set()

def getEntry() :
    global name
    name = entree.get()
    print(name)

def resume(event = 0):
    global acceptButton, TryAgainButton, Capturebutton, lmain, pause
    
    pause = False

    acceptButton.place_forget()
    TryAgainButton.place_forget()

    mainWindow.bind('<Return>', choice)
    Capturebutton.place(bordermode=tkinter.OUTSIDE, x = 530, y = 570, anchor=tkinter.CENTER, width=300, height=50)
    lmain.after(10, show_frame)
    

def show_frame():
    global pause, prevImg, button, indexImg

    
    success, img = capture.read()

    imgOut = segmentor.removeBG(img, imgList[indexImg], threshold=0.2)

    prevImg = Image.fromarray(imgOut)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if not pause:
        lmain.after(100, show_frame)

    key = cv2.waitKey(1)

    if keyboard.is_pressed('q') :
        if indexImg>0 :
            indexImg -= 1

    elif keyboard.is_pressed('d') :
        if indexImg<len(imgList)-1 :
            indexImg += 1
    

#timer function for inactivity sensitivity
timer = None

def reset_timer(event=None):
    global timer

    # pause the previous event
    if timer is not None:
        mainWindow.after_cancel(timer)

    # create new timer
    timer = mainWindow.after(60000, screenSaver)

#screen saver function called if inactivity detected bu the reset_timer function
def screenSaver() :
    global screen_saver

    #declaration of the screen Saver window
    screen_saver = tkinter.Toplevel(mainWindow)
    screen_saver.geometry("1520x1080+0+0")
    
    #image enzo declaration for screenSaver window
    canvas = Canvas(screen_saver, width=1520, height=1080)   
    canvas.create_image(0, 0, anchor=NW, image=sSimage)
    canvas.pack()

    

#screen Saver quit function called if any key pressed, it reset the timer
def quit_screen_saver(event = 0) :
    
    
    reset_timer()

    try :
        screen_saver

    except NameError :
        pass
    else : 
        screen_saver.destroy()
    
def check_music():
    global screen_saver

    try :
        screen_saver
    except NameError :
            pass
    else :

        ss_exists = screen_saver.winfo_exists()

        if ss_exists == 1:   

            stop_music()
        
        else : 
            

            if pygame.mixer.music.get_busy() == False :

                stop_music()
                play("music/mainWindow_music.wav")




    mainWindow.after(100, check_music)

def quit_printing_screen() :

    printing_screen.destroy()
    reset_timer
    stop_music()
    play("music/mainWindow_music.wav")
    resume()



def printingScreen() :
    global printing_screen, value_label
    #declaration of the screen Saver window
    printing_screen = tkinter.Toplevel(mainWindow)
    printing_screen.geometry("1920x1080+0+0")
    printing_screen.configure(bg='#03e8fc')
    
    
     #image enzo declaration for screenSaver window
    canvas = Canvas(printing_screen, width=1920, height=1080)
    canvas.create_image(0, 0, anchor=NW, image=print_image)
    canvas.pack()

    printing_screen.after(40000, quit_printing_screen)

    stop_music()
    play("music/printing_screen_music.wav")
    
def slideShow() :
    global indexSavedImg, listSavedImg,img

    random_num = random.randint(0,len(listSavedImg)-1)

    random_num2 = random.randint(0,len(listSavedImg)-1)

    random_num3 = random.randint(0,len(listSavedImg)-1)

    slide1.configure(image=num_choose(1,random_num))
 
    slide2.configure(image=num_choose(2,random_num2))

    slide3.configure(image=num_choose(3,random_num3))

    side_window.after(2500, slideShow)



#images for the slide show on the right side 
def num_choose(slide_number = 0, num = 0) :
    global new_image1, new_image2, new_image3
    
    img = (Image.open(f'savedImages/{listSavedImg[num]}'))

    resized_image = img.resize((320,240), Image.Resampling.LANCZOS)
    if slide_number == 1 :
        new_image1= ImageTk.PhotoImage(resized_image)
        return new_image1
    if slide_number == 2 :
        new_image2= ImageTk.PhotoImage(resized_image)
        return new_image2
    if slide_number == 3 :
        new_image3= ImageTk.PhotoImage(resized_image)
        return new_image3

   
# capture setup
capture = cv2.VideoCapture(0)
capture.set(3, 640)
capture.set(4, 480)
segmentor = SelfiSegmentation()


# background img list maker for keyboard bc switch
listImg = os.listdir("images")

imgList = []
for imgPath in listImg:
    img = cv2.imread(f'images/{imgPath}')
    imgList.append(img)
indexImg = 0

# list of savedImages :
listSavedImg = os.listdir("savedImages")

# settting up tkinter shit
# main window
mainWindow = tkinter.Tk(screenName="Camera Capture")
mainWindow.geometry("1120x1080+0+0")
mainWindow.configure(bg='#fa07fa')

#image for mainwindow
img = (Image.open("mainWindow_image.png"))
mainWindow_resized_image = img.resize((1520,1080), Image.LANCZOS)
img_final = ImageTk.PhotoImage(mainWindow_resized_image)
background = Label(mainWindow, compound=tkinter.LEFT,anchor=tkinter.CENTER,relief = tkinter.RAISED)
background.place(x=0,y=0)
background.configure(image =img_final)


#little right window
side_window = tkinter.Toplevel(mainWindow)
side_window.geometry("400x1080+1120+0")
side_window.configure(bg='#171717')



# images :
#image for the screenSaver
sSimage = PhotoImage(file="screen_saver_image.png")

#image for the printing screen
print_image = PhotoImage(file="print_image.png")


#image for the side window
side_window_image = PhotoImage(file="side_window_image.png")


# side windows slideshows pack :

pic = Label(side_window, compound=tkinter.LEFT, anchor=tkinter.CENTER, relief=tkinter.RAISED)
pic.configure(image= side_window_image)
pic.place(x=20,y=10)


slide1 = Label(side_window, compound=tkinter.LEFT, anchor=tkinter.CENTER, relief=tkinter.RAISED)
slide1.place(x=30,y=100)

slide2 = Label(side_window, compound=tkinter.LEFT, anchor=tkinter.CENTER, relief=tkinter.RAISED)
slide2.place(x=30,y=390)

slide3 = Label(side_window, compound=tkinter.LEFT, anchor=tkinter.CENTER, relief=tkinter.RAISED)
slide3.place(x=30,y=690)


#lmain
lmain = Label(mainWindow, compound=tkinter.LEFT, anchor=tkinter.CENTER, relief=tkinter.RAISED)
lmain.place(x=215,y=40)



#captureButton
Capturebutton = tkinter.Button(mainWindow, text="Prendre la photo", bg='#dbb184', command=choice)
Capturebutton.place(bordermode=tkinter.OUTSIDE, x = 530, y = 570, anchor=tkinter.CENTER, width=300, height=50)

# biding :
mainWindow.bind_all("<Motion>", quit_screen_saver)

play("music/mainWindow_music.wav")

slideShow()
reset_timer()   
show_frame()
check_music()
mainWindow.mainloop()