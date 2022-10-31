
from logging import exception
import os,requests
from telnetlib import Telnet
from turtle import update
from tkinter import W
from distutils import filelist
import shutil
import os,time,hashlib
from queue import LifoQueue

fileRelativePath = ""
filePathList = []
filePathList.append("")

base_path = os.getcwd()
currentPath = os.getcwd()
tempPath = currentPath + "\\Temp"


class PathTree:

    def __init__(self, name, level,absPath=None):
        self.name = name
        self.level = level
        self.sub_list = []
        self.absPath = absPath

    def add_sub(self, sub_name):
        self.sub_list.append(sub_name)


def get_path(path, path_tree, is_need_file=False, max_level=1):
    # print (is_need_file)
    if path_tree.level == max_level:
        return

    if os.path.isdir(path):

        for current_dir in os.listdir(path):

            full_path = os.path.join(path, current_dir)
            if os.path.isfile(full_path) and is_need_file:
                sub_path_tree = PathTree(current_dir, path_tree.level + 1,full_path)
                path_tree.add_sub(sub_path_tree)
                fileRelativePath = full_path.replace(base_path+"\\","",1)
                filePathList.insert(1,fileRelativePath)
            elif os.path.isdir(full_path):
                sub_path_tree = PathTree(current_dir, path_tree.level + 1,None)
                path_tree.add_sub(sub_path_tree)
                get_path(full_path, sub_path_tree, is_need_file)
                fileRelativePath = full_path.replace(base_path+"\\","",1)
                filePathList.insert(1,fileRelativePath)


def get_level_path_dict(level_map, path_tree):
    for sub_tree in path_tree.sub_list:
        if not level_map.get(sub_tree.level):
            level_map[sub_tree.name] = [sub_tree.level]
        else:
            level_map[sub_tree.name].append(sub_tree.level)
        if sub_tree.sub_list:
            get_level_path_dict(level_map, sub_tree)


def get_spe_str_by_level(sep_str:str, level:int)->str:
    result = ''
    for i in range(level):
        result += sep_str
    return result


def dsf_show(path_tree,localTxtName)->str:
    keyValueList = []
    q = LifoQueue()
    q.put(path_tree)
    sep_str = '   '
    try:
        f=open(localTxtName,'w',encoding='utf-8')
        a = 0
        while (not q.empty()):
            current_path_tree = q.get()
            # print (get_spe_str_by_level(sep_str, current_path_tree.level) + '|--' + current_path_tree.name)
            fileMd5 = ''
            createTime = ''
            modifyTime = ''
            fileSize = ''
            if current_path_tree.absPath != None:
                with open(current_path_tree.absPath,'rb') as fp:
                    data = fp.read()
                fileMd5 = hashlib.md5(data).hexdigest()
                createTime = time.ctime(os.path.getctime(current_path_tree.absPath))
                fileSize = os.path.getsize(current_path_tree.absPath)
                modifyTime = time.ctime(os.path.getmtime(current_path_tree.absPath))
            #f.write(get_spe_str_by_level(sep_str, current_path_tree.level) + '|--' + current_path_tree.name+ '--|'+fileMd5+'|'+str(fileSize)+'|'+createTime+'|'+modifyTime+'\n')
            f.write(filePathList[a])
            fileAttribute = "---" + fileMd5 + str(fileSize) + createTime + modifyTime
            f.write(fileAttribute + "\n")
            keyValue = {filePathList[a]:fileAttribute}
            keyValueList.append(keyValue)
            a += 1
            children = current_path_tree.sub_list
            if children and len(children) > 0:
                for child in children:
                    q.put(child)
        #print(keyValueList)            
        f.close()
    except:
        return "write Error"    
    ss = os.getcwd() + "\\localtree.txt"
    return ss


def show_path(path_tree,localTxtName = 'localtree.txt')->str:
    level_map = {}
    level_map[path_tree.level] = [path_tree.name]
    get_level_path_dict(level_map, path_tree)
    txtpath = dsf_show(path_tree,localTxtName)
    return txtpath


def check_param(path:str, need_file:int):
    if not os.path.exists(path):
        return 'path:%s not exists' % base_path
    try:
        need_file = int(need_file)
    except Exception as e:
        return 'is_need_file:%s not int e:%s' % (need_file, e)
    if need_file not in [0, 1]:
        return 'is_need_file:%s not in 0, 1' % need_file

    return ''


def getLocalFileInfo(base_path:str,loaclTxtName = 'localtree.txt')->str:
    """输入本地EPEDAPro项目地址，会在相同路径下产生一个localtree.txt文件，返回的txt文件地址

    Args:
        base_path (str): 本地EPEDAPro项目地址

    Returns:
        str: 生成的txt文件路径
    """
    base_path_tree = PathTree(base_path, 3)
    get_path(base_path, base_path_tree, True)

    txtPath = show_path(base_path_tree,loaclTxtName)
    return txtPath


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
    try:
        fileHandler  =  open  (txtPath,encoding='utf-8')
        while True:
            line = fileHandler.readline()
            if not line:
                break
            line = line.strip("\n")
            strList = line.split("---")
            #print(str)
            keyValueDic[strList[0]] = strList[1]
    except exception as e:
        print(e)        
    return keyValueDic


