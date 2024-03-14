
import tkinter
from tkinter.constants import BOTTOM, E, FLAT, HORIZONTAL, N, RIGHT, S, W, Y
import cv2 as cv
import numpy
import tkinter as tk
from tkinter import Scrollbar, filedialog, image_names
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import random
from math import *
from tkinter.simpledialog import askstring, askinteger, askfloat

global image_has_read
global gauss_has_done

gauss_has_done = False
image_has_read = False
window = tk.Tk()
window.title("AIP 61047040S")

screen_width = int(window.winfo_screenwidth()*0.8)
screen_height = int(window.winfo_screenheight()*0.8)
window.geometry(f"{screen_width}x{screen_height}")


Frame1 = tk.Frame(window,width = screen_width,height = screen_height*(1/7),padx=5,pady=5,relief=FLAT,highlightthickness = 5)
Frame2 = tk.Frame(width = screen_width*(1/2),height = screen_height*(6/7),padx=5,pady=5,relief=FLAT,highlightthickness = 5)
Frame3 = tk.Frame(width = screen_width*(1/2),height = screen_height*(6/7),padx=5,pady=5,relief=FLAT,highlightthickness = 5)
Frame1.pack_propagate(0)
Frame2.pack_propagate(0)
Frame3.pack_propagate(0)

Frame2.grid_columnconfigure(0, minsize= screen_width*(1/2), weight=1)
Frame2.grid_rowconfigure(0, minsize= screen_height*(6/7), weight=1)

Frame3.grid_columnconfigure(0, minsize= screen_width*(1/2), weight=1)
Frame2.grid_rowconfigure(0, minsize= screen_height*(6/7), weight=1)



Frame1.grid(row = 0,column=0,columnspan=2)
Frame2.grid(row = 1,column=0)
Frame3.grid(row = 1,column=1)




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
        lbl_2 = tk.Label(Frame2, image=imgTk)
        lbl_2.image = imgTk
        lbl_2.grid(column=0, row=0,sticky = S+N+E+W) 

    
        image_has_read = True


def bt_2_event():
    file_path = ""
    if image_has_read and gauss_has_done:
        file_path = filedialog.askdirectory()
        for i in range(len(file_path_read)-1,-1,-1):
            if file_path_read[i] == ".":
                file_path_read_dot = i
            elif file_path_read[i] == "/":
                file_path_read_name = file_path_read[i:file_path_read_dot]
                break

    if file_path != "":

        cv.imencode(file_path_read[file_path_read_dot:],img)[1].tofile(file_path+file_path_read_name+"_output.bmp")


    
def bt_3_event():  #  繪製高斯雜訊直方圖
    if image_has_read and gauss_has_done:
        plt.hist(GAUSS , bins= 256)
        plt.xlabel('Iensity')
        plt.ylabel('Frequency')
        plt.title("GAUSSIAN WHITE NOISE Histogram")   
        plt.savefig("Gauss.jpg")
        plt.close()
        img3 = Image.open("Gauss.jpg")
        img3 = img3.resize( (500,500) )
        imgTk2 =  ImageTk.PhotoImage(img3)
        lbl_3 = tk.Label(Frame3, image=imgTk2)
        lbl_3.image = imgTk2
        lbl_3.grid(column=0, row=0,sticky=W+E+N+S)
        

def bt_4_event():  #加入高斯雜訊
    global gauss_has_done
    gauss_has_done = False
    sigma = ""
    if image_has_read:
        sigma = askfloat("標準差","請輸入標準差值")
        if sigma != None:
            global GAUSS
            GAUSS = []   
            for i in range(500):
                for j in range(0,499,2):
                    r = random.random()
                    phy = random.random()
                    z1 = sigma*cos(2*pi*phy)*((-2)*log(r))**(1/2)
                    z2 = sigma*sin(2*pi*phy)*((-2)*log(r))**(1/2) 

                    (gray1,gray11,gray111) = img[i,j]
                    if gray1+z1>255:
                        gaussian_1 = 255
                    elif gray1+z1<0:
                        gaussian_1 = 0
                    else:
                        gaussian_1 = gray1 + z1
                    
                    img[i,j] = [gaussian_1,gaussian_1,gaussian_1]
                    GAUSS.append(z1)

                    (gray2,gray22,gray222)= img[i,j+1]
                    
                    if gray2+z2>255:
                        gaussian_2 = 255
                    elif gray2+z2<0:
                        gaussian_2 = 0
                    else:
                        gaussian_2 = gray2 + z2
                    img[i,j+1] = [gaussian_2,gaussian_2,gaussian_2]
                    GAUSS.append(z2)  #加入高斯雜訊

            global file_path_read_gray_gaussian
            file_path_read_gray_gaussian = file_path_read[:file_path_read_dot]+"_gray_gaussian"+file_path_read[file_path_read_dot:]
            cv.imencode(file_path_read[file_path_read_dot:],img)[1].tofile(file_path_read_gray_gaussian)
            img3 = Image.open(file_path_read_gray_gaussian)
            img3 = img3.resize( (500,500) )
            imgTk =  ImageTk.PhotoImage(img3)
            lbl_3 = tk.Label(Frame2, image=imgTk)
            lbl_3.image = imgTk
            lbl_3.grid(column=0, row=0,sticky = S+N+E+W)
            gauss_has_done = True
# def bt_3_event():  #讀取影像  繪製直方圖
#     if image_has_read:
#         A = []
#         for i in range(500):
#             for j in range(500):
#                 A.append(img.item(i,j,0))
                
#         plt.hist(A , bins= 256)
#         plt.xlabel('Iensity')
#         plt.ylabel('Frequency')
#         plt.title("Image Histogram")   
#         plt.savefig("histogram.jpg")
#         plt.close()

#         img3 = Image.open("histogram.jpg")

#         img3 = img3.resize( (500,500) )
#         imgTk2 =  ImageTk.PhotoImage(img3)
#         lbl_3 = tk.Label(Frame3, image=imgTk2)
#         lbl_3.image = imgTk2
#         lbl_3.grid(column=0, row=0,sticky=W+E+N+S)


bt_1 = tk.Button(Frame1, text="輸入檔案", bg='red', fg='white', font=('Arial', 12),command=bt_1_event)
bt_1['width'] = 25
bt_1['height'] = 4
bt_1['activebackground'] = 'red'
bt_1['activeforeground'] = 'yellow'
bt_1.grid(column=0, row=0,padx = 20)

bt_4 = tk.Button(Frame1, text="高斯雜訊", bg='orange', fg='white', font=('Arial', 12),command=bt_4_event)
bt_4['width'] = 25
bt_4['height'] = 4
bt_4['activebackground'] = 'red'
bt_4['activeforeground'] = 'yellow'
bt_4.grid(column=1, row=0,padx = 20)

bt_2 = tk.Button(Frame1, text="輸出檔案", bg='blue', fg='white', font=('Arial', 12),command=bt_2_event)
bt_2['width'] = 25
bt_2['height'] = 4
bt_2['activebackground'] = 'red'
bt_2['activeforeground'] = 'yellow'
bt_2.grid(column=3, row=0,padx = 20)

bt_3 = tk.Button(Frame1, text="直方圖", bg='green', fg='white', font=('Arial', 12),command=bt_3_event)
bt_3['width'] = 25
bt_3['height'] = 4
bt_3['activebackground'] = 'red'
bt_3['activeforeground'] = 'yellow'
bt_3.grid(column=2, row=0,padx = 20)



window.mainloop()
