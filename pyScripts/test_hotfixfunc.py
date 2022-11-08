import pytest
import hotfixFunc
import os


@pytest.fixture()
def set_up():
    print("[pytest with fixture] start")
    yield
    print("[pytest with fixture] end")


class TestDeleteAndDeletefolder():
    def test_delete_updateTemp(selt,set_up):
        qq = hotfixFunc.delete_updateTemp_folder()
        assert qq == True

    def test_delete_temp(self,set_up):
        ww = hotfixFunc.delete_temp_folder()
        assert ww == True

    def test_create_updateTemp(self,set_up):
        ee = hotfixFunc.create_updateTemp_folder()
        assert ee == True

    def test_create_temp(self,set_up):
        rr = hotfixFunc.create_temp_folder()
        assert rr == True        
            

class TestDownLoadCheckListTest():
    """down_load_oss_checkList(checkListTXtName: str = "\\edaCheckList.txt") -> bool
    参数类型为 str , 下载的标准对比文件的名称，默认值为 :"\\edaCheckList.txt"   
    标准输入为 "\\"+ 文件名 ，例： \\ddd.txt
    """
    @pytest.mark.parametrize("str1, boolee", [("\\ddd.txt", True), ("\\1, 2", True), ("\\ddd.log", True),("\\  ",False),("\\dd  dd.txt",True)])
    def test_download_checklist(self,set_up,str1,boolee):
        result = hotfixFunc.down_load_oss_checkList(str1)
        assert boolee == result



class TestGetLocalFileInfo():
    """getLocalFileInfo(basePath: str = os.getcwd(), localTxtName: str = currentPath + "\\updateTemp" + '\\localtree.txt') -> bool
    参数1为一个路径，函数会将此路径下所有文件名读出，类型为str,默认值为 os.getcwd(),路径必须存在，否则返回False
    参数2为生成文件的放置路径及文件名，会在类型为str
    """
    @pytest.mark.parametrize("str1,str2,getSucceed",[(os.getcwd(),os.getcwd() + "\\updateTemp\\ll.txt",True),(os.getcwd(),os.getcwd() + "\\updateTemp\\cc.txt",True),("asddasd","asdsaggdsa",False),("","",False),("","nn.txt",False)])
    def test_get_local_file_info(self,set_up,str1,str2,getSucceed):
        result = hotfixFunc.getLocalFileInfo(str1,str2)
        assert result == getSucceed


class TesttxtParse():
    """txt_parse(txtPath: str) -> dict
   参数是对比文件的路径， 参数类型为str，路径如果不存在，返回的字典为空
    """
    @pytest.mark.parametrize("str1",[(os.getcwd() + "\\updateTemp\\cc.txt"),("sdasd"),(""),(" ")])
    def test_txt_parse(self,set_up,str1):
        xtxList = hotfixFunc.txt_parse(str1)
        print(xtxList)


"""txt1:
"""
class TestdateCompare():
    """data_compare(keyValueDic1: dict, keyValueDic2: dict) -> list
    参数1为通过txt_parse方法生成的字典
    参数2为通过txt_parse方法生成的字典
    返回的是一个列表，存储需要替换的文件的相对路径
    """
    def test_date_compare(self,set_up):
        dic1 = hotfixFunc.txt_parse(os.getcwd() + "\\updateTemp\\cc.txt")
        dic2 = hotfixFunc.txt_parse(os.getcwd() + "\\updateTemp\\ll.txt")
        replacelist = hotfixFunc.data_compare(dic1,dic2)
        print(replacelist)
        print("#########################################################")

class TestgetAddFile():
    """get_add_file(keyValueDic1: dict, keyValueDic2: dict) -> list
    参数1为通过txt_parse方法生成的字典
    参数2为通过txt_parse方法生成的字典
    返回的是一个列表，存储需要增加的文件的相对路径
    """
    def test_get_add_file(self,set_up):
        open(os.getcwd() + "\\updateTemp\\ll.txt",'w', encoding='UTF-8').close()
        dic3 = hotfixFunc.txt_parse(os.getcwd() + "\\updateTemp\\cc.txt")
        dic4 = hotfixFunc.txt_parse(os.getcwd() + "\\updateTemp\\ll.txt")
        addlist = hotfixFunc.get_add_file(dic3,dic4)
        print(addlist)
        print("**********************************************************************")

