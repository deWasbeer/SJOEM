# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 10:47:56 2015

@author: Johan Antonissen (windhoos@gmail.com)
"""

from . import Input_data, Jacket
from math import pi,sqrt,sin,tan,degrees,radians,exp
from scipy.optimize import brentq,basinhopping

class stored_data:
    def __init__(self):
        self.pile_dimensions=0.0
        self.mudline_loads=0.0
        self.pile_top_loads=0.0
        self.weight=0.0
        
class Pile_dimensioning:
    def __init__(self,wireframe,jacket_dimensions):
        self.wireframe=wireframe
        self.jacket_dimensions=jacket_dimensions
        self.Width0=0.0
        self.Width45=0.0
        
        self.dimension=0.0
        self.distances=0.0
        
    def location(self):
        #For the jacket piles are assumed to have no inclination
        #Thus distance between piles is always equal
        jacket_base_width=self.wireframe[-1][4]
        self.Width0=jacket_base_width
        self.Width45=jacket_base_width*sqrt(2)
        self.distances=[self.Width0,self.Width45]
        return self.distances
        
    def area(self,D,wt):
        return pi/4.0*(D**2-(D-2*wt)**2)
        
    def volume(self,D,wt,L):
        return self.area(D,wt)*L
        
    def guess_dimensions(self):
        Dpile=self.jacket_dimensions[-1][0]
        wtpile=self.jacket_dimensions[-1][2]
        Lpile=Dpile*10
        Vpile=self.volume(Dpile,wtpile,Lpile)
        de=Dpile*3.0 #Estimated location where bending moment is zero in piles
        self.dimension=[Dpile,wtpile,Lpile,Vpile,de]
        
        return self.dimension
        
class Load_estimation:
    def __init__(self,Pile_distances,Loads,Reactivelist):
        self.Pile_distances=Pile_distances
        self.Loads=Loads
        self.Reactive=Reactivelist
        self.Dimensions=[0.0,0.0,0.0,0.0,0.0] #Dpile,wtpile,Lpile,Vpile,de
        self.phiPE=0.8
        self.pile_top_loads=0
        
    def printlistLOADS(self,pile_top_loads):
        print()
        print('Pile_top_loads[i]       = loadlist for inflow angle 0 [0] and 45 [1]')
        print('Pile_top_loads[i][j]    = loadlist for loadcase j')
        print('Pile_top_loads[i][j][k] = loadlist for pile 1 [0] at the front to 4 [3] at the back')
        print('                          list in order of [fx,fy,fz,mx,my,mz]')
        print(' numbering as follows:     2-------3                3 ')
        print('                           |       |               / \ ')
        print('          ------>          |       |              1   4 ')
        print('                           |       |               \ / ')
        print('                           1-------4                2 ')
        
        for angle in range(len(pile_top_loads)):
            for LC in range(len(pile_top_loads[angle])):
                for pile in range(len(pile_top_loads[angle][LC])):
                    if angle==0:
                        inflow='0'
                    else:
                        inflow='45'
                    print('angle',inflow,'LC',LC+1,'pile',pile+1,pile_top_loads[angle][LC][pile])  
                    
        text=open('Data-Piles.txt','a')
        text.write('\n'+'Pile_top_loads[i]       = loadlist for inflow angle 0 [0] and 45 [1]'+'\n')
        text.write('Pile_top_loads[i][j]    = loadlist for loadcase j'+'\n')
        text.write('Pile_top_loads[i][j][k] = loadlist for pile 1 [0] at the front to 4 [3] at the back'+'\n')
        text.write('                          list in order of [fx,fy,fz,mx,my,mz]'+'\n')
        text.write(' numbering as follows:     2-------3                3 '+'\n')
        text.write('                           |       |               / \ '+'\n')
        text.write('          ------>          |       |              1   4 '+'\n')
        text.write('                           |       |               \ / '+'\n')
        text.write('                           1-------4                2 '+'\n')
        
        for angle in range(len(pile_top_loads)):
            for LC in range(len(pile_top_loads[angle])):
                for pile in range(len(pile_top_loads[angle][LC])):
                    if angle==0:
                        inflow='0'
                    else:
                        inflow='45'
                    text.write('angle '+str(inflow)+' LC '+str(LC+1)+' pile '+str(pile+1)+' '+str(pile_top_loads[angle][LC][pile])+'\n')
        text.close()
                
    def printlist(self,pile_dimensions):
        print()
        print('Pile_dimensions[i] = Dimensions of foundation piles')
        print('Pile_dimensions[i] = Dpile')
        print('Pile_dimensions[i] = wtpile')
        print('Pile_dimensions[i] = Lpile')
        print('Pile_dimensions[i] = Vpile')
        print('Pile_dimensions[i] = depile (estimated inclination depth)')
        print(pile_dimensions)
        
        text=open('Data-Piles.txt','a')
        text.write('\n'+'Pile_dimensions[i] = Dimensions of foundation piles'+'\n')
        text.write('Pile_dimensions[i] = Dpile'+'\n')
        text.write('Pile_dimensions[i] = wtpile'+'\n')
        text.write('Pile_dimensions[i] = Lpile'+'\n')
        text.write('Pile_dimensions[i] = Vpile'+'\n')
        text.write('Pile_dimensions[i] = depile (estimated inclination depth)'+'\n')
        text.write(str(pile_dimensions)+'\n')
        text.close()
        
    def calculate_mudline_loads(self):
        #Estimate loads at mudline for each loadcase
        #for the 0 degree inflow angle
        LC1A0=self.Loads[-1][0][0][1]
        LC2A0=self.Loads[-1][0][1][1]
        LC3A0=self.Loads[-1][0][2][1]
        #for the 45 degree inflow angle
        LC1A45=self.Loads[-1][1][0][1]
        LC2A45=self.Loads[-1][1][1][1]
        LC3A45=self.Loads[-1][1][2][1]
        
        return [[LC1A0,LC2A0,LC3A0],[LC1A45,LC2A45,LC3A45]]
        
    def calculate_pile_top_loads(self,Mudline_loads,Pile_dimensions):
        #first for the 0 degree inflow angle
        pile_top_loads=[[],[]]
        for LC in range(len(Mudline_loads[0])):
            pile_top_loads[0].append([])
            base_shear_global0=Mudline_loads[0][LC][0]
            gravitational_load_global0=Mudline_loads[0][LC][2]
            overturning_moment_global0=Mudline_loads[0][LC][4]
            #Now we devide these by two to get the loads for half the frame
            base_shear=base_shear_global0/2.0
            gravitational_load=gravitational_load_global0/2.0
            overturning_moment=overturning_moment_global0/2.0
            reactivediff=self.Reactive[-1][0][LC]
            for pile in range(4):
                pile_top_loads[0][LC].append([0.0,0.0,0.0,0.0,0.0,0.0])
                #Note 'positive' is pointing upwards (fz),from left to right (fz) and with the direction of the clock (my) 
                #now load at pile 1 and 2 (front) are:
                if (pile == 0) or (pile == 1) :
                    fxpile12=base_shear/2.0+reactivediff[0][0] #TODO: added Rdiff
                    fzpile12=-gravitational_load/2.0+(overturning_moment+base_shear*Pile_dimensions[4])/self.Pile_distances[0]+reactivediff[0][2] #TODO: added Rdiff
                    mypile12=fxpile12*Pile_dimensions[4]
                    pile_top_loads[0][LC][pile][0]=int(fxpile12)
                    pile_top_loads[0][LC][pile][2]=int(fzpile12)
                    pile_top_loads[0][LC][pile][4]=int(mypile12)

                #and pile 3 and 4 (back) are:
                elif (pile == 2) or (pile == 3):
                    fxpile34=base_shear/2.0+reactivediff[1][0] #TODO: added Rdiff
                    fzpile34=-gravitational_load/2.0-(overturning_moment+base_shear*Pile_dimensions[4])/self.Pile_distances[0]+reactivediff[1][2] #TODO: added Rdiff
                    mypile34=fxpile34*Pile_dimensions[4]
                    pile_top_loads[0][LC][pile][0]=int(fxpile34)
                    pile_top_loads[0][LC][pile][2]=int(fzpile34)
                    pile_top_loads[0][LC][pile][4]=int(mypile34)
        
        #now for the 45 degree inflow angle
        for LC in range(len(Mudline_loads[1])):
            pile_top_loads[1].append([])
            base_shear_global45=Mudline_loads[1][LC][0]
            gravitational_load_global45=Mudline_loads[1][LC][2]
            overturning_moment_global45=Mudline_loads[1][LC][4]
            reactivediffL=self.Reactive[-1][1][LC]
            reactivediffR=self.Reactive[-1][2][LC]
            #here we do not devide by two since we we consider a 3D frame
            for pile in range(4):
                pile_top_loads[1][LC].append([0.0,0.0,0.0,0.0,0.0,0.0])
                #for the first pile (front)
                if pile == 0:
                    fxpile1=base_shear_global45/4.0+reactivediffL[0][0]/sqrt(2)+reactivediffL[0][1]/sqrt(2) #TODO: added Rdiff
                    fzpile1=-gravitational_load_global45/4.0+overturning_moment_global45/self.Pile_distances[1] +4*fxpile1*Pile_dimensions[4]/self.Pile_distances[1]+reactivediffL[0][2] #TODO: added Rdiff
                    mypile1=fxpile1*Pile_dimensions[4]
                    
                    pile_top_loads[1][LC][pile][0]=int(fxpile1)
                    pile_top_loads[1][LC][pile][2]=int(fzpile1)
                    pile_top_loads[1][LC][pile][4]=int(mypile1)
                elif (pile == 1) or (pile == 2):
                #for the two piles in the middle
                    fxpile23=base_shear_global45/4.0+reactivediffL[1][0]/sqrt(2)+reactivediffL[1][1]/sqrt(2) #TODO: added Rdiff
                    fzpile23=-gravitational_load_global45/4.0+reactivediffL[1][2] #TODO: added Rdiff
                    mypile23=fxpile23*Pile_dimensions[4]
                    
                    pile_top_loads[1][LC][pile][0]=int(fxpile23)
                    pile_top_loads[1][LC][pile][2]=int(fzpile23)
                    pile_top_loads[1][LC][pile][4]=int(mypile23)
                elif pile == 3:
                #for the last pile (back)
                    fxpile4=base_shear_global45/4.0+reactivediffR[1][0]/sqrt(2)+reactivediffR[1][1]/sqrt(2) #TODO: added Rdiff
                    fzpile4=-gravitational_load_global45/4.0-overturning_moment_global45/self.Pile_distances[1] - 4*fxpile4*Pile_dimensions[4]/self.Pile_distances[1]+reactivediffR[1][2] #TODO: added Rdiff
                    mypile4=fxpile4*Pile_dimensions[4]
                    
                    pile_top_loads[1][LC][pile][0]=int(fxpile4)
                    pile_top_loads[1][LC][pile][2]=int(fzpile4)
                    pile_top_loads[1][LC][pile][4]=int(mypile4)
                    
        self.pile_top_loads=pile_top_loads   
        
        return pile_top_loads
        
    def calculate_minimum_diameter(self,pile_top_loads):
        Dmin=0.0
        for angle in range(len(pile_top_loads)):
            for LC in range(len(pile_top_loads[angle])):
                for pile in range(len(pile_top_loads[angle][LC])):
                    pile_load=pile_top_loads[angle][LC][pile]
                    D=brentq(self.yieldtestSOLID,0.1,10.0,args=(pile_load,))
                    if D >= Dmin:
                        Dmin=D
        return Dmin
                    
    def yieldtestSOLID(self,D,pile_load):
        fx=pile_load[0]
        fz=pile_load[2]
        my=pile_load[4]
        sigmX=abs(fx/self.area(D,D/2.0))
        sigmZ=abs(fz/self.area(D,D/2.0))+abs(my*D*0.5/self.inertia(D,D/2.0))
        sigmTOT=sqrt(sigmX**2+sigmZ**2)
        return sigmTOT-Input_data.stored_data.sigmY
        
    def calculate_pile_dimensions(self,D,pile_top_loads,Dmin):
        D=D[0]
        #First we determine the minimum required wall thickness of the investigated diameter
        wtMAX=0.0
        for angle in range(len(pile_top_loads)):
            for LC in range(len(pile_top_loads[angle])):
                for pile in range(len(pile_top_loads[angle][LC])):
                    pile_load=pile_top_loads[angle][LC][pile]
                    #We calculate the minimum required wall thickness of the investigated pile diameter
                    wtYIELD=brentq(self.yieldtest,0.000001,D/2.0,args=(D,pile_load)) #minimum wall thickness toprevent yield
                    wtPILEDRIVE=0.00634+D/100.0 #minimum wall thickness to be able to drive pile in soil API PAGE 73
                    wt=max(wtYIELD,wtPILEDRIVE)
                    if wt >= wtMAX:
                        wtMAX=wt
                        
        LpileMAX=0.0
        #second we determine the pile maximum required length to withstand lateral loads
        for angle in range(len(pile_top_loads)):
            for LC in range(len(pile_top_loads[angle])):
                for pile in range(len(pile_top_loads[angle][LC])):
                    pile_load=pile_top_loads[angle][LC][pile]
                    Lpile=self.pile_length_from_lateral_capacity(D,pile_load)
                    if Lpile >= LpileMAX:
                        LpileMAX=Lpile
                        
                        
        #Third we determine the pile maximum required length to withstand axial loads
        for angle in range(len(pile_top_loads)):
            for LC in range(len(pile_top_loads[angle])):
                for pile in range(len(pile_top_loads[angle][LC])):
                    pile_load=pile_top_loads[angle][LC][pile]
                    Lpile=brentq(self.pile_length_from_axial_capacity,0.01,5000.0,args=(pile_load,D,wt))
                    if Lpile >= LpileMAX:
                        LpileMAX=Lpile
            
        self.Dimensions[0]=D
        self.Dimensions[1]=wtMAX
        self.Dimensions[2]=LpileMAX
        self.Dimensions[3]=self.volume(D,wtMAX,LpileMAX)
        self.Dimensions[4]=D*3.0
                        
        return self.volume(D,wtMAX,LpileMAX)
        
    def pile_length_from_lateral_capacity(self,D,loadcase_loads):
        #Blum's method
        fx=abs(loadcase_loads[0])
        my=abs(loadcase_loads[4])
        phiSOIL=Input_data.stored_data.PHIsoil
        rhoSOIL=Input_data.stored_data.RHOsoil
        n=2.0 #to include 3D effect
        Kp=(1+sin(phiSOIL))/(1-sin(phiSOIL))
        Ka=(1-sin(phiSOIL))/(1+sin(phiSOIL))
        lpile=brentq(self.blum,0.01,50.0,args=(D,fx,my,rhoSOIL,self.phiPE,n,Kp,Ka))
        lpile=int(lpile*1.3*100)/100.0
        return lpile
            
    def blum(self,Lpile,D,fx,my,rhoSOIL,phiPE,n,Kp,Ka):
        return phiPE*n*(Kp-Ka)*rhoSOIL*D*Lpile**2-6*(fx+my/Lpile)
            
    def pile_length_from_axial_capacity(self,L,pile_load,D,wt):
        K0=0.8
        delta=radians(degrees(Input_data.stored_data.PHIsoil)-10)
        Foutside=0.5*K0*tan(delta)*Input_data.stored_data.RHOsoil*pi*D**2*L**2
        Finside=0.5*K0*tan(delta)*Input_data.stored_data.RHOsoil*pi*(D-2*wt)**2*L**2
        Sq=1+sin(Input_data.stored_data.PHIsoil)
        Nq=(1+sin(Input_data.stored_data.PHIsoil))/(1-sin(Input_data.stored_data.PHIsoil))*exp(pi*tan(Input_data.stored_data.PHIsoil))
        P0=Input_data.stored_data.RHOsoil*L
        Qc=Sq*Nq*P0
        A_pile_end=pi/4.0*D**2
        Fendbear=Qc*A_pile_end
        if Finside >= Fendbear:
            #pile is plugged
            Fresistance=self.phiPE*(Foutside+Fendbear)
        else:
            #pile is not plugged
            Fresistance=self.phiPE*(Foutside+Finside)
            
        fz=abs(pile_load[2])
        return fz-Fresistance
            
    def yieldtest(self,wt,D,pile_load):
        fx=pile_load[0]
        fz=pile_load[2]
        my=pile_load[4]
        sigmX=abs(fx/self.area(D,wt))
        sigmZ=abs(fz/self.area(D,wt))+abs(my*D*0.5/self.inertia(D,wt))
        sigmTOT=sqrt(sigmX**2+sigmZ**2)
        return sigmTOT-Input_data.stored_data.sigmY
            
    def area(self,D,wt):
        return pi/4.0*(D**2-(D-2*wt)**2)
            
    def inertia(self,D,wt):
        return pi/64.0*(D**4-(D-2*wt)**4)
        
    def volume(self,D,wt,L):
        return self.area(D,wt)*L

def Calculate_piles():
    text=open('Data-Piles.txt','w')
    text.truncate()
    text.close()
    
    #First we get data to make calculations with
    Wireframe=Jacket.stored_data.wireframe
    LCjacket=Jacket.stored_data.loads
    Reactivelist=Jacket.stored_data.reactivelist
    
    Jacket_dimensions=Jacket.stored_data.Jacket_dimensions
    #d50=Input_data.stored_data.d50 Not used?
    #d90=Input_data.stored_data.d90 Not used?
    
    #Second the location of the piles is determined
    pile=Pile_dimensioning(Wireframe,Jacket_dimensions)
    Pile_distances=pile.location()
    Initial_dimensions=pile.guess_dimensions()
    
    #Third loads at the pile top are estimated
    loads=Load_estimation(Pile_distances,LCjacket,Reactivelist)
    Mudline_loads=loads.calculate_mudline_loads()
    
    #Fourth optimal pile dimensions are estimated
    Dimensions=Initial_dimensions
    Vnew=Dimensions[4]
    Ratio=10.0
    while Ratio >= 1.01:
        Vold=Vnew
        Pile_top_loads=loads.calculate_pile_top_loads(Mudline_loads,Dimensions)
        Dmin=loads.calculate_minimum_diameter(Pile_top_loads)
        Dminbound=[Dmin*1.01]
        Dmaxbound=[Dmin*10.0+5.0]
        D0=[Dmin*1.1]#,Minimal_dimensions[bay][0]*1.2]
        bounds=[(low, high) for low, high in zip(Dminbound, Dmaxbound)]
        minimizer_kwargs = dict(method="L-BFGS-B", bounds=bounds, args=(Pile_top_loads,Dmin*1.01))
        #Fifth optimal pile dimensions are iterated to
        basinhopping(loads.calculate_pile_dimensions,D0,minimizer_kwargs=minimizer_kwargs)
        Dimensions=loads.Dimensions
        Vnew=Dimensions[3]
        if Vold >= Vnew:
            Ratio=Vold/Vnew
        else:
            Ratio=Vnew/Vold
            
    #Print the outcomes
    loads.printlistLOADS(Pile_top_loads)
    loads.printlist(Dimensions)
            
    #Now data is stored
    stored_data.pile_dimensions=Dimensions
    stored_data.pile_top_loads=Pile_top_loads
    stored_data.mudline_loads=Mudline_loads
    stored_data.weight=4*Dimensions[3]*7850*9.81
    
    text=open('Data-Piles.txt','a')
    text.write('\n'+'stored data'+'\n')
    text.write('mudline_loads'+'\n')
    text.write(str(stored_data.mudline_loads)+'\n')
    text.write('pile_top_loads'+'\n')
    text.write(str(stored_data.pile_top_loads)+'\n')
    text.write('pile_dimensions'+'\n')
    text.write(str(stored_data.pile_dimensions)+'\n')
    text.write('weight'+'\n')
    text.write(str(stored_data.weight)+'\n')
    text.close()