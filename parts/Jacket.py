# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 10:36:49 2015

@author: Johan Antonissen (windhoos@gmail.com)
"""

from . import Site_conditions, Input_data, Elevations, Safety_factors, Tower
from math import pi,sqrt,sin,cos,tan,degrees,radians,atan,tanh,sinh,cosh
import numpy as np
from scipy.optimize import brentq,basinhopping

class stored_data:
    def __init__(self):
        self.wireframe=0.0
        self.Jacket_dimensions=0.0
        self.Sleeve_dimensions=0.0
        self.loads=0.0
        self.membersort=0.0
        self.environmental_loads_per_bay=0.0
        self.gravitational_loads_per_bay=0.0
        self.weight=0.0
        self.memberload=0.0
        self.reactivelist=0.0
        
class Wireframe_builder:
    def __init__(self,Dtower,Hinterface,Hdepth):
        self.Dtower=Dtower
        self.Hinterface=Hinterface
        self.Hdepth=Hdepth
        self.Hjacket=abs(Hdepth)+abs(Hinterface)
        self.batter=0.08 #predescribed batter old batter was 0.06 from rule of thumb
        self.Dspace=3.0
        
    def printlist(self,Wireframe):
        print()
        print('Wireframe[i]=     Datalist per bay')
        print('Wireframe[i][0]=  number of bays in foundation structure')
        print('Wireframe[i][1]=  height of respective bay i')
        print('Wireframe[i][2]=  angle of the respective bay brace')
        print('Wireframe[i][3]=  top width of the respective bay')
        print('Wireframe[i][4]=  bottom width of the respective bay')
        print('Wireframe[i][5]=  length diagonal brace')
        print('Wireframe[i][6]=  height of bottom bay element from mudline')
        print('Wireframe[i][7]=  Left top leg angle')
        print('Wireframe[i][8]=  Left top brace angle')
        print('Wireframe[i][9]=  Right top leg angle')
        print('Wireframe[i][10]= Right top brace angle')
        print('Wireframe[i][11]= Left bottom leg angle')
        print('Wireframe[i][12]= Left bottom brace angle')
        print('Wireframe[i][13]= Right bottom leg angle')
        print('Wireframe[i][14]= Right bottom brace angle')
        print('Wireframe[i][15]= Bay batter')
        
        for bay in range(len(Wireframe)):
            print('bay',bay+1,Wireframe[bay])
            
        text=open('Data-Jacket.txt','a')
        text.write('\n'+'Wireframe[i]=     Datalist per bay'+'\n')
        text.write('Wireframe[i][0]=  number of bays in foundation structure'+'\n')
        text.write('Wireframe[i][1]=  height of respective bay i'+'\n')
        text.write('Wireframe[i][2]=  angle of the respective bay brace'+'\n')
        text.write('Wireframe[i][3]=  top width of the respective bay'+'\n')
        text.write('Wireframe[i][4]=  bottom width of the respective bay'+'\n')
        text.write('Wireframe[i][5]=  length diagonal brace'+'\n')
        text.write('Wireframe[i][6]=  height of bottom bay element from mudline'+'\n')
        text.write('Wireframe[i][7]=  Left top leg angle'+'\n')
        text.write('Wireframe[i][8]=  Left top brace angle'+'\n')
        text.write('Wireframe[i][9]=  Right top leg angle'+'\n')
        text.write('Wireframe[i][10]= Right top brace angle'+'\n')
        text.write('Wireframe[i][11]= Left bottom leg angle'+'\n')
        text.write('Wireframe[i][12]= Left bottom brace angle'+'\n')
        text.write('Wireframe[i][13]= Right bottom leg angle'+'\n')
        text.write('Wireframe[i][14]= Right bottom brace angle'+'\n')
        text.write('Wireframe[i][15]= Bay batter'+'\n')
        
        for bay in range(len(Wireframe)):
            text.write('bay '+str(bay+1)+' '+str(Wireframe[bay])+'\n')
        text.close()
        
    def bracelength(self,Ltop,Lbottom,angle):
        Lhoriz=Ltop+abs(Ltop-Lbottom)/2
        Ldiag=Lhoriz*cos(angle*pi/180)
        return Ldiag
        
    def build(self):
        Ltop=2*self.Dspace+self.Dtower
        Lbottom=Ltop+2.0*self.batter*self.Hjacket
        maxbay=20
        datalist=[]
        difflist=[]
        for i in range(maxbay):
            datalist.append([])
            
        for i in range(maxbay):
            #Calculate different bay configurations
            bay=i+1
            Hbay=1.0*self.Hjacket/bay
            for j in range(bay):
                #Calculate dimensions of each bay
                Lbottom=Ltop+2*self.batter*Hbay
                Ltriangle=Lbottom-self.batter*Hbay
                angle=atan(Hbay/Ltriangle)*180/pi
                datalist[i].append([bay,Hbay,angle,Ltop,Lbottom])
                Ltop=Lbottom
      
        for i in range(maxbay):
            #now we compare which configuration has the top brace angle closest to 45 degrees
            bay=i+1
            mean=35.0*bay
            offset=0
            for j in range(bay):
                offset=offset+datalist[i][0][2] #here the zero looks only at the top brace angle
            difflist.append(mean-offset)
        difference=min(difflist,key=abs)
        for i in range(len(difflist)):
            difflist[i]=difflist[i]/difference

        configNR=difflist.index(1)
        wireframe=datalist[configNR]
        
        for i in range(wireframe[0][0]):
            wireframe[i].append(self.bracelength(wireframe[i][3],wireframe[i][4],wireframe[i][2]))
            wireframe[i].append((wireframe[i][0]-(i+1))*wireframe[i][1])
            
        #Finally we calculate member angles for future calculations
        for bay in range(wireframe[0][0]):
            batterangle=atan(2*wireframe[bay][1]/(wireframe[bay][4]-wireframe[bay][3]))
            #First for the top of the bay
            #       We have the following case                              + (vertical positive direction)
            #       ------------                    /  rotation positive    /\
            #      /\ A      B /\                  / ) +  direction         |
            #     / \brace    / \ leg             ------- angle = 0 RAD     |------> + (horizontal positive direction)
            # We calculate all the angles with respect to the nearest horizontal member with positive direction against the clock.
            philegA=pi+batterangle
            phibraceA=2*pi-radians(wireframe[bay][2])
            philegB=2*pi-batterangle
            phibraceB=pi+radians(wireframe[bay][2])
            wireframe[bay].append(degrees(philegA))
            wireframe[bay].append(degrees(phibraceA))
            wireframe[bay].append(degrees(philegB))
            wireframe[bay].append(degrees(phibraceB))
            
            #First we take a look at everything above the new horizontal bracelime of bottom of the bay
            #     | /               \ |
            #     |/ C            D \ |
            #     - - - - - - - - - - - (Horizontal raferece line (is no actual brace))
            philegC=batterangle
            phibraceC=radians(wireframe[bay][2])
            philegD=pi-batterangle
            phibraceD=pi-radians(wireframe[bay][2])
            wireframe[bay].append(degrees(philegC))
            wireframe[bay].append(degrees(phibraceC))
            wireframe[bay].append(degrees(philegD))
            wireframe[bay].append(degrees(phibraceD))
            wireframe[bay].append(self.batter)
            
        return wireframe
        
class Dimension_builder:
    def __init__(self,wireframe):
        self.wireframe=wireframe
        
    def printlist(self,Guessed_dimensions):
        print()
        print('Guessed_dimensions[i]=    Datalist per bay containing initial guesses of dimensions')
        print('Guessed_dimensions[i][0]= Dleg')
        print('Guessed_dimensions[i][1]= Dbrace')
        print('Guessed_dimensions[i][2]= wtleg')
        print('Guessed_dimensions[i][3]= wtbrace')
        for bay in range(len(Guessed_dimensions)):
            print('bay',bay+1,Guessed_dimensions[bay])
        
        text=open('Data-Jacket.txt','a')
        text.write('\n'+'Guessed_dimensions[i]=    Datalist per bay containing initial guesses of dimensions'+'\n')
        text.write('Guessed_dimensions[i][0]= Dleg'+'\n')
        text.write('Guessed_dimensions[i][1]= Dbrace'+'\n')
        text.write('Guessed_dimensions[i][2]= wtleg'+'\n')
        text.write('Guessed_dimensions[i][3]= wtbrace'+'\n')
        for bay in range(len(Guessed_dimensions)):
            text.write('bay '+str(bay+1)+' '+str(Guessed_dimensions[bay])+'\n')
        text.close()
        
    def guess(self):
        Guessed_dimension_list=[]
        for baynumber in range(len(self.wireframe)):
            Dleg=1.0
            Dbrace=Dleg*0.6
            
            wtleg=Dleg/60
            wtbrace=Dbrace/40
            Guessed_dimension_list.append([Dleg,Dbrace,wtleg,wtbrace])

        return Guessed_dimension_list
        
class Equivalent_diameter_builder:
    def __init__(self,Wireframe):
        self.Wireframe=Wireframe
        
    def printlist(self,Equivalent_diameter):
        print()
        print('Equivalent diameter[i]=          Datalist per bay')
        print('Equivalent diameter[i][0]=       Equivalent drag for 0 degree inflow')
        print('Equivalent diameter[i][1]=       Equivalent drag for 45 degree inflow')
        print('Equivalent diameter[i][2]=       Equivalent inertia for 0 degree inflow')
        print('Equivalent diameter[i][3]=       Equivalent inertia for 45 degree inflow')
        for bay in range(len(Equivalent_diameter)):
            print('bay',bay+1,Equivalent_diameter[bay])
            
        text=open('Data-Jacket.txt','a')
        text.write('\n'+'Equivalent diameter[i]=          Datalist per bay'+'\n')
        text.write('Equivalent diameter[i][0]=       Equivalent drag for 0 degree inflow'+'\n')
        text.write('Equivalent diameter[i][1]=       Equivalent drag for 45 degree inflow'+'\n')
        text.write('Equivalent diameter[i][2]=       Equivalent inertia for 0 degree inflow'+'\n')
        text.write('Equivalent diameter[i][3]=       Equivalent inertia for 45 degree inflow'+'\n')
        for bay in range(len(Equivalent_diameter)):
            text.write('bay '+str(bay+1)+' '+str(Equivalent_diameter[bay])+'\n')
        text.close()
        
    def builder(self,Dimensions):
        equivalent_diameter=[]
        
        for baynumber in range(len(Dimensions)):
            Ddrag0,Ddrag45,Dinertia0,Dinertia45=self.baycalculator(baynumber,Dimensions)
            equivalent_diameter.append([Ddrag0,Ddrag45,Dinertia0,Dinertia45])
            
        return equivalent_diameter
            
    def baycalculator(self,baynumber,Dimensions):
        #Calculated drag and inertia equivalent for a single bay
        #Baynumber counts from 0 as top
        #input: D,L,angle,wavedirection,configuration,allignment
        Ddrag0=0.0
        Ddrag45=0.0
        Dinertia0=0.0
        Dinertia45=0.0
        for i in range(4):
            #Calculate equivalent diameter of vertical bay piles (4) for 0 and 45 degrees
            Ddrag0=Ddrag0+self.equivalentDRAG(Dimensions[baynumber][0],0,0,0,'vertical',0)
            Ddrag45=Ddrag45+self.equivalentDRAG(Dimensions[baynumber][0],0,0,45,'vertical',0)
            Dinertia0=Dinertia0+(self.equivalentINERTIA(Dimensions[baynumber][0],0,0,0,'vertical',0))**2
            Dinertia45=Dinertia45+(self.equivalentINERTIA(Dimensions[baynumber][0],0,0,45,'vertical',0))**2
            #Caculate equivalent diameter for (diagonal) braces (4) for 0 degrees and perpendicular to waves
        for i in range(4):
            Ddrag0=Ddrag0+self.equivalentDRAG(Dimensions[baynumber][1],self.Wireframe[baynumber][5],self.Wireframe[baynumber][2],0,'diagonal','perpendicular')
            Dinertia0=Dinertia0+(self.equivalentINERTIA(Dimensions[baynumber][1],self.Wireframe[baynumber][5],self.Wireframe[baynumber][2],0,'diagonal','perpendicular'))**2
            #Calculate equivalent diameter for (diagonal) braces (4) for 0 degrees and parallel to waves
        for i in range(4):
            Ddrag0=Ddrag0+self.equivalentDRAG(Dimensions[baynumber][1],self.Wireframe[baynumber][5],self.Wireframe[baynumber][2],0,'diagonal','parallel')
            Dinertia0=Dinertia0+(self.equivalentINERTIA(Dimensions[baynumber][1],self.Wireframe[baynumber][5],self.Wireframe[baynumber][2],0,'diagonal','parallel'))**2
            #Caculate equivalent diameter for (diagonal) braces (8) for 45 degrees
        for i in range(8):
            Ddrag45=Ddrag45+self.equivalentDRAG(Dimensions[baynumber][1],self.Wireframe[baynumber][5],self.Wireframe[baynumber][2],45,'diagonal',0)
            Dinertia45=Dinertia45+(self.equivalentINERTIA(Dimensions[baynumber][1],self.Wireframe[baynumber][5],self.Wireframe[baynumber][2],45,'diagonal',0))**2
            #print '8 Diagonal braces 45:',Dinertia45
        Dinertia0=sqrt(Dinertia0)        
        Dinertia45=sqrt(Dinertia45)   
        
        return Ddrag0,Ddrag45,Dinertia0,Dinertia45
            
    def equivalentDRAG(self,D,L,angle,wavedirection,configuration,allignment):
        phi=radians(angle)
        if wavedirection == 0:
            if configuration == 'vertical':
                return D
            elif configuration == 'horizontal':
                if allignment == 'parallel':
                    return 0.0
                elif allignment == 'perpendicular':
                    return L
            elif configuration == 'diagonal':
                if allignment == 'parallel':
                    return D
                elif allignment == 'perpendicular':
                    return D/sin(phi)
        elif wavedirection == 45:
            if configuration == 'vertical':
                return D
            elif configuration == 'horizontal':
                return 1.22*0.5*L
            elif configuration == 'diagonal':
                return 1.22*(0.5*D+D/sin(phi))
        
    def equivalentINERTIA(self,D,L,angle,wavedirection,configuration,allignment):
        phi=radians(angle)
        if wavedirection == 0:
            if configuration == 'vertical':
                return D
            elif configuration == 'horizontal':
                if allignment == 'parallel':
                    return 0.0
                elif allignment == 'perpendicular':
                    return sqrt(D*L)
            elif configuration == 'diagonal':
                if allignment == 'parallel':
                    return D
                elif allignment == 'perpendicular':
                    return D/sqrt(sin(phi))
        elif wavedirection == 45:
            if configuration == 'vertical':
                return D
            elif configuration == 'horizontal':
                return 1.11*0.5*sqrt(D*L)
            elif configuration == 'diagonal':
                return 1.11*(0.5*D+0.5*D/(sqrt(sin(phi))))
                
class Bay_load_calculator:
    def __init__(self,Wireframe,LCenv,LCtower,Hmudline,Hinterface,Hmaxwet,Hdepth,Surge,HAT,rho_water):
        self.Wireframe=Wireframe
        self.LCenv=LCenv
        self.LCtower=LCtower
        self.Hmudline=Hmudline
        self.Hinterface=Hinterface
        self.Hmaxwet=Hmaxwet
        self.Hdepth=Hdepth
        self.Surge=Surge
        self.HAT=HAT
        self.rho_water = rho_water
        self.rho_steel=7850
        self.cm = 2.0
        self.cd = 1.0
        self.g = 9.81
        
    def printlistENVPERBAY(self,Environmental_load_per_bay):
        print()
        print('Environmental load per bay[i]             = Datalist per bay')
        print('Environmental load per bay[i][j]          = Datalist per bay per inflow angle')
        print('Environmental load per bay[i][j][k]       = Datalist per bay per inflow angle per load case')
        print('Environmental load per bay[i][j][k][0]    = Drag force induced on bay')
        print('Environmental load per bay[i][j][k][1]    = Inertia force induced on bay')
        print('Environmental load per bay[i][j][k][2]    = Drag moment induced on bay')
        print('Environmental load per bay[i][j][k][3]    = Inertia moment induced on bay')
        for bay in range(len(Environmental_load_per_bay)):
            for angle in range(len(Environmental_load_per_bay[bay])):
                for loadcase in range(len(Environmental_load_per_bay[bay][angle])):
                    if angle ==0:
                        angleplot='0 '
                    else:
                        angleplot='45'
                    print('bay',bay+1,'angle',angleplot,'LC',loadcase+1,Environmental_load_per_bay[bay][angle][loadcase])
                    
        text=open('Data-Jacket.txt','a')
        text.write('\n'+'Environmental load per bay[i]             = Datalist per bay'+'\n')
        text.write('Environmental load per bay[i][j]          = Datalist per bay per inflow angle'+'\n')
        text.write('Environmental load per bay[i][j][k]       = Datalist per bay per inflow angle per load case'+'\n')
        text.write('Environmental load per bay[i][j][k][0]    = Drag force induced on bay'+'\n')
        text.write('Environmental load per bay[i][j][k][1]    = Inertia force induced on bay'+'\n')
        text.write('Environmental load per bay[i][j][k][2]    = Drag moment induced on bay'+'\n')
        text.write('Environmental load per bay[i][j][k][3]    = Inertia moment induced on bay'+'\n')
        for bay in range(len(Environmental_load_per_bay)):
            for angle in range(len(Environmental_load_per_bay[bay])):
                for loadcase in range(len(Environmental_load_per_bay[bay][angle])):
                    if angle ==0:
                        angleplot='0 '
                    else:
                        angleplot='45'
                    text.write('bay '+str(bay+1)+' angle '+str(angleplot)+' LC '+str(loadcase+1)+' '+str(Environmental_load_per_bay[bay][angle][loadcase])+'\n')
        text.close()
            
    def printlistGRAVPERBAY(self,Gravitational_load_per_bay):
        print()
        print('Gravitational load per bay[i] = Load of bay')
        for bay in range(len(Gravitational_load_per_bay)):
            print('bay',bay+1,Gravitational_load_per_bay[bay])
            
        text=open('Data-Jacket.txt','a')
        text.write('\n'+'Gravitational load per bay[i] = Load of bay'+'\n')
        for bay in range(len(Gravitational_load_per_bay)):
            text.write('bay '+str(bay+1)+' '+str(Gravitational_load_per_bay[bay])+'\n')
        text.close()
            
    def printlistTOTAL(self,Loads_summed):
        print()
        print('Loads summed per bay[i]             = Datalist per bay')
        print('Loads summed per bay[i][j]          = Datalist per bay per inflow angle')
        print('Loads summed per bay[i][j][k]       = Datalist per bay per inflow angle per load case')
        print('Loads summed per bay[i][j][k][l]    = Datalist per bay per inflow angle per load case for top [0] and bottom [1]')
        print('Loads summed per bay[i][j][k][l]      This datalist has arrangement of [fx,fy,fz,mx,my,mz]')
        for bay in range(len(Loads_summed)):
            for angle in range(len(Loads_summed[bay])):
                for loadcase in range(len(Loads_summed[bay][angle])):
                    if angle ==0:
                        angleplot='0 '
                    else:
                        angleplot='45'
                    for location in range(len(Loads_summed[bay][angle][loadcase])):
                        if location ==0:
                            locationplot='top   '
                        else:
                            locationplot='bottom'
                        print('bay',bay+1,'angle',angleplot,'LC',loadcase+1,'location',locationplot,Loads_summed[bay][angle][loadcase][location])
                        
        text=open('Data-Jacket.txt','a')
        text.write('\n'+'Loads summed per bay[i]             = Datalist per bay'+'\n')
        text.write('Loads summed per bay[i][j]          = Datalist per bay per inflow angle'+'\n')
        text.write('Loads summed per bay[i][j][k]       = Datalist per bay per inflow angle per load case'+'\n')
        text.write('Loads summed per bay[i][j][k][l]    = Datalist per bay per inflow angle per load case for top [0] and bottom [1]'+'\n')
        text.write('Loads summed per bay[i][j][k][l]      This datalist has arrangement of [fx,fy,fz,mx,my,mz]'+'\n')
        for bay in range(len(Loads_summed)):
            for angle in range(len(Loads_summed[bay])):
                for loadcase in range(len(Loads_summed[bay][angle])):
                    if angle ==0:
                        angleplot='0 '
                    else:
                        angleplot='45'
                    for location in range(len(Loads_summed[bay][angle][loadcase])):
                        if location ==0:
                            locationplot='top   '
                        else:
                            locationplot='bottom'
                        text.write('bay '+str(bay+1)+' angle '+str(angleplot)+' LC '+str(loadcase+1)+' location '+str(locationplot)+' '+str(Loads_summed[bay][angle][loadcase][location])+'\n')
        text.close()
        
    def calculate_environmental_load_per_bay(self,Equivalent_dimensions):
        loadlist=[]
        for bay in range(len(Equivalent_dimensions)):
            loadlist.append([])
            bottom_of_bay=self.Hmudline+self.Wireframe[bay][6]
            top_of_bay=self.Hmudline+self.Wireframe[bay][6]+self.Wireframe[bay][1]
            for angle in range(2):
                loadlist[bay].append([])
                if angle == 0: #0 degree inflow
                    Ddrag=Equivalent_dimensions[bay][0]
                    Dinertia=Equivalent_dimensions[bay][2]
                if angle == 1: #45 degree inflow
                    Ddrag=Equivalent_dimensions[bay][1]
                    Dinertia=Equivalent_dimensions[bay][3]
                    
                for loadcase in range(len(self.LCenv)):
                    loadlist[bay][angle].append([])
                    waveheight=self.LCenv[loadcase][1]
                    wavenumber=self.LCenv[loadcase][2]
                    
                    Fdrag=self.get_integrated_drag_force(waveheight,wavenumber,bottom_of_bay,top_of_bay,Ddrag)*Safety_factors.stored_data.ScombENV
                    Finertia=self.get_integrated_inertia_force(waveheight,wavenumber,bottom_of_bay,top_of_bay,Dinertia)*Safety_factors.stored_data.ScombENV
                    Mdrag=self.get_integrated_drag_moment(waveheight,wavenumber,bottom_of_bay,top_of_bay,Ddrag,Fdrag) 
                    Minertia=self.get_integrated_inertia_moment(waveheight,wavenumber,bottom_of_bay,top_of_bay,Dinertia,Finertia)
                
                    loadlist[bay][angle][loadcase].append(int(Fdrag))
                    loadlist[bay][angle][loadcase].append(int(Finertia))
                    loadlist[bay][angle][loadcase].append(int(Mdrag))
                    loadlist[bay][angle][loadcase].append(int(Minertia))
                
        return loadlist
                
    def get_integrated_inertia_force(self, wave_height, wave_number, base, top, diameter):
        zeta = wave_height / 2.0
        k = wave_number
        a = base-self.HAT-self.Surge #Distance element bottom from MSL we move down from MSL so this value is negative
        b = top-self.HAT-self.Surge #Distance element top from MSL we move down from MSL so this value is negative
        d = self.Hdepth+self.HAT+self.Surge  #water depth of site this is the location of MSL
        
        if base >= 0:
            return 0
        elif top >= 0:
            b=0      
        return self.cm * (self.rho_water * pi * diameter**2 / 4.0) * zeta * self.g * ( tanh(k * d) / sinh(k * d)) * (sinh(k * (b + d))-sinh(k * (a + d)))        
        
    def get_integrated_drag_force(self, wave_height, wave_number, base, top, diameter):
        zeta = wave_height / 2.0
        k = wave_number
        a = base-self.HAT-self.Surge
        b = top-self.HAT-self.Surge
        d = self.Hdepth+self.HAT+self.Surge
        
        if base >= 0:
            return 0
        elif top >= 0:
            b=0
        return (self.cd * 0.5 * self.rho_water * diameter * zeta**2 * self.g * ( 2.0 / sinh(2.0 * k * d)) *
                 ((sinh(2.0 * k * (b + d)) / 4.0 + k * (b + d) / 2.0) - (sinh(2.0 * k * (a + d)) / 4.0 + k * (a + d) / 2.0))) 

    def get_integrated_inertia_moment(self, wave_height, wave_number, base, top, diameter,Finertia):
        zeta = wave_height / 2.0
        k = wave_number
        a = base-self.HAT-self.Surge
        b = top-self.HAT-self.Surge
        d = self.Hdepth+self.HAT+self.Surge

        if base >= 0:
            return 0
        elif top >= 0:
            b=0
        
        return -a*Finertia+(self.cm * (self.rho_water * pi * diameter**2 / 4.0) * zeta * self.g * ( tanh(k * d) / sinh(k * d)) *((b * sinh(k * (b + d)) - cosh(k * (b + d))/k) - (a * sinh(k * (a + d)) - cosh(k * (a + d))/k)))
    
    def get_integrated_drag_moment(self, wave_height, wave_number, base, top, diameter,Fdrag):
        zeta = wave_height / 2.0
        k = wave_number
        a = base-self.HAT-self.Surge
        b = top-self.HAT-self.Surge
        d = self.Hdepth+self.HAT+self.Surge

        if base >= 0:
            return 0
        elif top >= 0:
            b=0     

        return -a*Fdrag+(self.cd * 0.5 * self.rho_water * diameter * zeta**2 * self.g * ( 2.0 / sinh(2 * k * d)) *((b * (sinh(2.0 * k * (b + d))/ 4.0 + k * (b + d) / 2.0) - (cosh(2.0 * k * (b + d)) / (8.0 * k) + (k * (b + d))**2 / (4.0 * k))) -(a * (sinh(2.0 * k * (a + d))/ 4.0 + k * (a + d) / 2.0) - (cosh(2.0 * k * (a + d)) / (8.0 * k) + (k * (a + d))**2 / (4.0 * k)))))
        
    def calculate_gravitational_load_per_bay(self,Dimensions):
        loadlist=[]
        for bay in range(len(Dimensions)):
            Dleg=Dimensions[bay][0]
            Dbrace=Dimensions[bay][1]
            wtleg=Dimensions[bay][2]
            wtbrace=Dimensions[bay][3]
            Lleg=sqrt(self.Wireframe[bay][1]**2+(0.5*(self.Wireframe[bay][4]-self.Wireframe[bay][3]))**2)
            Lbrace=self.Wireframe[bay][5]
            
            Fleg=self.area(Dleg,wtleg)*Lleg*self.rho_steel*self.g
            Fbrace=self.area(Dbrace,wtbrace)*Lbrace*self.rho_steel*self.g
            
            F_g_of_bay = (4*Fleg + 8*Fbrace)*Safety_factors.stored_data.ScombGRAV
            loadlist.append(int(F_g_of_bay))

        return loadlist
    
    def area(self,D,wt):
        return pi/4.0*(D**2-(D-2*wt)**2)
        
    def calculate_load_summed(self,Environmental_load,Gravitational_load):
        #axial load ath the bottom of the bay. This could be due to the fact that there is actually a very small water speed at the mudline
        #and thus no extra load is gerenrated appart from the top node. Couldnt find an error however. possibly error is in faulty copied code from team play
        loadlist=[]
        for bay in range(len(Environmental_load)):
            loadlist.append([])
            for angle in range(2):
                loadlist[bay].append([])
                for loadcase in range(len(self.LCtower)):
                    loadlist[bay][angle].append([[],[]])
                        
                    Fxbay=sqrt(Environmental_load[bay][angle][loadcase][0]**2+Environmental_load[bay][angle][loadcase][1]**2)
                    Mybay=sqrt(Environmental_load[bay][angle][loadcase][2]**2+Environmental_load[bay][angle][loadcase][3]**2)
                    Fzbay=Gravitational_load[bay]
                    
                    #Loads at top of bay
                    if bay == 0:
                        Fxlastbay=self.LCtower[loadcase][0]
                        Mylastbay=self.LCtower[loadcase][4]
                        Fzlastbay=self.LCtower[loadcase][2]
                    else:
                        Fxlastbay=loadlist[bay-1][angle][loadcase][1][0]
                        Mylastbay=loadlist[bay-1][angle][loadcase][1][4]
                        Fzlastbay=loadlist[bay-1][angle][loadcase][1][2]
                        
                    FxtotTOP=Fxlastbay+Mybay/self.Wireframe[bay][1] #Load at the top of the bay JUST BELOW THE NODE
                    MytotTOP=Mylastbay
                    FztotTOP=Fzlastbay
                    
                    #Loads at bottom of bay   
                    FxtotBOT=FxtotTOP+Fxbay#-Mybay/self.Wireframe[bay][1]) #Load at the bottom of the bay ON THE NODE
                    MytotBOT=Mybay+Mylastbay+Fxlastbay*self.Wireframe[bay][1]
                    FztotBOT=Fzlastbay+Fzbay
                    
                    loadlist[bay][angle][loadcase][0]=[int(FxtotTOP),0.0,int(FztotTOP),0.0,int(MytotTOP),0.0]
                    loadlist[bay][angle][loadcase][1]=[int(FxtotBOT),0.0,int(FztotBOT),0.0,int(MytotBOT),0.0]
                    
        return loadlist
        
class Member_load_calculator:
    def __init__(self,wireframe):
        self.wireframe=wireframe
        
    def printlist(self,Member_loads):
        print()
        print('Member_loads[i]                = Datalist per bay')
        print('Member_loads[i][j]             = Datalist per bay per inflow angle where left and right indication shows loads at respective bay sides')
        print('Member_loads[i][j][k]          = Datalist per bay per inflow angle per load case')
        print('Member_loads[i][j][k][l]       = Datalist per bay per inflow ange per load case per side')
        print('                                 For left side of segment [0], for right side of segment [1]')
        print('Member loads[i][j][k][l][m]    = Datalist per bay per inflow angle per load case per side per member')
        print('                                 For leg [0], for brace [1]')
        print('Member_loads[i][j][k][l][m][n] = Datalist containing member information')
        print('                                 Size of member load [0], indication of load being either tensive or compressive [1]')
        print('                                 Tension loads are subjected to yield test only while compressive loads are subjected to both a yield as a buckling test')
        for bay in range(len(Member_loads)):
            for angle in range(len(Member_loads[bay])):
                if angle == 0:
                    bayside = '          '
                elif angle == 1:
                    bayside = 'left side '
                elif angle == 2:
                    bayside = 'right side'
                for loadcase in range(len(Member_loads[bay][angle])):
                    for side in range(len(Member_loads[bay][angle][loadcase])):
                        if side == 0:
                            sideinc = 'left of bay '
                        elif side == 1:
                            sideinc = 'right of bay'
                        for member in range(len(Member_loads[bay][angle][loadcase][side])):
                            if (member == 0):# or (member == 1):
                                membertype = 'leg  '
                            elif (member == 1):# or (member == 3):
                                membertype = 'brace'
                                
                            print('bay',bay+1,'angle',angle,bayside,'LC',loadcase+1,membertype,sideinc,Member_loads[bay][angle][loadcase][side][member])
            
        text=open('Data-jacket.txt','a')
        text.write('\n'+'Member_loads[i]                = Datalist per bay'+'\n')
        text.write('Member_loads[i][j]             = Datalist per bay per inflow angle where left and right indication shows loads at respective bay sides'+'\n')
        text.write('Member_loads[i][j][k]          = Datalist per bay per inflow angle per load case'+'\n')
        text.write('Member_loads[i][j][k][l]       = Datalist per bay per inflow ange per load case per side'+'\n')
        text.write('                                 For left side of segment [0], for right side of segment [1]'+'\n')
        text.write('Member loads[i][j][k][l][m]    = Datalist per bay per inflow angle per load case per side per member'+'\n')
        text.write('                                 For leg [0], for brace [1]'+'\n')
        text.write('Member_loads[i][j][k][l][m][n] = Datalist containing member information'+'\n')
        text.write('                                 Size of member load [0], indication of load being either tensive or compressive [1]'+'\n')
        text.write('                                 Tension loads are subjected to yield test only while compressive loads are subjected to both a yield as a buckling test'+'\n')
        for bay in range(len(Member_loads)):
            for angle in range(len(Member_loads[bay])):
                if angle == 0:
                    bayside = '          '
                elif angle == 1:
                    bayside = 'left side '
                elif angle == 2:
                    bayside = 'right side'
                for loadcase in range(len(Member_loads[bay][angle])):
                    for side in range(len(Member_loads[bay][angle][loadcase])):
                        if side == 0:
                            sideinc = 'left of bay '
                        elif side == 1:
                            sideinc = 'right of bay'
                        for member in range(len(Member_loads[bay][angle][loadcase][side])):
                            if (member == 0):# or (member == 1):
                                membertype = 'leg  '
                            elif (member == 1):# or (member == 3):
                                membertype = 'brace'
                                
                            text.write('bay '+str(bay+1)+' angle '+str(angle)+' '+str(bayside)+' LC '+str(loadcase+1)+' '+str(membertype)+' '+str(sideinc)+' '+str(Member_loads[bay][angle][loadcase][side][member])+'\n')
        text.close()
        
    def calculate(self,external_loads):
        wireframe=self.wireframe
        individual_loadlist = []
        member_loadlist = []
        reaction_list = []
        membersort=[]
        
        for bay in range(len(wireframe)):
            #Do the following for every bay
            #Create list in list for each bay
            individual_loadlist.append([])
            member_loadlist.append([])
            reaction_list.append([])
            for angle in range(2):
                #We compute for each inflow scenario infividually
                if angle == 0:
                    individual_loadlist[bay].append([])
                    member_loadlist[bay].append([])
                    reaction_list[bay].append([])
                #However angle 45 needs extra list for left and right side
                elif angle == 1:
                    for i in range(2):
                        individual_loadlist[bay].append([])
                        member_loadlist[bay].append([])
                        reaction_list[bay].append([])
                        
                for LC in range(3):
                    #For each loadcase we add three new lists
                    if angle == 0:
                        individual_loadlist[bay][0].append([])
                        member_loadlist[bay][0].append([])
                        reaction_list[bay][0].append([]) 
                    elif angle == 1:
                        for i in range(2):
                            individual_loadlist[bay][1+i].append([])
                            member_loadlist[bay][1+i].append([])
                            reaction_list[bay][1+i].append([])
                    for cross_section in range(2):
                        #Calculations are made firstly for top cross section and then for bottom
                        if cross_section == 0:
                            for side in range(2):
                                #DO THE FOLLOWING FOR THE 0 DEG ANGLE
                                if angle == 0:
                                    individual_loadlist[bay][0][LC].append([])
                                    member_loadlist[bay][0][LC].append([])
                                    reaction_list[bay][0][LC].append([]) 
                                elif angle == 1:
                                    for i in range(2):
                                        individual_loadlist[bay][1+i][LC].append([])
                                        member_loadlist[bay][1+i][LC].append([])
                                        reaction_list[bay][1+i][LC].append([])
                                        #We now have the following list: list[bay(0,baymax)][angle(0,1,2)][LC(1,2,3)][side(1,2)]
                                        
                                #We do the following for the right and lieft side
                                if angle == 0: #For zero degree inflow angle
                                    
                                    Hbay=wireframe[bay][1]
                                    Btop=wireframe[bay][3]
                                    Bbot=wireframe[bay][4]
                                    
                                    L1=(Bbot-Btop)/2.0
                                    L2=Bbot-L1
                                    L3=(sqrt(2)*Bbot-sqrt(2)*Btop)/2.0
                                    
                                    #phi1=atan(Hbay/L1)
                                    #phi2=atan(L1/L2)
                                    phi3=atan(Hbay/L3)
                                    
                                    top_bay_width = wireframe[bay][3]
                                    
                                    FxTOP=external_loads[bay][0][LC][0][0]/4.0
                                    FzTOP=external_loads[bay][0][LC][0][2]/4.0
                                    FmTOP=external_loads[bay][0][LC][0][4]/(2.0*top_bay_width)
                                    
                                    if bay != 0:
                                        FxADD=reaction_list[bay-1][0][LC][side][0]
                                        FyADD=reaction_list[bay-1][0][LC][side][1]
                                        FzADD=reaction_list[bay-1][0][LC][side][2]
                                    else:
                                        FxADD=0.
                                        FzADD=0.
                                        
                                    #Now we create the matrices for top
                                    if side == 0:     #Top left
                                        angle_leg = radians(wireframe[bay][7])
                                        angle_brace = radians(wireframe[bay][8])
                                    elif side == 1:     #Top right
                                        angle_leg = radians(wireframe[bay][9])
                                        angle_brace = radians(wireframe[bay][10])
                                        
                                    aa = cos(angle_leg)
                                    ab = cos(angle_brace)
                                    ba = sin(angle_leg)
                                    bb = sin(angle_brace)
                                            
                                    Matrix=np.array(([aa,ab],[ba,bb]),dtype=float)
                                    
                                    Vector_FxTOP=np.array(([-FxTOP,0]))
                                    Vector_FzTOP=np.array(([0,FzTOP]))
                                    if side == 0:
                                        Vector_FmTOP=np.array(([0,-FmTOP]))
                                    elif side == 1:
                                        Vector_FmTOP=np.array(([0,FmTOP]))
                                        
                                    Vector_FxADD=np.array(([-FxADD,0])) #check directionality
                                    Vector_FzADD=np.array(([0,-FzADD])) #check directionality
                                    
                                    Member_Load_FxTOP=np.linalg.solve(Matrix,Vector_FxTOP)
                                    Member_Load_FzTOP=np.linalg.solve(Matrix,Vector_FzTOP)
                                    Member_Load_FmTOP=np.linalg.solve(Matrix,Vector_FmTOP)
                                    Member_Load_FxADD=np.linalg.solve(Matrix,Vector_FxADD)
                                    Member_Load_FzADD=np.linalg.solve(Matrix,Vector_FzADD)
                                    
            
                                    #the data is stored per load case
                                    individual_loadlist[bay][0][LC][side]=[[int(Member_Load_FxTOP[0]),int(Member_Load_FzTOP[0]),int(Member_Load_FmTOP[0]),int(Member_Load_FxADD[0]),int(Member_Load_FzADD[0])],[int(Member_Load_FxTOP[1]),int(Member_Load_FzTOP[1]),int(Member_Load_FmTOP[1]),int(Member_Load_FxADD[1]),int(Member_Load_FzADD[1])]]
                                    #first we compute the leg load
                                    member_loadlist[bay][0][LC][side].append(int(Member_Load_FxTOP[0])+int(Member_Load_FzTOP[0])+int(Member_Load_FmTOP[0])+int(Member_Load_FxADD[0])+int(Member_Load_FzADD[0]))
                                    #second we compute the brace load
                                    member_loadlist[bay][0][LC][side].append(int(Member_Load_FxTOP[1])+int(Member_Load_FzTOP[1])+int(Member_Load_FmTOP[1])+int(Member_Load_FxADD[1])+int(Member_Load_FzADD[1]))
                                    
                                if angle == 1:
                                    top_bay_width =wireframe[bay][3]*sqrt(2)
                                    bottom_bay_width =wireframe[bay][4]*sqrt(2)
                                    if bay == 0:
                                        FxTOP=external_loads[bay][1][LC][0][0]/(sqrt(2)*4.0)
                                        FzTOP=external_loads[bay][1][LC][0][2]/(4.0)
                                        FmTOP=external_loads[bay][1][LC][0][4]/(top_bay_width)
                                    else:
                                        FxTOP=external_loads[bay][1][LC][0][0]/(sqrt(2)*4.0)
                                        FzTOP=external_loads[bay][1][LC][0][2]/(4.0)
                                        FmTOP=external_loads[bay][1][LC][0][4]/(top_bay_width)
                                    
                                    if bay != 0:
                                        FxADDLEFT= reaction_list[bay-1][1][LC][0][0]
                                        FyADDLEFT= reaction_list[bay-1][1][LC][0][1]
                                        FzADDLEFT= reaction_list[bay-1][1][LC][0][2]
                                        
                                        if side == 1:
                                            FxADDMID=  reaction_list[bay-1][2][LC][0][0]
                                            FyADDMID=  reaction_list[bay-1][2][LC][0][1]
                                            FzADDMID=  reaction_list[bay-1][2][LC][0][2]
                                        else:
                                            FxADDMID=  reaction_list[bay-1][2][LC][0][0]
                                            FyADDMID=  reaction_list[bay-1][2][LC][0][1]
                                            FzADDMID=  reaction_list[bay-1][2][LC][0][2]
                                        
                                        FxADDRIGHT=reaction_list[bay-1][2][LC][1][0]
                                        FyADDRIGHT=reaction_list[bay-1][2][LC][1][1]
                                        FzADDRIGHT=reaction_list[bay-1][2][LC][1][2]
                                        
                                    else:
                                        FxADDLEFT= 0.
                                        FyADDLEFT= 0.
                                        FzADDLEFT= 0.
                                        
                                        FxADDMID=  0.
                                        FyADDMID=  0.
                                        FzADDMID=  0.
                                        
                                        FxADDRIGHT=0.
                                        FyADDRIGHT=0.
                                        FzADDRIGHT=0.  
                                    #Now we create the matrices for top
                                    if side == 0:     #Top left    
                                        angle_leg = radians(wireframe[bay][7])
                                        angle_brace = radians(wireframe[bay][8])
                                    if side == 1:     #Top right
                                        angle_leg = radians(wireframe[bay][9])
                                        angle_brace = radians(wireframe[bay][10])
                                        
                                    aa = cos(angle_leg)
                                    ab = cos(angle_brace)
                                    ba = sin(angle_leg)
                                    bb = sin(angle_brace)
                                            
                                    Matrix=np.array(([aa,ab],[ba,bb]),dtype=float)
                                    
                                    Vector_FxTOP=np.array(([-FxTOP,0]))
                                    Vector_FzTOP=np.array(([0,FzTOP]))
                                    if side == 0:
                                        Vector_FmTOP=np.array(([0,-FmTOP]))
                                    elif side == 1:
                                        Vector_FmTOP=np.array(([0,FmTOP]))
                                    
                                    Vector_FxADDLEFT=np.array(([-FxADDLEFT,0])) #check directionality
                                    Vector_FyADDLEFT=np.array(([-FyADDLEFT,0])) #check directionality
                                    Vector_FzADDLEFT=np.array(([0,-FzADDLEFT])) #check directionality
                                    
                                    Vector_FxADDMID=np.array(([-FxADDMID,0])) #check directionality
                                    Vector_FyADDMID=np.array(([-FyADDMID,0])) #check directionality
                                    Vector_FzADDMID=np.array(([0,-FzADDMID])) #check directionality
                                    
                                    Vector_FxADDRIGHT=np.array(([-FxADDRIGHT,0])) #check directionality
                                    Vector_FyADDRIGHT=np.array(([-FyADDRIGHT,0])) #check directionality
                                    Vector_FzADDRIGHT=np.array(([0,-FzADDRIGHT])) #check directionality
                                    
                                    Member_load_FxTOP=np.linalg.solve(Matrix,Vector_FxTOP)
                                    Member_load_FzTOP=np.linalg.solve(Matrix,Vector_FzTOP)
                                    Member_load_FmTOP=np.linalg.solve(Matrix,Vector_FmTOP)
                                    
                                    if side == 0:
                                        #Left side left part
                                        Member_load_FxADDLEFT=np.linalg.solve(Matrix,Vector_FxADDLEFT)
                                        Member_load_FyADDLEFT=np.linalg.solve(Matrix,Vector_FyADDLEFT)
                                        Member_load_FzADDLEFT=np.linalg.solve(Matrix,Vector_FzADDLEFT)
                                        #Left side right paty
                                        Member_load_FxADDMID=np.linalg.solve(Matrix,Vector_FxADDMID)
                                        Member_load_FyADDMID=np.linalg.solve(Matrix,Vector_FyADDMID)
                                        Member_load_FzADDMID=np.linalg.solve(Matrix,Vector_FzADDMID)
                                        
                                    elif side == 1:
                                        #Left side left part
                                        Member_load_FxADDMID=np.linalg.solve(Matrix,Vector_FxADDMID)
                                        Member_load_FyADDMID=np.linalg.solve(Matrix,Vector_FyADDMID)
                                        Member_load_FzADDMID=np.linalg.solve(Matrix,Vector_FzADDMID)
                                        #Left side right paty
                                        Member_load_FxADDRIGHT=np.linalg.solve(Matrix,Vector_FxADDRIGHT)
                                        Member_load_FyADDRIGHT=np.linalg.solve(Matrix,Vector_FyADDRIGHT)
                                        Member_load_FzADDRIGHT=np.linalg.solve(Matrix,Vector_FzADDRIGHT)
                                        
                                    if side == 0:
                                        #Now loads are combined to yield member load
                                        #Firstly for the left bay
                                        individual_loadlist[bay][1][LC][0]=[[int(2*Member_load_FxTOP[0]),int(Member_load_FzTOP[0]),int(Member_load_FmTOP[0]),int(Member_load_FxADDLEFT[0]),int(Member_load_FyADDLEFT[0]),int(Member_load_FzADDLEFT[0])],[int(Member_load_FxTOP[1]),int(Member_load_FzTOP[1]),int(Member_load_FmTOP[1]),int(.5*Member_load_FxADDLEFT[1]),int(.5*Member_load_FyADDLEFT[1]),int(Member_load_FzADDLEFT[1])]]
                                        
                                        #Second for the right bay
                                        individual_loadlist[bay][2][LC][0]=[[int(0*Member_load_FxTOP[0]),int(Member_load_FzTOP[0]),int(0.),int(0*Member_load_FxADDMID[0]),int(0*Member_load_FyADDMID[0]),int(Member_load_FzADDMID[0])],[1*int(Member_load_FxTOP[1]),int(Member_load_FzTOP[1]),int(0.),int(1*Member_load_FxADDMID[1]),int(0*Member_load_FyADDMID[1]),int(Member_load_FzADDMID[1])]]
                                        
                                        #Thirdly we compute the leg load for left bay
                                        member_loadlist[bay][1][LC][0].append(int(2*Member_load_FxTOP[0])+int(Member_load_FzTOP[0])+int(Member_load_FmTOP[0])+int(Member_load_FxADDLEFT[0])+int(Member_load_FyADDLEFT[0])+int(Member_load_FzADDLEFT[0]))
                                        
                                        #Fourth we compute the brace load for the left bay
                                        member_loadlist[bay][1][LC][0].append(int(Member_load_FxTOP[1])+int(Member_load_FzTOP[1])+int(Member_load_FmTOP[1])+int(.5*Member_load_FxADDLEFT[1])+int(.5*Member_load_FyADDLEFT[1])+int(Member_load_FzADDLEFT[1]))
                                        
                                        #Fifth this is done for the leg of the right bay aswell
                                        member_loadlist[bay][2][LC][0].append(int(0*Member_load_FxTOP[0])+int(Member_load_FzTOP[0])+int(0.)+int(0*Member_load_FxADDMID[0])+int(0*Member_load_FyADDMID[0])+int(Member_load_FzADDMID[0]))
                                        
                                        #Sixth this is finally doe for the brace of the right bay                                               !
                                        member_loadlist[bay][2][LC][0].append(int(1*Member_load_FxTOP[1])+int(Member_load_FzTOP[1])+int(0.)+int(1*Member_load_FxADDMID[1])+int(0*Member_load_FyADDMID[1])+int(Member_load_FzADDMID[1]))
                                        
                                    elif side == 1:
                                        #Now loads are combined to yield member load
                                        #Firstly for the left bay
                                        individual_loadlist[bay][1][LC][1]=[[int(0*Member_load_FxTOP[0]),int(Member_load_FzTOP[0]),int(0.),int(0*Member_load_FxADDMID[0]),int(0*Member_load_FyADDMID[0]),int(Member_load_FzADDMID[0])],[int(Member_load_FxTOP[1]),int(Member_load_FzTOP[1]),int(0.),int(0*Member_load_FxADDMID[1]),int(1*Member_load_FyADDMID[1]),int(Member_load_FzADDMID[1])]]
                                        
                                        #Second for the right bay
                                        individual_loadlist[bay][2][LC][1]=[[int(2*Member_load_FxTOP[0]),int(Member_load_FzTOP[0]),int(Member_load_FmTOP[0]),int(Member_load_FxADDRIGHT[0]),int(Member_load_FyADDRIGHT[0]),int(Member_load_FzADDRIGHT[0])],[int(Member_load_FxTOP[1]),int(Member_load_FzTOP[1]),int(Member_load_FmTOP[1]),int(.5*Member_load_FxADDRIGHT[1]),int(.5*Member_load_FyADDRIGHT[1]),int(Member_load_FzADDRIGHT[1])]]
                                        
                                        member_loadlist[bay][1][LC][1].append(int(0*Member_load_FxTOP[0])+int(Member_load_FzTOP[0])+int(0.)+int(0*Member_load_FxADDMID[0])+int(0*Member_load_FyADDMID[0])+int(Member_load_FzADDMID[0]))
                                        member_loadlist[bay][1][LC][1].append(int(Member_load_FxTOP[1])+int(Member_load_FzTOP[1])+int(0.)+int(0.*Member_load_FxADDMID[1])+int(1.0*Member_load_FyADDMID[1])+int(Member_load_FzADDMID[1]))
                                        member_loadlist[bay][2][LC][1].append(int(2*Member_load_FxTOP[0])+int(Member_load_FzTOP[0])+int(Member_load_FmTOP[0])+int(Member_load_FxADDRIGHT[0])+int(Member_load_FyADDRIGHT[0])+int(Member_load_FzADDRIGHT[0]))
                                        member_loadlist[bay][2][LC][1].append(int(Member_load_FxTOP[1])+int(Member_load_FzTOP[1])+int(Member_load_FmTOP[1])+int(.5*Member_load_FxADDRIGHT[1])+int(.5*Member_load_FyADDRIGHT[1])+int(Member_load_FzADDRIGHT[1]))
                                    
                        elif cross_section == 1:
                            for side in range(2):
                                if angle == 0:
                                    #Now we calculate the difference in load directionality as a result of angular differences
                                    #We calculate the difference between horizontal bottom load and observed bottom load from braces
                                    bottom_bay_width =wireframe[bay][4]
                                
                                    FxBOT=external_loads[bay][0][LC][0][0]/4.0
                                    FzBOT=external_loads[bay][0][LC][0][2]/4.0
                                    FmBOT=external_loads[bay][0][LC][1][4]/(2.0*bottom_bay_width)
                                    
                                    if side == 0:     #Bottom left
                                        angle_leg = radians(wireframe[bay][11])
                                        angle_brace = radians(wireframe[bay][12])
                                        Fleg=member_loadlist[bay][0][LC][0][0]
                                        Fbrace=member_loadlist[bay][0][LC][1][1]
                                        
                                        FxADD=Fleg*cos(angle_leg)+Fbrace*cos(angle_brace)-FxBOT
                                        FyADD=0.
                                        FzADD=Fleg*sin(angle_leg)+Fbrace*sin(angle_brace)+FzBOT-FmBOT
                                        
                                    elif side == 1:     #Bottom right
                                        angle_leg = radians(wireframe[bay][13])
                                        angle_brace = radians(wireframe[bay][14])
                                        Fleg=member_loadlist[bay][0][LC][1][0]
                                        Fbrace=member_loadlist[bay][0][LC][0][1]
                                        
                                        FxADD=Fleg*cos(angle_leg)+Fbrace*cos(angle_brace)-FxBOT
                                        FyADD=0.
                                        FzADD=Fleg*sin(angle_leg)+Fbrace*sin(angle_brace)+FzBOT+FmBOT
                                      
                                    reaction_list[bay][0][LC][side]=[int(FxADD),int(FyADD),int(FzADD)]
                                    
                                elif angle == 1:
                                    Hbay=wireframe[bay][1]
                                    Btop=wireframe[bay][3]
                                    Bbot=wireframe[bay][4]
                                    
                                    bottom_bay_width =wireframe[bay][4]*sqrt(2)
                                        
                                    FxBOT=external_loads[bay][1][LC][0][0]/(sqrt(2)*4.0)
                                    FzBOT=external_loads[bay][1][LC][0][2]/(4.0)
                                    FmBOT=external_loads[bay][1][LC][1][4]/(bottom_bay_width)
                                    
                                    #member load bottom left bay left side
                                    FlegA1L=member_loadlist[bay][1][LC][0][0]
                                    FbraceA1R=member_loadlist[bay][1][LC][1][1]
                                    #member load bottom left bay right side
                                    FlegA1R=member_loadlist[bay][1][LC][1][0]
                                    FbraceA1L=member_loadlist[bay][1][LC][0][1]
                                    #member load bottom right bay left side
                                    #FlegA2L=member_loadlist[bay][2][LC][0][0]
                                    FbraceA2R=member_loadlist[bay][2][LC][1][1]
                                    #member load bottom right bay right side
                                    FlegA2R=member_loadlist[bay][2][LC][1][0]
                                    FbraceA2L=member_loadlist[bay][2][LC][0][1]
                                    
                                    L1=(Bbot-Btop)/2.0
                                    L2=Bbot-L1
                                    L3=(sqrt(2)*Bbot-sqrt(2)*Btop)/2.0
                                    
                                    #phi1=atan(Hbay/L1)
                                    #phi2=atan(L1/L2)
                                    phi3=atan(Hbay/L3)
                                    
                                    #FOR BOTTOM LEFT NODE
                                    FxylegN1=FlegA1L*cos(phi3)
                                    FxlegN1=FxylegN1/sqrt(2)
                                    FylegN1=FxylegN1/sqrt(2)
                                    FzlegN1=FlegA1L*sin(phi3)
                                    
                                    FxybraceONEMEMBERN1=FbraceA1R*cos(atan(Hbay/(sqrt(L1**2+L2**2))))
                                    FxbraceONEMEMBERN1=FxybraceONEMEMBERN1*cos(L1/L2)
                                    FybraceONEMEMBERN1=FxybraceONEMEMBERN1*sin(L1/L2)
                                    FxbraceN1=FxbraceONEMEMBERN1+FybraceONEMEMBERN1
                                    FybraceN1=FxbraceN1
                                    FzbraceN1=2*FbraceA1R*sin(atan(Hbay/(sqrt(L1**2+L2**2))))    
                                    
                                    FxN1=FxlegN1+FxbraceN1
                                    FyN1=FylegN1+FybraceN1
                                    FzN1=FzlegN1+FzbraceN1
                                    
                                    #For middle node
                                    FxybraceleftN2=FbraceA1L*cos(atan(Hbay/(sqrt(L1**2+L2**2))))
                                    FzbraceleftN2=FbraceA1L*sin(atan(Hbay/(sqrt(L1**2+L2**2))))
                                    FxbraceleftN2=FxybraceleftN2*cos(atan(L1/L2))
                                    FybraceleftN2=FxybraceleftN2*sin(atan(L1/L2))
                                    
                                    FxybracerightN2=FbraceA2R*cos(atan(Hbay/(sqrt(L1**2+L2**2))))
                                    FzbracerightN2=FbraceA2R*sin(atan(Hbay/(sqrt(L1**2+L2**2))))
                                    FxbracerightN2=FxybracerightN2*cos(atan(L1/L2))
                                    FybracerightN2=FxybracerightN2*sin(atan(L1/L2))
                                    
                                    FxylegN2=FlegA1R*cos(atan(Hbay/(sqrt(2)*L1)))
                                    FzlegN2=FlegA1R*sin(atan(Hbay/(sqrt(2)*L1)))
                                    FxlegN2=FxylegN2/sqrt(2)
                                    FylegN2=FxylegN2/sqrt(2)
                                    
                                    FxN2=-FxbraceleftN2-FybracerightN2-FxlegN2
                                    FyN2=FybraceleftN2+FxbracerightN2+FylegN2
                                    FzN2=FzbraceleftN2+FzbracerightN2+FzlegN2
                                        
                                    #for right node
                                    FxylegleftN3=FlegA2R*cos(phi3)
                                    FxlegleftN3=FxylegleftN3/sqrt(2)
                                    FylegleftN3=FxylegleftN3/sqrt(2)
                                    FzlegleftN3=FlegA2R*sin(phi3)
                                    
                                    FxybraceleftONEMEMBERN3=FbraceA2L*cos(atan(Hbay/(sqrt(L1**2+L2**2))))
                                    FxbraceleftONEMEMBERN3=FxybraceleftONEMEMBERN3*cos(L1/L2)
                                    FybraceleftONEMEMBERN3=FxybraceleftONEMEMBERN3*sin(L1/L2)
                                    FxbraceleftN3=FxbraceleftONEMEMBERN3+FybraceleftONEMEMBERN3
                                    FybraceleftN3=FxbraceleftN3
                                    FzbraceleftN3=2*FbraceA2L*sin(atan(Hbay/(sqrt(L1**2+L2**2)))) 
                                    
                                    FxN3=-FxlegleftN3-FxbraceleftN3
                                    FyN3=-FylegleftN3-FybraceleftN3
                                    FzN3=FzlegleftN3+FzbraceleftN3
                                    
                                    dFxN1=FxN1-FxBOT
                                    dFyN1=FyN1-FxBOT
                                    dFzN1=FzN1-(-FzBOT+FmBOT)
                                    if side == 0: #right part of bay
                                        dFxN2=FyN2-FxBOT
                                        dFyN2=FxN2-FxBOT
                                        dFzN2=FzN2-(-FzBOT)
                                    elif side == 1: #leftpart of bay
                                        dFxN2=FxN2-FxBOT #goed
                                        dFyN2=FyN2-FxBOT #goed
                                        dFzN2=FzN2-(-FzBOT)
                                    
                                    dFxN3=FxN3-FxBOT
                                    dFyN3=FyN3-FxBOT
                                    dFzN3=FzN3-(-FzBOT-FmBOT)
                                    
                                    if side == 0:
                                        reaction_list[bay][1][LC][0]=[int(abs(dFxN1)),int(abs(dFyN1)),int(dFzN1)]
                                        reaction_list[bay][2][LC][0]=[int((dFxN2)),int((dFyN2)),int(dFzN2)]
                                    elif side == 1:
                                        reaction_list[bay][1][LC][1]=[int((dFxN2)),int((dFyN2)),int(dFzN2)]
                                        reaction_list[bay][2][LC][1]=[int(abs(dFxN3)),int(abs(dFyN3)),int(dFzN3)]
                                        
        for bay in range(len(self.wireframe)):
            membersort.append([])
            for angle in range(3):
                membersort[bay].append([])
                for loadcase in range(3):
                    membersort[bay][angle].append([])
                    for side in range(2):
                        membersort[bay][angle][loadcase].append([])
                        Fleg=member_loadlist[bay][angle][loadcase][side][0]
                        Fbrace=member_loadlist[bay][angle][loadcase][side][1]
                        if Fleg >= 0:
                            membersort[bay][angle][loadcase][side].append([abs(Fleg),'tension'])
                        else:
                            membersort[bay][angle][loadcase][side].append([abs(Fleg),'compression'])
                        if Fbrace >= 0:
                            membersort[bay][angle][loadcase][side].append([abs(Fbrace),'tension'])
                        else:
                            membersort[bay][angle][loadcase][side].append([abs(Fbrace),'compression'])
        
        return membersort,member_loadlist,reaction_list
        
class Maximum_load_selecter:
    def __init__(self,wireframe):
        self.wireframe=wireframe
        
    def printlist(self,Maximum_loads,Maximum_loc):
        print()
        print('Maximum_loads[i]    = Maximum loads per bay')
        print('Maximum_loads[i][j] = List with maximum tension and compression loads per leg and brace')
        print('                      Max compressive leg load[0], Max tensive leg load[1], Max compressive brace load[2], Max tensive brace load[3]')
        for bay in range(len(Maximum_loads)):
            for element in range(len(Maximum_loads[bay])):
                print('bay',bay+1,Maximum_loads[bay][element],' Located at: ',Maximum_loc[bay][element])
            
        text=open('Data-Jacket.txt','a')
        text.write('\n'+'Maximum_loads[i]    = Maximum loads per bay'+'\n')
        text.write('Maximum_loads[i][j] = List with maximum tension and compression loads per leg and brace'+'\n')
        text.write('                      Max compressive leg load[0], Max tensive leg load[1], Max compressive brace load[2], Max tensive brace load[3]'+'\n')
        for bay in range(len(Maximum_loads)):
            for element in range(len(Maximum_loads[bay])):
                text.write('bay '+str(bay+1)+' '+str(Maximum_loads[bay][element])+' Located at: '+str(Maximum_loc[bay][element])+'\n')
        text.close()
        
    def select(self,Memberloads):
        Maximum_loads=[]
        Maximum_loc=[]
        for bay in range(len(self.wireframe)):
            Maximum_loads.append([])
            Maximum_loc.append([])
            #The largest compressive and tensive loads are selected for braces and legs
            Max_compressive_load_leg = 0.0
            Max_tensive_load_leg = 0.0
            Max_compressive_load_brace = 0.0
            Max_tensive_load_brace = 0.0
            
            for angle in range(len(Memberloads[bay])):
                for loadcase in range(len(Memberloads[bay][angle])):
                    for side in range(len(Memberloads[bay][angle][loadcase])):
                        for member in range(len(Memberloads[bay][angle][loadcase][side])):
                            if angle == 0:
                                angleprint = '0 d       '
                            elif angle == 1:
                                angleprint = '45 d left '
                            elif angle == 2:
                                angleprint = '45 d right'
                                
                            if side == 0:
                                sideprint = 'left side '
                            elif side == 1:
                                sideprint = 'right side'
                                
                            if (Memberloads[bay][angle][loadcase][side][member][1] == 'compression'):
                                if (member == 0) or (member == 2):
                                    if abs(Memberloads[bay][angle][loadcase][side][member][0]) >= abs(Max_compressive_load_leg):
                                        Max_compressive_load_leg = Memberloads[bay][angle][loadcase][side][member][0]
                                        Max_comp_leg_loc=['Max comp leg   - angle:',angleprint,'LC:',loadcase+1,'side:',sideprint]
                                else:
                                    if abs(Memberloads[bay][angle][loadcase][side][member][0]) >= abs(Max_compressive_load_brace):
                                        Max_compressive_load_brace = Memberloads[bay][angle][loadcase][side][member][0]
                                        Max_comp_bra_loc=['Max comp brace - angle:',angleprint,'LC:',loadcase+1,'side:',sideprint]
                                        
                            elif (Memberloads[bay][angle][loadcase][side][member][1] == 'tension'):
                                if (member == 0) or (member == 2):
                                    if abs(Memberloads[bay][angle][loadcase][side][member][0]) >= abs(Max_tensive_load_leg):
                                        Max_tensive_load_leg = Memberloads[bay][angle][loadcase][side][member][0]
                                        Max_tens_leg_loc=['Max tens leg   - angle:',angleprint,'LC:',loadcase+1,'side:',sideprint]
                                else:
                                    if abs(Memberloads[bay][angle][loadcase][side][member][0]) >= abs(Max_tensive_load_brace):
                                        Max_tensive_load_brace = Memberloads[bay][angle][loadcase][side][member][0]
                                        Max_tens_bra_loc=['Max tens brace - angle:',angleprint,'LC:',loadcase+1,'side:',sideprint]
                                    
            Maximum_loads[bay]=[abs(Max_compressive_load_leg),abs(Max_tensive_load_leg),abs(Max_compressive_load_brace),abs(Max_tensive_load_brace)]
            Maximum_loc[bay]=[Max_comp_leg_loc,Max_tens_leg_loc,Max_comp_bra_loc,Max_tens_bra_loc]
        
        return Maximum_loads,Maximum_loc
         
class Dimension_optimizer:
    def __init__(self,Wireframe,Guessed_dimensions,equivalent,bayload,member,maxloads):
        #Values that never change
        self.Wireframe=Wireframe
        self.sigmY=Input_data.stored_data.sigmY
        self.Ed=Input_data.stored_data.Ed
        self.v=0.287 #Poisson ratio
        
        #Instances to continue calculations with        
        self.equivalent=equivalent
        self.bayload=bayload
        self.member=member
        self.maxloads=maxloads     
        
        #List of found data
        self.Equivalent_dimensions=[]
        self.Environmental_load_per_bay=[]
        self.Gravitational_load_per_bay=[]
        self.Loads_summed=[]
        
        self.Membersort=[]
        self.Memberload=[]
        self.Reactivelist=[]
        self.Maximum_loads=[]
        self.Maximum_loc=[]
        
        #List to keep track of optimization
        self.guess_dimensions=Guessed_dimensions
        self.final_dimensionlist=[]
        self.intermediate_dimensionlist=[]
        self.bay=0
        self.ratio=0
        self.minbound=0
        self.maxbound=0
        self.wtleg=0
        self.wtbrace=0
        
    def printlistMIN(self,Minimal_dimensions):
        print()
        print('Minimal_dimensions[i]    = Minimum required diameter per bay of solid member from preliminary analysis')
        print('Minimal_dimensions[i][j] = Minimum required diameter for respective bay leg[0] and brace [1]')
        for bay in range(len(Minimal_dimensions)):
            print('bay',bay+1,Minimal_dimensions[bay])
            
        text=open('Data-Jacket.txt','a')
        text.write('\n'+'Minimal_dimensions[i]    = Minimum required diameter per bay of solid member from preliminary analysis'+'\n')
        text.write('Minimal_dimensions[i][j] = Minimum required diameter for respective bay leg[0] and brace [1]'+'\n')
        for bay in range(len(Minimal_dimensions)):
            text.write('bay '+str(bay+1)+' '+str(Minimal_dimensions[bay])+'\n')
        text.close()
            
    def printlistOPT(self,Optimal_dimensions):
        print()
        print('Optimal_dimensions[i]    = Datalist per bay')
        print('Optimal_dimensions[i][j] = Optimal dimensions of respective bay')
        print('Optimal_dimensions[i][0] = Dleg')
        print('Optimal_dimensions[i][1] = Dbrace')
        print('Optimal_dimensions[i][2] = wtleg')
        print('Optimal_dimensions[i][3] = wtbrace')
        for bay in range(len(Optimal_dimensions)):
            print('bay',bay+1,Optimal_dimensions[bay])
            
        text=open('Data-Jacket.txt','a')
        text.write('\n'+'Optimal_dimensions[i]    = Datalist per bay'+'\n')
        text.write('Optimal_dimensions[i][j] = Optimal dimensions of respective bay'+'\n')
        text.write('Optimal_dimensions[i][0] = Dleg'+'\n')
        text.write('Optimal_dimensions[i][1] = Dbrace'+'\n')
        text.write('Optimal_dimensions[i][2] = wtleg'+'\n')
        text.write('Optimal_dimensions[i][3] = wtbrace'+'\n')
        for bay in range(len(Optimal_dimensions)):
            text.write('bay '+str(bay+1)+' '+str(Optimal_dimensions[bay])+'\n')
        text.close()
        
    def calculate_minimal_dimensions(self,Maximum_loads):
        #Here we use brentq to find the sero of a function
        #First we calculate the minimal leg dimensions
        Dminlist=[]
        for bay in range(len(self.Wireframe)):
            Dminlist.append([])
            Dyieldcomp=brentq(self.yieldcheckPRELIM,0.0001,10.0,args=(Maximum_loads[bay][0],))
            Dyieldtens=brentq(self.yieldcheckPRELIM,0.0001,10.0,args=(Maximum_loads[bay][1],))
            Deuler=brentq(self.eulerPRELIM,0.0001,10.0,args=(self.Wireframe[bay][1]*(1.0+self.Wireframe[bay][15]),Maximum_loads[bay][0]))
            Dminlist[bay].append(max([Dyieldcomp,Dyieldtens,Deuler]))
            
        #Then for the minimal brace dimensions
        for bay in range(len(self.Wireframe)):
            Dyieldcomp=brentq(self.yieldcheckPRELIM,0.0001,10.0,args=(Maximum_loads[bay][2],))
            Dyieldtens=brentq(self.yieldcheckPRELIM,0.0001,10.0,args=(Maximum_loads[bay][3],))
            Deuler=brentq(self.eulerPRELIM,0.0001,10.0,args=(self.Wireframe[bay][5],Maximum_loads[bay][2]))
            Dminlist[bay].append(max([Dyieldcomp,Dyieldtens,Deuler]))
            
        return Dminlist
            
    def yieldcheckPRELIM(self,D,F):
        return F/self.areaPRELIM(D)- self.sigmY
            
    def eulerPRELIM(self,D,L,F):
        Keff = 1.0
        Rgyra=sqrt(self.inertiaPRELIM(D)/self.areaPRELIM(D)) #Radius of gyration
        slenderness=Keff*L/Rgyra #Slenderness parameter
        slendernessE=pi*sqrt(self.Ed/self.sigmY) #Slenderness Euler limit
        slendernessR=slenderness/slendernessE #Reduced slenderness ratio
        if slendernessR <= 1.0:
            sigmMAX=self.sigmY
            return F/self.areaPRELIM(D)- sigmMAX
        else:
            sigmMAX=self.sigmY/slendernessR**2
            return F/self.areaPRELIM(D) - sigmMAX
            
    def areaPRELIM(self,D):
        return pi/4.0*D**2
        
    def inertiaPRELIM(self,D):
        return pi/64.0*D**4
        
    def calculate_optimal_dimensions(self,Minimal_dimensions):
        for bay in range(len(self.Wireframe)):
            #First we create lists to save our dimensions
            #Final_dimensionlist has an equal structure as 'Dimensionlist': [Dleg,Dbrace,Dpile,wtleg,wtbrace,wtpile]
            self.final_dimensionlist.append([0.0,0.0,0.0,0.0])
            self.intermediate_dimensionlist.append(self.guess_dimensions[bay])
            
        for bay in range(len(self.Wireframe)):
            self.ratio=self.guess_dimensions[bay][1]/self.guess_dimensions[bay][0]
            #Set minium diameter erqual to minimum required solid stave diameter:
            if Minimal_dimensions[bay][0] >= Minimal_dimensions[bay][1]/self.ratio:
                dmin=Minimal_dimensions[bay][0]
            else:
                dmin=Minimal_dimensions[bay][1]/self.ratio
            #Check if minimum diameter is at least larger as last iteration:    
            if bay != 0:
                if dmin <= self.final_dimensionlist[bay-1][0]:
                    dmin = self.final_dimensionlist[bay-1][0]
                    
            #Reset brace dimensions for curretn bay to zero        
            self.wtleg=0
            self.wtbrace=0
            Ratio=10.0  
            Anew=10.0
            while Ratio >= 1.01:
                self.bay=bay
                xmin=[dmin*1.1]
                xmax=[dmin*100.0+5.0]
                x0=[Minimal_dimensions[bay][0]*1.2]
                bounds=[(low, high) for low, high in zip(xmin, xmax)]
                minimizer_kwargs = dict(method="L-BFGS-B", bounds=bounds)
                Aold=Anew
                Dmin=basinhopping(self.areaOPT,x0,minimizer_kwargs=minimizer_kwargs)
                Dmin=Dmin['x'][0]
                Anew=self.area(Dmin,self.final_dimensionlist[bay][2])
                if abs(Anew) >= abs(Aold):
                    Ratio=abs(Anew)/abs(Aold)
                else:
                    Ratio=abs(Aold)/abs(Anew)
                self.wtleg=self.final_dimensionlist[bay][2]
                self.wtbrace=self.final_dimensionlist[bay][3]

        return self.final_dimensionlist
                
    def areaOPT(self,D):
        D=D[0]
        bay=self.bay
        #First we create a new dimensionlist
        for bays in range(len(self.Wireframe)):
            if self.final_dimensionlist[bays] != [0.0,0.0,0.0,0.0]:
                self.intermediate_dimensionlist[bays]=self.final_dimensionlist[bays]

        #Now we add the current dimension guess to the intermediate list
        self.intermediate_dimensionlist[bay][0]=D
        self.intermediate_dimensionlist[bay][1]=D*self.ratio #here the intial brace/leg ratio is applied

        #We repeat the calculation sequence to find maximum loads of each bay
        Equivalent_dimensions=self.equivalent.builder(self.intermediate_dimensionlist)
        Environmental_load_per_bay=self.bayload.calculate_environmental_load_per_bay(Equivalent_dimensions)
        Gravitational_load_per_bay=self.bayload.calculate_gravitational_load_per_bay(self.intermediate_dimensionlist)
        Loads_summed=self.bayload.calculate_load_summed(Environmental_load_per_bay,Gravitational_load_per_bay)
                
        Membersort,Memberload,Reactivelist=self.member.calculate(Loads_summed)
        Maximum_loads,Maximum_loc=self.maxloads.select(Membersort)
        
        #These data is saved for future use
        self.Equivalent_dimensions=Equivalent_dimensions
        self.Environmental_load_per_bay=Environmental_load_per_bay
        self.Gravitational_load_per_bay=Gravitational_load_per_bay
        self.Loads_summed=Loads_summed
        
        self.Membersort=Membersort
        self.Memberload=Memberload
        self.Reactivelist=Reactivelist
        self.Maximum_loads=Maximum_loads
        self.Maximum_loc=Maximum_loc

        #the minimum required wall thicknesses for these loads are calculated
        #first for the leg
        wtyieldcomp=brentq(self.yieldcheck,0.00001,D/2.0,args=(D,Maximum_loads[bay][0]))
        wtyieldtens=brentq(self.yieldcheck,0.00001,D/2.0,args=(D,Maximum_loads[bay][1]))
        wteuler=brentq(self.euler,0.00001,D/2.0,args=(D,self.Wireframe[bay][1]*(1.0+self.Wireframe[bay][15]),Maximum_loads[bay][0]))
        
        #Now we check if a local buckling calculation is required:
        L=self.Wireframe[bay][1]*(1.0+self.Wireframe[bay][15]) #Member length
        R=D/2.0 #Radius
        n=1.2 #Buckling mode
        wtleg=max([wtyieldcomp,wtyieldtens,wteuler])
        
        #Now Cx is estimated, if an earlyer iteration was availible Cx is computed from that value othweise its computed from the current maximal wt
        if self.wtleg != 0:
            wtlegguess=self.wtleg
        else:
            wtlegguess=wtleg
        wtlegguessOLD=0.00000000000000001
        while abs(wtlegguess/wtlegguessOLD)>=1.05: 
            wtlegguessOLD=wtlegguess
            Cx=max([1-(0.4*L/R*sqrt(wtlegguess/R)-0.2)/n,0.6])
                
            if R/wtleg <= self.Ed*Cx/(40*self.sigmY):
                #No local buckling check required
                wtlocalbuckling=wtleg
            else:
                #Local buckling check required
                try:
                    wtlocalbuckling=brentq(self.localbuckling,0.000000001,D/2.0,args=(D,self.Wireframe[bay][1]*(1.0+self.Wireframe[bay][15]))) #D/(1.2*sqrt(self.Ed/self.sigmY))
                except ValueError:
                    #If we get an error this means the structure wall thickness has to be set equal to the vale where local buckling does definatly not occur
                    wtlocalbuckling=R/(self.Ed*Cx/(40*self.sigmY))
            wtlegguess=wtlocalbuckling
                
        wtleg=max([wtyieldcomp,wtyieldtens,wteuler,wtlocalbuckling])
        
        #second for the brace
        wtyieldcomp=brentq(self.yieldcheck,0.00001,D*self.ratio/2.0,args=(D*self.ratio,Maximum_loads[bay][2]))
        wtyieldtens=brentq(self.yieldcheck,0.00001,D*self.ratio/2.0,args=(D*self.ratio,Maximum_loads[bay][3]))
        wteuler=brentq(self.euler,0.00001,D*self.ratio/2.0,args=(D*self.ratio,self.Wireframe[bay][5],Maximum_loads[bay][2]))
        
        #Now we check if a local buckling calculation is required:
        wtbrace=max([wtyieldcomp,wtyieldtens,wteuler])
        L=self.Wireframe[bay][5]
        R=D*self.ratio/2.0
        n=1.0
        if self.wtbrace != 0:
            wtbraceguess=self.wtbrace
        else:
            wtbraceguess=wtbrace
        wtbraceguessOLD=0.00000000000000001
        while abs(wtbraceguess/wtbraceguessOLD)>=1.05:
            wtbraceguessOLD=wtbraceguess
            Cx=max([1-(0.4*L/R*sqrt(wtbraceguess/R)-0.2)/n,0.6])
            
            if R/wtbrace <= self.Ed*Cx/(40*self.sigmY):
                #No local buckling check required
                wtlocalbuckling=wtbrace
            else:
                #Local buckling check required
                try:
                    wtlocalbuckling=brentq(self.localbuckling,0.000000000001,D*self.ratio/2.0,args=(D*self.ratio,self.Wireframe[bay][5])) #D*self.ratio/(1.2*sqrt(self.Ed/self.sigmY))
                except ValueError:
                    #If we get an error this means the structure wall thickness has to be set equal to the vale where local buckling does not occur
                    wtlocalbuckling=R/(self.Ed*Cx/(40*self.sigmY))
            wtbraceguess=wtlocalbuckling
        wtbrace=max([wtyieldcomp,wtyieldtens,wteuler,wtlocalbuckling])
        
        #finally we store the found dimensions in the finaldimensionlist
        self.final_dimensionlist[bay][0]=D
        self.final_dimensionlist[bay][1]=D*self.ratio
        self.final_dimensionlist[bay][2]=wtleg
        self.final_dimensionlist[bay][3]=wtbrace
        
        return self.area(D,wtleg)
        
    def yieldcheck(self,wt,D,F):
        return F/self.area(D,wt)- self.sigmY
        
    def euler(self,wt,D,L,F):
        Keff = 1.0
        Rgyra=sqrt(self.inertia(D,wt)/self.area(D,wt)) #Radius of gyration
        slenderness=Keff*L/Rgyra #Slenderness parameter
        slendernessE=pi*sqrt(self.Ed/self.sigmY) #Slenderness Euler limit
        slendernessR=slenderness/slendernessE #Reduced slenderness ratio
        if slendernessR <= 1.0:
            sigmMAX=self.sigmY
            return F/self.area(D,wt)- sigmMAX
        else:
            sigmMAX=self.sigmY/slendernessR**2
            return F/self.area(D,wt) - sigmMAX
            
    def localbuckling(self,wt,D,L):
        #method adopted from GL 6.6.5
        R=(D-wt)/2.0
        #axial compressive buckling factor
        n=1.0 #both ends simply supported
        Cx=max([1-(0.4*L/R*sqrt(wt/R)-0.2)/n,0.6])
        Cphi=n
        
        #ideal buckling stress for axial compression
        sigmxi=0.605*self.Ed*Cx*wt/R
        
        #reduced slenderness of shell for axial compressive loading
        lambdasx=sqrt(self.sigmY/sigmxi)
        if lambdasx <= 0.25:
            kx=1.0
        elif lambdasx <= 1.0:
            kx=1.233-0.933*lambdasx
        elif lambdasx <= 1.5:
            kx=0.3/(lambdasx**3)
        else:
            kx=0.2/(lambdasx**2)
            
        #Calculate aditional material factor
        if lambdasx <= 0.25:
            Ym=1.0*Safety_factors.stored_data.partial_safety_material_uls
        elif lambdasx <= 2.0:
            Ym=(1.0+0.318*(lambdasx-0.25)/1.75)*Safety_factors.stored_data.partial_safety_material_uls
        else:
            Ym=1.45*Safety_factors.stored_data.partial_safety_material_uls
            
        #calculate ultimate buckling stress
        sigmxu=kx*self.sigmY/Ym
        
        #calculate ideal buckling stress check circumferential compressive loading
        sigmphii=(self.Ed*(wt/R)**2)*(0.275+2.03*(Cphi/(L/R*sqrt(wt/R)))**4)       
        
        #calculate reduced slenderness of the shell for circumferential compressive loading
        lambdasphi=sqrt(self.sigmY/sigmphii)
        
        #calculate refuction factor as function of reduced slenderness
        if lambdasphi <= 0.4:
            kphi=1.0
        elif lambdasphi <= 1.2:
            kphi=1.274-0.686*lambdasphi
        else:
            kphi=0.65/(lambdasphi**2)
        
        #calculate ultimate buckling stress from circumerential compressive loading
        sigmphiu=kphi*self.sigmY/Ym
        
        #calculate combined loading
        ratio=(sigmxi/sigmxu)**1.25 + (sigmphii/sigmphiu)**1.25
            
        return ratio-1
                
    def area(self,D,wt):
        return pi/4.0*(D**2-(D-2*wt)**2)
        
    def inertia(self,D,wt):
        return pi/64.0*(D**4-(D-2*wt)**4)
                    
class Sleeve_calculation:
    def __init__(self,wireframe,loadlist,memberload,baydimensions):
        self.wireframe=wireframe
        self.loadlist=loadlist
        self.memberload=memberload
        self.baydimensions=baydimensions
        self.sleevelist=[]
        self.sigmY=Input_data.stored_data.sigmY
        
    def printlist(self,sleevelist):
        print()
        print('sleevelist[i]    = Datalist per bay')
        print('sleevelist[i][j] = Sleeve information data')
        print('sleevelist[i][0] = ADDITIONAL required leg wall thickness')
        print('sleevelist[i][1] = ADDITIONAL required brace wall thickness')
        print('sleevelist[i][2] = Leg sleeve length')
        print('sleevelist[i][3] = Brace sleeve length')
        print('sleevelist[i][4] = Stress concentration factor (SCF) leg')
        print('sleevelist[i][5] = Stress concentration factor (SCF) brace')
        print('sleevelist[i][6] = total additonal load of bay (N) due to total sleeve weight')
        for bay in range(len(sleevelist)):
            print('bay',bay+1,sleevelist[bay])
            
        text=open('Data-Jacket.txt','a')
        text.write('\n'+'sleevelist[i]    = Datalist per bay'+'\n')
        text.write('sleevelist[i][j] = Sleeve information data'+'\n')
        text.write('sleevelist[i][0] = ADDITIONAL required leg wall thickness'+'\n')
        text.write('sleevelist[i][1] = ADDITIONAL required brace wall thickness'+'\n')
        text.write('sleevelist[i][2] = Leg sleeve length'+'\n')
        text.write('sleevelist[i][3] = Brace sleeve length'+'\n')
        text.write('sleevelist[i][4] = Stress concentration factor (SCF) leg'+'\n')
        text.write('sleevelist[i][5] = Stress concentration factor (SCF) brace'+'\n')
        text.write('sleevelist[i][6] = total additonal load of bay (N) due to total sleeve weight'+'\n')
        for bay in range(len(sleevelist)):
            text.write('bay '+str(bay+1)+' '+str(sleevelist[bay])+'\n')
        text.close()
            
    def calculate(self):
        #First we calculate the dimensions of the sleeves
        self.Kjoint()
        #Then we calculate the additional weight effect on the load in the structure
        #This load is not optimized again, it only has effect on the base loads for the foundation pile calculation
        self.add_sleeve_load()
        return self.sleevelist,self.loadlist
        
    def Kjoint(self):
        memberload=self.memberload
        baydimensions=self.baydimensions
        #SCF method adopted from API RP2A page 211 Efthymiou method
        for bay in range(len(self.wireframe)):
            #Basiq required values
            Dleg=baydimensions[bay][0]
            Dbrace=baydimensions[bay][1]
            wtleg=baydimensions[bay][2]
            wtbrace=baydimensions[bay][3]
            Lleg=self.wireframe[bay][1]*(1+self.wireframe[bay][15])
            Lbrace=self.wireframe[bay][5]
            Lsleeveleg=Lleg/20.0
            Lsleevebrace=Lbrace/20.0
            
            #values to compute stress concentration factors
            beta=Dbrace/Dleg
            gamma=Dleg/(2*wtleg)
            tau=wtbrace/wtleg
            #alpha=2*Lleg/Dleg
            phi=radians(self.wireframe[bay][2])
            xi=(tan(phi)*Dleg/2.0)/Dleg*2.0 #ratio between gap between braces and leg diameter
            
            #maximum loads
            Flegmax=max(memberload[bay][0],memberload[bay][1])
            Fbracemax=max(memberload[bay][2],memberload[bay][3])
            
            #SCF calculation
            SCFleg=tau**0.9*gamma*0.5*(0.67-beta**2+1.16*beta)*sin(phi)*(1.64+0.29*beta**-0.38*atan(8*xi))
            SCFbrace=1+SCFleg*(1.97-1.57*beta**0.25)*tau**-0.14*(sin(phi))**0.7+beta**(1.5*gamma**0.5*tau**-1.22*(sin(2*phi))**1.8)*(0.131-0.084*atan(14*xi+4.2*beta))
            
            #This the additional stress at the leg and brace are:
            Flegmax=Flegmax*SCFleg
            Fbracemax=Fbracemax*SCFbrace
            
            #The new required diameter to overcome this stress is
            Dinnerleg=Dleg-wtleg
            Dinnerbrace=Dbrace-wtbrace
            try:
                wtlegnew=brentq(self.yieldcheck,wtleg,10.0,args=(Dinnerleg,Flegmax))
            except ValueError:
                #If we get an error here that means that the new found brace thickness due to YIELD is smaller as the already existing
                #wall thickness due to yield and buckling. In that case no addional wall thickness is thus required.
                wtlegnew=wtleg
            
            try:
                wtbracenew=brentq(self.yieldcheck,wtbrace,10.0,args=(Dinnerbrace,Fbracemax))
            except ValueError:
                wtbracenew=wtbrace
                
            
            #This the increased thickness is:
            wtlegincrease=wtlegnew-wtleg
            wtbraceincrease=wtbracenew-wtbrace
            
            #Thus the additional volume is:
            Alegincrease=self.area(wtlegincrease,Dleg)
            Vlegincrease=Alegincrease*Lsleeveleg
            Vlegtotincrease=16*Vlegincrease
            Abraceincrease=self.area(wtbraceincrease,Dbrace)
            Vbraceincrease=Abraceincrease*Lsleevebrace
            Vbracetotincrease=8*Vbraceincrease
            
            #This the additional weight of this bay is:
            Fzbay_sleeve=int(9.81*8000*(Vlegtotincrease+Vbracetotincrease))
            
            self.sleevelist.append([wtlegincrease,wtbraceincrease,Lsleeveleg,Lsleevebrace,SCFleg,SCFbrace,Fzbay_sleeve])
        
    def add_sleeve_load(self):
        Fsleevestop=0.0
        Fsleevesbottom=0.0
        for bay in range(len(self.wireframe)):
            Fsleevestop=Fsleevesbottom
            Fsleevesbottom=self.sleevelist[bay][6]+Fsleevesbottom
            for angle in range(len(self.loadlist[bay])):
                for loadcase in range(len(self.loadlist[bay][angle])):
                    self.loadlist[bay][angle][loadcase][0][2]=self.loadlist[bay][angle][loadcase][0][2]+Fsleevestop
                    self.loadlist[bay][angle][loadcase][1][2]=self.loadlist[bay][angle][loadcase][1][2]+Fsleevesbottom
            
        
    def area(self,wt,D):
        #Area calculated from inner diameter
        return pi/4.0*((D+2*wt)**2-D**2)
        
    def yieldcheck(self,wt,D,F):
        return F/self.area(wt,D)- self.sigmY
        
class Final_weight:
    def __init__(self,Wireframe,Jacket_dimensions,Sleeve_dimensions):
        self.Wireframe=Wireframe
        self.Jacket_dimensions=Jacket_dimensions
        self.Sleeve_dimensions=Sleeve_dimensions
        self.rho_steel=7850
    
    def calculate(self):
        Jacket=self.Jacket_dimensions
        Sleeve=self.Sleeve_dimensions
        Wire=self.Wireframe
        Volume=0.0
        for bay in range(len(Wire)):
            Vleg=4*self.volume(Jacket[bay][0],Jacket[bay][2],Wire[bay][1]*(1.0+Wire[bay][15]))
            Vbrace=8*self.volume(Jacket[bay][1],Jacket[bay][3],Wire[bay][5])
            Vlegsleeve=8*self.volume(Jacket[bay][0],Sleeve[bay][0],Sleeve[bay][2])
            Vbracesleeve=16*self.volume(Jacket[bay][1],Sleeve[bay][1],Sleeve[bay][3])
            Volume=Volume+Vleg+Vbrace+Vlegsleeve+Vbracesleeve
            
        Mass_jacket=Volume*self.rho_steel*9.81
        
        return Mass_jacket
        
    def volume(self,D,wt,L):
        return self.area(D,wt)*L
        
    def area(self,D,wt):
        return pi/4.0*(D**2-(D-2*wt)**2)
        
def Calculate_jacket():
    text=open('Data-Jacket.txt','w')
    text.truncate()
    text.close()
    
    #Loadcase environmental information
    LCenv=Site_conditions.stored_data.LCcompilation
    #Elevation heights note these are all with respect to SWL
    Hinterface = Elevations.stored_data.Hinterface
    Hmudline= Elevations.stored_data.Hmudline
    Hmaxwet= Elevations.stored_data.Hcrest
    Hdepth = Input_data.stored_data.Hdepth #this value is absolute!!!
    Surge = Input_data.stored_data.Surge
    HAT = Input_data.stored_data.HAT
    density_water = Input_data.stored_data.RHOwater
    #Tower information
    Dtower=Tower.stored_data.Dbottom
    LCtower=Tower.stored_data.loadbottom
    
    #First the wireframe is built
    frame=Wireframe_builder(Dtower,Hinterface,Hdepth)
    Wireframe=frame.build()
    
    #Second inital dimensions are estimated
    dimension=Dimension_builder(Wireframe)
    Guessed_dimensions=dimension.guess()
    
    #Third equivalent diameters are estimated
    equivalent=Equivalent_diameter_builder(Wireframe)
    Equivalent_dimensions=equivalent.builder(Guessed_dimensions)
    
    #Fourth loads per bay are calculated
    bayload=Bay_load_calculator(Wireframe,LCenv,LCtower,Hmudline,Hinterface,Hmaxwet,Hdepth,Surge,HAT,density_water)
    Environmental_load_per_bay=bayload.calculate_environmental_load_per_bay(Equivalent_dimensions)
    Gravitational_load_per_bay=bayload.calculate_gravitational_load_per_bay(Guessed_dimensions)
    
    #Fifth total loading per bay is calculated
    Loads_summed=bayload.calculate_load_summed(Environmental_load_per_bay, Gravitational_load_per_bay)
    
    #Sixth member loads are calculated
    member=Member_load_calculator(Wireframe)
    Membersort,Memberload,Reactivelist=member.calculate(Loads_summed)
    
    #Seventh mamximum loads per bay are picked per bay per loadcase
    maxloads=Maximum_load_selecter(Wireframe)
    Maximum_loads,Maximum_loc=maxloads.select(Membersort)
    
    #Eighth minimal required diameter for loads is calculated for solid member
    optimizer=Dimension_optimizer(Wireframe,Guessed_dimensions,equivalent,bayload,member,maxloads)
    Minimal_dimensions=optimizer.calculate_minimal_dimensions(Maximum_loads)
    
    #Ninth optimal structure is calculated
    Optimal_dimensions=optimizer.calculate_optimal_dimensions(Minimal_dimensions)
    
    #Tenth sleeve dimensions are calculated
    sleeves=Sleeve_calculation(Wireframe,optimizer.Loads_summed,optimizer.Maximum_loads,Optimal_dimensions)
    Sleevelist,Loads_summed=sleeves.calculate()
    
    #Eleventh jacket weight is calculated
    weight=Final_weight(Wireframe,Optimal_dimensions,Sleevelist)
    stored_data.weight=weight.calculate()
    
    #Finally the optimal data is printed
    frame.printlist(Wireframe)
    Guessed_dimensions=optimizer.guess_dimensions
    dimension.printlist(Guessed_dimensions)
    Equivalent_dimensions=optimizer.Equivalent_dimensions
    equivalent.printlist(Equivalent_dimensions)
    Environmental_load_per_bay=optimizer.Environmental_load_per_bay
    Gravitational_load_per_bay=optimizer.Gravitational_load_per_bay
    bayload.printlistENVPERBAY(Environmental_load_per_bay)
    bayload.printlistGRAVPERBAY(Gravitational_load_per_bay)
    bayload.printlistTOTAL(Loads_summed)
    Membersort=optimizer.Membersort
    member.printlist(Membersort)
    Maximum_loads=optimizer.Maximum_loads
    Maximum_loc=optimizer.Maximum_loc
    maxloads.printlist(Maximum_loads,Maximum_loc)
    optimizer.printlistMIN(Minimal_dimensions)
    optimizer.printlistOPT(Optimal_dimensions)
    sleeves.printlist(Sleevelist)
    
    #Now data is stored for the pile module
    stored_data.wireframe=Wireframe
    stored_data.loads=Loads_summed
    stored_data.membersort=optimizer.Membersort
    stored_data.memberload=optimizer.Memberload
    stored_data.reactivelist=optimizer.Reactivelist
    stored_data.environmental_loads_per_bay=Environmental_load_per_bay
    stored_data.gravitational_loads_per_bay=Gravitational_load_per_bay
    stored_data.Jacket_dimensions=Optimal_dimensions
    stored_data.Sleeve_dimensions=Sleevelist
    
    text=open('Data-Jacket.txt','a')
    text.write('\n'+'stored data'+'\n')
    text.write('Wireframe'+'\n')
    text.write(str(stored_data.wireframe)+'\n')
    text.write('loads'+'\n')
    text.write(str(stored_data.loads)+'\n')
    text.write('environmental_loads_per_bay'+'\n')
    text.write(str(stored_data.environmental_loads_per_bay)+'\n')
    text.write('gravitational_loads_per_bay'+'\n')
    text.write(str(stored_data.gravitational_loads_per_bay)+'\n')
    text.write('memberload'+'\n')
    text.write(str(stored_data.memberload)+'\n')
    text.write('Jacket_dimensions'+'\n')
    text.write(str(stored_data.Jacket_dimensions)+'\n')
    text.write('Sleeve_dimensions'+'\n')
    text.write(str(stored_data.Sleeve_dimensions)+'\n')
    text.write('weight'+'\n')
    text.write(str(stored_data.weight)+'\n')
    text.write('membersort'+'\n')
    text.write(str(stored_data.membersort)+'\n')
    text.write('reactivelist'+'\n')
    text.write(str(stored_data.reactivelist)+'\n')
    text.close()