
import tkinter
from tkinter.constants import BOTTOM, HORIZONTAL, RIGHT, Y
import cv2 as cv
import numpy
import tkinter as tk
from tkinter import Scrollbar, filedialog, image_names
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

global image_has_read


image_has_read = False
window = tk.Tk()
window.title("AIP 61047040S")
window.geometry('1200x1200')



#lbl_1 = tk.Label(window, text='檔案', bg='yellow', fg='#263238', font=('Arial', 12))
#lbl_1.grid(column=1, row=0)
def bt_1_event():
    global img
    global image_has_read
    global file_path_read
    global file_path_read_gray
    global file_path_read_dot


    file_path_read = ""
    file_path_read = filedialog.askopenfilename()   
    if file_path_read != "":
        img = cv.imdecode(numpy.fromfile(file_path_read,dtype = numpy.uint8),1)
        img = cv.resize(img, (500, 500), interpolation=cv.INTER_AREA)

        for i in range(len(file_path_read)-1,-1,-1): #檔名處理
            if file_path_read[i] == ".":
                file_path_read_dot = i
                break
            
        file_path_read_gray = file_path_read[:file_path_read_dot]+"_gray"+file_path_read[file_path_read_dot:]


        for i in range(500):  #匯入影像自動轉灰階
            for j in range(500):
                (b,g,r) = img[i,j]
                gray = r*0.299+g*0.587+b*0.114
                img[i,j] = [gray,gray,gray]
        cv.imencode(file_path_read[file_path_read_dot:],img)[1].tofile(file_path_read_gray)

        
        


        img2 = Image.open(file_path_read_gray)
        img2 = img2.resize( (500,500) )
        imgTk =  ImageTk.PhotoImage(img2)
        lbl_2 = tk.Label(window, image=imgTk)
        lbl_2.image = imgTk
        lbl_2.grid(column=0, row=1) 

    
        image_has_read = True


def bt_2_event():
    file_path = ""
    if image_has_read:
        file_path = filedialog.askdirectory()
        for i in range(len(file_path_read)-1,-1,-1):
            if file_path_read[i] == ".":
                file_path_read_dot = i
            elif file_path_read[i] == "/":
                file_path_read_name = file_path_read[i:file_path_read_dot]
                break

    if file_path != "":

        cv.imencode(file_path_read[file_path_read_dot:],img)[1].tofile(file_path+file_path_read_name+".bmp")

def bt_3_event():
    if image_has_read:
        A = []
        for i in range(500):
            for j in range(500):
                A.append(img.item(i,j,0))
                
        plt.hist(A , bins= 256)
        plt.xlabel('Iensity')
        plt.ylabel('Frequency')
        plt.title("Image Histogram")   
        plt.savefig("histogram.jpg")
        plt.close()

        img3 = Image.open("histogram.jpg")

        img3 = img3.resize( (500,500) )
        imgTk2 =  ImageTk.PhotoImage(img3)
        lbl_3 = tk.Label(window, image=imgTk2)
        lbl_3.image = imgTk2
        lbl_3.grid(column=2, row=1)
    



bt_1 = tk.Button(window, text="輸入檔案", bg='green', fg='white', font=('Arial', 12),command=bt_1_event)
bt_1['width'] = 25
bt_1['height'] = 4
bt_1['activebackground'] = 'red'
bt_1['activeforeground'] = 'yellow'
bt_1.grid(column=0, row=0)


bt_2 = tk.Button(window, text="輸出檔案", bg='red', fg='white', font=('Arial', 12),command=bt_2_event)
bt_2['width'] = 25
bt_2['height'] = 4
bt_2['activebackground'] = 'red'
bt_2['activeforeground'] = 'yellow'
bt_2.grid(column=2, row=0)

bt_3 = tk.Button(window, text="直方圖", bg='blue', fg='white', font=('Arial', 12),command=bt_3_event)
bt_3['width'] = 25
bt_3['height'] = 4
bt_3['activebackground'] = 'red'
bt_3['activeforeground'] = 'yellow'
bt_3.grid(column=1, row=0)



window.mainloop()
