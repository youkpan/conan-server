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

gen_update_time = False #False 
debug = False

steamcmdpath = "C:\\conan"
mods_install = steamcmdpath+"\\Mods"

ModsName = {}
Mods = {}
ModDownload = {}
    
ModsName[0]="Improved_Quality_of_Life"
Mods[0]=1657730588
ModDownload[0]=True


ModsName[1]="TheColdEmbrace-Main"
Mods[1]=1113901982
ModDownload[1]=True


ModsName[2]="LitManItemStackAndContainerSize"
Mods[2]=1125427722
ModDownload[2]=True

ModsName[3]="300"
Mods[3]=1386174080
ModDownload[3]=True


##MASSI MODS

ModsName[4]="RA"
Mods[4]=1542041983
ModDownload[4]=True

ModsName[5]="Pippi"
Mods[5]=880454836
ModDownload[5]=True


ModsName[6]="DungeonMasterTools"
Mods[6]=1699858371
ModDownload[6]=True


ModsName[7]="Tutorial"
Mods[7]=1734383367
ModDownload[7]=True


ModsName[8]="NumericHUD"
Mods[8]=1753303494
ModDownload[8]=True


ModsName[9]="EEWAExtraFeatLightsabers"
Mods[9]=1795327310
ModDownload[9]=True 

ModsName[10]="StylistPlus"
Mods[10]=1159180273
ModDownload[10]=True 


def main(gen_update_time ,debug ,steamcmdpath,mods_install ,ModsName ,Mods,ModDownload ):
    update_time = get_data("update_time",{})
    print("update_time",update_time)
    #update_time = {}
    for idx in update_time.keys():
        print(idx,"update_time",update_time[idx])

    proc = 0
    #re = stop_game_server(proc)
    if True or debug  :
        proc = start_game_server(steamcmdpath,proc)
        time.sleep(10)

    hours_count = 0
    while(True):

        has_mod_update = False
        if debug:
            has_mod_update = True
        after_cmd = ""
        modlistfile = ""

        for idx in ModsName.keys():
            workshopid= Mods[idx]
            print("-------------",str(idx))
            try:
                t=update_time[workshopid]
                print(ModsName[idx],"last update_time",t)
            except Exception as e:
                update_time[workshopid] = ""

            try:
                update_time1 = get_update_time(workshopid)
            except Exception as e:
                try:
                    update_time1 = get_update_time(workshopid)
                except Exception as e:
                    print(ModsName[idx],"not get update_time")
            
            print(ModsName[idx],"get update_time",update_time1)

            if(debug):
                input("waite")

            if(update_time[workshopid]!=update_time1 and update_time1!="" and not gen_update_time or (idx==0 and debug)):
                
                print("getting Mod:",ModsName[idx])
                cmd = steamcmdpath+"\\steamcmd +login teluwl Pan7777777 +force_install_dir \""+mods_install+"\" +\"workshop_download_item 440900 "+str(workshopid)+"\" +quit "
                out = run_cmd(cmd)
                if out.find("Success. Downloaded item")>0:
                    print(" download ",ModsName[idx]," Success !!")
                    after_cmd += "move /Y "+mods_install+"\\steamapps\\workshop\\content\\440900\\"+str(workshopid)+"\\"+ModsName[idx]+".pak "+steamcmdpath+"\\server\\ConanSandbox\\Mods\\ \n"
                    
                    update_time[workshopid] = update_time1
                    
                    has_mod_update = True    
                else:
                    print("not download ",ModsName[idx],"!!")

            if gen_update_time:
                update_time[workshopid] = update_time1
                save_data("update_time",update_time)

            modlistfile += mods_install+"\\steamapps\\workshop\\content\\440900\\"+str(workshopid)+"\\"+ModsName[idx]+".pak\n"

        save_file("modlist.txt",modlistfile.encode())
        #print("please copy save/modlist.txt to "+steamcmdpath+"\\server\\ConanSandbox\\Mods\\")

        if(has_mod_update):
            shut_down_cmd = ""
            #win32api.GenerateConsoleCtrlEvent(win32con.CTRL_C_EVENT, pid)
            re = stop_game_server(proc)
            if re==0:
                print("stop_game_server error")
            time.sleep(10)
            print("after_cmd",after_cmd)
            run_cmd(after_cmd)
            print("start_game_server")
            save_data("update_time",update_time)
            #input()

        window = find_game_window()
        if window==0:
            proc = start_game_server(steamcmdpath,proc)

        if not debug and not gen_update_time:
            time.sleep(3600)

        hours_count+=1

        hour =datetime.now().hour 
        if debug or gen_update_time or hours_count %4==3 and (hour >= 3 and hour <=7 or hour >= 15 and hour <=19) :

            game_info,game_update_time = get_game_info(steamcmdpath,443030)
            #print(game_info)
            print("game_update_time",game_update_time)

            if gen_update_time:
                update_time[443030] = game_update_time
                save_data("update_time",update_time)

            if debug or update_time[443030] != game_update_time:
                update_time[443030] = game_update_time
                save_data("update_time",update_time)
                #input()
                re = stop_game_server(proc)
                #update server
                proc =start_game_server(steamcmdpath,proc) 

        gen_update_time = False




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

def save_data(name,data):
    output = open('./save/%s.pkl'%name, 'wb')
    pickle.dump(data, output, -1)
    output.close()
    
