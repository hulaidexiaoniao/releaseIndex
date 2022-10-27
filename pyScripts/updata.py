
import os,requests
from turtle import update
from tkinter import W
from distutils import filelist
import shutil


def data_compare(keyValueDic1:dict,keyValueDic2:dict)->list:
    """对比由两个文件夹生成的字典,返回存在差异的数据

    Args:
        keyValueList1 (Dic): 当前本地的包生成的字典
        keyValueList2 (Dic): 用于替换的包生成的字典

    Returns:
        _type_: 返回的有差异的文件列表，存储文件相对路径
    """
    diff = keyValueDic1.keys() &  keyValueDic2
    diff_vals = [(k, keyValueDic1[k], keyValueDic2[k]) for k in diff if keyValueDic1[k] != keyValueDic2[k]]
    #需要替换的文件
    needReplaceList = []
    for differFile in diff_vals:
        ss = differFile[0]
        needReplaceList.append(ss)
    #print(needReplaceList)
    return needReplaceList


def get_add_file(keyValueDic1:dict,keyValueDic2:dict)->list: 
    #本地需增加的文件
    needAddFile = keyValueDic1.keys()-keyValueDic2.keys()
    #print(needAddFile)
    return needAddFile

def txt_parse(txtPath:str)->dict:
    """解析txt为一个字典

    Args:
        txt (_type_): txt文件路径

    Returns:
        _type_: 以文件相对路径为键，文件属性为值的字典
    """
    keyValueDic = {}
    fileHandler  =  open  (txtPath,encoding='utf-8')
    while True:
        line = fileHandler.readline()
        if not line:
            break
        line = line.strip("\n")
        str = line.split("---")
        #print(str)
        keyValueDic[str[0]] = str[1]
    return keyValueDic

def down_load_file(needRepalceFile:list,needAddFile:list)->None:
    """"下载需要增加与替换的文件

    Args:
        needRepalceFile (_type_): 需要替换的文件目录
        needAddFile (_type_): 需要下载的文件目录
    """
    baseUrlAddress = "https://edahotfix.oss-cn-hangzhou.aliyuncs.com/EPEDAPro/"
    for replaceFile in needRepalceFile:
        destPath = tempPath + "\\" + replaceFile
        replaceFileUrl = replaceFile.replace("\\","/")
        Url = baseUrlAddress + replaceFileUrl
        try:
            downLoad = requests.get(Url)
            os.makedirs(os.path.dirname(destPath), exist_ok=True)
            with open(destPath, "wb") as code:
                code.write(downLoad.content)
                code.close()
        except:
            print("downLoad Error")
            updatelog = open(tempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write(Url + " download error \n") 
            updatelog.close()    
    for addFile in needAddFile:
        destPath1 = tempPath + "\\" + addFile
        addFileUrl = addFile.replace("\\","/")
        Url1 = baseUrlAddress + addFileUrl 
        try:  
            downLoad1 = requests.get(Url1)
            os.makedirs(os.path.dirname(destPath1), exist_ok=True)
            with open(destPath1, "wb") as code1:
                code1.write(downLoad1.content)
                code1.close()  
        except:
            updatelog = open(tempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write(Url1 + " download error \n") 
            updatelog.close()           


def remove_file_to_destpath(needReplaceFile:list,needAddFile:list)->None:
    """移动文件到指定位置，先删除，再移动
    Args:
        needReplaceFile (_type_): 需要替换的文件，即需要先删除的文件
        needAddFile (_type_): 需要增加的文件
    """
    currPath = os.getcwd()
    currPath = currPath.strip("EPEDAPro")
    #currPath = currPath + "\\EPEDAPro"
    for replaceFile in needReplaceFile:
        soucreReplaceFilePath = tempPath + "\\" + replaceFile
        replacePath = currPath + "\\" + replaceFile
        try:
            os.remove(replacePath)
            shutil.move(soucreReplaceFilePath,replacePath)
        except:
            print(replacePath + " is using")
            updatelog = open(tempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write(replacePath + " updata error\n") 
            updatelog.close()        
    for addFile in needAddFile:
        addPath = currPath + "\\" + addFile  
        sourceAddFilePath = tempPath + "\\" + addFile
        shutil.move(sourceAddFilePath,addPath)
     

if __name__ == '__main__':
    currentPath = os.getcwd()
    tempPath = currentPath + "\\Temp"
    if os.path.exists(tempPath):
        shutil.rmtree(tempPath)
    os.makedirs(tempPath) 
    file = open(tempPath + "\\updata.log",W)
    file = open(tempPath + "\\edaCheckList.txt",W)
    url = "https://edahotfix.oss-cn-hangzhou.aliyuncs.com/edaCheckList.txt"
    down_res = requests.get(url)
    with open(tempPath + "\\edaCheckList.txt",'wb') as file:
        file.write(down_res.content)
    Dic1 = txt_parse(tempPath + "\\edaCheckList.txt") 
    #Dic1 = txt_parse(r"C:\Users\wulongan\Desktop\python--\edaCheckList.txt") 
    #解析本地文件生成的txt
    Dic2 = txt_parse(r"C:\Users\wulongan\Desktop\python--\tree3.txt")  
    ss1 = data_compare(Dic1,Dic2) 
    ss2 = get_add_file(Dic1,Dic2)
    down_load_file(ss1,ss2)
    remove_file_to_destpath(ss1,ss2)



