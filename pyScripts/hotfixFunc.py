from logging import exception
import os,requests, sys
print(sys.path)

import shutil
import os,hashlib
from queue import LifoQueue
from PyQt5.QtCore import QObject , pyqtSignal


fileRelativePath = ""
filePathList = []
filePathList.append("")

base_path = os.getcwd()
currentPath = os.getcwd()
tempPath = currentPath + "\\Temp"
updateTempPath = currentPath + "\\updateTemp"


class ExceptionOccurred(QObject):
    sigLocalTxtGenerateError = pyqtSignal(str)
    sigDateCompareError = pyqtSignal(str)
    sigGetAddFileListError = pyqtSignal(str)
    sigTxtFileParseError = pyqtSignal(str)
    sigDownLoadFileError = pyqtSignal(str)
    sigRemoveFileError = pyqtSignal(str)
    sigDeleteTempError = pyqtSignal(str)
    sigCreateTempError = pyqtSignal(str)
    sigDeleteUpdatetempError = pyqtSignal(str)
    sigCreateUpdatetempError = pyqtSignal(str)
    sigDownLoadCheckListError = pyqtSignal(str)
    sigJudgeFileWritableError = pyqtSignal(str)
    def __init__(self):
        super().__init__()


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
    try:
        f=open(localTxtName,'w',encoding='utf-8')
        a = 0
        while (not q.empty()):
            current_path_tree = q.get()
            # print (get_spe_str_by_level(sep_str, current_path_tree.level) + '|--' + current_path_tree.name)
            fileMd5 = ''
            fileSize = ''
            if current_path_tree.absPath != None:
                with open(current_path_tree.absPath,'rb') as fp:
                    data = fp.read()
                fileMd5 = hashlib.md5(data).hexdigest()
                fileSize = os.path.getsize(current_path_tree.absPath)
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
        updatelog = open(updateTempPath + "\\updata.log",'a', encoding='UTF-8') 
        updatelog.write(str(e))
        updatelog.close() 
        errorOccurred = ExceptionOccurred()
        errorOccurred.sigLocalTxtGenerateError.emit("本地项目生成文本文件失败")
    ss = localTxtName
    return ss


def show_path(path_tree,localTxtName)->str:
    level_map = {}
    level_map[path_tree.level] = [path_tree.name]
    get_level_path_dict(level_map, path_tree)
    localtxt = localTxtName
    txtpath = dsf_show(path_tree,localtxt)
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


def getLocalFileInfo(basePath = os.getcwd(),localTxtName = currentPath + "\\updateTemp" + '\\localtree.txt')->bool:
    """输入本地项目地址，生成一份用于对照的文本

    Args:
        base_path (_type_, str): 本地项目所在的路径
        loaclTxtName (_type_, str): 生成文本放置路径及名称

    Returns:
        bool: 生成成功或失败
    """
    if os.path.exists(basePath):
       basePath = basePath
    else:
        return False 
    base_path_tree = PathTree(basePath, 3)
    get_path(basePath, base_path_tree, True)

    txtPath = show_path(base_path_tree,localTxtName)
    if os.path.exists(txtPath):
        return True
    else:
        return False


def data_compare(keyValueDic1:dict,keyValueDic2:dict)->list:
    """对比由两个文件生成的字典,返回存在差异的数据

    Args:
        keyValueList1 (Dic): 当前本地的包生成的字典
        keyValueList2 (Dic): 用于替换的包生成的字典

    Returns:
        list: 返回的有差异的文件列表，存储文件相对路径
    """
    needReplaceList = []
    try:
        diff = keyValueDic1.keys() &  keyValueDic2
        diff_vals = [(k, keyValueDic1[k], keyValueDic2[k]) for k in diff if keyValueDic1[k] != keyValueDic2[k]] 
        #print(diff_vals)
        for differFile in diff_vals:
            ss = differFile[0]
            needReplaceList.append(ss)
        return needReplaceList
    except Exception as e:
        updatelog = open(updateTempPath + "\\updata.log",'a', encoding='UTF-8') 
        updatelog.write(str(e))
        updatelog.close() 
        errorOccurred = ExceptionOccurred()
        errorOccurred.sigDateCompareError.emit("文件比对失败")
    return needReplaceList    



