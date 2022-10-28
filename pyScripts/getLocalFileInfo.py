import os,time,hashlib
from queue import LifoQueue


fileRelativePath = ""
filePathList = []
filePathList.append("")

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


def dsf_show(path_tree)->str:
    keyValueList = []
    q = LifoQueue()
    q.put(path_tree)
    sep_str = '   '
    try:
        f=open('localtree.txt','w',encoding='utf-8')
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


def show_path(path_tree)->str:
    level_map = {}
    level_map[path_tree.level] = [path_tree.name]
    get_level_path_dict(level_map, path_tree)
    txtpath = dsf_show(path_tree)
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


def getLocalFileInfo(base_path:str)->str:
    """输入本地EPEDAPro项目地址，会在相同路径下产生一个localtree.txt文件，返回的txt文件地址

    Args:
        base_path (str): 本地EPEDAPro项目地址

    Returns:
        str: 生成的txt文件路径
    """
    base_path_tree = PathTree(base_path, 3)
    get_path(base_path, base_path_tree, True)

    txtPath = show_path(base_path_tree)
    return txtPath


if __name__ == '__main__':
    base_path = os.getcwd()
    #base_path = r'C:\Users\wulongan\Desktop\python--\EPEPDAPro1'
    localTxtPath = getLocalFileInfo(base_path)
    print(localTxtPath)
