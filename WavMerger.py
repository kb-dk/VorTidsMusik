#!/usr/bin/env python

import shutil
import subprocess
import os
import sys

prevDir = ''
counter = 0
for root, dir, files in os.walk('/home/dth/vortidsmusik'):
    if "Vor_Tids_Musik" in os.path.basename(root):
        if prevDir != os.path.basename(root):
            counter += 1
            prevDir = os.path.basename(root)
            files.sort()
            print prevDir + '----------------------------------'
            fileCounter = 0
            fileName1 = ''
            for file in files:
                if os.path.splitext(file)[1] == '.wav' and not 'tmp' in file:
                    fileCounter += 1
                    print 'Merging '+file
                    if (fileCounter == 1):
                        fileName1 = file
                        try:
                            os.mkdir('/home/dth/VorTidsMusik/'+prevDir)
                        except OSError:
                            print "Dir already exists"
                    elif(fileCounter == 2):
                        p = subprocess.Popen('sox '+'/home/dth/vortidsmusik/'+prevDir+'/'+fileName1+' '+'/home/dth/vortidsmusik/'+prevDir+'/'+file+' /home/dth/VorTidsMusik/'+prevDir+'/'+prevDir+'.wav', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
                        retval = p.wait()
                    else:
                        shutil.copy2('/home/dth/VorTidsMusik/'+prevDir+'/'+prevDir+'.wav','/home/dth/VorTidsMusik/'+prevDir+'/'+prevDir+'tmp.wav')
                        p = subprocess.Popen('sox '+'/home/dth/VorTidsMusik/'+prevDir+'/'+prevDir+'tmp.wav '+'/home/dth/vortidsmusik/'+prevDir+'/'+file+' /home/dth/VorTidsMusik/'+prevDir+'/'+prevDir+'.wav', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
                        retval = p.wait()
                        os.remove('/home/dth/VorTidsMusik/'+prevDir+'/'+prevDir+'tmp.wav')
            if (fileCounter == 1):
                        try:
                            os.mkdir('/home/dth/VorTidsMusik/'+prevDir)
                        except OSError:
                            print "Dir already exists"
                        shutil.copy2('/home/dth/vortidsmusik/'+prevDir+'/'+fileName1,'/home/dth/VorTidsMusik/'+prevDir+'/'+prevDir+'.wav')
