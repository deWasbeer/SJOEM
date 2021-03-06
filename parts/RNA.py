# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:42:44 2015

@author: Johan Antonissen (windhoos@gmail.com)
"""
from . import Input_data,Site_conditions,Elevations,Safety_factors
from math import pi

class stored_data:
    def __init__(self):
        self.RNAloads=[[0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0]]
        self.Deflection=0.0

def Calculate_RNA():
    Drotor=Input_data.stored_data.Drotor
    LC=Site_conditions.stored_data.LCcompilation
    Hhub=Elevations.stored_data.Hhub
    Loadlist=[]    
    
    for i in range(3):
        Loadlist.append([0.0,0.0,0.0,0.0,0.0,0.0])
        fz=Input_data.stored_data.Mrna*9.81
        if i==0:
            fx=thrustforce(LC[0][0],Drotor)*1.5  #Additional safety factor for thrust of 1,5 used as stated by Zaaijer.
        else:
            fx=dragforce(LC[i][0],Drotor,Hhub)
        #Calculate some possible induced moment in hub assumed as moment equal to load on one blade times half its length
        my=fx/3.0*Drotor/2.0
        
        Loadlist[i][0]=int(fx*Safety_factors.stored_data.ScombENV)
        Loadlist[i][2]=int(fz*Safety_factors.stored_data.ScombGRAV)
        Loadlist[i][4]=int(my*Safety_factors.stored_data.ScombENV)
        
    stored_data.RNAloads=Loadlist
    
    #Calculate max blade deflection
    #Estimated deflection is 1/500*R**2, approximated from calculated blade curvature
    #Taken from introduction to wind exersize
    D_max=1/500.0*(Drotor/2.0)**2
    stored_data.Deflection=D_max
    
    print('RNA loads calculated for all loadcases: ')
    print("Each loadcase's loads are: [fx (N),fy (N),fz (N),mx (Nm),my (Nm),mz (Nm)]")
    for i in range(len(stored_data.RNAloads)):
        print(stored_data.RNAloads[i])
    print()
    print('Maximum blade deflection:',D_max,'m')
    print()
    
    text=open('Data-RNA.txt','w')
    text.truncate()
    text.write('RNA loads calculated for all loadcases: '+'\n')
    text.write("Each loadcase's loads are: [fx (N),fy (N),fz (N),mx (Nm),my (Nm),mz (Nm)]"+'\n')
    for i in range(len(stored_data.RNAloads)):
        text.write(str(stored_data.RNAloads[i])+'\n')
    text.write('\n'+'stored data'+'\n')
    text.write('RNA loads'+'\n'+str(stored_data.RNAloads)+'\n')
    text.write('Maximum blade deflection: '+str(D_max)+'m')
    text.close()
    
def thrustforce(windspeed,Drotor):
    rho_air=1.225
    a= 1.0/3.0
    Ct=4.0*a*(1.0-a)
    return 0.5*Ct*rho_air*windspeed**2*pi/4.0*Drotor**2
    
def dragforce(REFwindspeed,Drotor,Hhub):
    Uhub=Site_conditions.get_wind_speed_at_height(REFwindspeed,Hhub)
    Cd=1.2
    rho_air=1.225
    Bblade=Drotor*0.025
    return 0.5*Cd*rho_air*Uhub**2.0*3.0*Drotor/2.0*Bblade