def get_add_file(keyValueDic1:dict,keyValueDic2:dict)->list: 
    """对比两个字典，返回需要增加的文件列表

    Args:
        keyValueDic1 (dict): 标准对照文件生成的字典
        keyValueDic2 (dict): 本地生成的字典

    Returns:
        list: 需要增加的文件相对路径列表
    """
    needAddFile = []
    try:
        needAddFile = keyValueDic1.keys()-keyValueDic2.keys()
        #print(needAddFile)
        return needAddFile
    except Exception as e:
        updatelog = open(updateTempPath + "\\updata.log",'a', encoding='UTF-8') 
        updatelog.write(str(e))
        updatelog.close() 
        errorOccurred = ExceptionOccurred()
        errorOccurred.sigGetAddFileListError.emit("获取需要增加文件列表失败")
    return needAddFile


def txt_parse(txtPath:str)->dict:
    """把txt文件解析为一个字典

    Args:
        txtPath (str): txt文件路径

    Returns:
        dict: 生成的字典
    """
    keyValueDic = {}
    if os.path.exists(txtPath) == False or txtPath == None:
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
        updatelog = open(updateTempPath + "\\updata.log",'a', encoding='UTF-8') 
        updatelog.write(str(e))
        updatelog.close() 
        errorOccurred = ExceptionOccurred()
        errorOccurred.sigTxtFileParseError.emit("文本文件解析失败")   
    return keyValueDic


