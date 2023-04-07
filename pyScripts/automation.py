import os
import shutil
import tkinter as tk
import modifyFile
import getLocalFileInfo
import threading
from tkinter import filedialog
from tkinter import StringVar,ttk
import tkinter.messagebox
import datetime


fileRelativePath = ""
filePathList = []
filePathList.append("")
win = tk.Tk()
# 设置主窗口
win.geometry('620x220')
win.title("EDAPro Auto Publish")

labe1 = tk.Label(win,text="原 文 件：",font=("微软雅黑"))
labe2 = tk.Label(win,text="SVNRevision:",font=("微软雅黑"))
labe3 = tk.Label(win,text="是否修改:",font=("微软雅黑"))
labe4 = tk.Label(win,text="发布目录：",font=("微软雅黑"))
labe1.place(x=20,y=10)
labe2.place(x=20,y=40)
labe3.place(x=20,y=70)
labe4.place(x=20,y=100)


#选择文件标签按钮
labelc1 = tk.Label(win,text="选择文件",font=("微软雅黑",10, "underline"),fg='blue')
labelc1.place(x=530 ,y=10)

# labelc2 = tk.Label(win,text="选择文件",font=("微软雅黑",10, "underline"),fg='blue')
# labelc2.place(x=530 ,y=40)

labelc3 = tk.Label(win,text="选择文件",font=("微软雅黑",10, "underline"),fg='blue')
labelc3.place(x=530 ,y=100)

labelc4 = tk.Label(win,text="选择文件",font=("微软雅黑",10, "underline"),fg='blue')
# labelc4.place(x=530 ,y=70)
# labelc4.place_forget()

e1_Txt = StringVar()
e2_Txt = StringVar()
e3_Txt = StringVar()
e4_Txt = StringVar()
# 创建输入框控件
entry1 = tk.Entry(win,textvariable=e1_Txt,width=60)
# entry1.insert(0,r'r"C:\Users\wulongan\Desktop\EpEDAPro\trunk\EPEDAPro\bin\x64"')
entry1.place(x= 95,y=13)


# 创建输入框控件
entry2 = tk.Entry(win,textvariable=e2_Txt,width=50)
# entry2.insert(0,r'C:\Users\wulongan\Desktop')
entry2.place(x= 125,y=43)

#下拉框属性
values = ["True", "False"]
var = tk.StringVar()
entry3=ttk.Combobox(win, values=values, textvariable = var,width=57)
entry3.place(x= 95,y=73)
entry3_Txt = tk.Entry(win,textvariable=e4_Txt,width=55)
entry3_Txt.place(x= 120,y=73)
entry3_Txt.place_forget()
# entry3 = tk.Entry(win,width=60)
# entry3.insert(0,'True')
# entry3.place(x= 95,y=73)
# 创建输入框控件
entry4 = tk.Entry(win,textvariable=e3_Txt,width=60)
# entry4.insert(0,r'r"C:\Users\wulongan\Downloads\releaseIndex-main\EPEDAProSDK.txt"')
entry4.place(x= 95,y=103)

#获取路径()
def get_path1(self):
    # 返回一个字符串，可以获取到任意文件的路径。
    path1 = filedialog.askdirectory(title='请选择文件')
    e1_Txt.set(path1)
    
def get_path2(self):
    path2 = filedialog.askdirectory(title='请选择文件')
    e2_Txt.set(path2)

def get_path3(self):
    path3 = filedialog.askopenfilenames(title='请选择文件')
    e3_Txt.set(path3)

def get_path4(self):
    path4 = filedialog.askdirectory(title='请选择文件')
    e4_Txt.set(path4)

finalDir = ""
version = ""