class TestDownloadFile():
    """ down_load_file(needRepalceFile: list, needAddFile: list, baseUrlAddress: str = "https://edahotfix.oss-cn-hangzhou.aliyuncs.com/EPEDAPro/") -> bool
    参数1类型为list,是通过data_compare生成的list,存储需要替换的文件的相对路径
    参数2类型为list,是通过get_add_file生成的list,存储需要增加的文件的相对路径
    """
    def test_down_load_file(self,set_up):
        list1 = ['EPEDAPro\\resources\\images\\export_success.png', 'EPEDAPro\\Translator\\Chinese\\matrix_zh.qm', 
        'EPEDAPro\\rangesconfig\\SurfaceAnalyzer\\SurfaceAnalyzerRanges.json', 'EPEDAPro\\Translator\\Chinese\\cam_menubar_actions_zh.qm',
         'EPEDAPro\\Translator\\Chinese\\graphic_coordinate_zh.qm', 'EPEDAPro\\CAMGuide\\base\\epcam\\epcam.py', 'EPEDAPro\\Viewbar_View.dll', 
         'EPEDAPro\\zlibwapi.dll', 'EPEDAPro\\CAMGuide\\PreGuide\\Net\\drill_classify_attribute.py', 'EPEDAPro\\vcruntime140_1.dll',
          'EPEDAPro\\CAMGuide\\base\\rangesconfig\\DFM_SignalLayerOpt\\SignalLayerOptRanges.json', 'EPEDAPro\\resources\\font\\Alibaba-PuHuiTi-B.ttf', 
          'EPEDAPro\\api-ms-win-crt-runtime-l1-1-0.dll', 'EPEDAPro\\Widget_Common.dll']  
        list2 = ['EPEDAPro\\CAMGuide\\PreGuideForQuote\\Net\\drill_classify_attribute.py', 'EPEDAPro\\resources\\images\\dropDowm.png', 'EPEDAPro\\Viewbar_Status.dll', 'Resources\\qtwebengine_resources.pak', 'EPEDAPro\\CAMGuide\\RobotCam\\Inner\\inner_check1.py', 'EPEDAPro\\Translator\\MixedLanguage\\graphic_menubar_dfm_zh_en.qm', 
        'EPEDAPro\\resources\\images\\camJobVs_step1.png', 'EPEDAPro\\CAMGuide\\Robot\\panel_edge\\diran_panel\\target-df.py', 
        'EPEDAPro\\CAMGuide\\base\\__pycache__\\layer_info.cpython-37.pyc']
        downloadsuccess = hotfixFunc.down_load_file(list1,list2)
        print("downloadsuccess = ",downloadsuccess)


