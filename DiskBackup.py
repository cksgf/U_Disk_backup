import os
from shutil import copy as shutilCopy
from time import sleep,strftime,localtime,time
from psutil import disk_partitions
from configparser import ConfigParser
from json import dumps,loads
if not os.path.isfile('config.ini'):
    with open('config.ini','w') as f:
        f.write(r'''[file]
fileSuffix = doc,docx,xls,xlsx,ppt,pptx,wps,txt,text
[path]
backupPath = D:\bakeup''')
config = ConfigParser()
config.readfp(open('config.ini'))
buckFileText = config.get("file","fileSuffix")
buckFileText = list( '.' + i for i in buckFileText.split(','))
backup = config.get("path","backupPath")
backupPath = os.path.join(backup,'Bakeup')
oldBackupPath = os.path.join(backup,'OldBakeup')
fileJson = os.path.join(backup,'file.json')
for i in (backup,backupPath,oldBackupPath):
    if not os.path.isdir(i):
        try:
            os.makedirs(i)
        except:
            pass
if os.path.isfile(fileJson):
    with open(fileJson,'r') as f:
        data = loads(f.read())
else :
    data = {}
    with open(fileJson,'w') as f:
        f.write(dumps(data))
t = []
for k,v in data.items():
    if time() - int(v) >604800:
        try:
            os.remove(k)
        except:
            pass
        t.append(k)
for i in t:
    try:
        del data[i]
    except:
        pass
    
with open(fileJson,'w') as f:
    f.write(dumps(data))
def getRemovableDisk():
    RemovableDisk = []
    for i in disk_partitions():
        if 'removable' in i.opts.lower():
            RemovableDisk.append(i.device)
    if len(RemovableDisk) == 0:
        sleep(5)
    else :
        sleep(1)
    return RemovableDisk
def getWillCopyFileName(filename):
    filePathList = filename.split(os.sep)
    if len(filePathList) == 1:
        return os.path.join(backupPath,filename)
    else:
        return os.path.join(*([backupPath] + filePathList[1:]))
def doCopy(old,new):
    dir_temp = os.path.split(new)[0]
    if not os.path.isdir(dir_temp):
        os.makedirs(dir_temp)
    try:
        shutilCopy(old,new)
    except:
        pass
def main():
    for i in getRemovableDisk():
        for dirpath, dirnames, filenames in os.walk(i):
            for filename in filenames:
                filesplit = os.path.splitext(filename)
                if (filesplit[1].lower() not in buckFileText) or ('~$' in filesplit[1]):
                    continue
                filenamepath = os.path.join(dirpath,filename)
                willCopyFile = getWillCopyFileName(filenamepath)
                if not os.path.isfile(willCopyFile):
                    doCopy(old = filenamepath,new = willCopyFile)
                elif os.stat(filenamepath).st_mtime > os.stat(willCopyFile).st_mtime:
                    path_temp = os.path.split(willCopyFile.replace(backupPath,oldBackupPath))
                    time_temp = strftime("%Y-%m-%d %H_%M_%S_",localtime(os.stat(willCopyFile).st_mtime)) 
                    oldbuckupfilename = os.path.join(path_temp[0],time_temp+path_temp[1])
                    doCopy(willCopyFile,oldbuckupfilename)
                    
                    os.remove(willCopyFile)
                    doCopy(old = filenamepath,new = willCopyFile)
                    data[oldbuckupfilename] = time()
                    with open(fileJson,'w') as f:
                        f.write(dumps(data))
                else :
                    pass
while True:
    main()

