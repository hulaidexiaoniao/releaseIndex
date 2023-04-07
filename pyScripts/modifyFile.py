import json
import os

txt1 = {
 "pcb": "RobotCam.json",
 "precheck": "PreGuide.json",
 "pcb_execute": "Robot.json",
 "part_precheck": "PreGuideForQuote.json",
 "dxf": "DXF.json"
}
txt2 = {
    "ClientIp": "127.0.0.1",
    "DBPath": "c:/checklist",
    "OS": 0,
    "Port": 8009,
    "SelectionOutsideHint": True,
    "ServerIp": "127.0.0.1",
    "SharePath": "c/Project/EPCAM/trunk/bin/x64/Release/job/",
    "TimeOut": 100000,
	"ThreadCount": 10,
	"use_specifiled_suffix": True,
    "suffix": "+++",
    "layer_copy_suffix": "_org",
	"Movement_factor":0.9,
	"Shift_confict": 0.1,
	"contour_accuracy": 24,
	"guide":"pcb",
	"modify_hotkey":True,
	"PythonHome":True,
	"ViewMode":"Cache"
}

txt3 = [
"[VS]\n",
"tol=0.65\n",
"\n"
"[useDB]\n",
"name = mongo\n",
"\n"
"[openMixedPanel]\n",
"state = 0\n"
]
def CamGuide(path_camguide):
    path_CamGuide = path_camguide + "\\release\\CAMGuide\\config\\Cam_Module.json"
    sss = os.path.exists(path_CamGuide)
    if not os.path.exists(path_CamGuide):
        path_CamGuide = path_camguide + "\\EPEDAPro\\CAMGuide\\config\\Cam_Module.json"
    data1 = json.dumps(txt1, indent=1)
    with open(path_CamGuide, 'w',newline='\n') as fp1:
        fp1.seek(0)
        fp1.truncate()
        fp1.write(data1)
        
def Server(path_server):
    path_Server = path_server + "\\release\\config\\server.json"
    ss = os.path.exists(path_Server)
    if not os.path.exists(path_Server):
        path_Server = path_server + "\\EPEDAPro\\config\\server.json"
    data2 = json.dumps(txt2, indent=1)
    with open(path_Server, 'w',newline='\n') as fp2:
        fp2.seek(0)
        fp2.truncate()
        data2.replace('True','true')
        fp2.write(data2)

def EDAConfig(path_config,version):
    path_configs = path_config + "\\release\\EDAConfig.ini"
    if not os.path.exists(path_configs):
        path_configs = path_config + "\\EPEDAPro\\EDAConfig.ini"
    os.remove(path_configs)
    with open(path_configs,"a") as ss:
        for item in txt3:
            ss.write(item)
    pp = os.path.join(os.path.expanduser('~'),"Desktop") + "\\P" + version
    dd = os.path.join(os.path.expanduser('~'),"Desktop") + "\\K" + version
    os.rename(pp,dd)
    


# if __name__=='__main__':
# #     CamGuide()
# #     Server()
#     ss = r"C:\Users\wulongan\Desktop\EpEDAPro\trunk\EPEDAPro\bin\x64"
#     EDAConfig(ss)
