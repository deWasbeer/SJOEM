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
        self.sleevelist=[]
    
    def compute(self):
        self.build_joints()
        self.build_sleeves()
        
        return self.jointlist,self.sleevelist
        
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
                    
    def build_sleeves(self):
        sleevelist=[]
        wireframe=self.wireframe
        jointlist=self.jointlist
        for bay in range(len(wireframe)):
            sleevelist.append([])
            nodetop=jointlist[bay]
            nodebot=jointlist[bay+1]
            
            ztopleg=nodetop[0][2]-(nodetop[0][2]-nodebot[0][2])/5.0
            zbotleg=nodetop[0][2]-4*(nodetop[0][2]-nodebot[0][2])/5.0
            
            ztopbrace=nodetop[0][2]-(nodetop[0][2]-nodebot[1][2])/5.0
            zbotbrace=nodetop[0][2]-4*(nodetop[0][2]-nodebot[1][2])/5.0            
            
            for i in range(4):
                xtopleg=nodetop[i][0]-(nodetop[i][0]-nodebot[i][0])/5.0
                xbotleg=nodetop[i][0]-4*(nodetop[i][0]-nodebot[i][0])/5.0
                ytopleg=nodetop[i][1]-(nodetop[i][1]-nodebot[i][1])/5.0
                ybotleg=nodetop[i][1]-4*(nodetop[i][1]-nodebot[i][1])/5.0
                if i != 3:
                    xtopbraceL=nodetop[i][0]-(nodetop[i][0]-nodebot[i+1][0])/5.0   
                    xbotbraceL=nodetop[i][0]-4*(nodetop[i][0]-nodebot[i+1][0])/5.0
                    ytopbraceL=nodetop[i][1]-(nodetop[i][1]-nodebot[i+1][1])/5.0  
                    ybotbraceL=nodetop[i][1]-4*(nodetop[i][1]-nodebot[i+1][1])/5.0
                    
                    xtopbraceR=nodetop[i+1][0]-(nodetop[i+1][0]-nodebot[i][0])/5.0   
                    xbotbraceR=nodetop[i+1][0]-4*(nodetop[i+1][0]-nodebot[i][0])/5.0
                    ytopbraceR=nodetop[i+1][1]-(nodetop[i+1][1]-nodebot[i][1])/5.0  
                    ybotbraceR=nodetop[i+1][1]-4*(nodetop[i+1][1]-nodebot[i][1])/5.0
                else:
                    xtopbraceL=nodetop[i][0]-(nodetop[i][0]-nodebot[0][0])/5.0   
                    xbotbraceL=nodetop[i][0]-4*(nodetop[i][0]-nodebot[0][0])/5.0
                    ytopbraceL=nodetop[i][1]-(nodetop[i][1]-nodebot[0][1])/5.0  
                    ybotbraceL=nodetop[i][1]-4*(nodetop[i][1]-nodebot[0][1])/5.0
                    
                    xtopbraceR=nodetop[0][0]-(nodetop[0][0]-nodebot[i][0])/5.0   
                    xbotbraceR=nodetop[0][0]-4*(nodetop[0][0]-nodebot[i][0])/5.0
                    ytopbraceR=nodetop[0][1]-(nodetop[0][1]-nodebot[i][1])/5.0  
                    ybotbraceR=nodetop[0][1]-4*(nodetop[0][1]-nodebot[i][1])/5.0
                
                sleevelist[bay].append([[xtopleg,ytopleg,ztopleg],[xbotleg,ybotleg,zbotleg],[xtopbraceL,ytopbraceL,ztopbrace],[xbotbraceL,ybotbraceL,zbotbrace],[xtopbraceR,ytopbraceR,ztopbrace],[xbotbraceR,ybotbraceR,zbotbrace]])
        
        self.sleevelist=sleevelist
        
