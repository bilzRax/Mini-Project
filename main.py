import cv2,ctypes
from tkinter import *
import threading as tr
from PIL import ImageTk, Image
import winsound
import tkinter.messagebox as tkMessageBox
from tensorflow.keras.models import load_model

def predict():
        def pred():
                count = 0
                cap = cv2.VideoCapture(0)
                model =  load_model('./model/model.h5')
                classes = ['No Accident', 'Accident']
                while 1:
                        ret, img = cap.read()
                        imgc=img.copy()
                        img = cv2.resize(img,(224,224))
                        img = img.reshape(-1,224,1)/255.0
                        pred = model.predict(img)
                        txt = classes[pred[1].argmax()]
                        if 'No' not in txt:
                                if count>=5:
                                        winsound.Beep(2500,1000)
                                        count=0
                                cv2.putText(imgc,txt, (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (50,100,255),2)
                                count+=1
                        else:
                                cv2.putText(imgc,txt, (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (100,255,100),2)
                        cv2.imshow('Car Accident Detection',imgc)
                        k = cv2.waitKey(30) & 0xff
                        if k == 27:
                                break
                        
                cap.release()
                cv2.destroyAllWindows()
        tr.Thread(target=pred).start()
def Exit():
    global home
    result = tkMessageBox.askquestion(
        "Car Accident Detection", 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        home.destroy()
        exit()
    else:
        tkMessageBox.showinfo(
            'Return', 'You will now return to the main screen')


home = Tk()
home.title("Car Accident Detection")

img = Image.open("images/home.png")
img = ImageTk.PhotoImage(img)
panel = Label(home, image=img)
panel.pack(side="top", fill="both", expand="yes")
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
lt = [w, h]
a = str(lt[0]//2-450)
b= str(lt[1]//2-320)
home.geometry("900x653+"+a+"+"+b)
home.resizable(0,0)

photo = Image.open("images/1.png")
img2 = ImageTk.PhotoImage(photo)
b1=Button(home, highlightthickness = 0, bd = 0,activebackground="#FFCCC2", image = img2,command=predict)
b1.place(x=0,y=209)

photo = Image.open("images/2.png")
img3 = ImageTk.PhotoImage(photo)
b2=Button(home, highlightthickness = 0, bd = 0,activebackground="#FFCCC2", image = img3,command=Exit)
b2.place(x=0,y=282)

home.mainloop()
