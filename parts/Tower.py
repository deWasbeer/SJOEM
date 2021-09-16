# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 10:45:15 2015

@author: Johan Antonissen (windhoos@gmail.com)
"""

from . import Input_data,Site_conditions, Elevations, Safety_factors ,RNA
from math import pi,sqrt
from scipy.optimize import brentq,basinhopping

class stored_data:
    def __init__(self):
        self.Htower=0.0
        self.Dtop=0.0
        self.wttop=0.0
        self.Dbottom=0.0
        self.wtbottom=0.0
        self.Tower_dimensions=0.0
        self.Tower_loads=0.0
        self.weight=0.0
        self.loadbottom=[]
        
class Calculation:
    def __init__(self):
        self.sigmY=Input_data.stored_data.sigmY
        self.Ed=Input_data.stored_data.Ed
        self.v=0.287 #Poisson ratio
        self.rho=1.225
        self.Cd=1.2
        self.Dsegment = 0.0
        self.wtsegment = 0.0
        self.Asegment = 0.0
    
    def area(self,D,wt):
        A=pi/4.0*(D**2-(D-2*wt)**2)
        return A
        
    def inertia(self,D,wt):
        I=pi/64.0*(D**4-(D-2*wt)**4)
        return I
        
    def yieldcheck(self,wt,D,loadlist):
        fx=loadlist[0]
        fz=loadlist[2]
        my=loadlist[4]
        sigmZ=fz/self.area(D,wt) + my*D/2.0/self.inertia(D,wt)
        sigmX=fx/self.area(D,wt)
        return  sqrt(sigmX**2+sigmZ**2) - self.sigmY
    
    def drag(self,D,H,U):
        Fdrag=0.5*self.Cd*U**2*D*H*self.rho*Safety_factors.stored_data.ScombENV
        return Fdrag
        
    def weight(self,D,wt,H):
        V=pi/4.0*(D**2-(D-2*wt)**2)*H
        Fg=V*8000.0*9.81*Safety_factors.stored_data.ScombGRAV
        return Fg
        
    def overhang_moment(self,Rsegment,Rtop,Helement,Htower,Blade_deflection):
        #Here the diameter at the bottom is calculated by linearizing
        R_bottom=Htower*(Rsegment-Rtop)/Helement+Rtop
        Doverhang=Blade_deflection+5.0+R_bottom #Distance from center tower to tip front nacelle
        Mrna=Input_data.stored_data.Mrna
        Fz=Mrna*9.81
        My=Fz*Doverhang/2.0 #It's assumed that the centre of mass of the RNA is located 1/4 for the overhang distance from the tower center axis
        return My
        
    def euler(self,wt,D,loadlist,L):
        Keff = 0.25
        Rgyra=sqrt(self.inertia(D,wt)/self.area(D,wt)) #Radius of gyration
        slenderness=Keff*L/Rgyra #Slenderness parameter
        slendernessE=pi*sqrt(self.Ed/self.sigmY) #Slenderness Euler limit
        slendernessR=slenderness/slendernessE #Reduced slenderness ratio
        #sigmC=pi**2*self.Ed/slenderness**2 #Euler bucking stress
        sigmY=self.sigmY
        fz=loadlist[2]
        my=loadlist[4]
        if slendernessR <= 1.0:
            sigmMAX=sigmY
            return abs(fz/self.area(D,wt))+abs(my*D/2.0/self.inertia(D,wt))- sigmMAX
        else:
            sigmMAX=sigmY/slendernessR**2
            return abs(fz/self.area(D,wt))+abs(my*D/2.0/self.inertia(D,wt)) - sigmMAX
            
    def find_max_lambda_wt(self,wt,D,loadlist):
        fz=loadlist[2]
        my=loadlist[4]
        radius=D/2
        sigm_ad=fz/(2*pi*radius*wt)
        sigm_bd=my/(pi*radius**2*wt)
        ea=0.83/sqrt(1+0.001*radius/wt)
        eb=0.1887+0.8113*ea
        e=(ea*sigm_ad+eb*sigm_bd)/(sigm_ad+sigm_bd)
        sigm_el=self.Ed/(radius/wt*sqrt(3*(1-0.3**2)))
        lambdaA=sqrt(self.sigmY/(e*sigm_el))
        return lambdaA-1.0
        
    def buckling(self,wt,D,loadlist,H):
        #Buckling accoridng to DNV riso page 177
        R=D/2.0
        fz=loadlist[2]
        my=loadlist[4]
        sigmAD=fz/(2*pi*R*wt)
        sigmBD=my/(pi*R**2*wt)
        Ea=0.83/sqrt(1+0.01*R/wt)
        Eb=0.1887+0.8113*Ea
        E=(Ea*sigmAD+Eb*sigmBD)/(sigmAD+sigmBD)
        sigmEL=self.Ed/(R/wt*sqrt(3*(1-self.v**2)))
        lambdaA=sqrt(self.sigmY/(E*sigmEL))
        if lambdaA <= 0.3:
            sigmCR=self.sigmY
        else:
            sigmCR=(1.5-0.913*sqrt(lambdaA))*self.sigmY
        
        Nel=0.25*pi**2*self.Ed*pi*R**3*wt/(H**2)
        lambdaR=sqrt(sigmCR/(Nel/(2*pi*R*wt)))
        k=R/2.0
        e=0.34*(lambdaR-0.2)*k
        if lambdaR <= 0.2:
            e=0
        if e >= 2/1000.0*H:
            e=2*e-2/1000.0*H
        return fz/(2*pi*R*wt)+Nel/(Nel-fz)*(my+fz*e)/(pi*R**2*wt)-sigmCR
        
    def areaMIN(self,D,DOLD,Dtower_top,LC_data,Loadlist,wtOLD,Hrna,Helement,Htower,Hincrement,Blade_deflection):
        LoadlistTEMP=Loadlist
        try:
            D=D[0]
        except TypeError:
            D=D
            
        wtlist=()
        for LC in range(len(Loadlist)):
            Uelement=Site_conditions.get_wind_speed_at_height(LC_data[LC][0],Helement)
            #First we calculate the altered data trough its changed diameter
            Fx_drag=self.drag((D+DOLD)/2.0,Hincrement,Uelement) #the drag of the element
            Fz_weight=self.weight((D+DOLD)/2.0,wtOLD,Hincrement) #the weight of the element
            My_overhang=self.overhang_moment(D/2.0,Dtower_top/2.0,Helement,Htower,Blade_deflection) #estimated effect of overhang
            LoadlistTEMP[LC][0]=LoadlistTEMP[LC][0]+Fx_drag
            LoadlistTEMP[LC][2]=LoadlistTEMP[LC][2]+Fz_weight
            LoadlistTEMP[LC][4]=LoadlistTEMP[LC][4]+My_overhang-Fx_drag*Hincrement/2.0+LoadlistTEMP[LC][0]*Hincrement
            wtYIELD=    brentq(self.yieldcheck,0.00000000001,D/2.0,args=(D,LoadlistTEMP[LC]))
            wtEULER=    brentq(self.euler,0.0000000000001,D/2.0,args=(D,LoadlistTEMP[LC],Htower))
            wtMAX=      D/200.0 #Penalty value to keep operation within limits
            wtguess=max(wtYIELD,wtEULER,wtMAX)
            try:
                wt_lambda=  brentq(self.find_max_lambda_wt,wtguess,D/2.0,args=(D,LoadlistTEMP[LC]))
                wtmin=max(wtYIELD,wtEULER,wt_lambda)
                wtBUCK=     brentq(self.buckling,wtmin,D/2.0,args=(D,LoadlistTEMP[LC],Htower))
                wt=max(wtYIELD,wtEULER,wtBUCK)
            except ValueError:
                wt=wtguess
            wtlist=wtlist+(wt,)
            
            LoadlistTEMP[LC][4]=LoadlistTEMP[LC][4]-My_overhang+Fx_drag*Hincrement/2.0-LoadlistTEMP[LC][0]*Hincrement
            LoadlistTEMP[LC][0]=LoadlistTEMP[LC][0]-Fx_drag
            LoadlistTEMP[LC][2]=LoadlistTEMP[LC][2]-Fz_weight
            
        wt=max(wtlist)
    
        self.Dsegment = D
        self.wtsegment= wt
        self.Asegment= self.area(D,wt)
        
        return self.area(D,wt)
        
def Calculate_tower():
    RNA_loads = RNA.stored_data.RNAloads
    Blade_deflection=RNA.stored_data.Deflection
    LC_data = Site_conditions.stored_data.LCcompilation
    Hhub = Elevations.stored_data.Hhub
    Hint = Elevations.stored_data.Hinterface
    Htower = abs(Hhub-Hint)
    stored_data.Htower = Htower
    
    #First we calculate the  top of the tower
    DtowerTOP = 3.0 #Any value can be inserted here this value should be equal to RNA width
    stored_data.Dtop = DtowerTOP
    
    top_tower = Calculation()
    wtTOPlist=()
    for i in range(len(LC_data)):
        wtTOP=brentq(top_tower.yieldcheck,0.00000001,DtowerTOP/2.0,args=(DtowerTOP,RNA_loads[i]))
        wtTOPlist=wtTOPlist+(wtTOP,)
    wtTOP=max(wtTOPlist)
    stored_data.wttop=wtTOP
    
    #Now we calculate tower dimensions along its height.
    Steps = 10
    Dtower=DtowerTOP
    Hincrement = Htower/(float(Steps)) #Height of one segment
    Dimensionlist=[]
    Loadlist=[]
    Dimensionlist.append([Hhub, Dtower,wtTOP])
    Loadlist.append(RNA_loads)
    
    #Now we calculate the loads per element
    Segment=Calculation()
    for Step in range(Steps):
        Loadlist.append([])
        Helement=float((Steps-Step))*Hincrement+Hint #Height of top element from MSL
        Hrna=abs(Htower-float((Steps-Step))*Hincrement)+Hincrement #distance from rna to element
        DOLD=Dimensionlist[Step][1]
        wtOLD=Dimensionlist[Step][2]
        #Now we calculate the loads on the tower
        if DOLD >= 5:
            Dmin=[4.5]
        elif DOLD >= 8:
            Dmin=[6.]
        else:
            Dmin=[3.0]
        Dmax=[15.0]
        D0=[Dmin[0]*1.1]
        bounds=[(low, high) for low, high in zip(Dmin, Dmax)]
        minimizer_kwargs = dict(method="L-BFGS-B", bounds=bounds, args=(DOLD,DtowerTOP,LC_data,Loadlist[Step],wtOLD,Hrna,Helement,Htower,Hincrement,Blade_deflection))
        Dsegment=basinhopping(Segment.areaMIN,D0,minimizer_kwargs=minimizer_kwargs)
        Dsegment=Dsegment['x'][0]
        Dimensionlist.append([Helement,Dsegment,Segment.wtsegment])
        for LC in range(len(LC_data)):
            Loadlist[Step+1].append([0.0,0.0,0.0,0.0,0.0,0.0])
            Uelement=Site_conditions.get_wind_speed_at_height(LC_data[LC][0],Helement)
            
            Fx_drag=Segment.drag((Dsegment+DOLD)/2.0,Hincrement,Uelement)
            Fz_weight=Segment.weight((Dsegment+DOLD)/2.0,Segment.wtsegment,Hincrement)
    
            Loadlist[Step+1][LC][0]=int(Loadlist[Step][LC][0]+Fx_drag)
            Loadlist[Step+1][LC][2]=int(Loadlist[Step][LC][2]+Fz_weight)
            Loadlist[Step+1][LC][4]=int(Loadlist[Step][LC][4]+(Loadlist[Step+1][LC][0]-Fx_drag-Fx_drag)*Hincrement)
        
        print('H[m]: ',Helement,', D[m]: ',int(Dsegment*100)/100.0,', wt[cm]: ',int(Segment.wtsegment*10000)/100.0)
        
    #Once all segments are calculated the final effect of overhang is added to the moments
    #During the optimization this value was determined using linerisation
    for Step in range(len(Loadlist)):   
        for LC in range(len(LC_data)):
            Loadlist[Step][LC][4]=int(Loadlist[Step][LC][4]+Segment.overhang_moment(Dimensionlist[-1][1]/2.0,DtowerTOP/2.0,Hint,Htower,Blade_deflection))
     
    stored_data.Tower_loads=Loadlist
    stored_data.Tower_dimensions=Dimensionlist
    stored_data.Dbottom=Dimensionlist[-1][1]
    stored_data.wtbottom=Dimensionlist[-1][2]
    
    #And finally a slab of weight is added to represent acces platform
    loadbottom=Loadlist[-1]
    for LC in range(len(LC_data)):
        Aplatform=stored_data.Dbottom**2
        Hplatform=0.1
        Vplatform=Aplatform*Hplatform
        Fplatformweight=Vplatform*9.81*7850
        Fz=Loadlist[-1][LC][2]
        loadbottom[LC][2]=int(Fz+Fplatformweight)
    
    stored_data.loadbottom = loadbottom
    stored_data.weight= loadbottom[0][2]
    
    print('D towerbottom = ',stored_data.Dbottom)
    print('wt towerbottom = ',stored_data.wtbottom)
    print('Loads tower bottom per load case:')
    for i in range(len(LC_data)):
        print('Loadcase',i+1,'=',stored_data.loadbottom[i])
        
    text=open('Data-Tower.txt','w')
    text.truncate()
    text.write('D towerbottom = '+str(stored_data.Dbottom)+'\n')
    text.write('wt towerbottom = '+str(stored_data.wtbottom)+'\n')
    text.write('Loads tower bottom per load case:'+'\n')
    for i in range(len(LC_data)):
        text.write('Loadcase '+str(i+1)+' = '+str(stored_data.loadbottom[i])+'\n')
    text.write('\n')
    text.write('stored data'+'\n')
    text.write('Htower '+str(stored_data.Htower)+'\n')
    text.write('Dtop '+str(stored_data.Dtop)+'\n')
    text.write('Dbottom '+str(stored_data.Dbottom)+'\n')
    text.write('wttop '+str(stored_data.wttop)+'\n')
    text.write('wtbottom '+str(stored_data.wtbottom)+'\n')
    text.write('weight '+str(stored_data.weight)+'\n')
    text.write('loadbottom '+str(stored_data.loadbottom)+'\n'+'\n')
    text.write('Tower_dimensions '+'\n'+str(stored_data.Tower_dimensions)+'\n')
    text.write('Tower_loads '+'\n'+str(stored_data.Tower_loads)+'\n')
    text.close()