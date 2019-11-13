#coding:utf-8    
import pickle
from datetime import datetime
import sys
import os
import time
import win32api 
import subprocess
import win32con
import signal
import win32process
import win32event
import win32gui


if sys.version_info[0] == 2:
    from urllib2 import urlopen  # Python 2
else:
    from urllib.request import urlopen  # Python3
    import urllib.request
    import urllib.parse
 

def _MyCallback( hwnd, extra ):
    windows = extra
    temp=[]
    temp.append(int(hwnd))
    temp.append(win32gui.GetClassName(hwnd))
    temp.append(win32gui.GetWindowText(hwnd))
    windows[hwnd] = temp
  
def find_window(name):
    windows = {}
    win32gui.EnumWindows(_MyCallback, windows)
    #print "Enumerated a total of  windows with %d classes" ,(len(windows))
    #print '------------------------------'
    #print classes
    #print '-------------------------------'
    for hwnd in windows.keys() :
        #print  windows[item]
        if windows[hwnd][2].find(name)!=-1:
            return hwnd
    return 0
  
 
def run_cmd(cmd):
    cmd +='\nexit'
    print(cmd)
    #save_file("updatemod.bat",cmd.encode())
    #p = os.popen(".\\save\\updatemod.bat")

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    try:
        info = p.stdout.read().decode()
    except Exception as e:
        info = p.stdout.read()
    
    return info
    #print(str(p.read().decode()) )
    #print("please input :")
    #p.write(input())
    #print(p.read())     
    #input()
 

def get_server_pid():
    cmd = "tasklist /FI \"IMAGENAME eq \"ConanSandboxServer-Win64-Test.exe\"\" "

while True:
  
    try:
        main(gen_update_time ,debug ,steamcmdpath,mods_install ,ModsName ,Mods,ModDownload )
    except Exception as e:
        print(e)
        raise e