class nodewriter:
    def __init__(self,wireframe,jointlist,sleevelist):
        self.wireframe=wireframe
        self.jointlist=jointlist
        self.sleevelist=sleevelist
        self.nodecount=0
        
    def compute(self):
        wireframe=self.wireframe
        jointlist=self.jointlist
        sleevelist=self.sleevelist
        text=open('ANSYS-beam188.txt','w')
        text.truncate()
        text.write('!THIS FIILE IS USED AS INPUT FILE FOR ANSYS TO BUILD A BEAM180 JACKET'+'\n')
        text.write('/TITLE, Jacket BEAM188'+'\n')
        text.write('/PREP7'+'\n')
        text.write('\n'+'!Keypoints'+'\n')
        nodecounter=0
        for bay in range(len(wireframe)):
            for i in range(4):
                #Nodes at top bay
                nodecounter=nodecounter+1
                text.write('k,'+str(nodecounter)+','+str(jointlist[bay][i][0])+','+str(jointlist[bay][i][1])+','+str(jointlist[bay][i][2])+'\n')
            for i in range(4):
                #Nodes at top leg sleeves
                nodecounter=nodecounter+1
                text.write('k,'+str(nodecounter)+','+str(sleevelist[bay][i][0][0])+','+str(sleevelist[bay][i][0][1])+','+str(sleevelist[bay][i][0][2])+'\n')
                #Nodes at top brace sleeves left
                nodecounter=nodecounter+1
                text.write('k,'+str(nodecounter)+','+str(sleevelist[bay][i][2][0])+','+str(sleevelist[bay][i][2][1])+','+str(sleevelist[bay][i][2][2])+'\n')
                #Nodes at top brace sleeves right
                nodecounter=nodecounter+1
                text.write('k,'+str(nodecounter)+','+str(sleevelist[bay][i][4][0])+','+str(sleevelist[bay][i][4][1])+','+str(sleevelist[bay][i][4][2])+'\n')
                
            for i in range(4):
                #Nodes at bottom leg sleeves
                nodecounter=nodecounter+1
                text.write('k,'+str(nodecounter)+','+str(sleevelist[bay][i][1][0])+','+str(sleevelist[bay][i][1][1])+','+str(sleevelist[bay][i][1][2])+'\n')
                #Nodes at bottom brace sleeves left
                nodecounter=nodecounter+1
                text.write('k,'+str(nodecounter)+','+str(sleevelist[bay][i][5][0])+','+str(sleevelist[bay][i][5][1])+','+str(sleevelist[bay][i][5][2])+'\n')
                #Nodes at bottom brace sleeves right
                nodecounter=nodecounter+1
                text.write('k,'+str(nodecounter)+','+str(sleevelist[bay][i][3][0])+','+str(sleevelist[bay][i][3][1])+','+str(sleevelist[bay][i][3][2])+'\n')
                
            if bay == len(wireframe)-1:
                for i in range(4):
                    #Nodes at bottom bay
                    nodecounter=nodecounter+1
                    text.write('k,'+str(nodecounter)+','+str(jointlist[bay+1][i][0])+','+str(jointlist[bay+1][i][1])+','+str(jointlist[bay+1][i][2])+'\n')
                    
        text.close()
        self.nodecount=nodecounter
        return self.nodecount
        
