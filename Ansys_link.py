# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 17:46:47 2015

@author: Johan Antonissen (windhoos@gmail.com)
"""
from math import pi,sqrt
from parts import Input_data, Tower, Jacket

class nodebuilder:
    def __init__(self,wireframe):
        self.wireframe=wireframe
        
        self.jointlist=[]
    
    def compute(self):
        self.build_joints()
        
        return self.jointlist
        
    def build_joints(self):
        jointlist=[]
        wireframe=self.wireframe
        for bay in range(len(wireframe)):
            if bay == 0:
                jointlist.append([])
                z=wireframe[0][1]+wireframe[0][6]
                W_bay=wireframe[0][3]
                for i in range(4):
                    if i == 0:
                        #joint 1
                        x,y=-W_bay/2.0,-W_bay/2.0
                        jointlist[0].append([x,y,z])
                    elif i == 1:
                        #joint 2
                        x,y=W_bay/2.0,-W_bay/2.0
                        jointlist[0].append([x,y,z])
                    elif i == 2:
                        #joint 3
                        x,y=W_bay/2.0,W_bay/2.0
                        jointlist[0].append([x,y,z])
                    elif i == 3:
                        #joint 4
                        x,y=-W_bay/2.0,W_bay/2.0
                        jointlist[0].append([x,y,z])
            
            jointlist.append([])
            z=wireframe[bay][6]
            W_bay=wireframe[bay][4]
            for i in range(4):
                if i == 0:
                    #joint 1
                    x,y=-W_bay/2.0,-W_bay/2.0
                    jointlist[bay+1].append([x,y,z])
                elif i == 1:
                    #joint 2
                    x,y=W_bay/2.0,-W_bay/2.0
                    jointlist[bay+1].append([x,y,z])
                elif i == 2:
                    #joint 3
                    x,y=W_bay/2.0,W_bay/2.0
                    jointlist[bay+1].append([x,y,z])
                elif i == 3:
                    #joint 4
                    x,y=-W_bay/2.0,W_bay/2.0
                    jointlist[bay+1].append([x,y,z])
                    
        self.jointlist=jointlist
        
class nodewriter:
    def __init__(self,wireframe,jointlist):
        self.wireframe=wireframe
        self.jointlist=jointlist
        self.nodecount=0
        
    def compute(self):
        wireframe=self.wireframe
        jointlist=self.jointlist
        text=open('ANSYS-link180.txt','w')
        text.truncate()
        text.write('!THIS FIILE IS USED AS INPUT FILE FOR ANSYS TO BUILD A link180 JACKET'+'\n')
        text.write('/TITLE, Jacket LINK180'+'\n')
        text.write('/PREP7'+'\n')
        text.write('\n'+'!nodes'+'\n')
        nodecounter=0
        for bay in range(len(wireframe)):
            for i in range(4):
                #Nodes at top bay
                nodecounter=nodecounter+1
                text.write('n,'+str(nodecounter)+','+str(jointlist[bay][i][0])+','+str(jointlist[bay][i][1])+','+str(jointlist[bay][i][2])+'\n')
                
            if bay == len(wireframe)-1:
                for i in range(4):
                    #Nodes at bottom bay
                    nodecounter=nodecounter+1
                    text.write('n,'+str(nodecounter)+','+str(jointlist[bay+1][i][0])+','+str(jointlist[bay+1][i][1])+','+str(jointlist[bay+1][i][2])+'\n')
                    
        text.close()
        self.nodecount=nodecounter
        return self.nodecount
        
class elementwriter:
    def __init__(self,jacketlist,nodecount,Ed):
        self.Ed=Ed
        self.nodecount=nodecount
        self.jacketlist=jacketlist
        
    def area(self,D,wt):
        return pi/4.0*(D**2-(D-2*wt)**2)
        
    def compute(self):
        text=open('ANSYS-link180.txt','a')
        text.write('\n'+'!ELEMENTS'+'\n')
        jacketlist=self.jacketlist
        baycount=len(jacketlist)
        typecounter=1
        
        #First we create libraries containing data for the elements
        text.write('\n'+'!Element type creation'+'\n')
        text.write('mp,ex,'+str(typecounter)+','+str(self.Ed)+'\n')
        text.write('mp,prxy,'+str(typecounter)+',0.3'+'\n')
        text.write('mp,dens,'+str(typecounter)+',0'+'\n'+'\n')
        text.write('ET,1,link180'+'\n')
        
        for bay in range(baycount):
            
            Aleg=self.area(jacketlist[bay][0],jacketlist[bay][2])
            Abrace=self.area(jacketlist[bay][1],jacketlist[bay][3])
            for i in range(2):
                if i == 0:
                    A=Aleg
                elif i == 1:
                    A=Abrace
                text.write('R,'+str(typecounter)+','+str(A)+'\n')
                typecounter=typecounter+1
        
        text.write('\n'+'!Element creation'+'\n')        
        #Then we create the elements and attach the data to them
        
        for bay in range(baycount):
            #Leg element creation
            text.write('\n'+'!leg'+'\n')
            text.write('TYPE,1'+'\n')
            text.write('MAT,1'+'\n')
            text.write('REAL,'+str(2*bay+1)+'\n')
            for i in range(4):
                text.write('E,'+str(bay*4+i+1)+','+str(bay*4+i+5)+'\n')
            
            #Brace element creation
            text.write('\n'+'!brace'+'\n')
            text.write('TYPE,1'+'\n')
            text.write('MAT,1'+'\n')
            text.write('REAL,'+str(2*bay+2)+'\n')
            for i in range(4):
                if i != 3:
                    #Left brace
                    text.write('E,'+str(bay*4+i+1)+','+str(bay*4+i+6)+'\n')
                    #Right brace
                    text.write('E,'+str(bay*4+i+2)+','+str(bay*4+i+5)+'\n')
                else:
                    #Left brace
                    text.write('E,'+str(bay*4+i+1)+','+str(bay*4+i+2)+'\n')
                    #Right brace
                    text.write('E,'+str(bay*4+i-2)+','+str(bay*4+i+5)+'\n')
                    
        text.close()
        
class loadbuilder:
    def __init__(self,wireframe,tower_loads,jacket_env_loads,jacket_grav_loads):
        self.wireframe=wireframe
        self.tower_loads=tower_loads
        self.jacket_env_loads=jacket_env_loads
        self.jacket_grav_loads=jacket_grav_loads
        
        self.planeloads=[]
        
    def compute(self):
        self.load_creator()
        self.load_writer()
        
    def load_creator(self):
        wireframe=self.wireframe
        L_tower=self.tower_loads
        L_jacket_e=self.jacket_env_loads
        L_jacket_g=self.jacket_grav_loads
        
        bays=len(wireframe)
        planeloads=[]
        for bay in range(bays):
            if bay == 0:
                planeloads.append([[[],[]],[[],[]],[[],[]]])
            planeloads.append([])
            for LC in range(3):
                planeloads[bay+1].append([])
                for angle in range(2):
                    planeloads[bay+1][LC].append([])
                    for node in range(4):
                        if bay == 0:
                            Fx_tower=abs(L_tower[LC][0])
                            Fz_tower=abs(L_tower[LC][2])
                            My_tower=abs(L_tower[LC][4])
                                
                            if angle == 0:
                                if (node == 0) or (node == 3):
                                    Fx=Fx_tower/4.0
                                    Fy=0.0
                                    Fz=-Fz_tower/4.0+My_tower/(2.0*wireframe[bay][3]) #/sqrt(2)
                                    planeloads[bay][LC][angle].append([int(Fx),int(Fy),int(Fz)])
                                elif (node == 1) or (node == 2):
                                    Fx=Fx_tower/4.0
                                    Fy=0.0
                                    Fz=-Fz_tower/4.0-My_tower/(2.0*wireframe[0][3]) #/sqrt(2)
                                    planeloads[bay][LC][angle].append([int(Fx),int(Fy),int(Fz)])
                                    
                            elif angle == 1:
                                if node == 0:
                                    Fx=1/sqrt(2)*Fx_tower/4.0
                                    Fy=1/sqrt(2)*Fx_tower/4.0
                                    Fz=-Fz_tower/4.0+My_tower/(wireframe[0][3]*sqrt(2)) #/2
                                    planeloads[bay][LC][angle].append([int(Fx),int(Fy),int(Fz)])
                                elif (node == 1) or (node == 3):
                                    Fx=1/sqrt(2)*Fx_tower/4.0
                                    Fy=1/sqrt(2)*Fx_tower/4.0
                                    Fz=-Fz_tower/4.0
                                    planeloads[bay][LC][angle].append([int(Fx),int(Fy),int(Fz)])
                                elif node == 2:
                                    Fx=1/sqrt(2)*Fx_tower/4.0
                                    Fy=1/sqrt(2)*Fx_tower/4.0
                                    Fz=-Fz_tower/4.0-My_tower/(wireframe[0][3]*sqrt(2)) #/2
                                    planeloads[bay][LC][angle].append([int(Fx),int(Fy),int(Fz)])
                                    
                        if angle == 0:
                            if (node == 0) or (node == 3):
                                
                                Fx_env=sqrt(L_jacket_e[bay][angle][LC][0]**2+L_jacket_e[bay][angle][LC][1]**2)
                                Fz_grav=abs(L_jacket_g[bay])
                                My_env=sqrt(L_jacket_e[bay][angle][LC][2]**2+L_jacket_e[bay][angle][LC][3]**2)
                                Hbay=wireframe[bay][1]
                                #W_top=wireframe[bay][3]
                                W_bot=wireframe[bay][4]
                                
                                FxTOT_top=My_env/Hbay
                                FxTOT_bot=Fx_env-FxTOT_top
                                #FzTOT_top=0.0
                                FzTOT_bot=Fz_grav
                                #MyTOT_top=0.0
                                MyTOT_bot=My_env
                                
                                Fx_top=FxTOT_top/4.0+planeloads[bay][LC][angle][node][0]
                                Fx_bot=FxTOT_bot/4.0
                                Fy_top=0.0
                                Fy_bot=0.0
                                Fz_top=0.0+planeloads[bay][LC][angle][node][2]
                                Fz_bot=-FzTOT_bot/4.0+MyTOT_bot/(2*W_bot)
                                planeloads[bay][LC][angle][node][0]=int(Fx_top)
                                planeloads[bay][LC][angle][node][1]=int(Fy_top)
                                planeloads[bay][LC][angle][node][2]=int(Fz_top)
                                planeloads[bay+1][LC][angle].append([int(Fx_bot),int(Fy_bot),int(Fz_bot)])
                                
                            elif (node == 1) or (node == 2):
                                
                                Fx_env=sqrt(L_jacket_e[bay][angle][LC][0]**2+L_jacket_e[bay][angle][LC][1]**2)
                                Fz_grav=abs(L_jacket_g[bay])
                                My_env=sqrt(L_jacket_e[bay][angle][LC][2]**2+L_jacket_e[bay][angle][LC][3]**2)
                                Hbay=wireframe[bay][1]
                                #W_top=wireframe[bay][3]
                                W_bot=wireframe[bay][4]
                                
                                FxTOT_top=My_env/Hbay
                                FxTOT_bot=Fx_env-FxTOT_top
                                #FzTOT_top=0.0
                                FzTOT_bot=Fz_grav
                                #MyTOT_top=0.0
                                MyTOT_bot=My_env
                                
                                Fx_top=FxTOT_top/4.0+planeloads[bay][LC][angle][node][0]
                                Fx_bot=FxTOT_bot/4.0
                                Fy_top=0.0
                                Fy_bot=0.0
                                Fz_top=0.0+planeloads[bay][LC][angle][node][2]
                                Fz_bot=-FzTOT_bot/4.0-MyTOT_bot/(2*W_bot)
                                planeloads[bay][LC][angle][node][0]=int(Fx_top)
                                planeloads[bay][LC][angle][node][1]=int(Fy_top)
                                planeloads[bay][LC][angle][node][2]=int(Fz_top)
                                planeloads[bay+1][LC][angle].append([int(Fx_bot),int(Fy_bot),int(Fz_bot)])
                                
                        elif angle == 1:
                            if node == 0:
                                
                                Fx_env=sqrt(L_jacket_e[bay][angle][LC][0]**2+L_jacket_e[bay][angle][LC][1]**2)
                                Fz_grav=abs(L_jacket_g[bay])
                                My_env=sqrt(L_jacket_e[bay][angle][LC][2]**2+L_jacket_e[bay][angle][LC][3]**2)
                                Hbay=wireframe[bay][1]
                                #W_top=wireframe[bay][3]
                                W_bot=wireframe[bay][4]
                                
                                FxTOT_top=My_env/Hbay
                                FxTOT_bot=Fx_env-FxTOT_top
                                #FzTOT_top=0.0
                                FzTOT_bot=Fz_grav
                                #MyTOT_top=0.0
                                MyTOT_bot=My_env
                                
                                Fx_top=1/sqrt(2)*FxTOT_top/4.0+planeloads[bay][LC][angle][node][0]
                                Fx_bot=1/sqrt(2)*FxTOT_bot/4.0
                                Fy_top=1/sqrt(2)*FxTOT_top/4.0+planeloads[bay][LC][angle][node][1]
                                Fy_bot=1/sqrt(2)*FxTOT_bot/4.0
                                Fz_top=0.0+planeloads[bay][LC][angle][node][2]
                                Fz_bot=-FzTOT_bot/4.0+MyTOT_bot/(W_bot*sqrt(2))#/2
                                planeloads[bay][LC][angle][node][0]=int(Fx_top)
                                planeloads[bay][LC][angle][node][1]=int(Fy_top)
                                planeloads[bay][LC][angle][node][2]=int(Fz_top)
                                planeloads[bay+1][LC][angle].append([int(Fx_bot),int(Fy_bot),int(Fz_bot)])
                                
                            elif (node==1) or (node==3):
                                
                                Fx_env=sqrt(L_jacket_e[bay][angle][LC][0]**2+L_jacket_e[bay][angle][LC][1]**2)
                                Fz_grav=abs(L_jacket_g[bay])
                                My_env=sqrt(L_jacket_e[bay][angle][LC][2]**2+L_jacket_e[bay][angle][LC][3]**2)
                                Hbay=wireframe[bay][1]
                                #W_top=wireframe[bay][3]
                                W_bot=wireframe[bay][4]
                                
                                FxTOT_top=My_env/Hbay
                                FxTOT_bot=Fx_env-FxTOT_top
                                #FzTOT_top=0.0
                                FzTOT_bot=Fz_grav
                                #MyTOT_top=0.0
                                MyTOT_bot=My_env
                                
                                Fx_top=1/sqrt(2)*FxTOT_top/4.0+planeloads[bay][LC][angle][node][0]
                                Fx_bot=1/sqrt(2)*FxTOT_bot/4.0
                                Fy_top=1/sqrt(2)*FxTOT_top/4.0+planeloads[bay][LC][angle][node][1]
                                Fy_bot=1/sqrt(2)*FxTOT_bot/4.0
                                Fz_top=0.0+planeloads[bay][LC][angle][node][2]
                                Fz_bot=-FzTOT_bot/4.0
                                planeloads[bay][LC][angle][node][0]=int(Fx_top)
                                planeloads[bay][LC][angle][node][1]=int(Fy_top)
                                planeloads[bay][LC][angle][node][2]=int(Fz_top)
                                planeloads[bay+1][LC][angle].append([int(Fx_bot),int(Fy_bot),int(Fz_bot)])
                                
                            elif node == 2:
                                
                                Fx_env=sqrt(L_jacket_e[bay][angle][LC][0]**2+L_jacket_e[bay][angle][LC][1]**2)
                                Fz_grav=abs(L_jacket_g[bay])
                                My_env=sqrt(L_jacket_e[bay][angle][LC][2]**2+L_jacket_e[bay][angle][LC][3]**2)
                                Hbay=wireframe[bay][1]
                                #W_top=wireframe[bay][3]
                                W_bot=wireframe[bay][4]
                                
                                FxTOT_top=My_env/Hbay
                                FxTOT_bot=Fx_env-FxTOT_top
                                #FzTOT_top=0.0
                                FzTOT_bot=Fz_grav
                                #MyTOT_top=0.0
                                MyTOT_bot=My_env
                                
                                Fx_top=1/sqrt(2)*FxTOT_top/4.0+planeloads[bay][LC][angle][node][0]
                                Fx_bot=1/sqrt(2)*FxTOT_bot/4.0
                                Fy_top=1/sqrt(2)*FxTOT_top/4.0+planeloads[bay][LC][angle][node][1]
                                Fy_bot=1/sqrt(2)*FxTOT_bot/4.0
                                Fz_top=0.0+planeloads[bay][LC][angle][node][2]
                                Fz_bot=-FzTOT_bot/4.0-MyTOT_bot/(W_bot*sqrt(2)) #/2
                                planeloads[bay][LC][angle][node][0]=int(Fx_top)
                                planeloads[bay][LC][angle][node][1]=int(Fy_top)
                                planeloads[bay][LC][angle][node][2]=int(Fz_top)
                                planeloads[bay+1][LC][angle].append([int(Fx_bot),int(Fy_bot),int(Fz_bot)])
                        
        self.planeloads=planeloads
            
    def load_writer(self):
        loads=self.planeloads
        counter=0
        bays=len(loads)-1
        text=open('ANSYS-link180.txt','a')
        text.write('\n'+'!ANSYS LOADFILES ARE CREATED'+'\n')
        text.write('/SOLU'+'\n')
        for LC in range(3):
            for angle in range(2):
                counter=counter+1
                if angle == 0:
                    ANGLE=0
                else:
                    ANGLE=45
                text.write('\n'+'!LOADSTEP '+str(counter)+': LC '+str(LC+1)+' angle '+str(ANGLE)+'\n')
                text.write('\n'+'!CONSTRAINTS'+'\n')
                for node in range(4):
                    nodeBOT=4*(bays)+node+1
                    #Finally we constrain nodes to the subsoil
                    text.write('D,'+str(nodeBOT)+',ux,0'+'\n')
                    text.write('D,'+str(nodeBOT)+',uy,0'+'\n')
                    text.write('D,'+str(nodeBOT)+',uz,0'+'\n')
                    
                text.write('\n'+'!FORCES'+'\n')
                for plane in range(len(loads)):
                    for node in range(4):
                        
                        nodeNR=plane*4+node+1
                        FX=loads[plane][LC][angle][node][0]
                        FY=loads[plane][LC][angle][node][1]
                        FZ=loads[plane][LC][angle][node][2]
                        
                        text.write('F,'+str(nodeNR)+',fx,'+str(FX)+'\n')
                        text.write('F,'+str(nodeNR)+',fy,'+str(FY)+'\n')
                        text.write('F,'+str(nodeNR)+',fz,'+str(FZ)+'\n')
    
                text.write('KBC,1'+'\n')
                text.write('LSWRITE'+'\n')
        
        text.close()
        
class static_analysis:
    def __init__(self,wireframe,jacketdimensions):
        self.wireframe=wireframe
        self.jacketdimensions=jacketdimensions
        
    def compute(self):
        text=open('ANSYS-link180.txt','a')
        text.write('\n'+'!ANSYS SOLUTIONS ARE CREATED'+'\n')
        text.write('/SOLU'+'\n')
        text.write('LSSOLVE,1,6,1'+'\n')
        text.close()
        self.graphics()
        self.create_tables()
        self.write_images()
        self.write_text()

    def create_tables(self):
        text=open('ANSYS-link180.txt','a')
        text.write('/post1'+'\n')
        text.write('ETABLE,Fx,SMISC,1'+'\n') #Axial force
        text.write('ETABLE,Sx,LS,1'+'\n') #Internal stress
        text.write('ETABLE,A,LS,2'+'\n') #Area
        text.close()
        
    def graphics(self):
        text=open('ANSYS-link180.txt','a')
        text.write('/auto,1'+'\n')
        text.write('/RGB,index,100,100,100,0'+'\n')
        text.write('/RGB,index,80,80,80,13'+'\n')
        text.write('/RGB,index,60,600,600,14'+'\n')
        text.write('/RGB,index,0,0,0,15'+'\n')
        text.write('/angle,1,-90,xs,0'+'\n')
        text.write('/angle,1,105,ys,1'+'\n')
        text.write('/angle,1,25,xs,1'+'\n')
        text.write('/angle,1,-180,ys,1'+'\n')
        text.write('/angle,1,10,xs,1'+'\n')
        text.write('/angle,1,10,ys,1'+'\n')
        text.write('/auto,1'+'\n')
        text.write('EPLOT'+'\n')
        text.write('/pnum,node,1'+'\n')
        text.write('/replot'+'\n')
        text.write('/image,save,LINK-node,png'+'\n')
        text.write('/pnum,elem,1'+'\n')
        text.write('/replot'+'\n')
        text.write('/image,save,LINK-elem,png'+'\n')
        text.write('/pnum,node,0'+'\n')
        text.write('/pnum,elem,0'+'\n')
        text.close()
        
    def write_images(self):
        text=open('ANSYS-link180.txt','a')
        text.write('/post1'+'\n')
        LCcounter=1
        for LC in range(3):
            for angle in range(2):
                if angle == 0:
                    angleNR = 0
                elif angle == 1:
                    angleNR = 45
                text.write('/post1'+'\n')
                text.write('SET,'+str(LCcounter)+'\n')
                text.write('ETABLE,REFL'+'\n')
                text.write('PLLS,Fx,Fx,1,0'+'\n')
                text.write('/image,save,LINK-FX-LC'+str(LC+1)+'A'+str(angleNR)+',png'+'\n')
                text.write('/post1'+'\n')
                text.write('PLLS,Sx,Sx,1,0'+'\n')
                text.write('/image,save,LINK-SX-LC'+str(LC+1)+'A'+str(angleNR)+',png'+'\n')
                LCcounter=LCcounter+1
        text.close()
                
    def write_text(self):
        text=open('ANSYS-link180.txt','a')
        text.write('/post1'+'\n')
        LCcounter=1
        for LC in range(3):
            for angle in range(2):
                if angle == 0:
                    angleNR = 0
                elif angle == 1:
                    angleNR = 45
                text.write('/post1'+'\n')
                text.write('SET,'+str(LCcounter)+'\n')
                text.write('ETABLE,REFL'+'\n')
                text.write('/output,LINK-FEXT'+str(LC+1)+'A'+str(angleNR)+',out'+'\n')
                text.write('FLIST'+'\n')
                text.write('/output,LINK-ERES'+str(LC+1)+'A'+str(angleNR)+',out'+'\n')
                text.write('PRESOL,ELEM'+'\n')
                text.write('/output,LINK-LOADS-LC'+str(LC+1)+'A'+str(angleNR)+',out'+'\n')
                text.write('PRESOL,F,x'+'\n')
                text.write('/output,LINK-STRESS-LC'+str(LC+1)+'A'+str(angleNR)+',out'+'\n')
                text.write('PRESOL,S,x'+'\n')
                text.write('/output'+'\n')
                LCcounter=LCcounter+1
        text.close()
        
def ansys():
#def main():
    #Ed=str(2.e11)
    Ed=str(Input_data.stored_data.Ed)
    
    #wireframe=[[2, 16.69, 42.1536595359841, 17.101249112742135, 19.771649112742136, 13.667817989808237, 16.69, 265.4260787400991, 317.8463404640159, 274.5739212599009, 222.15365953598408, 85.42607874009914, 42.1536595359841, 94.57392125990086, 137.84634046401592, 0.08], [2, 16.69, 38.33478236213461, 19.771649112742136, 22.442049112742136, 16.556211994722393, 0.0, 265.4260787400991, 321.66521763786534, 274.5739212599009, 218.3347823621346, 85.42607874009914, 38.33478236213461, 94.57392125990086, 141.6652176378654, 0.08]]
    wireframe=Jacket.stored_data.wireframe
    #jacketdimensions=[[0.53938685241171935, 0.32363211144703158, 0.021887070822416265, 0.012842544105040935], [0.59332554765289136, 0.35599532859173483, 0.023544664589400452, 0.014881691457659524]]
    jacketdimensions=Jacket.stored_data.Jacket_dimensions 
    #tower_load=[[2654083, 0.0, 4922811, 0.0, 178932153, 0.0], [2083014, 0.0, 4922811, 0.0, 117938697, 0.0], [2520451, 0.0, 4922811, 0.0, 140909950, 0.0]]
    tower_load=Tower.stored_data.loadbottom
    #jacket_environmental_load=[[[[186192, 82077, 986020, 427734], [1085501, 120590, 5628819, 621747], [715764, 115395, 3728904, 596359]], [[292158, 90614, 1547183, 472225], [1703280, 133133, 8832287, 686419], [1123120, 127398, 5851094, 658390]]], [[[214698, 162073, 3691824, 2736875], [2313397, 325381, 38775115, 5425085], [1342625, 291993, 22614770, 4880271]], [[342227, 178956, 5884729, 3021974], [3687531, 359276, 61807121, 5990215], [2140130, 322410, 36047703, 5388648]]]]
    jacket_environmental_load=Jacket.stored_data.environmental_loads_per_bay
    #jacket_gravitational_load=[524726, 689753]
    jacket_gravitational_load=Jacket.stored_data.gravitational_loads_per_bay
    
    nodecalc=nodebuilder(wireframe)
    jointlist=nodecalc.compute()
    nodeANSYS=nodewriter(wireframe,jointlist)
    nodecount=nodeANSYS.compute()
    elementANSYS=elementwriter(jacketdimensions,nodecount,Ed)
    elementANSYS.compute()
    loadANSYS=loadbuilder(wireframe,tower_load,jacket_environmental_load,jacket_gravitational_load)
    loadANSYS.compute()
    staticANSYS=static_analysis(wireframe,jacketdimensions)
    staticANSYS.compute()
#main()