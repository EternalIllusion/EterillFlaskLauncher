# -*- coding: utf-8 -*-
from threading import Thread
from os import popen,path,getcwd,system,chdir,listdir
from re import findall
from random import randint
from pickle import dump,load
from base64 import b64encode
from io import FileIO
from time import sleep
import sys
import json
from flask import Flask,request,redirect
printf=print
##STARTUP PATH##
app_path=getcwd()
chdir(app_path)

def searchdirs(app_path=app_path):
    ccwd=getcwd()
    try:
        chdir(app_path)
        rtv={}
        printf(f"<SC>Searching:{app_path}")
        dl=listdir(app_path)
        if 'desc.json' in dl:
            with open("desc.json",'r',encoding="utf-8") as desc:
                desc=json.loads(desc.read())
            desc=desc["info"]["name"] if desc["info"]["name"] else "Untitled"
            rtv[str(desc)]=app_path
        for dli in dl:
            if 'AppData' in dli:continue
            if 'Program Files' in dli:continue
            if 'cache' in dli:continue
            if 'Cache' in dli:continue
            if path.isfile(dli):continue
            nxt=searchdirs(app_path+"\\"+dli)
            for it in nxt:rtv[it]=nxt[it]
    except:pass
    chdir(ccwd)
    return rtv
app_dirs={}
def refappdirs(sv=False):
    global app_dirs
    if path.exists("projects.json") and not sv:
        with open("projects.json","r") as cfg:
            app_dirs=json.loads(cfg.read())
    else:
        with open("projects.json","w") as cfg:
            app_dirs=searchdirs()
            json.dump(app_dirs, cfg)
refappdirs()
##SETUP##
try:
    from setup import *
    printf("Setup Script:setup.py")
except:
    if path.exists("setup.bat"):
        system("start setup.bat")
        sleep(3)
    else:printf("No Setup Script detected.Skip Setup.")
false=False
true=True
##HTML##
header='''
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>EterIll Launcher Console Interface</title>
<style type="text/css">
<!--
body {
	font: 100%/1.4 Verdana, Arial, Helvetica, sans-serif;
	background-color: #4E5869;
	margin: 0;
	padding: 0;
	color: #000;
}
ul, ol, dl {
	padding: 0;
	margin: 0;
}
h1, h2, h3, h4, h5, h6, p {
	margin-top: 0;
	padding-right: 15px;
	padding-left: 15px;
}
a img {
	border: none;
}
.red:link {
    color: #f00;
}
.red:visited {
    color: #d00;
}
a:link {
	color: #414958;
	text-decoration: underline;
}
a:visited {
	color: #4E5869;
	text-decoration: underline;
}
a:hover, a:active, a:focus {
	text-decoration: none;
}
.title {
    flex: 1;
    justify-content: center;
}
.container {
	width: 80%;
	max-width: 1260px;
	min-width: 780px;
	background-color: #FFF;
	margin: 0 auto;
}
.header {
	background-color: #6F7D94;
    color: #fff;
}

.content {
	padding: 10px 0;
}
.content ul, .content ol {
	padding: 0 15px 15px 40px;
}
.footer {
    color: #eee;
	padding: 10px 0;
	background-color: #6F7D94;
}
.fltrt {
    float: right;
	margin-left: 8px;
}
.fltlft { 
    float: left;
	margin-right: 8px;
}
.clearfloat { 
    clear: both;
	height: 0;
	font-size: 1px;
	line-height: 0px;
}
span{
    color:#F00;
}
table.console {
    margin: 5%;
    margin-top: 0;
    margin-bottom: 0;
    width: 90%;
    border: solid #888;
}
table.console td {
    border: solid #ccc;
}
-->
</style>
</head>
'''
def main(status,pid,HTML,desc):
    return f'''{header}<body>
<div class="container">
    <div class="header"><!-- end .header -->
        <h3>EterIll WA Launcher | WebApps通用启动器</h3>
    </div>
    <div class="content">
        <h3 align="center">-= ＥＴＥＲＩＬＬ　ＷＥＢＡＰＰ　ＬＡＵＮＣＨＥＲ =-</h3>
        <div class="controller">
            <h2>控制台</h2>
            <table width=100% border="1" class="console">
                <tr>
                    <td>
                        <p>项目:[{proj}] <a href="./chgproj">【切换项目】</a></p>
                        <p>状态:[{status}]</p>
                        <p>PID:{pid}</p></td>
                    <td align="center">{HTML}</td>
                    <td align="center"><span><a href="/quit" class="red">-=【完全退出】=-</a></span></td>
                </tr>
            </table>
        </div>
        <h2>属性</h2>
        <p>{desc}</p>
        <h2>&nbsp;</h2>
        <!-- end .content --></div>
    <div class="footer">
        <p>&copy;Eternal_Illusion(AKA.EterIll),2024 Do not copy.</p>
        <!-- end .footer --></div>
    <!-- end .container --></div>
</body>
'''
def selectver(app_names):
    return f'''{header}<body>
<div class="container">
    <div class="header"><!-- end .header -->
        <h3>EterIll WA Launcher | WebApps通用启动器</h3>
    </div>
    <div class="content">
        <div class="controller">
            <h2>选择版本</h2>
            <form method="post" align="center">{genselect("target","选择版本: ",**app_names)}<hr /><input name="" type="submit" value="启动" /></form>
            
        </div>
        <!-- end .content --></div>
    <div class="footer">
        <p>&copy;Eternal_Illusion(AKA.EterIll),2024 Do not copy.</p>
        <!-- end .footer --></div>
    <!-- end .container --></div>
</body>
'''
##DEF##
#test if var defined
def ifdef(name):
    varl=globals() if name in globals() else locals()
    return name in varl