class elementwriter:
    def __init__(self,jacketlist,sleevelist,nodecount,Ed):
        self.Ed=Ed
        self.nodecount=nodecount
        self.jacketlist=jacketlist
        self.sleevelist=sleevelist
        
    def area(self,D,wt):
        return pi/4.0*(D**2-(D-2*wt)**2)
        
    def compute(self):
        text=open('ANSYS-beam188.txt','a')
        text.write('\n'+'!ELEMENTS'+'\n')
        jacketlist=self.jacketlist
        sleevelist=self.sleevelist
        baycount=len(jacketlist)
        typecounter=1
        
        #First we create libraries containing data for the elements
        text.write('\n'+'!Element type creation'+'\n')
        text.write('mp,ex,'+str(typecounter)+','+str(self.Ed)+'\n')
        text.write('mp,prxy,'+str(typecounter)+',0.3'+'\n')
        text.write('mp,dens,'+str(typecounter)+',0'+'\n'+'\n')
        
        for bay in range(baycount):
            Dleg=jacketlist[bay][0]
            wtleg=jacketlist[bay][2]
            Dbrace=jacketlist[bay][1]
            wtbrace=jacketlist[bay][3]
            Dlegsleeve=jacketlist[bay][0]
            wtlegsleeve=jacketlist[bay][2]+sleevelist[bay][0]
            Dbracesleeve=jacketlist[bay][1]
            wtbracesleeve=jacketlist[bay][3]+sleevelist[bay][1]
            
            #Aleg=self.area(jacketlist[bay][0],jacketlist[bay][2])
            #Abrace=self.area(jacketlist[bay][1],jacketlist[bay][3])
            #Alegsleeve=self.area(jacketlist[bay][0],jacketlist[bay][2]+sleevelist[bay][0])
            #Abracesleeve=self.area(jacketlist[bay][1],jacketlist[bay][3]+sleevelist[bay][1])
            
            for i in range(4):
                if i == 0:
                    #A=Alegsleeve #ET1
                    Rout=Dlegsleeve/2.0
                    Rin=Rout-wtlegsleeve
                    Name='LEGSL0000'+str(bay)
                elif i == 1:
                    #A=Abracesleeve #ET2
                    Rout=Dbracesleeve/2.0
                    Rin=Rout-wtbracesleeve
                    Name='BRACESL00'+str(bay)
                elif i == 2:
                    #A=Aleg
                    Rout=Dleg/2.0
                    Rin=Rout-wtleg
                    Name='LEG000000'+str(bay)
                elif i == 3:
                    #A=Abrace
                    Rout=Dbrace/2.0
                    Rin=Rout-wtbrace
                    Name='BRACE0000'+str(bay)
                    
                text.write('ET,'+str(typecounter)+',beam188'+'\n')
                text.write('SECTYPE,'+str(typecounter)+',beam,ctube,'+Name+'\n')
                text.write('SECDATA,'+str(Rin)+','+str(Rout)+'\n')
                typecounter=typecounter+1
        
        text.write('\n'+'!Element creation'+'\n')        
        #Then we create the elements and attach the data to them
        Lnum=0
        for bay in range(baycount):
            
            #Top leg sleeve element creation
            text.write('\n'+'!leg sleeve'+'\n')
            text.write('TYPE,'+str(4*bay+1)+'\n')
            text.write('SECNUM,'+str(4*bay+1)+'\n')
            #text.write('REAL,'+str(4*bay+1)+'\n')
            text.write('MAT,'+str(1)+'\n')
            for i in range(4):
                text.write('L,'+str(bay*28+i+1)+','+str(bay*28+3*i+5)+'\n')
                Lnum=Lnum+1
                text.write('Lmesh,'+str(Lnum)+','+str(Lnum)+'\n')
            
            #Top brace sleeve element creation
            text.write('\n'+'!brace sleeve'+'\n')
            text.write('TYPE,'+str(4*bay+2)+'\n')
            text.write('SECNUM,'+str(4*bay+2)+'\n')
            #text.write('REAL,'+str(4*bay+2)+'\n')
            text.write('MAT,'+str(1)+'\n')
            for i in range(4):
                #Left brace
                text.write('L,'+str(bay*28+i+1)+','+str(bay*28+3*i+6)+'\n')
                Lnum=Lnum+1
                text.write('Lmesh,'+str(Lnum)+','+str(Lnum)+'\n')
                #Right brace
                if i != 3:
                    text.write('L,'+str(bay*28+i+2)+','+str(bay*28+3*i+7)+'\n')
                    Lnum=Lnum+1
                    text.write('Lmesh,'+str(Lnum)+','+str(Lnum)+'\n')
                else:
                    text.write('L,'+str(bay*28+i-3+1)+','+str(bay*28+3*i+7)+'\n')
                    Lnum=Lnum+1
                    text.write('Lmesh,'+str(Lnum)+','+str(Lnum)+'\n')
                    
            #Leg element creation
            text.write('\n'+'!leg'+'\n')
            text.write('TYPE,'+str(4*bay+3)+'\n')
            text.write('SECNUM,'+str(4*bay+3)+'\n')
            #text.write('REAL,'+str(4*bay+3)+'\n')
            text.write('MAT,'+str(1)+'\n')
            for i in range(4):
                text.write('L,'+str(bay*28+3*i+5)+','+str(bay*28+3*i+17)+'\n')
                Lnum=Lnum+1
                text.write('Lmesh,'+str(Lnum)+','+str(Lnum)+'\n')
            
            #Brace element creation
            text.write('\n'+'!brace'+'\n')
            text.write('TYPE,'+str(4*bay+4)+'\n')
            text.write('SECNUM,'+str(4*bay+4)+'\n')
            #text.write('REAL,'+str(4*bay+4)+'\n')
            text.write('MAT,'+str(1)+'\n')
            for i in range(4):
                #Left brace
                text.write('L,'+str(bay*28+3*i+6)+','+str(bay*28+3*i+19)+'\n')
                Lnum=Lnum+1
                text.write('Lmesh,'+str(Lnum)+','+str(Lnum)+'\n')
                #Right brace
                if i != 3:
                    text.write('L,'+str(bay*28+3*i+7)+','+str(bay*28+3*i+18)+'\n')
                    Lnum=Lnum+1
                    text.write('Lmesh,'+str(Lnum)+','+str(Lnum)+'\n')
                else:
                    text.write('L,'+str(bay*28+3*i+7)+','+str(bay*28+3*i+18)+'\n')
                    Lnum=Lnum+1
                    text.write('Lmesh,'+str(Lnum)+','+str(Lnum)+'\n')
            
            #Bot leg sleeve element creation
            text.write('\n'+'!leg sleeve'+'\n')
            text.write('TYPE,'+str(4*bay+1)+'\n')
            text.write('SECNUM,'+str(4*bay+1)+'\n')
            #text.write('REAL,'+str(4*bay+1)+'\n')
            text.write('MAT,'+str(1)+'\n')
            for i in range(4):
                text.write('L,'+str(bay*28+3*i+17)+','+str(bay*28+i+29)+'\n')
                Lnum=Lnum+1
                text.write('Lmesh,'+str(Lnum)+','+str(Lnum)+'\n')
            
            #Bot brace sleeve element creation
            text.write('\n'+'!brace sleeve'+'\n')
            text.write('TYPE,'+str(4*bay+2)+'\n')
            text.write('SECNUM,'+str(4*bay+2)+'\n')
            #text.write('REAL,'+str(4*bay+2)+'\n')
            text.write('MAT,'+str(1)+'\n')
            for i in range(4):
                #Left brace
                text.write('L,'+str(bay*28+3*i+18)+','+str(bay*28+i+29)+'\n')
                Lnum=Lnum+1
                text.write('Lmesh,'+str(Lnum)+','+str(Lnum)+'\n')
                #Right brace
                if i != 3:
                    text.write('L,'+str(bay*28+3*i+19)+','+str(bay*28+i+30)+'\n')
                    Lnum=Lnum+1
                    text.write('Lmesh,'+str(Lnum)+','+str(Lnum)+'\n')
                else:
                    text.write('L,'+str(bay*28+3*i+19)+','+str(bay*28+i-3+29)+'\n')
                    Lnum=Lnum+1
                    text.write('Lmesh,'+str(Lnum)+','+str(Lnum)+'\n')
                    
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
                                    Fz=-Fz_tower/4.0+My_tower/(2.0*wireframe[bay][3])
                                    planeloads[bay][LC][angle].append([int(Fx),int(Fy),int(Fz)])
                                elif (node == 1) or (node == 2):
                                    Fx=Fx_tower/4.0
                                    Fy=0.0
                                    Fz=-Fz_tower/4.0-My_tower/(2.0*wireframe[0][3])
                                    planeloads[bay][LC][angle].append([int(Fx),int(Fy),int(Fz)])
                                    
                            elif angle == 1:
                                if node == 0:
                                    Fx=1/sqrt(2)*Fx_tower/4.0
                                    Fy=1/sqrt(2)*Fx_tower/4.0
                                    Fz=-Fz_tower/4.0+My_tower/(wireframe[0][3]*sqrt(2))
                                    planeloads[bay][LC][angle].append([int(Fx),int(Fy),int(Fz)])
                                elif (node == 1) or (node == 3):
                                    Fx=1/sqrt(2)*Fx_tower/4.0
                                    Fy=1/sqrt(2)*Fx_tower/4.0
                                    Fz=-Fz_tower/4.0
                                    planeloads[bay][LC][angle].append([int(Fx),int(Fy),int(Fz)])
                                elif node == 2:
                                    Fx=1/sqrt(2)*Fx_tower/4.0
                                    Fy=1/sqrt(2)*Fx_tower/4.0
                                    Fz=-Fz_tower/4.0-My_tower/(wireframe[0][3]*sqrt(2))
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
                                Fz_bot=-FzTOT_bot/4.0+MyTOT_bot/(W_bot*sqrt(2))
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
                                Fz_bot=-FzTOT_bot/4.0-MyTOT_bot/(W_bot*sqrt(2))
                                planeloads[bay][LC][angle][node][0]=int(Fx_top)
                                planeloads[bay][LC][angle][node][1]=int(Fy_top)
                                planeloads[bay][LC][angle][node][2]=int(Fz_top)
                                planeloads[bay+1][LC][angle].append([int(Fx_bot),int(Fy_bot),int(Fz_bot)])
                
        self.planeloads=planeloads
            
    def load_writer(self):
        loads=self.planeloads
        counter=0
        bays=len(loads)-1
        text=open('ANSYS-beam188.txt','a')
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
                    nodeBOT=28*(bays)+node+1
                    #Finally we constrain nodes to the subsoil
                    text.write('DK,'+str(nodeBOT)+',ALL'+'\n')
                    #text.write('DK,'+str(nodeBOT)+',ux,0'+'\n')
                    #text.write('DK,'+str(nodeBOT)+',uy,0'+'\n')
                    #text.write('DK,'+str(nodeBOT)+',uz,0'+'\n')
                    
                text.write('\n'+'!FORCES'+'\n')
                for plane in range(len(loads)):
                    for node in range(4):
                        #if plane != len(loads)-1:
                        nodeNR=plane*28+node+1
                        FX=loads[plane][LC][angle][node][0]
                        FY=loads[plane][LC][angle][node][1]
                        FZ=loads[plane][LC][angle][node][2]
                        text.write('FK,'+str(nodeNR)+',fx,'+str(FX)+'\n')
                        text.write('FK,'+str(nodeNR)+',fy,'+str(FY)+'\n')
                        text.write('FK,'+str(nodeNR)+',fz,'+str(FZ)+'\n')
                        
                text.write('KBC,1'+'\n')
                text.write('LSWRITE'+'\n')
        
        text.close()
        
