from encodings import utf_8
from genericpath import isfile
from importlib.resources import contents
from operator import contains
import sys
import os
import shutil
from queue import LifoQueue

firstLayer = ''
secondLayer = ''
thirdLayer = ''
fourthLayer = ''
fifthLayer = ''
sixthLayer = ''
seventhLayer = ''
eighthLayer = ''
ninthLayer = ''
tenthLayer = ''
eleventhLayer = ''
twelfthLayer = ''
thirteenthLayer = ''
fourteenthLayer = ''
addressList = []
absolutePathList = []
#从basePath拿取所需的文件
basePath = r"C:\Users\wulongan\Desktop\EpEDAPro\trunk\EPEDAPro\bin\x64"
#新的文件放置地址
newFilePath = os.getcwd()+ "\\" + "EPEDAPro_1027"
#isSDKdir 读取的是proSDK目录时为true，读取的是完整pro目录时为false
isSDKdir = True       


if __name__ == '__main__':
    #读取目录
    fileHandler  =  open  (r"C:\Users\wulongan\Desktop\python--\EPEDAProSDK.txt",encoding='utf-8')
    while  True:
        # Get next line from file
        line  =  fileHandler.readline()
        # If line is empty then end of file reached
        if  not  line  :
            break
        #去掉右边的空格    
        s = line.rstrip()    
        s1 = "|--"
        #当前行前面有多少空格
        b =s.find(s1)
        if b == 12:
            firstLayer = line.strip()
            firstLayer = firstLayer.strip("|--")
            #print(firstLayer)
            addressList.append(firstLayer)
        elif b == 15:
            secondLayer = line.strip()
            secondLayer = secondLayer.strip("|--")
            addressstr = firstLayer + "\\" + secondLayer
            addressList.append(addressstr)
        elif b == 18:
            thirdLayer = line.strip() 
            thirdLayer = thirdLayer.strip("|--")
            addressstr = firstLayer+"\\"+secondLayer+"\\"+thirdLayer
            addressList.append(addressstr)
        elif b == 21:
            fourthLayer = line.strip()
            fourthLayer = fourthLayer.strip("|--")
            addressstr = firstLayer+"\\"+secondLayer+"\\"+thirdLayer+"\\"+fourthLayer
            addressList.append(addressstr)   
        elif b == 24:
            fifthLayer = line.strip()
            fifthLayer = fifthLayer.strip("|--")
            addressstr = firstLayer+"\\"+secondLayer+"\\"+thirdLayer+"\\"+fourthLayer+"\\"+fifthLayer
            addressList.append(addressstr)   
        elif b == 27:
            sixthLayer = line.strip()
            sixthLayer = sixthLayer.strip("|--")
            addressstr = firstLayer+"\\"+secondLayer+"\\"+thirdLayer+"\\"+fourthLayer+"\\"+fifthLayer+"\\"+sixthLayer
            addressList.append(addressstr)    
        elif b == 30:
            seventhLayer = line.strip()
            seventhLayer = seventhLayer.strip("|--")
            addressstr = firstLayer+"\\"+secondLayer+"\\"+thirdLayer+"\\"+fourthLayer+"\\"+fifthLayer+"\\"+sixthLayer+"\\"+seventhLayer
            addressList.append(addressstr)
        elif b == 33:
            eighthLayer = line.strip()
            eighthLayer = eighthLayer.strip("|--")
            addressstr = firstLayer+"\\"+secondLayer+"\\"+thirdLayer+"\\"+fourthLayer+"\\"+fifthLayer+"\\"+sixthLayer+"\\"+seventhLayer+"\\"+eighthLayer
            addressList.append(addressstr)
        elif b == 36:
            ninthLayer = line.strip()
            ninthLayer = ninthLayer.strip("|--")
            addressstr = firstLayer+"\\"+secondLayer+"\\"+thirdLayer+"\\"+fourthLayer+"\\"+fifthLayer+"\\"+sixthLayer+"\\"+seventhLayer+"\\"+eighthLayer+"\\"+ninthLayer
            addressList.append(addressstr)  
        elif b == 39:
            tenthLayer = line.strip()
            tenthLayer = tenthLayer.strip("|--")
            addressstr = firstLayer+"\\"+secondLayer+"\\"+thirdLayer+"\\"+fourthLayer+"\\"+fifthLayer+"\\"+sixthLayer+"\\"+seventhLayer+"\\"+eighthLayer+"\\"+ninthLayer+"\\"+tenthLayer
            addressList.append(addressstr)
        elif b == 42:
            eleventhLayer = line.strip()
            eleventhLayer = eleventhLayer.strip("|--")
            addressstr = firstLayer+"\\"+secondLayer+"\\"+thirdLayer+"\\"+fourthLayer+"\\"+fifthLayer+"\\"+sixthLayer+"\\"+seventhLayer+"\\"+eighthLayer+"\\"+ninthLayer+"\\"+tenthLayer+"\\"+eleventhLayer
            addressList.append(addressstr)
        elif b == 45:
            twelfthLayer = line.strip()
            twelfthLayer = twelfthLayer.strip("|--")
            addressstr = firstLayer+"\\"+secondLayer+"\\"+thirdLayer+"\\"+fourthLayer+"\\"+fifthLayer+"\\"+sixthLayer+"\\"+seventhLayer+"\\"+eighthLayer+"\\"+ninthLayer+"\\"+tenthLayer+"\\"+eleventhLayer+"\\"+twelfthLayer
            addressList.append(addressstr) 
        elif b == 48:
            thirteenthLayer = line.strip()
            thirteenthLayer = thirteenthLayer.strip("|--")
            addressstr = firstLayer+"\\"+secondLayer+"\\"+thirdLayer+"\\"+fourthLayer+"\\"+fifthLayer+"\\"+sixthLayer+"\\"+seventhLayer+"\\"+eighthLayer+"\\"+ninthLayer+"\\"+tenthLayer+"\\"+eleventhLayer+"\\"+twelfthLayer+"\\"+thirteenthLayer
            addressList.append(addressstr) 
        elif b == 51:
            fourteenthLayer = line.strip()
            fourteenthLayer = fourteenthLayer.strip("|--")
            addressstr = firstLayer+"\\"+secondLayer+"\\"+thirdLayer+"\\"+fourthLayer+"\\"+fifthLayer+"\\"+sixthLayer+"\\"+seventhLayer+"\\"+eighthLayer+"\\"+ninthLayer+"\\"+tenthLayer+"\\"+eleventhLayer+"\\"+twelfthLayer+"\\"+thirteenthLayer+"\\"+fourteenthLayer
            addressList.append(addressstr)                   
        # Close Close    
    fileHandler.close()
    #print(addressList)
    for relativePath in addressList:
        if isSDKdir:
            absolutePath = basePath + "\\" + relativePath 
        else:
            absolutePath = basePath + relativePath    
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