def notmain():
    labe1_Txt = labe1.cget('text') 
    if labe1_Txt =="CMA_SDK ：":
        labe1.config(text="原 文 件：",font=("微软雅黑"))
        labe2.config(text="目标文件：",font=("微软雅黑"))
        labe3.config(text="是否修改:",font=("微软雅黑"))
        labe4.config(text="新 文 件：",font=("微软雅黑"))
        labe1.place(x=20,y=10)
        labe2.place(x=20,y=40)
        labe3.place(x=20,y=70)
        labe4.place(x=20,y=100)
        entry1.place(x= 95,y=13)
        entry1.config(width=60)
        entry2.place(x= 95,y=43)
        entry2.config(width=60)
        labelc4.place_forget()
        entry3.place(x= 95,y=73)
        entry3.config(width=57)
        entry3_Txt.place_forget()
        entry4.place(x= 95,y=103)
        entry4.config(width=60)
        b1.config(text='导出')
        # b2.config(text='复制模式')
    if labe1_Txt == "原 文 件：":
        baseAddress = ''
        baseNum = 0
        addressList = []
        absolutePathList = []
        #从basePath拿取所需的文件
        basePath = entry1.get()
        if len(basePath)==0:
            tkinter.messagebox.showerror(title='出错啦',message='原文件地址为空')
            return
        
        #新的文件放置地址
        svnrevision = entry2.get()
        date = datetime.datetime.now().strftime('%y%m%d')
        date = date[1:]
        if len(svnrevision) < 5:
            svnrevision = "0" + svnrevision
        newdirname = date + svnrevision
        newdirname = int(newdirname)
        newdirname = hex(newdirname)
        newdirname = newdirname.lstrip("0x")
        version = newdirname.upper()
        newFilePath = os.path.join(os.path.expanduser('~'),"Desktop") + "\\P" + version
        finalDir = newFilePath
        if len(newFilePath)==0:
            tkinter.messagebox.showerror(title='出错啦',message='新文件地址为空')
        #isSDKdir 读取的是proSDK目录时为true，读取的是完整pro目录时为false
        else:

            isSDKdir = entry3.get() 
            #目录地址
            directoryAddress = entry4.get()
            #读取目录
            if len(directoryAddress) == 0:
                tkinter.messagebox.showerror(title='出错啦',message='releaseIndex地址为空')
            else:
                try:
                    win.title("Executing")
                    fileHandler  =  open  (directoryAddress,encoding='utf-8')

                    while  True:
                        # Get next line from file
                        line  =  fileHandler.readline()
                        # If line is empty then end of file reached
                        if  not  line  :
                            break
                        #去掉右边的空格    
                        s = line.rstrip()    
                        s1 = "|--"
                        line = line.strip()
                        line = line.strip(s1)
                        #当前行前面有多少空格
                        b =s.find(s1)
                        if b > baseNum:
                            line = baseAddress + "\\" + line
                        elif b == baseNum:
                            baseAddress = baseAddress.rsplit("\\",1)[0]
                            line = baseAddress + "\\" + line
                        else:
                            a = (baseNum-b)/3 + 1
                            while(a>0):
                                baseAddress = baseAddress.rsplit("\\",1)[0]
                                a = a-1
                            line = baseAddress + "\\" + line    
                        c = line.lstrip('\\')    
                        addressList.append(c)
                        baseAddress = line
                        baseNum = b                 
                        # Close Close    
                    fileHandler.close()
                    #print(addressList)
                    for relativePath in addressList:
                        absolutePath = basePath + "\\" + relativePath 
                        #print(absolutePath)
                        absolutePathList.append(absolutePath)
                    os.mkdir(newFilePath)    
                    for absolutePath1 in absolutePathList:
                        if os.path.exists(absolutePath1):
                            if os.path.isdir(absolutePath1):
                                #目录
                                curPath = absolutePath1.replace(basePath,'',1)
                                curPath = newFilePath + curPath
                                os.mkdir(curPath)
                            if os.path.isfile(absolutePath1):
                                #文件
                                curPath = absolutePath1.replace(basePath,'',1)
                                curPath = newFilePath + curPath
                                shutil.copyfile(absolutePath1,curPath)
                        else:
                            print(absolutePath1)  
                    if entry3.get() == "False":
                        modifyFile.CamGuide(newFilePath)
                        modifyFile.Server(newFilePath)   
                        debugpath = newFilePath + "\\EPEDAPro\\debug.log" 
                        if not os.path.exists(debugpath):
                            debugpath = newFilePath + "\\release\\debug.log"
                        open(debugpath,"w").close()
                        if os.path.exists(newFilePath + '\\release'):
                            os.rename(newFilePath + '\\release',newFilePath + '\\EPEDAPro')
                        win.title("EDAPro Auto Publish")
                        b2.config(state="normal")
                    else:
                        if os.path.exists(newFilePath + '\\release'):
                            os.rename(newFilePath + '\\release',newFilePath + '\\EPEDAPro')
                        win.title("EDAPro Auto Publish")
                except Exception as e:
                    tkinter.messagebox.showerror(title='错误',message=e)
                    print(e)