class static_analysis:
    def __init__(self,wireframe,jacketdimensions,sleevedimensions):
        self.wireframe=wireframe
        self.jacketdimensions=jacketdimensions
        self.sleevedimensions=sleevedimensions
        
    def compute(self):
        text=open('ANSYS-beam188.txt','a')
        text.write('\n'+'!ANSYS SOLUTIONS ARE CREATED'+'\n')
        text.write('/SOLU'+'\n')
        text.write('LSSOLVE,1,6,1'+'\n')
        text.close()
        self.graphics()
        self.create_tables()
        self.write_images()
        self.write_text()

    def create_tables(self):
        text=open('ANSYS-beam188.txt','a')
        text.write('/post1'+'\n')
        text.write('ETABLE,Fxi,SMISC,1'+'\n') #Axial force node i
        text.write('ETABLE,Fxj,SMISC,14'+'\n')
        text.write('ETABLE,Myi,SMISC,2'+'\n') #Bending moment node i
        text.write('ETABLE,Myj,SMISC,15'+'\n')
        text.write('ETABLE,Mzi,SMISC,3'+'\n')
        text.write('ETABLE,Mzj,SMISC,16'+'\n')
        text.write('ETABLE,SFyi,SMISC,6'+'\n') #Shear force node i
        text.write('ETABLE,SFyj,SMISC,19'+'\n')
        text.write('ETABLE,SFzi,SMISC,5'+'\n')
        text.write('ETABLE,SFzj,SMISC,18'+'\n')
        text.write('ETABLE,SDIRi,SMISC,31'+'\n') #Axial direct stress node i F/A
        text.write('ETABLE,SDIRj,SMISC,36'+'\n')
        text.write('SADD,NULL,Fxi,Fxi,1,-1'+'\n')
        text.close()
        
    def graphics(self):
        text=open('ANSYS-beam188.txt','a')
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
        text.write('/eshape,1'+'\n')
        text.write('NPLOT'+'\n')
        text.write('/pnum,node,1'+'\n')
        text.write('/replot'+'\n')
        text.write('/image,save,BEAM-node,png'+'\n')
        text.write('/pnum,elem,1'+'\n')
        text.write('/replot'+'\n')
        text.write('/image,save,BEAM-elem,png'+'\n')
        text.write('/pnum,node,0'+'\n')
        text.write('/pnum,elem,0'+'\n')
        text.close()
        
    def write_images(self):
        text=open('ANSYS-beam188.txt','a')
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
                text.write('PLLS,SDIRi,SDIRj,1,0'+'\n')
                text.write('/image,save,BEAM-SX-LC'+str(LC+1)+'A'+str(angleNR)+',png'+'\n')
                text.write('PLESOL,S,EQV'+'\n')
                text.write('/image,save,BEAM-SMISES-LC'+str(LC+1)+'A'+str(angleNR)+',png'+'\n')
                text.write('PLLS,Fxi,Fxj,1,0'+'\n')
                text.write('/image,save,BEAM-FORCEX-LC'+str(LC+1)+'A'+str(angleNR)+',png'+'\n')
                text.write('PLLS,Myi,Myj,1,0'+'\n')
                text.write('/image,save,BEAM-MOMENTY-LC'+str(LC+1)+'A'+str(angleNR)+',png'+'\n')
                text.write('PLLS,Mzi,Mzj,1,0'+'\n')
                text.write('/image,save,BEAM-MOMENTZ-LC'+str(LC+1)+'A'+str(angleNR)+',png'+'\n')
                LCcounter=LCcounter+1
        text.close()
                
    def write_text(self):
        text=open('ANSYS-beam188.txt','a')
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
                text.write('/output,BEAM-LOADS-LC'+str(LC+1)+'A'+str(angleNR)+',out'+'\n')
                #text.write('PRETAB,FXI,NULL,FXJ,NULL,SFyi,NULL,SFyj,NULL,SFzi,NULL,SFzj,NULL,SDIRi,NULL,SDIRJ'+'\n')
                text.write('PRESOL,F'+'\n')
                text.write('PRESOL,M'+'\n')
                text.write('/output,BEAM-STRESS-LC'+str(LC+1)+'A'+str(angleNR)+',out'+'\n')
                text.write('PRESOL,S,COMP'+'\n')
                text.write('PRESOL,S,PRIN'+'\n')
                text.write('/output'+'\n')
                LCcounter=LCcounter+1
        text.close()
        