def down_load_file(needRepalceFile:list,needAddFile:list,baseUrlAddress = "https://edahotfix.oss-cn-hangzhou.aliyuncs.com/EPEDAPro/")->bool:
    """下载需要增加与替换的文件

    Args:
        needRepalceFile (list): 需要替换掉的文件列表
        needAddFile (list): 需要增加的文件列表
        baseUrlAddress (str, optional): 下载文件的url前缀

    Returns:
        bool:下载全部成功返回True,有一个失败就返回False
    """
    downLoadsuccess = True
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
        except Exception as e:
            downLoadsuccess  = False
            updatelog = open(updateTempPath + "\\updata.log",'a', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close()
            errorOccurred = ExceptionOccurred()
            errorOccurred.sigDownLoadFileError.emit(destPath)
            return  downLoadsuccess    
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
        except Exception as e:
            downLoadsuccess  = False
            updatelog = open(updateTempPath + "\\updata.log",'a', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close()
            errorOccurred = ExceptionOccurred()
            errorOccurred.sigDownLoadFileError.emit(destPath1)
            return downLoadsuccess
    return downLoadsuccess



def remove_file_to_destpath(needReplaceFile:list,needAddFile:list)->bool:
    """移动文件到指定位置

    Args:
        needReplaceFile (list): 需要替换的文件列表
        needAddFile (list): 需要增加的文件列表

    Returns:
        bool: 移动文件全部成功返回True,有一个不成功返回False
    """
    moveFileSuccess = True
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
            updatelog = open(updateTempPath + "\\updata.log",'a', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close()  
            moveFileSuccess = False 
            errorOccurred = ExceptionOccurred()
            errorOccurred.sigRemoveFileError.emit(replacePath)
            return moveFileSuccess
    for addFile in needAddFile:
        addPath = currPath + "\\" + addFile  
        sourceAddFilePath = tempPath + "\\" + addFile
        try:
            shutil.move(sourceAddFilePath,addPath)
        except Exception as e:
            updatelog = open(updateTempPath + "\\updata.log",'a', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close()  
            moveFileSuccess  = False  
            errorOccurred = ExceptionOccurred()
            errorOccurred.sigRemoveFileError.emit(addPath)
            return moveFileSuccess
    return moveFileSuccess
     

def delete_temp_folder()->bool:
    """删除本地Temp文件夹

    Returns:
        bool: 删除成功返回true，失败返回false
    """
    currentPath = os.getcwd()
    tempPath = currentPath + "\\Temp"
    try:
        if os.path.exists(tempPath):
            shutil.rmtree(tempPath)
        return True    
    except Exception as e:
            updatelog = open(updateTempPath + "\\updata.log",'a', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close() 
            errorOccurred = ExceptionOccurred()
            errorOccurred.sigDeleteTempError.emit("删除本地Temp文件夹失败")
    return False


def create_temp_folder()->bool:
    """本地路径下创建Temp文件夹，返回创建结果

    Returns:
        bool: 创建成功返回True，失败返回False
    """
    currentPath = os.getcwd()
    tempPath = currentPath + "\\Temp"
    try:
        os.makedirs(tempPath)
        return True
    except Exception as e:
            updatelog = open(updateTempPath + "\\updata.log",'a', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close()
            errorOccurred = ExceptionOccurred()
            errorOccurred.sigCreateTempError.emit("创建Temp文件夹失败")
    return False    


def down_load_oss_checkList(checkListTXtName = "\\edaCheckList.txt")->bool:
    """下载标准对比文件

    Args:
        checkListTXtName (str, optional): Defaults to "\edaCheckList.txt".下载的对照文件在本地的文件名

    Returns:
        bool: 下载成功返回True，下载失败返回False
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
            updatelog = open(updateTempPath + "\\updata.log",'a', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close()
            errorOccurred = ExceptionOccurred()
            errorOccurred.sigDownLoadCheckListError.emit("下载标准比对文件失败")
    return False   


def delete_updateTemp_folder()->bool:
    """删除updateTemp文件夹，返回创建结果

    Returns:
        bool: 删除成功返回True，失败返回False
    """
    currentPath = os.getcwd()
    updateTempPath = currentPath + "\\updateTemp"
    try:
        if os.path.exists(updateTempPath):
            shutil.rmtree(updateTempPath)
        return True    
    except Exception as e:
            updatelog = open(updateTempPath + "\\updata.log",'a', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close() 
            errorOccurred = ExceptionOccurred()
            errorOccurred.sigDeleteUpdatetempError.emit("删除updateTemp文件夹失败")
    return False


def create_updateTemp_folder()->bool:
    """创建updateTemp文件夹，返回创建结果

    Returns:
        bool: 创建成功返回True，失败返回False
    """
    currentPath = os.getcwd()
    updateTempPath = currentPath + "\\updateTemp"
    try:
        os.makedirs(updateTempPath)
        return True
    except Exception as e:
            updatelog = open(updateTempPath + "\\updata.log",'a', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close()
            errorOccurred = ExceptionOccurred()
            errorOccurred.sigCreateUpdatetempError.emit("创建updateTemp文件夹失败")
    return False   


def judge_file_writable(replaceList:list)->bool:
    """判断所有需要替换的文件是否可写

    Args:
        replaceList (list): 需要被替换的文件列表

    Returns:
        bool: 所有文件当前都可写返回True,有一个不可写就返回False
    """
    allFileWritAble = True
    for replaceFile in replaceList:
        currPath = os.getcwd()
        currPath = currPath.strip("EPEDAPro")
        replaceFilePath = currPath + "\\" + replaceFile
        try:
            if os.access(replaceFilePath,os.W_OK):
                continue
            else:
                allFileWritAble = False
                return allFileWritAble
        except Exception as e:
            updatelog = open(updateTempPath + "\\updata.log",'a', encoding='UTF-8') 
            updatelog.write(str(e))
            updatelog.close()
            errorOccurred = ExceptionOccurred()
            errorOccurred.sigJudgeFileWritableError.emit("创建updateTemp文件夹失败")
            allFileWritAble = False
            return allFileWritAble
    return allFileWritAble        

        

if __name__ == '__main__':
    # #删除本地updateTemp文件夹
    # delUpdateTemp = delete_updateTemp_folder() 
    # #创建updateTemp文件夹
    # createUpdateTemp = create_updateTemp_folder()
    # #删除Temp文件夹
    # delTemp =  delete_temp_folder()
    # #创建Temp文件夹
    # createTemp = create_temp_folder()
    # #下载checkList
    # loadCheckList = down_load_oss_checkList()
    # #把本地路径写成txt
    # generatelocaltxt = getLocalFileInfo()
    # #解析两份txt文件为dic
    # standardCheckList = txt_parse(r"C:\Users\wulongan\Desktop\python--\EPEDAPro_1028\EPEDAPro\updateTemp\edaCheckList.txt")
    # localCheckList = txt_parse(r"C:\Users\wulongan\Desktop\python--\EPEDAPro_1028\EPEDAPro\updateTemp\localtree.txt")
    # #获取需要替换的文件列表
    # needReplaceFileList = data_compare(standardCheckList,localCheckList)
    # #获取需要增加的文件列表
    # needAddFileList = get_add_file(standardCheckList,localCheckList)
    # #下载所有需要的文件
    # # dowmLoadFileResult = down_load_file(needAddFileList,needAddFileList)
    # # #移动下载的文件到相应位置
    # # removeFileResult = remove_file_to_destpath(needAddFileList,needAddFileList)