class TestmoveFile():
    """ remove_file_to_destpath: (needReplaceFile: list, needAddFile: list) -> bool
    参数1类型为list,是通过data_compare生成的list,存储需要替换的文件的相对路径
    参数2类型为list,是通过get_add_file生成的list,存储需要增加的文件的相对路径
    """
    def test_move_file1(self,set_up):
        list1 = ['EPEDAPro\\resources\\images\\export_success.png', 'EPEDAPro\\Translator\\Chinese\\matrix_zh.qm', 
        'EPEDAPro\\rangesconfig\\SurfaceAnalyzer\\SurfaceAnalyzerRanges.json', 'EPEDAPro\\Translator\\Chinese\\cam_menubar_actions_zh.qm',
         'EPEDAPro\\Translator\\Chinese\\graphic_coordinate_zh.qm', 'EPEDAPro\\CAMGuide\\base\\epcam\\epcam.py', 'EPEDAPro\\Viewbar_View.dll', 
         'EPEDAPro\\zlibwapi.dll', 'EPEDAPro\\CAMGuide\\PreGuide\\Net\\drill_classify_attribute.py', 'EPEDAPro\\vcruntime140_1.dll',
          'EPEDAPro\\CAMGuide\\base\\rangesconfig\\DFM_SignalLayerOpt\\SignalLayerOptRanges.json', 'EPEDAPro\\resources\\font\\Alibaba-PuHuiTi-B.ttf', 
          'EPEDAPro\\api-ms-win-crt-runtime-l1-1-0.dll', 'EPEDAPro\\Widget_Common.dll']  
        list2 = ['EPEDAPro\\CAMGuide\\PreGuideForQuote\\Net\\drill_classify_attribute.py', 'EPEDAPro\\resources\\images\\dropDowm.png', 'EPEDAPro\\Viewbar_Status.dll', 'Resources\\qtwebengine_resources.pak', 'EPEDAPro\\CAMGuide\\RobotCam\\Inner\\inner_check1.py', 'EPEDAPro\\Translator\\MixedLanguage\\graphic_menubar_dfm_zh_en.qm', 
        'EPEDAPro\\resources\\images\\camJobVs_step1.png', 'EPEDAPro\\CAMGuide\\Robot\\panel_edge\\diran_panel\\target-df.py', 
        'EPEDAPro\\CAMGuide\\base\\__pycache__\\layer_info.cpython-37.pyc']
        movesuccess = hotfixFunc.remove_file_to_destpath(list1,list2)
        print("movesuccess = ",movesuccess)
        assert movesuccess == False
    
    def test_move_file2(self,set_up):
        list1 = ['EPEDAPro\\zlibwapi.dll', 'EPEDAPro\\Viewbar_View.dll']
        list2 = ['EPEDAPro\\Widget_Common.dll']
        cc = os.getcwd()
        os.makedirs(os.path.dirname(cc + "\\EPEDAPro"), exist_ok=True)
        open(cc + "\\EPEDAPro\\zlibwapi.dll","w")
        open(cc + "\\EPEDAPro\\Widget_Common.dll","w")
        open(cc + "\\EPEDAPro\\Viewbar_View.dll","w")
        movesuccess = hotfixFunc.remove_file_to_destpath(list1,list2)
        print("movesuccess = ",movesuccess)


class TestJudgeFileWritable():
    def test_judge_file_writable1(self,set_up):
        list1 = ['EPEDAPro\\resources\\images\\export_success.png', 'EPEDAPro\\Translator\\Chinese\\matrix_zh.qm', 
        'EPEDAPro\\rangesconfig\\SurfaceAnalyzer\\SurfaceAnalyzerRanges.json', 'EPEDAPro\\Translator\\Chinese\\cam_menubar_actions_zh.qm',
         'EPEDAPro\\Translator\\Chinese\\graphic_coordinate_zh.qm', 'EPEDAPro\\CAMGuide\\base\\epcam\\epcam.py', 'EPEDAPro\\Viewbar_View.dll', 
         'EPEDAPro\\zlibwapi.dll', 'EPEDAPro\\CAMGuide\\PreGuide\\Net\\drill_classify_attribute.py', 'EPEDAPro\\vcruntime140_1.dll',
          'EPEDAPro\\CAMGuide\\base\\rangesconfig\\DFM_SignalLayerOpt\\SignalLayerOptRanges.json', 'EPEDAPro\\resources\\font\\Alibaba-PuHuiTi-B.ttf', 
          'EPEDAPro\\api-ms-win-crt-runtime-l1-1-0.dll', 'EPEDAPro\\Widget_Common.dll']  
        allfileWritable = hotfixFunc.judge_file_writable(list1)
        print("allfileWritable = ",allfileWritable)
        assert allfileWritable == False

    def test_judge_file_writable2(self,set_up):
        dic5 = hotfixFunc.txt_parse(os.getcwd() + "\\updateTemp\\cc.txt")
        dic6 = hotfixFunc.txt_parse(os.getcwd() + "\\updateTemp\\ll.txt")
        addlist = hotfixFunc.get_add_file(dic5,dic6) 
        fileWritable = hotfixFunc.judge_file_writable(addlist)
        print("fileWritable = ",fileWritable)
        assert fileWritable == True


if __name__ == '__main__':
    pytest.main(['-s', 'test_hotfixfunc.py'])