'''
class buckling_analysis:
    def __init__(self,wireframe):
        self.wireframe=wireframe
        
    def compute(self):
        text=open('ANSYS-beam188.txt','a')
        text.write('\n'+'!ANSYS BUCKLING ARE CREATED'+'\n')
        bays=len(self.wireframe)
        LCcounter=1
        for LC in range(3):
            for angle in range(2):
                if angle == 0:
                    angleNR = 0
                elif angle == 1:
                    angleNR = 45
                text.write('/SOLU'+'\n')
                text.write('ANTYPE,buckle'+'\n')
                text.write('BUCOPT,LANB,4,'+'\n')
                text.write('MXPAND,4,,,YES'+'\n')
                text.write('LSSOLVE,'+str(LCcounter)+','+str(LCcounter)+',1'+'\n')
                text.write('/POST1'+'\n')
                text.write('/output,BUCK-LC'+str(LC+1)+'A'+str(angleNR)+',out'+'\n')
                text.write('SET,LIST'+'\n')
                text.write('/output'+'\n')
                for buckmode in range(5):
                    if buckmode !=0:
                        text.write('/post1'+'\n')
                        text.write('SET,1,'+str(buckmode)+'\n')
                        text.write('PLNSOL,U,SUM,1,3'+'\n')
                        text.write('/replot'+'\n')
                        text.write('/image,save,BMODE'+str(buckmode)+'-DISP-LC'+str(LC+1)+'A'+str(angleNR)+',png'+'\n')
                        text.write('/post1'+'\n')
                        text.write('PLESOL,F,X,1,3'+'\n')
                        text.write('/replot'+'\n')
                        text.write('/image,save,BMODE'+str(buckmode)+'-FORCEX-LC'+str(LC+1)+'A'+str(angleNR)+',png'+'\n')
                        text.write('/post1'+'\n')
                LCcounter=LCcounter+1
        text.close()
'''
        