def copy_dir(src_path, target_path):
    if os.path.isdir(src_path) and os.path.isdir(target_path):		
        filelist_src = os.listdir(src_path)							
        for file in filelist_src:
            path = os.path.join(os.path.abspath(src_path), file)	
            find1 = "ep_python-3.7.3"
            find2 = "GeneratedFiles"
            if find1 in path or find2 in path :
                continue
            if os.path.isdir(path):
                path1 = os.path.join(os.path.abspath(target_path), file)	
                if not os.path.exists(path1):						
                    os.mkdir(path1)
                copy_dir(path,path1)			
            else:								
                with open(path, 'rb') as read_stream:
                    contents = read_stream.read()
                    path1 = os.path.join(target_path, file)
                    with open(path1, 'wb') as write_stream:
                        write_stream.write(contents)
        # return 	True					
    else:
        # return False
        print("lslslslslsl")

def check():
    svnrevision = entry2.get()
    date = datetime.datetime.now().strftime('%y%m%d')
    date = date[1:]
    if len(svnrevision) < 5:
        svnrevision = "0" + svnrevision
    newdirname = date + svnrevision
    newdirname = int(newdirname)
    newdirname = hex(newdirname)
    newdirname = newdirname.lstrip("0x")
    version = newdirname.upper()
    newFilePath = os.path.join(os.path.expanduser('~'),"Desktop") + "\\P" + version
    finalDir = newFilePath
    getLocalFileInfo.checkList_produce(finalDir)

def mongochangefile():
    svnrevision = entry2.get()
    date = datetime.datetime.now().strftime('%y%m%d')
    date = date[1:]
    if len(svnrevision) < 5:
        svnrevision = "0" + svnrevision
    newdirname = date + svnrevision
    newdirname = int(newdirname)
    newdirname = hex(newdirname)
    newdirname = newdirname.lstrip("0x")
    version = newdirname.upper()
    newFilePath = os.path.join(os.path.expanduser('~'),"Desktop") + "\\P" + version
    finalDir = newFilePath
    modifyFile.EDAConfig(finalDir,version)


b1 = tk.Button(win, text="发布", command=lambda: threading.Thread(target=notmain).start())
b1.place(x=170,y=150)
b1.config(width=8,font=("微软雅黑"))
b2 = tk.Button(win, text="CheckList", command=lambda: threading.Thread(target=check).start())
b2.place(x=360,y=150)
b2.config(width=8,font=("微软雅黑"))
srcpath = r"C:\Users\wulongan\Desktop\EpEDAPro\trunk\EPEDAPro\EPEDAPro"
dstpath = r"C:\Users\wulongan\Desktop\EpEDAPro\trunk\EPEDAPro\bin\x64\Release"
b3 = tk.Button(win, text="文件汇总", command=lambda: threading.Thread(target=copy_dir(srcpath,dstpath)).start())
b3.place(x=10,y=150)
b3.config(width=8,font=("微软雅黑"))
b4 = tk.Button(win, text="mongo版本", command=lambda: threading.Thread(target=mongochangefile).start())
b4.place(x=500,y=150)
b4.config(width=8,font=("微软雅黑"))

labelc1.bind('<Button-1>',get_path1)
# labelc2.bind('<Button-1>',get_path2)
labelc3.bind('<Button-1>',get_path3)
labelc4.bind('<Button-1>',get_path4)

win.mainloop()