def get_data(name,default):
    try:
        pkl = open('./save/%s.pkl'%name, 'rb')
        data =  pickle.load( pkl)
        pkl.close()  
    except Exception as e:
        save_data(name,default)
        data =get_data(name,default)
        data = default
    return data

def save_file(name,data):
    try:
        f = open('./save/%s'%name, 'wb')
        f.write(data)
        f.close()  
    except Exception as e:
        print("save file error",str(e))
    return data

def get_update_time(id):

    #url = "http://mysea.hayoou.com/curl.php?url="+urllib.parse.quote('https://steamcommunity.com/sharedfiles/filedetails/?id=%d'%(id), safe='/', encoding=None, errors=None)
    #print(url)
    url = 'https://steamcommunity.com/sharedfiles/filedetails/?id=%d'%(id)
    print(url)
    url = "http://mysea.hayoou.com/curl.php?steam_update_time=1&id=%d"%(id)
    print(url)

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    values ={}
    data = urllib.parse.urlencode(values)

    req = urllib.request.Request(url)

    #req.add_header('Referer', 'https://www.iesdouyin.com/share/user/')
    #req.add_header(':authority', 'www.douyin.com')
    req.add_header('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')
    req.add_header('user-agent', user_agent)

    response = urllib.request.urlopen(req)
    html = response.read().decode()

    return html
    '''
    #html = urlopen( get_video_url(vid) ).read().decode()
    #"author":{"uid":"93957793296"
    start =  html.find('更新日期')
    start =  html.find('"detailsStatRight">',start+10)
    start =  html.find('"detailsStatRight">',start+10)
    start =  html.find('"detailsStatRight">',start+10)+19

    end =  html.find('<',start)
    update_time = html[start:end]
    if(len(update_time)>40):
            update_time = ""
    return update_time
    '''

def run_cmd(cmd):
    cmd +='\nexit'
    print(cmd)
    #save_file("updatemod.bat",cmd.encode())
    #p = os.popen(".\\save\\updatemod.bat")

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    info = p.stdout.read().decode()
    return info
    #print(str(p.read().decode()) )
    #print("please input :")
    #p.write(input())
    #print(p.read())     
    #input()

def get_game_info(steamcmdpath,steamid):
    p = subprocess.Popen(steamcmdpath + "\\steamcmd +login anonymous +app_info_update 1 +app_info_print "+str(steamid)+" +quit", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    info = p.stdout.read().decode()
    start = info.find("last change :")+13
    end = info.find("\"",start+13)

    update_time = info[start:end]
    return info ,update_time

def start_game_server(steamcmdpath,proc):
    window = find_game_window()
    if window>0:
        return proc
    proc= 0 
    info = run_cmd(steamcmdpath + "\\steamcmd +login anonymous +force_install_dir \"C:\\conan\\server\" +app_update 443030 +quit")
    print(info,"starting ConanSandboxServer")
    proc = subprocess.Popen(steamcmdpath + "\\server\\ConanSandboxServer.exe -log ", stdin=subprocess.PIPE)
    return proc

def press_ctrl_c(window):
    win32gui.SetForegroundWindow(window)
    time.sleep(2)
    # 按下ctrl+close
    win32api.keybd_event(0x11, 0, 0, 0)
    time.sleep(1)
    win32api.keybd_event(0x43, 0, 0, 0)
    time.sleep(2)
    win32api.keybd_event(0x43, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(1)
    win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)

def find_game_window():
    return find_window("- Conan Exiles - press Ctrl+C to shutdown")

def stop_game_server(proc,waitstop=True):
    print ("stop_game_server sending ctrl c")   
    #os.kill(19816,signal.CTRL_C_EVENT)
    #win32api.GenerateConsoleCtrlEvent(win32con.CTRL_C_EVENT, 14204)
    #
    #os.kill(19816)
    #appname = "hayoou"# "11.30/10经10采无神/hayoou.com 哈友社区长期稳定优化 - Conan Exiles - press Ctrl+C to shutdown"# "ConanSandboxServer-Win64-Test.exe"
    #window = win32gui.FindWindow("ConsoleWindowClass", appname)
    window = find_game_window()
    if window==0:
        return 0 
    try:
        print("find window",window)
        press_ctrl_c(window)
        time.sleep(30)
        count = 0
        if waitstop:
            window = find_game_window()
            while window>0:
                time.sleep(20)
                window = find_game_window()
                if count % 20 == 19:
                    press_ctrl_c(window)
                count +=1
                #if count >40:
                #    os.kill(window)
    except:
        pass

    return 1
    '''
     
    try:
        #win32api.GenerateConsoleCtrlEvent(win32con.CTRL_C_EVENT, 0)
        proc.send_signal(signal.CTRL_C_EVENT)

        proc.wait()
        time.sleep(60)
    except KeyboardInterrupt:
        print( "ignoring ctrl c")
    '''

#stop_game_server(1)


def get_server_pid():
    cmd = "tasklist /FI \"IMAGENAME eq \"ConanSandboxServer-Win64-Test.exe\"\" "

while True:
  
    try:
        main(gen_update_time ,debug ,steamcmdpath,mods_install ,ModsName ,Mods,ModDownload )
    except Exception as e:
        print(e)
        #raise e