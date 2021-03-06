# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:46:24 2015

@author: Johan Antonissen (windhoos@gmail.com)
"""

from . import Input_data, Site_conditions

class stored_data:
    def __init__(self):
        #Elevations with respect to SWL
        self.Hhub=0.0
        self.Hinterface=0.0
        self.Hcrest=0.0
        self.Hswl=0.0
        self.Hmudline=0.0

def Determine_elevations():
    Drotor=Input_data.stored_data.Drotor
    Hdepth=Input_data.stored_data.Hdepth
    Hcrest=Site_conditions.stored_data.max_crest
    Hinterface=Hcrest+1.5
    Hhub=Hinterface+Drotor/2.0+5.0
    
    stored_data.Hhub=Hhub
    stored_data.Hinterface=Hinterface
    stored_data.Hcrest=Hcrest
    stored_data.Hmudline=-abs(Hdepth)
    
    print('Following elevations where determined with respect to SWL: ')
    print('Hub:        ',stored_data.Hhub,'m')
    print('Hinterface: ',stored_data.Hinterface,'m')
    print('Hcrest:     ',stored_data.Hcrest,'m')
    print('Hswl:       ', 0.0,'m')
    print('Hmudline:   ',stored_data.Hmudline,'m')
    print()
    
    text=open('Data-Elevations.txt','w')
    text.truncate()
    text.write('Following elevations where determined with respect to SWL: '+'\n')
    text.write('Hub:        '),text.write(str(stored_data.Hhub)),text.write('m'+'\n')
    text.write('Hinterface: '),text.write(str(stored_data.Hinterface)),text.write('m'+'\n')
    text.write('Hcrest:     '),text.write(str(stored_data.Hcrest)),text.write('m'+'\n')
    text.write('Hswl:       '),text.write(str(0.0)),text.write('m'+'\n')
    text.write('Hmudline:   '),text.write(str(stored_data.Hmudline)),text.write('m'+'\n')
    text.write('\n')
    text.close()