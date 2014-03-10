#!/usr/bin/env python

import xml.etree.ElementTree as ET
import os
import wave
import contextlib
import sys
from datetime import datetime
from datetime import timedelta

def channel_mapping(channel):
    if 'Program 1' in channel:
        return 'DR P1','P1_logo.png'
    elif 'Program 2' in channel:
        return 'DR P2','P2_logo.png'
    elif 'Program 3' in channel:
        return 'DR P3','P3_logo.png'

counter = 0

for root, dir, files in os.walk('/home/mbn/IDEA-Projects/VorTidsMusik/output/'):
    for file in files:
        counter += 1
        linestring = open('/home/mbn/IDEA-Projects/VorTidsMusik/Chaostemplate.xml', 'r').read()
        tree = ET.ElementTree(file='/home/mbn/IDEA-Projects/VorTidsMusik/output/'+file)
        parent_map = dict((c, p) for p in tree.getiterator() for c in p)
        root = tree.getroot()
        
        fname=(file.replace('.xml','')).upper()
        print fname
        with contextlib.closing(wave.open('/home/mbn/VorTidsMusik/Vor_Tids_Musik-'+fname+'/Vor_Tids_Musik-'+fname+'.wav','r')) as f:
            frames=f.getnframes()
            rate=f.getframerate()
            duration=frames/float(rate)

        for record in root:
            for node in record.iterfind('./pbcoreDateAvaliable/dateAvaliableStart'):
                try:
                    startTime = datetime.strptime(node.text+'T00:00:00', '%Y-%m-%dT%H:%M:%S')
                except ValueError:
                    startTime = datetime.strptime((node.text).replace('00-00','01-01')+'T00:00:00', '%Y-%m-%dT%H:%M:%S')
                linestring = linestring.replace('###START_TIME###', datetime.strftime(startTime,'%Y-%m-%dT%H:%M:%S'))
                linestring = linestring.replace('###END_TIME###', datetime.strftime(startTime+timedelta(seconds=duration),'%Y-%m-%dT%H:%M:%S'))
            for node in record.iterfind('./publisher'):
                if node.text == 'Danmarks Radio':
                        channel = ''
                        logofilename = ''
                else:
                    channel, logofilename = channel_mapping((node.text).replace('Danmarks Radio - ',''))
                linestring = linestring.replace('###CHANNEL###', channel)
                linestring = linestring.replace('###LOGO_FILENAME###',logofilename)
            linestring = linestring.replace('###TITLE###','Vor Tids Musik')
            for node in record.iterfind('./descriptionType'):
                if node.text == 'kortomtale':
                    for child in parent_map[node]:
                        linestring = linestring.replace('###ABSTRACT###', child.text)
                elif node.text == 'langomtale1':
                    for child in parent_map[node]:
                        try:
                            linestring = linestring.replace('###DESCRIPTION1### ###DESCRIPTION2###',child.text)
                        except TypeError:
                            linestring = linestring.replace('###DESCRIPTION1### ###DESCRIPTION2###','')
            linestring = linestring.replace('###PUBLISHER###', 'Danmarks Radio')
# INDSAET CONTRIBUTORS HER::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            for node in record.iterfind('./identifier'):
                linestring = linestring.replace('###PROGRAM_ID###', node.text)
                linestring = linestring.replace('###FILENAME###', 'Vor_Tids_Musik-'+node.text+'.wav')
                id = (node.text).upper()
        with open("/home/mbn/VorTidsMusik/Vor_Tids_Musik-"+id+'/'+id+'-CHAOS.xml', "w") as chaos:
            chaos.write((linestring).encode('UTF-8'))            