#auto get ipv4 addr.
def getip():
    for i in popen("ipconfig","r"):
        s=findall('^\s*IPv4.*',i)
        if len(s)!=0:return findall(':.*\d$',s[0])[0].strip(': ')
#PRIVATE:search available versions
def searchver(path):
    dirs=listdir(path)
    vers=[]
    for i in dirs:
        if ".py" in i:
            try:
                with open(i,"r",encoding="utf-8") as fi:
                    veri=int(findall('#@__core__=\d*\n',fi.read(100))[0].split("=")[-1].replace("\n",""))
            except:continue
            vers+=[[veri,i]]
    printf(f"<PM>SEARCHING VERSIONS\n -Versions found:{len(vers)}\n -SEARCH RESULTS:")
    for i in vers:
        printf(f"  -CODE:{i[0]}|FILENAME:{i[1]}")
    printf("<PM>VERSION SEARCHING FINISHED.")
    for i in range(len(vers)):
        for j in range(len(vers)-1,i,-1):
            if vers[i][0]<vers[j][0]:
                vers[i],vers[j]=vers[j],vers[i]
    return vers
#check pid list for imagename
def pidlist(imagename="python",typ="Console"):
    #available typ: "Services" "Console"
    rpidlist=[]
    for u in popen("tasklist","r"):
        if imagename in u and typ in u:
            rpidlist.append(int(findall(f" \d* {typ}",u)[0].replace(typ,"").strip()))
    return rpidlist
#PRIVATE:start version
def runver(path,nowindow=False):
    pydir=sys.executable
    if nowindow:pydir=pydir.replace("python.exe","pythonw.exe")
    pl=pidlist()
    printf(f'<LAUNCHER>EXECUTE "start {pydir} {path}"')
    system(f"start {pydir} {path}")
    pla=pidlist()
    plr=[]
    for i in pla:
        if not i in pl:plr.append(i)
    return plr
#PRIVATE:handle desc file
def handledesc(splasht=False):
    try:
    #if 1==1:
        with open("desc.json",'r',encoding="utf-8") as desc:
            desc=json.loads(desc.read())
    except:
    #if 1==1:
        printf("[WARN]DESC FILE NOT FOUND!")
        return None
    try:
    #if 1==1:
        with open("env.json",'r',encoding="utf-8") as envj:
            envj=json.loads(envj.read())
    except:
    #if 1==1:
        printf("[INFO]ENVIRONMENT FILE NOT FOUND!")
        envj={"app_host_ip":"","app_host_port":8000}
    info,splash=desc["info"],desc["splash"]
    info["app_ip"]=envj["app_host_ip"] if envj["app_host_ip"] else getip()
    info["app_port"]=envj["app_host_port"]
    info["applink"]=f"<a href='http://{info['app_ip']}:{info['app_port']}/' target='_blank'>-=[打开应用|OPEN APP]=-</a>"
    desct=""
    for i in range(len(splash)):
        for inf in info:
            if inf in splash[i]:
                splash[i]=splash[i].replace("{{"+str(inf)+"}}",str(info[inf]))
        printf(splash[i])
        desct+="<p>"+splash[i]+"</p>"
    if not splasht:return desct,info
    else:return desct
