import threading
import os
import RPi.GPIO as GPIO
from tkinter import *
import time
import picamera
import subprocess
import PIL
from PIL import ImageTk, Image

os.chdir('/home/pi/code/toastboxy/Python/')

camera = picamera.PiCamera()
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#camera.preview_fullscreen=False
#camera.preview_window(100,100,260,200)
#use_video_port=True

tkimage = {}
jpgimage = {}
pic = {}
picname = {}

time_old=time.time()
camera.resolution = (2592,1944)
#camera.hflip = True
#camera.vflip = True
camera.preview_alpha = 220
global done
done = False
global bigfont
bigfont = 'arial',250,'bold'
smallfont = 'arial',25,'bold'

def esc(event):
    camera.stop_preview()

def countdown():
    for i in range(1,4):#change to 4
        time.sleep(1)
        c1.itemconfigure(text1,font=(bigfont),text='%i' % (5-i))
        c1.update()
    time.sleep(1)
    c1.itemconfigure(text1,font=(smallfont),text='SMILE :-)')
    c1.update()
	
def initialize():
    main.number = 0
    for i in range (1,5):
        print (i)
        c1.itemconfigure(tkimage[i], image = picturey, anchor=NW)
    c1.itemconfigure(text1,font=(smallfont),text='GET\nREADY\nPUSH\nTHE\nBUTTON')
    c1.update()
    camera.resolution = (1296,972)
    camera.start_preview(fullscreen=False, window=(54,54,1296,972))
    #camera.start_preview(fullscreen=False, window=(-200,0,1920,1080))
	

def processing():
    while 1:
        if done:
            break
        c1.itemconfigure(text1,font=(smallfont),text='PRO\nCESS\nING.')
        c1.update()
        time.sleep(0.3)
        print ("Procsessing.")
        c1.itemconfigure(text1,font=(smallfont),text='PRO\nCESS\nING..')
        c1.update()
        time.sleep(0.3)
        print ("Procsessing..")
        c1.itemconfigure(text1,font=(smallfont),text='PRO\nCESS\nING...')
        c1.update()
        time.sleep(0.3)
        print ("Procsessing...")
        
def stuff(event):
    global done
    global time_old
    time_new = time.time()
    print (time_old)
    print (time_new)
    print (time_new - time_old)
    if main.number < 5 and ((time_new - time_old) > 5):
        time_old = time_new
        main.number += 1
        print("cam%i.jpg" % main.number)
        if main.number > 0 and main.number < 5:
            picname[main.number] = time.strftime("%Y%m%d-%H%M%S")
            #camera.start_preview(fullscreen=False, window=(-200,0,1920,1080))
            countdown()
            camera.stop_preview()
            camera.resolution = (2592,1944)
            camera.capture('storage/single_%s.jpg' % picname[main.number])#,resize=(740,555))
            
            im = Image.open('storage/single_%s.jpg' % picname[main.number])
            im = im.resize((740,555), Image.ANTIALIAS)
            jpgimage[main.number] = ImageTk.PhotoImage(im)
            c1.itemconfigure(tkimage[main.number], image = jpgimage[main.number], anchor=NW)
            
            c1.itemconfigure(text1,font=(smallfont),text='TAKE\nA\nPICTURE\n:-)')
            c1.update()
            time.sleep(2)
            camera.resolution = (1296,972)
            camera.start_preview(fullscreen=False, window=(54,54,1296,972))
            #camera.start_preview(fullscreen=False, window=(-200,0,1920,1080))

        if main.number == 4:
            camera.stop_preview()
            c1.itemconfigure(text1,font=(smallfont),text='PICTURE\nOK?')
            c1.update()
            
        if main.number == 5:
            imgname = time.strftime("%Y%m%d-%H%M%S")
            c1.itemconfigure(text1,font=(smallfont),text='JUST\nA\nMOMENT\nSTARTING\nPRINTER')
            c1.update()
            time.sleep(1)
            #processing
            #t = threading.Thread(target=processing)
            #t.start()
            print ("collage_%s.jpg" % imgname)
            command = "convert  -size 2802x1891 xc:skyblue \
	    -draw \"image over 0,0 2802,1891 'frame.gif'\" \
	    -draw \"image over 90,90 1110,832 'storage/single_%s.jpg'\" \
	    -draw \"image over 1230,90 1110,832 'storage/single_%s.jpg'\" \
	    -draw \"image over  90,952 1110,832 'storage/single_%s.jpg'\" \
	    -draw \"image over 1230,952 1110,832 'storage/single_%s.jpg'\" \
	    -quality 100 storage/collage_%s.jpg" % (picname[1],picname[2],picname[3],picname[4],imgname)
            print (command)
            subprocess.call(command, shell=True)
            #subprocess.call(command, shell=False)
            #done = True
            command = "lp -d Canon_CP910 /home/pi/code/toastboxy/Python/storage/collage_%s.jpg" % (imgname)
            subprocess.call(command, shell=True)
            #time.sleep(1)
            initialize()
    #GPIO.add_event_detect(23,GPIO.FALLING,stuff,bouncetime=1000)
        
def undo(event):
    print("UNDO")
    if main.number != 0:
        c1.itemconfigure(tkimage[main.number], image = picturey, anchor=NW)
        main.number -=1
        camera.resolution = (1296,972)
        camera.start_preview(fullscreen=False, window=(54,54,1296,972))    
	
main = Tk()
main.state = True
main.number = 0
main.attributes("-fullscreen", main.state)
c1 = Canvas(main, width=1920, height=1080, bg='lightblue')
c1.pack()
#text1 = c1.create_text(1400,250, anchor=NW, font=('arial',250,'bold'),text="5")
text1 = c1.create_text(1520,250, anchor=NW, font=(bigfont),text="5")
#c2 = Canvas(main, width=760, height=571, bg='blue')
#c2.pack()
#c1.itemconfig(text1,fill='red')

picturey = PhotoImage(file='camy.gif')
tkimage[1] = c1.create_image(0,0,image=picturey, anchor=NW)
tkimage[2] = c1.create_image(760,0,image=picturey, anchor=NW)
tkimage[3] = c1.create_image(0,571,image=picturey, anchor=NW)
tkimage[4] = c1.create_image(760,571,image=picturey, anchor=NW)
initialize()

#GPIO.add_event_detect(23,GPIO.FALLING,stuff,3000)
#GPIO.add_event_detect(24,GPIO.FALLING,undo,3000)
#try:
#    GPIO.wait_for_edge(23, GPIO.FALLING)
#    print ("FALLING detected\n")
#    time.sleep(0.5)
#except KeyboardInterrupt:
#    GPIO.cleanup()

main.bind("<Button-1>", stuff)
main.bind("<Button-3>", undo)
main.bind("<Escape>", esc)
#main.bind(GPIO.wait_for_edge(23, GPIO.FALLING),stuff)

main.mainloop()
#GPIO.cleanup()