def down_load_file(needRepalceFile:list,needAddFile:list,baseUrlAddress = "https://edahotfix.oss-cn-hangzhou.aliyuncs.com/EPEDAPro/")->bool:
    """"下载需要增加与替换的文件

    Args:
        needRepalceFile (_type_): 需要替换的文件目录
        needAddFile (_type_): 需要下载的文件目录
    """
    downLoadsuccessFileNum = 0
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
            downLoadsuccessFileNum += 1    
        except exception as e:
            updatelog = open(tempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write(Url + " download error \n") 
            updatelog.write(e)
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
            downLoadsuccessFileNum += 1     
        except exception as e:
            updatelog = open(tempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write(Url1 + " download error \n")
            updatelog.write(e) 
            updatelog.close()  
    if(downLoadsuccessFileNum == 0):
        return False
    else:
        return True            



def remove_file_to_destpath(needReplaceFile:list,needAddFile:list)->bool:
    """移动文件到指定位置，先删除，再移动
    Args:
        needReplaceFile (_type_): 需要替换的文件，即需要先删除的文件
        needAddFile (_type_): 需要增加的文件
    """
    moveFailedFileNum = 0
    currPath = os.getcwd()
    currPath = currPath.strip("EPEDAPro")
    #currPath = currPath + "\\EPEDAPro"
    for replaceFile in needReplaceFile:
        soucreReplaceFilePath = tempPath + "\\" + replaceFile
        replacePath = currPath + "\\" + replaceFile
        try:
            os.remove(replacePath)
            shutil.move(soucreReplaceFilePath,replacePath)
        except exception as e:
            updatelog = open(tempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write(replacePath + " updata error\n") 
            updatelog.write(e)
            updatelog.close()  
            moveFailedFileNum += 1      
    for addFile in needAddFile:
        addPath = currPath + "\\" + addFile  
        sourceAddFilePath = tempPath + "\\" + addFile
        try:
            shutil.move(sourceAddFilePath,addPath)
        except exception as e:
            updatelog = open(tempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write(replacePath + " updata error\n") 
            updatelog.write(e)
            updatelog.close()  
            moveFailedFileNum += 1  
    if(moveFailedFileNum == 0):
        return True
    else:
        return False            
     
def delete_temp_folder()->bool:
    currentPath = os.getcwd()
    tempPath = currentPath + "\\Temp"
    try:
        if os.path.exists(tempPath):
            shutil.rmtree(tempPath)
        return True    
    except exception as e:
            updatelog = open(tempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write("remove Temp folder error\n") 
            updatelog.write(e)
            updatelog.close() 
            return False

def create_temp_folder()->bool:
    currentPath = os.getcwd()
    tempPath = currentPath + "\\Temp"
    try:
        os.makedirs(tempPath)
        return True
    except exception as e:
            updatelog = open(tempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write("create Temp folder error\n") 
            updatelog.write(e)
            updatelog.close()
            return False     

def down_load_oss_checkList()->bool:
    url = "https://edahotfix.oss-cn-hangzhou.aliyuncs.com/edaCheckList.txt"
    try:
        down_res = requests.get(url)
        with open(tempPath + "\\edaCheckList.txt",'wb') as file:
            file.write(down_res.content)
        return True    
    except exception as e:
            updatelog = open(tempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write("download checkList error\n") 
            updatelog.write(e)
            updatelog.close()
            return False   



# if __name__ == '__main__':
#     currentPath = os.getcwd()
#     tempPath = currentPath + "\\Temp"
#     if os.path.exists(tempPath):
#         shutil.rmtree(tempPath)
#     os.makedirs(tempPath) 
#     file = open(tempPath + "\\updata.log",W)
#     file = open(tempPath + "\\edaCheckList.txt",W)
#     url = "https://edahotfix.oss-cn-hangzhou.aliyuncs.com/edaCheckList.txt"
#     down_res = requests.get(url)
#     with open(tempPath + "\\edaCheckList.txt",'wb') as file:
#         file.write(down_res.content)
#     Dic1 = txt_parse(tempPath + "\\edaCheckList.txt") 
#     #Dic1 = txt_parse(r"C:\Users\wulongan\Desktop\python--\edaCheckList.txt") 
#     #解析本地文件生成的txt
#     Dic2 = txt_parse(r"C:\Users\wulongan\Desktop\python--\tree3.txt")  
#     ss1 = data_compare(Dic1,Dic2) 
#     ss2 = get_add_file(Dic1,Dic2)
#     down_load_file(ss1,ss2)
#     remove_file_to_destpath(ss1,ss2)