#gen select form
def genselect(ids,label,**k):
    s=""
    for i in k.keys():s+=f'<option value="{k[i]}">{i}</option>'
    return f'<label for="{ids}">{label}</label><select name="{ids}" id="{ids}">{s}</select>'
#gen group select form
def genselectg(ids,label,**k):
    s=""
    for i in k.keys():
        s+=f'<optgroup label="{i}">'
        for j in k[i].keys():s+=f'<option value="{k[i][j]}">{j}</option>'
    return f'<label for="{ids}">{label}</label><select name="{ids}" id="{ids}">{s}</select>'


#test methods



'''
printf("=========================\nType exit for quit,type info for stat.")
while(running):
    pl=pidlist()
    printf(rp,pl)
    running=rp in pl
    if running == False:
        printf(1)#exit()
    cmd=input("CMD>")
    if cmd=="exit":
        for p in rp:
            system(f"taskkill /PID {p} /F")
        printf(2)#exit()
    else:printf("PIDS:",rp)
   '''


app=Flask('Org_NoahStudios_EterIllWAL_flask_Instance')
@app.route('/',methods=["POST","GET"])
def route_slash():
    global rp,running,vers
    if request.method=="GET":
        vers=searchver(app_path)
        verselg={}
        for ii in vers:
            verselg[str(ii[0])]=str(ii[1])
        return main("正在运行" if running else "<span>已停止</span>",rp,'<hr /><a href="/stop" class="red">-=【退出】=-</a><hr />' if running else f'<hr /><form method="post" align="center">{genselect("ver", "版本: ", **verselg)}<br />{genselect("pythonw", "无控制台:", **{"关":"0","开":"1"})}<br /><input name="" type="submit" value="启动" /></form><hr />',descs)
    else:
        versel=request.form.get("ver")
        pythonw=int(request.form.get("pythonw"))
        rp+=runver(f"{app_path}/{versel}",pythonw)
        running=True
        return redirect('/')
    return redirect('/')
@app.route('/stop',methods=["POST","GET"])
def route_stop():
    global rp,running
    for p in rp:
        system(f"taskkill /PID {p} /F")
        rp=[]
        running=False
    return redirect('/')
@app.route('/quit',methods=["POST","GET"])
def route_quit():
    route_stop()
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_func()
    return "<script>self.close();</script>EXITED!"
@app.route('/chgproj',methods=["POST","GET"])
def route_chgproj():
    global proj,vers
    if request.method=="POST":
        sel=request.form.get("target")
        if sel==proj:
            return redirect("/")
        else:
            route_stop()
            vers=searchver(app_dirs[sel])
            proj=sel
            return redirect("/")
    else:
        refappdirs(True)
        vl={}
        for i in app_dirs:vl[i]=i
        return selectver(vl)





###APP###
descs,finfo=handledesc()
sleep(1)
proj=finfo["name"] if finfo["name"] else ""
if not proj:
    if app_dirs:
        printf("[INFO]<LAUNCHER>NO VERSION SUPPORTED.SWITCHING TO ANOTHER PROJECT.")
        for i in app_dirs:
            vers=searchver(app_dirs[i])
            if vers:
                chdir(app_dirs[i])
                app_path=app_dirs[i]
                _,finfo=handledesc()
                proj=finfo["name"]
                break
    else:
        printf("[ERROR]<LAUNCHER>NO VERSION SUPPORTED.EXITING IN 5 secs.")
        sleep(5)
        raise RuntimeError("[ERROR]<LAUNCHER>NO VERSION SUPPORTED.")
#if ver available
vers=searchver(app_path)
max_ver,verdir=0,""
for i in vers:
    if i[0]>max_ver:max_ver,verdir=i[0],i[1]
printf(f"[INFO]<LAUNCHER>Launching Version[CODE:{max_ver}]")
rp=runver(f"{app_path}/{verdir}",false)
printf("[INFO]PIDs:",rp)
running=true
system("start http://localhost:5678/")
printf(
    """
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
    #############################################
    ##        ####          ###    ####  ########
    ##  ##############  ########  #####  ########
    ##        ########  ########  #####  ########
    ##  ##############  ########  #####  ########
    ##        ########  #######    ####        ##
    #############################################
-= ＥＴＥＲＩＬＬ　ＷＥＢＡＰＰ　ＬＡＵＮＣＨＥＲ =-
    ©Eternal_Illusion,2024
STARTING ON PORT 5678.
    """

)
app.run("localhost",port=5678)

