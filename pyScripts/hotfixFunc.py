
from asyncio.windows_events import NULL
from logging import exception
import os,requests
from xmlrpc.client import Boolean
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
updateTempPath = currentPath + "\\updateTemp"


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
    currentPath = os.getcwd()
    updateTempPath = currentPath + "\\updateTemp"
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
            fileAttribute = "---" + fileMd5 + str(fileSize)
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
    except exception as e:
        updatelog = open(updateTempPath + "\\updata.log",'w', encoding='UTF-8') 
        updatelog.write(str(e))
        updatelog.close() 
    ss = localTxtName
    return ss


def show_path(path_tree,localTxtName)->str:
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


def getLocalFileInfo(base_path = os.getcwd(),loaclTxtName = currentPath + "\\updateTemp" + '\\localtree.txt')->bool:
    """输入本地EPEDAPro项目地址，会在updateTemp文件夹中产生一个localtree.txt文件，返回的txt文件地址

    Args:
        base_path (str): 本地EPEDAPro项目地址

    Returns:
        str: 生成的txt文件路径
    """
    if os.path.exists(base_path):
       base_path = base_path
    else:
        return False 
    base_path_tree = PathTree(base_path, 3)
    get_path(base_path, base_path_tree, True)

    txtPath = show_path(base_path_tree,loaclTxtName)
    if os.path.exists(txtPath):
        return True
    else:
        return False


def data_compare(keyValueDic1:dict,keyValueDic2:dict)->list:
    """对比由两个文件夹生成的字典,返回存在差异的数据

    Args:
        keyValueList1 (Dic): 当前本地的包生成的字典
        keyValueList2 (Dic): 用于替换的包生成的字典

    Returns:
        _type_: 返回的有差异的文件列表，存储文件相对路径
    """
    try:
        diff = keyValueDic1.keys() &  keyValueDic2
        diff_vals = [(k, keyValueDic1[k], keyValueDic2[k]) for k in diff if keyValueDic1[k] != keyValueDic2[k]] 
        #print(diff_vals)
        needReplaceList = []
        for differFile in diff_vals:
            ss = differFile[0]
            needReplaceList.append(ss)
        return needReplaceList
    except Exception as e:
        updatelog = open(updateTempPath + "\\updata.log",'w', encoding='UTF-8') 
        updatelog.write(str(e))
        updatelog.close() 



def get_add_file(keyValueDic1:dict,keyValueDic2:dict)->list: 
    #本地需增加的文件
    try:
        needAddFile = keyValueDic1.keys()-keyValueDic2.keys()
        #print(needAddFile)
        return needAddFile
    except Exception as e:
        updatelog = open(updateTempPath + "\\updata.log",'w', encoding='UTF-8') 
        updatelog.write(str(e))
        updatelog.close() 


def txt_parse(txtPath:str)->dict:
    """解析txt为一个字典

    Args:
        txt (_type_): txt文件路径

    Returns:
        _type_: 以文件相对路径为键，文件属性为值的字典
    """
    keyValueDic = {}
    if os.path.exists(txtPath) == False or txtPath == NULL:
        return keyValueDic
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
    except Exception as e:
        updatelog = open(updateTempPath + "\\updata.log",'w', encoding='UTF-8') 
        updatelog.write(str(e))
        updatelog.close()    
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
        except Exception as e:
            updatelog = open(updateTempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close()
            continue
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
        except Exception as e:
            updatelog = open(updateTempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close()
            continue 
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
        except Exception as e:
            updatelog = open(updateTempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close()  
            moveFailedFileNum += 1 
            continue     
    for addFile in needAddFile:
        addPath = currPath + "\\" + addFile  
        sourceAddFilePath = tempPath + "\\" + addFile
        try:
            shutil.move(sourceAddFilePath,addPath)
        except Exception as e:
            updatelog = open(updateTempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close()  
            moveFailedFileNum += 1  
            continue
    if(moveFailedFileNum == 0):
        return True
    else:
        return False            
     

def delete_temp_folder()->bool:
    """删除本地Temp文件夹，删除成功返回true，失败返回false

    Returns:
        bool: 删除成功或失败
    """
    currentPath = os.getcwd()
    tempPath = currentPath + "\\Temp"
    try:
        if os.path.exists(tempPath):
            shutil.rmtree(tempPath)
        return True    
    except Exception as e:
            updatelog = open(updateTempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close() 
            return False

def create_temp_folder()->bool:
    """本地路径下创建Temp文件夹，返回创建结果

    Returns:
        bool: 创建成功或失败
    """
    currentPath = os.getcwd()
    tempPath = currentPath + "\\Temp"
    try:
        os.makedirs(tempPath)
        return True
    except Exception as e:
            updatelog = open(updateTempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close()
            return False     

def down_load_oss_checkList(checkListTXtName = "\\edaCheckList.txt")->bool:
    """下载用于对比的checklist文件，返回下载

    Returns:
        bool: 返回下载成功或失败结果
    """
    url = "https://edahotfix.oss-cn-hangzhou.aliyuncs.com/edaCheckList.txt"
    currentPath = os.getcwd()
    updateTempPath = currentPath + "\\updateTemp"
    try:
        down_res = requests.get(url)
        with open(updateTempPath + checkListTXtName,'wb') as file:
            file.write(down_res.content)
        return True    
    except Exception as e:
            updatelog = open(updateTempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close()
            return False   

def delete_updateTemp_folder()->bool:
    """删除updateTemp文件夹，返回创建结果

    Returns:
        bool: _description_
    """
    currentPath = os.getcwd()
    updateTempPath = currentPath + "\\updateTemp"
    try:
        if os.path.exists(updateTempPath):
            shutil.rmtree(updateTempPath)
        return True    
    except Exception as e:
            updatelog = open(updateTempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close() 
            return False


def create_updateTemp_folder()->bool:
    """创建updateTemp文件夹，返回创建结果

    Returns:
        bool: _description_
    """
    currentPath = os.getcwd()
    updateTempPath = currentPath + "\\updateTemp"
    try:
        os.makedirs(updateTempPath)
        return True
    except Exception as e:
            updatelog = open(updateTempPath + "\\updata.log",'w', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close()
            return False   



if __name__ == '__main__':
    #删除本地updateTemp文件夹
    delUpdateTemp = delete_updateTemp_folder() 
    #创建updateTemp文件夹
    createUpdateTemp = create_updateTemp_folder()
    #删除Temp文件夹
    delTemp =  delete_temp_folder()
    #创建Temp文件夹
    createTemp = create_temp_folder()
    #下载checkList
    loadCheckList = down_load_oss_checkList()
    #把本地路径写成txt
    generatelocaltxt = getLocalFileInfo()
    #解析两份txt文件为dic
    standardCheckList = txt_parse(r"C:\Users\wulongan\Desktop\python--\EPEDAPro_1028\EPEDAPro\updateTemp\edaCheckList.txt")
    localCheckList = txt_parse(r"C:\Users\wulongan\Desktop\python--\EPEDAPro_1028\EPEDAPro\updateTemp\localtree.txt")
    #获取需要替换的文件列表
    needReplaceFileList = data_compare(standardCheckList,localCheckList)
    #获取需要增加的文件列表
    needAddFileList = get_add_file(standardCheckList,localCheckList)
    #下载所有需要的文件
    # dowmLoadFileResult = down_load_file(needAddFileList,needAddFileList)
    # #移动下载的文件到相应位置
    # removeFileResult = remove_file_to_destpath(needAddFileList,needAddFileList)




