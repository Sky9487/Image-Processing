import tkinter as tk
from PIL import Image, ImageTk
import numpy
from tkinter import Scrollbar, filedialog, image_names
import cv2 as cv
from tkinter.constants import BOTTOM, E, FLAT, HORIZONTAL, N, RIGHT, S, W, Y

global image_has_read
global img_GRAY

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
# Frame2.grid_rowconfigure(0, minsize= screen_height*(6/7), weight=1)


Frame3.grid_columnconfigure(0, minsize= screen_width*(1/2), weight=1)
# Frame2.grid_rowconfigure(0, minsize= screen_height*(6/7), weight=1)



Frame1.grid(row = 0,column=0,columnspan=2)
Frame2.grid(row = 1,column=0,rowspan=2)
Frame3.grid(row = 1,column=1,rowspan=2)


def bt_1_event():   #輸入影像
    global img,img2
    global img_GRAY
    global image_has_read
    global file_path_read
    global file_path_read_gray
    global file_path_read_gray2
    global file_path_read_dot


    Convolusion_has_done = False
    file_path_read = ""
    file_path_read = filedialog.askopenfilename()   
    if file_path_read != "":
        img = cv.imdecode(numpy.fromfile(file_path_read,dtype = numpy.uint8),1)
        img = cv.resize(img, (512,512), interpolation=cv.INTER_AREA)

        for i in range(len(file_path_read)-1,-1,-1): #檔名處理
            if file_path_read[i] == ".":
                file_path_read_dot = i
                break
            
        file_path_read_gray = file_path_read[:file_path_read_dot]+"_gray"+file_path_read[file_path_read_dot:]
        file_path_read_gray2 = file_path_read[:file_path_read_dot]+"_gray2"+file_path_read[file_path_read_dot:]

        Zero = []
        for i in range(514):
            Zero.append(0)   #for zero pendding
        img_GRAY = [] 
        img_GRAY.append(Zero) #zero pendding
        
        for i in range(512): #匯入影像自動轉灰階
            temp = [0]
            for j in range(512):
                (b,g,r) = img[i,j]
                gray = r*0.299+g*0.587+b*0.114
                img[i,j] = [gray,gray,gray]
                temp.append(int(gray))
            temp.append(0)
            img_GRAY.append(temp)
        img_GRAY.append(Zero)
        


        cv.imencode(file_path_read[file_path_read_dot:],img)[1].tofile(file_path_read_gray) #原圖灰階檔
        # cv.imencode(file_path_read[file_path_read_dot:],img)[1].tofile(file_path_read_gray2)  #小波轉換檔

        
        


        img2 = Image.open(file_path_read_gray)
        img2 = img2.resize( (512,512) )
        imgTk =  ImageTk.PhotoImage(img2)
        lbl_2 = tk.Label(Frame2, image=imgTk)
        lbl_2.image = imgTk
        lbl_2.grid(column=0, row=0,sticky = N) 

    
        image_has_read = True

def bt_2_event():  #卷積設定
    global newWindow
    newWindow = tk.Toplevel(height=100,width=100)
    newWindow.title("Convolution")
    global C
    C = [[0,0,0] for i in range(3)]
    for i in range(3):
        for j in range(3):
            C[i][j] = tk.StringVar()
            entry = tk.Entry(newWindow,textvariable=C[i][j],width=15)
            entry.grid(row=i,column=j)
    
    mybutton = tk.Button(newWindow, text='OK',command=OK_event)
    mybutton.grid(row=3, column=1)




def OK_event():
    global Convolusion_has_done
    global img_Convolution
    Con = [[0,0,0] for i in range(3)]
    flag = 0
    for i in range(3):
        for j in range(3):
            Con[i][j] = C[i][j].get()
            if Con[i][j] == "":
                tk.messagebox.showinfo(title="Error", message="請輸入數字，並完整輸入每一格",parent = newWindow)
                flag = 1
                break
            elif len(Con[i][j]) == 1:
                Con[i][j] = eval(Con[i][j])
            elif (Con[i][j][0] == "0") and (Con[i][j][1]!="."):
                tk.messagebox.showinfo(title="Error", message="請輸入數字，並完整輸入每一格",parent = newWindow)
                flag = 1
                break
            else:
                Con[i][j] = eval(Con[i][j])

            if isinstance(Con[i][j],int) or isinstance(Con[i][j],float):
                pass
            else:
                tk.messagebox.showinfo(title="Error", message="請輸入數字，並完整輸入每一格",parent = newWindow)
                flag = 1
                break
        if flag:
            break   
    else:
        newWindow.destroy()
        Con.reverse()
        for i in range(3):
            Con[i].reverse()
        
        Convolusion =[]
        for i in range(1,513):
            temp2 = []
            for j in range(1,513):
                total = 0
                for k in range(3):
                    for l in range(3):
                        total = total + Con[k][l]*img_GRAY[i+k-1][j+l-1]
                    
                if total < 0:
                    total = 0
                elif total >255:
                    total = 255

                temp2.append(total)
            Convolusion.append(temp2)
        

        Convolusion = numpy.array(Convolusion)
        # img_Convolution = Image.fromarray(Convolusion)
        cv.imwrite('output.jpg', Convolusion)

        img_Convolution = Image.open("output.jpg")
        img_Convolution = img_Convolution.resize( (512,512) )
        imgTk3 =  ImageTk.PhotoImage(img_Convolution)
        lbl_8 = tk.Label(Frame3, image=imgTk3)
        lbl_8.image = imgTk3
        lbl_8.grid(column=0, row=0,sticky = N) 
        img_Convolution = numpy.array(img_Convolution)

        Convolusion_has_done = True
        

                    




def bt_3_event():  #輸出影像
    file_path = ""
    if image_has_read and Convolusion_has_done:
        file_path = filedialog.askdirectory()
        for i in range(len(file_path_read)-1,-1,-1):
            if file_path_read[i] == ".":
                file_path_read_dot = i
            elif file_path_read[i] == "/":
                file_path_read_name = file_path_read[i:file_path_read_dot]
                break

    if file_path != "":
      
        cv.imencode(file_path_read[file_path_read_dot:],img_Convolution)[1].tofile(file_path+file_path_read_name+"_output.bmp")


bt_1 = tk.Button(Frame1, text="輸入檔案", bg='red', fg='white', font=('Arial', 12),command=bt_1_event)
bt_1['width'] = 25
bt_1['height'] = 4
bt_1['activebackground'] = 'red'
bt_1['activeforeground'] = 'yellow'
bt_1.grid(column=0, row=0,padx = 20)


bt_2 = tk.Button(Frame1, text="Convolution", bg='blue', fg='white', font=('Arial', 12),command=bt_2_event)
bt_2['width'] = 25
bt_2['height'] = 4
bt_2['activebackground'] = 'red'
bt_2['activeforeground'] = 'yellow'
bt_2.grid(column=1, row=0,padx = 20)

bt_3 = tk.Button(Frame1, text="輸出影像", bg='green', fg='white', font=('Arial', 12),command=bt_3_event)
bt_3['width'] = 25
bt_3['height'] = 4
bt_3['activebackground'] = 'red'
bt_3['activeforeground'] = 'yellow'
bt_3.grid(column=2, row=0,padx = 20)



window.mainloop()