def ansys():
#def main():
    #Ed=str(2.e11)
    Ed=str(Input_data.stored_data.Ed)
    
    #wireframe=[[2, 16.69, 42.15365953598298, 17.101249112742856, 19.771649112742857, 13.667817989809011, 16.69, 265.4260787400991, 317.84634046401703, 274.5739212599009, 222.15365953598297, 85.42607874009914, 42.15365953598298, 94.57392125990086, 137.84634046401703, 0.08], [2, 16.69, 38.33478236213366, 19.771649112742857, 22.442049112742858, 16.556211994723174, 0.0, 265.4260787400991, 321.6652176378663, 274.5739212599009, 218.33478236213367, 85.42607874009914, 38.33478236213366, 94.57392125990086, 141.66521763786633, 0.08]]
    wireframe=Jacket.stored_data.wireframe
    #jacketdimensions=[[0.56641827640041886, 0.33985096584025132, 0.022476915730175351, 0.013486149438105211], [0.6230601140404608, 0.37383606842427647, 0.024724607700018286, 0.014834764620010972]]
    jacketdimensions=Jacket.stored_data.Jacket_dimensions
    #sleevedimensions=[[0.080446189201382884, 0.0, 0.9012600000000001, 0.68339089949045051, 5.7605431368905711, 3.7531560450487467, 185011], [0.072292092670387692, 0.0087286592301644549, 0.9012600000000001, 0.82781059973615867, 5.3068320221373169, 3.4001823505574809, 184172]]
    sleevedimensions=Jacket.stored_data.Sleeve_dimensions    
    #tower_load=[[2654083, 0.0, 4922811, 0.0, 178932153, 0.0], [2083014, 0.0, 4922811, 0.0, 117938697, 0.0], [2520451, 0.0, 4922811, 0.0, 140909950, 0.0]]
    tower_load=Tower.stored_data.loadbottom
    #jacket_environmental_load=[[[[195523, 90510, 1035434, 471680], [1139901, 132980, 5910908, 685627], [751635, 127250, 3915778, 657630]], [[306799, 99924, 1624720, 520742], [1788640, 146812, 9274918, 756943], [1179405, 140487, 6144323, 726035]]], [[[225458, 178725, 3876840, 3018066], [2429334, 358812, 40718334, 5982468], [1409910, 321993, 23748111, 5381679]], [[359378, 197343, 6179643, 3332457], [3872332, 396189, 64904591, 6605660], [2247383, 355535, 37854237, 5942287]]]]
    jacket_environmental_load=Jacket.stored_data.environmental_loads_per_bay
    #jacket_gravitational_load=[570869, 744788]
    jacket_gravitational_load=Jacket.stored_data.gravitational_loads_per_bay
    nodecalc=nodebuilder(wireframe)
    jointlist,sleevelist=nodecalc.compute()
    nodeANSYS=nodewriter(wireframe,jointlist,sleevelist)
    nodecount=nodeANSYS.compute()
    elementANSYS=elementwriter(jacketdimensions,sleevedimensions,nodecount,Ed)
    elementANSYS.compute()
    loadANSYS=loadbuilder(wireframe,tower_load,jacket_environmental_load,jacket_gravitational_load)
    loadANSYS.compute()
    staticANSYS=static_analysis(wireframe,jacketdimensions,sleevedimensions)
    staticANSYS.compute()
    #buckANSYS=buckling_analysis(wireframe)
    #buckANSYS.compute()
    
#main()