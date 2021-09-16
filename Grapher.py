# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 14:14:58 2015

@author: Johan Antonissen (windhoos@gmail.com)
"""

import matplotlib.pyplot as plt
from math import sqrt,degrees
import numpy as np
from parts import Tower,Jacket,Piles

def grapher():
    #Tower_dimensions=[[63.38, 3.0, 0.012078829786994007], [58.38, 3.1423268035273897, 0.017956153163013654], [53.38, 3.5070215628012646, 0.020040123216007226], [48.38, 3.809407126189237, 0.021768040721081353], [43.38, 4.0711594059000493, 0.023263768033714567], [38.38, 4.3039358617688075, 0.024593919210107472], [33.38, 4.5148099372622275, 0.02579891392721273], [28.380000000000003, 4.7084321504394708, 0.026905326573939833], [23.380000000000003, 4.8880414766258475, 0.02793166558071913], [18.380000000000003, 5.0559940465612607, 0.028891394551778634], [13.380000000000003, 5.2140637860674284, 0.029794650206099591]]
    Tower_dimensions=Tower.stored_data.Tower_dimensions
    #Tower_loads=[[[2603873, 0.0, 1976371, 0.0, 19529054, 0.0], [1307965, 0.0, 1976371, 0.0, 9809743, 0.0], [1582638, 0.0, 1976371, 0.0, 11869790, 0.0]], [[2609839, 0.0, 2057122, 0.0, 32563334, 0.0], [1380629, 0.0, 2057122, 0.0, 16531229, 0.0], [1670562, 0.0, 2057122, 0.0, 20002790, 0.0]], [[2615409, 0.0, 2182647, 0.0, 45626454, 0.0], [1445397, 0.0, 2171533, 0.0, 23596294, 0.0], [1748931, 0.0, 2171533, 0.0, 28551523, 0.0]], [[2620893, 0.0, 2338999, 0.0, 58717209, 0.0], [1502534, 0.0, 2285944, 0.0, 30966122, 0.0], [1818389, 0.0, 2287014, 0.0, 37469825, 0.0]], [[2626083, 0.0, 2523476, 0.0, 71834651, 0.0], [1553918, 0.0, 2407810, 0.0, 38607252, 0.0], [1884502, 0.0, 2424807, 0.0, 46727052, 0.0]], [[2630844, 0.0, 2734176, 0.0, 84976970, 0.0], [1601308, 0.0, 2548502, 0.0, 46495319, 0.0], [1945499, 0.0, 2584002, 0.0, 56302055, 0.0]], [[2635084, 0.0, 2969659, 0.0, 98141792, 0.0], [1643737, 0.0, 2707407, 0.0, 54607933, 0.0], [2000131, 0.0, 2763939, 0.0, 66166130, 0.0]], [[2638743, 0.0, 3228782, 0.0, 111326359, 0.0], [1680530, 0.0, 2884040, 0.0, 62918602, 0.0], [2047523, 0.0, 2964094, 0.0, 76285265, 0.0]], [[2641783, 0.0, 3510608, 0.0, 124527675, 0.0], [1711249, 0.0, 3077985, 0.0, 71398050, 0.0], [2087104, 0.0, 3184017, 0.0, 86621834, 0.0]], [[2644189, 0.0, 3814345, 0.0, 137742605, 0.0], [1735669, 0.0, 3288865, 0.0, 80015346, 0.0], [2118579, 0.0, 3423294, 0.0, 97136043, 0.0]], [[2645966, 0.0, 4348671, 0.0, 150967992, 0.0], [1753777, 0.0, 4348671, 0.0, 88738962, 0.0], [2141926, 0.0, 4348671, 0.0, 107787305, 0.0]]]
    Tower_loads=Tower.stored_data.Tower_loads
    #Jacket_wireframe=[[2, 16.69, 45.81632876541941, 15.219663782616497, 17.222463782616497, 11.305444969123634, 16.69, 266.5663696375495, 314.1836712345806, 273.4336303624505, 225.8163287654194, 86.56636963754949, 45.81632876541941, 93.43363036245051, 134.1836712345806, 0.06], [2, 16.69, 42.48445357671731, 17.222463782616497, 19.225263782616498, 13.439381916664752, 0.0, 266.5663696375495, 317.51554642328273, 273.4336303624505, 222.4844535767173, 86.56636963754949, 42.48445357671731, 93.43363036245051, 137.5155464232827, 0.06]]
    Jacket_wireframe=Jacket.stored_data.wireframe
    #Jacket_environmental_loads_per_bay=[[[[187362, 85490, 992217, 445519], [1092323, 125604, 5664197, 647599], [720263, 120193, 3752341, 621156]], [[290155, 94342, 1536575, 491653], [1691603, 138611, 8771733, 714660], [1115420, 132639, 5810980, 685478]]], [[[214329, 167733, 3685482, 2832444], [2309423, 336744, 38708504, 5614526], [1340318, 302189, 22575920, 5050687]], [[335885, 185175, 5775672, 3126976], [3619193, 371760, 60661697, 6198352], [2100468, 333612, 35379659, 5575883]]]]
    Jacket_environmental_loads_per_bay=Jacket.stored_data.environmental_loads_per_bay
    #Jacket_gravitational_loads_per_bay=[513550, 659800]
    Jacket_gravitational_loads_per_bay=Jacket.stored_data.gravitational_loads_per_bay
    #Jacket_loads=[[[[[2711133, 0.0, 4348671.0, 0.0, 150967992, 0.0], [2851910, 0.0, 5052064.0, 0.0, 196216814, 0.0]], [[2095364, 0.0, 4348671.0, 0.0, 88738962, 0.0], [2853297, 0.0, 5052064.0, 0.0, 123710597, 0.0]], [[2369811, 0.0, 4348671.0, 0.0, 107787305, 0.0], [2872148, 0.0, 5052064.0, 0.0, 147339456, 0.0]]], [[[2742629, 0.0, 4348671.0, 0.0, 150967992, 0.0], [2951073, 0.0, 5052064.0, 0.0, 196742479, 0.0]], [[2281086, 0.0, 4348671.0, 0.0, 88738962, 0.0], [3451049, 0.0, 5052064.0, 0.0, 126810297, 0.0]], [[2492511, 0.0, 4348671.0, 0.0, 107787305, 0.0], [3265204, 0.0, 5052064.0, 0.0, 149387320, 0.0]]]], [[[[3130410, 0.0, 5052064.0, 0.0, 196216814, 0.0], [3124070, 0.0, 5915109.0, 0.0, 248463365, 0.0]], [[5196830, 0.0, 5052064.0, 0.0, 123710597, 0.0], [5187141, 0.0, 5915109.0, 0.0, 210445691, 0.0]], [[4258247, 0.0, 5052064.0, 0.0, 147339456, 0.0], [4246109, 0.0, 5915109.0, 0.0, 218409598, 0.0]]], [[[3344591, 0.0, 5052064.0, 0.0, 196742479, 0.0], [3334620, 0.0, 5915109.0, 0.0, 252563715, 0.0]], [[7104586, 0.0, 5052064.0, 0.0, 126810297, 0.0], [7089285, 0.0, 5915109.0, 0.0, 245385850, 0.0]], [[5411180, 0.0, 5052064.0, 0.0, 149387320, 0.0], [5392000, 0.0, 5915109.0, 0.0, 239699922, 0.0]]]]]
    Jacket_loads=Jacket.stored_data.loads
    #Jacket_member_loads=[[[[[4311872, 'tension', 'uni-directional load', 3], [758944, 'compression', 'uni-directional load', 4], [6498452, 'compression', 'uni-directional load', 5], [825009, 'tension', 'uni-directional load', 6]], [[2233465, 'tension', 'uni-directional load', 3], [633791, 'compression', 'uni-directional load', 4], [4420044, 'compression', 'uni-directional load', 5], [686169, 'tension', 'uni-directional load', 6]], [[2890530, 'tension', 'uni-directional load', 3], [701141, 'compression', 'uni-directional load', 4], [5077109, 'compression', 'uni-directional load', 5], [759620, 'tension', 'uni-directional load', 6]]], [[[6533618, 'tension', 'uni-directional load', 3], [691534, 'compression', 'uni-directional load', 5], [1967172, 'compression', 'uni-directional load', 4], [611115, 'tension', 'uni-directional load', 3]], [[3647242, 'tension', 'uni-directional load', 3], [566766, 'compression', 'uni-directional load', 5], [1808753, 'compression', 'uni-directional load', 4], [500856, 'tension', 'uni-directional load', 3]], [[4554840, 'tension', 'uni-directional load', 3], [623920, 'compression', 'uni-directional load', 5], [1881322, 'compression', 'uni-directional load', 4], [551364, 'tension', 'uni-directional load', 3]]], [[[2226038, 'compression', 'uni-directional load', 5], [699265, 'compression', 'uni-directional load', 4], [8720197, 'compression', 'uni-directional load', 5], [791284, 'tension', 'uni-directional load', 6]], [[2046772, 'compression', 'uni-directional load', 5], [589007, 'compression', 'uni-directional load', 4], [5833822, 'compression', 'uni-directional load', 5], [666516, 'tension', 'uni-directional load', 6]], [[2128891, 'compression', 'uni-directional load', 5], [639514, 'compression', 'uni-directional load', 4], [6741420, 'compression', 'uni-directional load', 5], [723670, 'tension', 'uni-directional load', 6]]]], [[[[4950007, 'tension', 'uni-directional load', 3], [854085, 'compression', 'uni-directional load', 4], [7392866, 'compression', 'uni-directional load', 5], [919244, 'tension', 'uni-directional load', 6]], [[3460459, 'tension', 'uni-directional load', 3], [1692397, 'compression', 'uni-directional load', 5], [5903317, 'compression', 'uni-directional load', 5], [1797046, 'tension', 'uni-directional load', 6]], [[3883095, 'tension', 'uni-directional load', 3], [1323515, 'compression', 'uni-directional load', 4], [6325954, 'compression', 'uni-directional load', 5], [1412787, 'tension', 'uni-directional load', 6]]], [[[7574534, 'tension', 'uni-directional load', 3], [820542, 'compression', 'uni-directional load', 5], [2212434, 'compression', 'uni-directional load', 4], [735062, 'tension', 'uni-directional load', 3]], [[6136519, 'tension', 'uni-directional load', 3], [1883490, 'compression', 'uni-directional load', 5], [3500980, 'tension', 'counter-directional load', 2], [1687277, 'tension', 'uni-directional load', 3]], [[6441736, 'tension', 'uni-directional load', 3], [1409135, 'compression', 'uni-directional load', 5], [2925949, 'tension', 'counter-directional load', 2], [1262338, 'tension', 'uni-directional load', 3]]], [[[2469718, 'compression', 'uni-directional load', 5], [828809, 'compression', 'uni-directional load', 4], [10017393, 'compression', 'uni-directional load', 5], [925191, 'tension', 'uni-directional load', 6]], [[3908109, 'compression', 'counter-directional load', 1], [1781023, 'compression', 'uni-directional load', 4], [8579378, 'compression', 'uni-directional load', 5], [1988138, 'tension', 'uni-directional load', 6]], [[3266208, 'compression', 'counter-directional load', 1], [1356085, 'compression', 'uni-directional load', 4], [8884595, 'compression', 'uni-directional load', 5], [1513784, 'tension', 'uni-directional load', 6]]]]]
    Jacket_member_loads=Jacket.stored_data.membersort
    #Pile_top_loads=[[[[866934, 0.0, 5035656, 0.0, 236861, 0.0], [866934, 0.0, 5035656, 0.0, 236861, 0.0], [866934, 0.0, -7993993, 0.0, 236861, 0.0], [866934, 0.0, -7993993, 0.0, 236861, 0.0]], [[1968065, 0.0, 4198195, 0.0, 537708, 0.0], [1968065, 0.0, 4198195, 0.0, 537708, 0.0], [1968065, 0.0, -7156532, 0.0, 537708, 0.0], [1968065, 0.0, -7156532, 0.0, 537708, 0.0]], [[1465023, 0.0, 4341663, 0.0, 400268, 0.0], [1465023, 0.0, 4341663, 0.0, 400268, 0.0], [1465023, 0.0, -7300000, 0.0, 400268, 0.0], [1465023, 0.0, -7300000, 0.0, 400268, 0.0]]], [[[956200, 0.0, 7907918, 0.0, 261250, 0.0], [956200, 0.0, -1479168, 0.0, 261250, 0.0], [956200, 0.0, -1479168, 0.0, 261250, 0.0], [956200, 0.0, -10866255, 0.0, 261250, 0.0]], [[2817533, 0.0, 7983090, 0.0, 769797, 0.0], [2817533, 0.0, -1479168, 0.0, 769797, 0.0], [2817533, 0.0, -1479168, 0.0, 769797, 0.0], [2817533, 0.0, -10941427, 0.0, 769797, 0.0]], [[1972140, 0.0, 7631496, 0.0, 538821, 0.0], [1972140, 0.0, -1479168, 0.0, 538821, 0.0], [1972140, 0.0, -1479168, 0.0, 538821, 0.0], [1972140, 0.0, -10589833, 0.0, 538821, 0.0]]]]
    Pile_top_loads=Piles.stored_data.pile_top_loads
    
    #Sequence
    TowerGraph(Tower_dimensions,Tower_loads)
    Jacket_load_per_bay(Jacket_environmental_loads_per_bay,Jacket_gravitational_loads_per_bay)
    Jacket_load_combined(Jacket_wireframe,Tower_loads,Jacket_loads)
    Jacket_wireframe_loads(Jacket_wireframe,Jacket_member_loads)
    Pile_loads(Pile_top_loads)
    
def TowerGraph(dimensions, loads):
    #1) we save tower data for graph use
    Hlist=[]
    Dlist=[]
    wtlist=[]
    fxLC1=[]
    fxLC2=[]
    fxLC3=[]
    fzLC1=[]
    fzLC2=[]
    fzLC3=[]
    myLC1=[]
    myLC2=[]
    myLC3=[]
    for segment in range(len(dimensions)):
        Hlist.append(int(dimensions[segment][0]*1000.0)/1000.0)
        Dlist.append(dimensions[segment][1])
        wtlist.append(dimensions[segment][2])
        fxLC1.append(loads[segment][0][0]/1000.0)
        fxLC2.append(loads[segment][1][0]/1000.0)
        fxLC3.append(loads[segment][2][0]/1000.0)
        fzLC1.append(loads[segment][0][2]/1000.0)
        fzLC2.append(loads[segment][1][2]/1000.0)
        fzLC3.append(loads[segment][2][2]/1000.0)
        myLC1.append(loads[segment][0][4]/1000.0)
        myLC2.append(loads[segment][1][4]/1000.0)
        myLC3.append(loads[segment][2][4]/1000.0)
    #1b) we create a graph for the diameter
    xmin=min(Dlist)*0.95
    ymin=min(Hlist)
    xmax=max(Dlist)*1.05
    ymax=max(Hlist)
    plt.plot(Dlist,Hlist,'k-')
    plt.axis([xmin,xmax,ymin,ymax])
    plt.xlabel('Diameter (m)')
    plt.ylabel('Height (m)')
    plt.title('Tower diameter')
    plt.savefig('Tower - diameter.png',dpi=200)
    plt.show()
    plt.clf()
    
    #1c) we create a graph with tower dimensions
    xmin=min(wtlist)*0.95
    ymin=min(Hlist)
    xmax=max(wtlist)*1.05
    ymax=max(Hlist)
    plt.plot(wtlist,Hlist,'k-')
    plt.axis([xmin,xmax,ymin,ymax])
    plt.xlabel('Wall thickness (m)')
    plt.ylabel('Height (m)')
    plt.savefig('Tower - wall thickness.png',dpi=200)
    plt.show()
    plt.clf()
    
    #1d) we plot the load progression
    #For fx load
    xmin1=min(fxLC1)
    xmin2=min(fxLC2)
    xmin3=min(fxLC3)
    xmin=min(xmin1,xmin2,xmin3)
    xmax1=max(fxLC1)
    xmax2=max(fxLC2)
    xmax3=max(fxLC3)
    xmax=max(xmax1,xmax2,xmax3)*1.1
    ymin=min(Hlist)
    ymax=max(Hlist)
    
    plt.plot(fxLC1,Hlist,'r-',label='Loadcase 1')
    plt.plot(fxLC2,Hlist,'b--',label='Loadcase 2')
    plt.plot(fxLC3,Hlist,'g-.',label='Loadcase 3')
    plt.axis([xmin,xmax,ymin,ymax])
    plt.xlabel('Fx (kN)')
    plt.ylabel('Height (m)')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    plt.savefig('Tower - fx.png',dpi=200,bbox_inches='tight')
    plt.show()
    plt.clf()
    
    #For fz load
    xmin1=min(fzLC1)
    xmin2=min(fzLC2)
    xmin3=min(fzLC3)
    xmin=min(xmin1,xmin2,xmin3)
    xmax1=max(fzLC1)
    xmax2=max(fzLC2)
    xmax3=max(fzLC3)
    xmax=max(xmax1,xmax2,xmax3)*1.1
    ymin=min(Hlist)
    ymax=max(Hlist)
    
    plt.plot(fzLC1,Hlist,'r-',label='Loadcase 1')
    plt.plot(fzLC2,Hlist,'b--',label='Loadcase 2')
    plt.plot(fzLC3,Hlist,'g-.',label='Loadcase 3')
    plt.axis([xmin,xmax,ymin,ymax])
    plt.xlabel('Fz (kN)')
    plt.ylabel('Height (m)')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    plt.savefig('Tower - fz.png',dpi=200,bbox_inches='tight')
    plt.show()
    plt.clf()
    
    #For my load
    xmin1=min(myLC1)
    xmin2=min(myLC2)
    xmin3=min(myLC3)
    xmin=min(xmin1,xmin2,xmin3)
    xmax1=max(myLC1)
    xmax2=max(myLC2)
    xmax3=max(myLC3)
    xmax=max(xmax1,xmax2,xmax3)*1.1
    ymin=min(Hlist)
    ymax=max(Hlist)
    
    plt.plot(myLC1,Hlist,'r-',label='Loadcase 1')
    plt.plot(myLC2,Hlist,'b--',label='Loadcase 2')
    plt.plot(myLC3,Hlist,'g-.',label='Loadcase 3')
    plt.axis([xmin,xmax,ymin,ymax])
    plt.xlabel('My (MNm)')
    plt.ylabel('Height (m)')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    plt.savefig('Tower - my.png',dpi=200,bbox_inches='tight')
    plt.show()
    plt.clf()
    
def Jacket_load_per_bay(environmental_loads_per_bay,gravitational_loads_per_bay):
    #2) we save jacket data for graph use
    #2a) We gather data for estimation loads acting on a bay
    bays=len(environmental_loads_per_bay)
    inflow_angles=len(environmental_loads_per_bay[0])
    loadcases=len(environmental_loads_per_bay[0][0])
    FdragA0L1=[]
    FinertiaA0L1=[]
    FtotA0L1=[]
    MdragA0L1=[]
    MinertiaA0L1=[]
    MtotA0L1=[]
    
    FdragA0L2=[]
    FinertiaA0L2=[]
    FtotA0L2=[]
    MdragA0L2=[]
    MinertiaA0L2=[]
    MtotA0L2=[]
    
    FdragA0L3=[]
    FinertiaA0L3=[]
    FtotA0L3=[]
    MdragA0L3=[]
    MinertiaA0L3=[]
    MtotA0L3=[]
    
    FdragA45L1=[]
    FinertiaA45L1=[]
    FtotA45L1=[]
    MdragA45L1=[]
    MinertiaA45L1=[]
    MtotA45L1=[]
    
    FdragA45L2=[]
    FinertiaA45L2=[]
    FtotA45L2=[]
    MdragA45L2=[]
    MinertiaA45L2=[]
    MtotA45L2=[]
    
    FdragA45L3=[]
    FinertiaA45L3=[]
    FtotA45L3=[]
    MdragA45L3=[]
    MinertiaA45L3=[]
    MtotA45L3=[]
    for bay in range(bays):
        for loadcase in range(loadcases):
            for angle in range(inflow_angles):
                fdrag=int(environmental_loads_per_bay[bay][angle][loadcase][0])/1000.0
                finertia=int(environmental_loads_per_bay[bay][angle][loadcase][1])/1000.0
                ftot=int(sqrt(fdrag**2+finertia**2))
                mdrag=int(environmental_loads_per_bay[bay][angle][loadcase][2])/1000.0
                minertia=int(environmental_loads_per_bay[bay][angle][loadcase][3])/1000.0
                mtot=int(sqrt(mdrag**2+minertia**2))
                if (loadcase == 0) and (angle == 0):
                    FdragA0L1.append(fdrag)
                    FinertiaA0L1.append(finertia)
                    FtotA0L1.append(ftot)
                    MdragA0L1.append(mdrag)
                    MinertiaA0L1.append(minertia)
                    MtotA0L1.append(mtot)
                elif (loadcase == 0) and (angle == 1):
                    FdragA45L1.append(fdrag)
                    FinertiaA45L1.append(finertia)
                    FtotA45L1.append(ftot)
                    MdragA45L1.append(mdrag)
                    MinertiaA45L1.append(minertia)
                    MtotA45L1.append(mtot)
                elif (loadcase == 1) and (angle == 0):
                    FdragA0L2.append(fdrag)
                    FinertiaA0L2.append(finertia)
                    FtotA0L2.append(ftot)
                    MdragA0L2.append(mdrag)
                    MinertiaA0L2.append(minertia)
                    MtotA0L2.append(mtot)
                elif (loadcase == 1) and (angle == 1):
                    FdragA45L2.append(fdrag)
                    FinertiaA45L2.append(finertia)
                    FtotA45L2.append(ftot)
                    MdragA45L2.append(mdrag)
                    MinertiaA45L2.append(minertia)
                    MtotA45L2.append(mtot)
                elif (loadcase == 2) and (angle == 0):
                    FdragA0L3.append(fdrag)
                    FinertiaA0L3.append(finertia)
                    FtotA0L3.append(ftot)
                    MdragA0L3.append(mdrag)
                    MinertiaA0L3.append(minertia)
                    MtotA0L3.append(mtot)
                elif (loadcase == 2) and (angle == 1):
                    FdragA45L3.append(fdrag)
                    FinertiaA45L3.append(finertia)
                    FtotA45L3.append(ftot)
                    MdragA45L3.append(mdrag)
                    MinertiaA45L3.append(minertia)
                    MtotA45L3.append(mtot)
                    
    N=len(FdragA0L1)
    ind = np.arange(N)
    margin=0.025
    width=(1-2*margin)/6.0 #width of ONE bar in ONE bar grouping
    
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),ha='center', va='bottom')
    
    #2b) Create graphs for drag forces
    fig=plt.figure()
    ax=fig.add_subplot(111)

    rectsFdA0L1 = ax.bar(ind, FdragA0L1, width, color=(1.0,0.0,0.0),hatch=('\\'))
    rectsFdA45L1 = ax.bar(ind+width, FdragA45L1, width, color=(1.0,0.5,0.0),hatch=('//'))
    rectsFdA0L2 = ax.bar(ind+2*(width), FdragA0L2, width, color=(0.0,1.0,0.0),hatch=('.'))
    rectsFdA45L2 = ax.bar(ind+3*(width), FdragA45L2, width, color=(0.0,1.0,0.5),hatch=('o'))
    rectsFdA0L3 = ax.bar(ind+4*(width), FdragA0L3, width, color=(0.0,0.0,1.0),hatch=('+'))
    rectsFdA45L3 = ax.bar(ind+5*(width), FdragA45L3, width, color=(0.0,0.5,1.0),hatch=('-'))
    ymin,ymax=ax.get_ylim()
    ax.set_ylim(ymin,ymax*1.1)
    
    
    ax.set_ylabel('Force (kN)')
    ax.set_title('Drag force per bay,inflow angle,load case')
    ax.set_xticks(ind+width*3)
    xlabel=[]
    for bay in range(bays):
        if bay==0:
            add=' (top)'
        elif bay==bays-1:
            add=' (bottom)'
        else:
            add=''
        xlabel.append('bay '+str(bay+1)+add)
        
    ax.set_xticklabels(xlabel)
    
    ax.legend( (rectsFdA0L1[0], rectsFdA45L1[0],rectsFdA0L2[0], rectsFdA45L2[0],rectsFdA0L3[0], rectsFdA45L3[0]), ('A0 LC1','A45 LC1','A0 LC2','A45 LC2','A0 LC3','A45 LC3')
    ,loc='center left', bbox_to_anchor=(1, 0.5) )
                
    autolabel(rectsFdA0L1)
    autolabel(rectsFdA45L1)
    autolabel(rectsFdA0L2)
    autolabel(rectsFdA45L2)
    autolabel(rectsFdA0L3)
    autolabel(rectsFdA45L3)
    
    plt.savefig('Jacket - Drag forces.png',dpi=200,bbox_inches='tight')
    plt.show()
    plt.clf()
    
    #2c) Now for the inertia forces
    fig=plt.figure()
    ax=fig.add_subplot(111)

    rectsFiA0L1 = ax.bar(ind, FinertiaA0L1, width, color=(1.0,0.0,0.0),hatch=('\\'))
    rectsFiA45L1 = ax.bar(ind+width, FinertiaA45L1, width, color=(1.0,0.5,0.0),hatch=('//'))
    rectsFiA0L2 = ax.bar(ind+2*(width), FinertiaA0L2, width, color=(0.0,1.0,0.0),hatch=('.'))
    rectsFiA45L2 = ax.bar(ind+3*(width), FinertiaA45L2, width, color=(0.0,1.0,0.5),hatch=('o'))
    rectsFiA0L3 = ax.bar(ind+4*(width), FinertiaA0L3, width, color=(0.0,0.0,1.0),hatch=('+'))
    rectsFiA45L3 = ax.bar(ind+5*(width), FinertiaA45L3, width, color=(0.0,0.5,1.0),hatch=('-'))
    ymin,ymax=ax.get_ylim()
    ax.set_ylim(ymin,ymax*1.1)
    
    ax.set_ylabel('Force (kN)')
    ax.set_title('Inertia force per bay,inflow angle,load case')
    ax.set_xticks(ind+width*3)
    xlabel=[]
    for bay in range(bays):
        if bay==0:
            add=' (top)'
        elif bay==bays-1:
            add=' (bottom)'
        else:
            add=''
        xlabel.append('bay '+str(bay+1)+add)
        
    ax.set_xticklabels(xlabel)
    
    ax.legend( (rectsFiA0L1[0], rectsFiA45L1[0],rectsFiA0L2[0], rectsFiA45L2[0],rectsFiA0L3[0], rectsFiA45L3[0]), ('A0 LC1','A45 LC1','A0 LC2','A45 LC2','A0 LC3','A45 LC3')
    ,loc='center left', bbox_to_anchor=(1, 0.5) )
                
    autolabel(rectsFiA0L1)
    autolabel(rectsFiA45L1)
    autolabel(rectsFiA0L2)
    autolabel(rectsFiA45L2)
    autolabel(rectsFiA0L3)
    autolabel(rectsFiA45L3)
    
    plt.savefig('Jacket - Inertia forces.png',dpi=200,bbox_inches='tight')
    plt.show()
    plt.clf()
    
    #2d) Now for the combined forces
    fig=plt.figure()
    ax=fig.add_subplot(111)

    rectsFcA0L1 = ax.bar(ind, FtotA0L1, width, color=(1.0,0.0,0.0),hatch=('\\'))
    rectsFcA45L1 = ax.bar(ind+width, FtotA45L1, width, color=(1.0,0.5,0.0),hatch=('//'))
    rectsFcA0L2 = ax.bar(ind+2*(width), FtotA0L2, width, color=(0.0,1.0,0.0),hatch=('.'))
    rectsFcA45L2 = ax.bar(ind+3*(width), FtotA45L2, width, color=(0.0,1.0,0.5),hatch=('o'))
    rectsFcA0L3 = ax.bar(ind+4*(width), FtotA0L3, width, color=(0.0,0.0,1.0),hatch=('+'))
    rectsFcA45L3 = ax.bar(ind+5*(width), FtotA45L3, width, color=(0.0,0.5,1.0),hatch=('-'))
    ymin,ymax=ax.get_ylim()
    ax.set_ylim(ymin,ymax*1.1)
    
    ax.set_ylabel('Force (kN)')
    ax.set_title('Combined force per bay,inflow angle,load case')
    ax.set_xticks(ind+width*3)
    xlabel=[]
    for bay in range(bays):
        if bay==0:
            add=' (top)'
        elif bay==bays-1:
            add=' (bottom)'
        else:
            add=''
        xlabel.append('bay '+str(bay+1)+add)
        
    ax.set_xticklabels(xlabel)
    
    ax.legend( (rectsFcA0L1[0], rectsFcA45L1[0],rectsFcA0L2[0], rectsFcA45L2[0],rectsFcA0L3[0], rectsFcA45L3[0]), ('A0 LC1','A45 LC1','A0 LC2','A45 LC2','A0 LC3','A45 LC3')
    ,loc='center left', bbox_to_anchor=(1, 0.5) )
                
    autolabel(rectsFcA0L1)
    autolabel(rectsFcA45L1)
    autolabel(rectsFcA0L2)
    autolabel(rectsFcA45L2)
    autolabel(rectsFcA0L3)
    autolabel(rectsFcA45L3)
    
    plt.savefig('Jacket - Combined force.png',dpi=200,bbox_inches='tight')
    plt.show()
    plt.clf()
    
    #2e) Now for the drag moment
    fig=plt.figure()
    ax=fig.add_subplot(111)

    rectsMdA0L1 = ax.bar(ind, MdragA0L1, width, color=(1.0,0.0,0.0),hatch=('\\'))
    rectsMdA45L1 = ax.bar(ind+width, MdragA45L1, width, color=(1.0,0.5,0.0),hatch=('//'))
    rectsMdA0L2 = ax.bar(ind+2*(width), MdragA0L2, width, color=(0.0,1.0,0.0),hatch=('.'))
    rectsMdA45L2 = ax.bar(ind+3*(width), MdragA45L2, width, color=(0.0,1.0,0.5),hatch=('o'))
    rectsMdA0L3 = ax.bar(ind+4*(width), MdragA0L3, width, color=(0.0,0.0,1.0),hatch=('+'))
    rectsMdA45L3 = ax.bar(ind+5*(width), MdragA45L3, width, color=(0.0,0.5,1.0),hatch=('-'))
    ymin,ymax=ax.get_ylim()
    ax.set_ylim(ymin,ymax*1.1)
    
    ax.set_ylabel('Moment (kNm)')
    ax.set_title('Drag induced moment per bay,inflow angle,load case')
    ax.set_xticks(ind+width*3)
    xlabel=[]
    for bay in range(bays):
        if bay==0:
            add=' (top)'
        elif bay==bays-1:
            add=' (bottom)'
        else:
            add=''
        xlabel.append('bay '+str(bay+1)+add)
        
    ax.set_xticklabels(xlabel)
    
    ax.legend( (rectsMdA0L1[0], rectsMdA45L1[0],rectsMdA0L2[0], rectsMdA45L2[0],rectsMdA0L3[0], rectsMdA45L3[0]), ('A0 LC1','A45 LC1','A0 LC2','A45 LC2','A0 LC3','A45 LC3')
    ,loc='center left', bbox_to_anchor=(1, 0.5) )
                
    autolabel(rectsMdA0L1)
    autolabel(rectsMdA45L1)
    autolabel(rectsMdA0L2)
    autolabel(rectsMdA45L2)
    autolabel(rectsMdA0L3)
    autolabel(rectsMdA45L3)
    
    plt.savefig('Jacket - Drag moment.png',dpi=200,bbox_inches='tight')
    plt.show()
    plt.clf()
    
    #2f) And for inertia moment
    fig=plt.figure()
    ax=fig.add_subplot(111)

    rectsMiA0L1 = ax.bar(ind, MinertiaA0L1, width, color=(1.0,0.0,0.0),hatch=('\\'))
    rectsMiA45L1 = ax.bar(ind+width, MinertiaA45L1, width, color=(1.0,0.5,0.0),hatch=('//'))
    rectsMiA0L2 = ax.bar(ind+2*(width), MinertiaA0L2, width, color=(0.0,1.0,0.0),hatch=('.'))
    rectsMiA45L2 = ax.bar(ind+3*(width), MinertiaA45L2, width, color=(0.0,1.0,0.5),hatch=('o'))
    rectsMiA0L3 = ax.bar(ind+4*(width), MinertiaA0L3, width, color=(0.0,0.0,1.0),hatch=('+'))
    rectsMiA45L3 = ax.bar(ind+5*(width), MinertiaA45L3, width, color=(0.0,0.5,1.0),hatch=('-'))
    ymin,ymax=ax.get_ylim()
    ax.set_ylim(ymin,ymax*1.1)
    
    ax.set_ylabel('Moment (kNm)')
    ax.set_title('Inertia induced moment per bay,inflow angle,load case')
    ax.set_xticks(ind+width*3)
    xlabel=[]
    for bay in range(bays):
        if bay==0:
            add=' (top)'
        elif bay==bays-1:
            add=' (bottom)'
        else:
            add=''
        xlabel.append('bay '+str(bay+1)+add)
        
    ax.set_xticklabels(xlabel)
    
    ax.legend( (rectsMiA0L1[0], rectsMiA45L1[0],rectsMiA0L2[0], rectsMiA45L2[0],rectsMiA0L3[0], rectsMiA45L3[0]), ('A0 LC1','A45 LC1','A0 LC2','A45 LC2','A0 LC3','A45 LC3')
    ,loc='center left', bbox_to_anchor=(1, 0.5) )
                
    autolabel(rectsMiA0L1)
    autolabel(rectsMiA45L1)
    autolabel(rectsMiA0L2)
    autolabel(rectsMiA45L2)
    autolabel(rectsMiA0L3)
    autolabel(rectsMiA45L3)
    
    plt.savefig('Jacket - Inertia moment.png',dpi=200,bbox_inches='tight')
    plt.show()
    plt.clf()
    
    #2g) And combined moment
    fig=plt.figure()
    ax=fig.add_subplot(111)

    rectsMtotA0L1 = ax.bar(ind, MtotA0L1, width, color=(1.0,0.0,0.0),hatch=('\\'))
    rectsMtotA45L1 = ax.bar(ind+width, MtotA45L1, width, color=(1.0,0.5,0.0),hatch=('//'))
    rectsMtotA0L2 = ax.bar(ind+2*(width), MtotA0L2, width, color=(0.0,1.0,0.0),hatch=('.'))
    rectsMtotA45L2 = ax.bar(ind+3*(width), MtotA45L2, width, color=(0.0,1.0,0.5),hatch=('o'))
    rectsMtotA0L3 = ax.bar(ind+4*(width), MtotA0L3, width, color=(0.0,0.0,1.0),hatch=('+'))
    rectsMtotA45L3 = ax.bar(ind+5*(width), MtotA45L3, width, color=(0.0,0.5,1.0),hatch=('-'))
    ymin,ymax=ax.get_ylim()
    ax.set_ylim(ymin,ymax*1.1)
    
    ax.set_ylabel('Moment (kNm)')
    ax.set_title('Combined moment per bay,inflow angle,load case')
    ax.set_xticks(ind+width*3)
    xlabel=[]
    for bay in range(bays):
        if bay==0:
            add=' (top)'
        elif bay==bays-1:
            add=' (bottom)'
        else:
            add=''
        xlabel.append('bay '+str(bay+1)+add)
        
    ax.set_xticklabels(xlabel)
    
    ax.legend( (rectsMtotA0L1[0], rectsMtotA45L1[0],rectsMtotA0L2[0], rectsMtotA45L2[0],rectsMtotA0L3[0], rectsMtotA45L3[0]), ('A0 LC1','A45 LC1','A0 LC2','A45 LC2','A0 LC3','A45 LC3')
    ,loc='center left', bbox_to_anchor=(1, 0.5) )
                
    autolabel(rectsMtotA0L1)
    autolabel(rectsMtotA45L1)
    autolabel(rectsMtotA0L2)
    autolabel(rectsMtotA45L2)
    autolabel(rectsMtotA0L3)
    autolabel(rectsMtotA45L3)
    
    plt.savefig('Jacket - Combined moment.png',dpi=200,bbox_inches='tight')
    plt.show()
    plt.clf()
    
    #2h) Weight per bay
    N=len(gravitational_loads_per_bay)
    width = 0.8
    ind = np.arange(N)
    for bay in range(N):
        gravitational_loads_per_bay[bay]=gravitational_loads_per_bay[bay]/1000.0
        
    Yval=gravitational_loads_per_bay
    fig,ax=plt.subplots()
    rectangle=ax.bar(ind,Yval,width,color=(0.0,0.5,1.0))
    ax.set_ylabel('Weight (kN)')
    ax.set_title('Jacket weight per bay')
    ax.set_xticks(ind+width*0.5)
    xlabel=[]
    for bay in range(N):
        if bay==0:
            add=' (top)'
        elif bay==N-1:
            add=' (bottom)'
        else:
            add=''
        xlabel.append('bay '+str(bay+1)+add)
        
    ax.set_xticklabels(xlabel)
    autolabel(rectangle)
    
    plt.savefig('Jacket - bay weight.png',dpi=200,bbox_inches='tight')
    plt.show()
    plt.clf()
    
def Jacket_load_combined(wireframe,tower_loads,jacket_loads):
    #First we gather information for the y axis
    Yloc=[]
    for bay in range(len(wireframe)):
        Hbay=wireframe[bay][1]
        HbayBOT=wireframe[bay][6]
        HbayTOP=Hbay+HbayBOT
        Yloc.append(HbayTOP)
        Yloc.append(HbayTOP)
        if bay == len(wireframe)-1:
            Yloc.append(0.0)
            Yloc.append(0.0)
    YlocABOVE=[]
    YlocMIDDLE=[]
    YlocBELOW=[]
    for height in range(len(Yloc)):
        YlocABOVE.append(Yloc[height]+1.0)
        YlocABOVE.append(Yloc[height]+1.0)
    for height in range(len(Yloc)):
        YlocMIDDLE.append(Yloc[height])
        YlocMIDDLE.append(Yloc[height])
    for height in range(len(Yloc)):
        YlocBELOW.append(Yloc[height]-1.0)
        YlocBELOW.append(Yloc[height]-1.0)
            
    #Then we gather information for the x axis
    Fxlist=[]
    Fzlist=[]
    Mylist=[]
    for bay in range(len(wireframe)):
        for angle in range(2):
            if bay == 0:
                Fxlist.append([])
                Fzlist.append([])
                Mylist.append([])
            for loadcase in range(len(jacket_loads[bay][angle])):
                if bay == 0:
                    Fxlist[angle].append([])
                    Fzlist[angle].append([])
                    Mylist[angle].append([])
                if bay ==0:
                    Fxlist[angle][loadcase].append(0.0)
                    Fxlist[angle][loadcase].append(tower_loads[-1][loadcase][0]/1000.0)
                    Fzlist[angle][loadcase].append(0.0)
                    Fzlist[angle][loadcase].append(tower_loads[-1][loadcase][2]/1000.0)
                    Mylist[angle][loadcase].append(0.0)
                    Mylist[angle][loadcase].append(tower_loads[-1][loadcase][4]/1000000.0)
                else:
                    Fxlist[angle][loadcase].append(Fxlist[angle][loadcase][-1])
                    Fxlist[angle][loadcase].append(jacket_loads[bay-1][angle][loadcase][1][0]/1000.0)
                    Fzlist[angle][loadcase].append(Fzlist[angle][loadcase][-1])
                    Fzlist[angle][loadcase].append(jacket_loads[bay-1][angle][loadcase][1][2]/1000.0)
                    Mylist[angle][loadcase].append(jacket_loads[bay-1][angle][loadcase][1][4]/1000000.0)
                    Mylist[angle][loadcase].append(jacket_loads[bay-1][angle][loadcase][1][4]/1000000.0)
                if bay == len(wireframe)-1:
                    Fxlist[angle][loadcase].append(Fxlist[angle][loadcase][-1])
                    Fxlist[angle][loadcase].append(0.0)
                    Fzlist[angle][loadcase].append(Fzlist[angle][loadcase][-1])
                    Fzlist[angle][loadcase].append(0.0)
                    Mylist[angle][loadcase].append(jacket_loads[bay][angle][loadcase][1][4]/1000000.0) #TODO: changed here
                    Mylist[angle][loadcase].append(0.0)
                    
    #First we create a plot for fx:
    Ymin=-1.0
    Ymax=max(Yloc)
    Xmin='?'
    Xmax='?'
    for angle in range(len(Fxlist)):
        for loadcase in range(len(Fxlist[angle])):
            for load in range(len(Fxlist[angle][loadcase])):
                if (Xmin == '?') and (Fxlist[angle][loadcase][load] != 0.0):
                    Xmin=Fxlist[angle][loadcase][load]
                if (Fxlist[angle][loadcase][load] != 0.0) and (Fxlist[angle][loadcase][load] <= Xmin):
                    Xmin=Fxlist[angle][loadcase][load]
                if (Xmax == '?') and (Fxlist[angle][loadcase][load] != 0.0):
                    Xmax=Fxlist[angle][loadcase][load]
                if (Fxlist[angle][loadcase][load] != 0.0) and (Fxlist[angle][loadcase][load] >= Xmax):
                    Xmax=Fxlist[angle][loadcase][load]
    
    Ymax=Ymax*1.05
    Xmin=Xmin*0.95
    Xmax=Xmax*1.05
    
    XcutABOVE=[]

    for location in range(int(len(Yloc)/2)):
         XcutABOVE.append(0.0)
         XcutABOVE.append(Xmax*2)
         XcutABOVE.append(0.0)
         XcutABOVE.append(0.0)
    plt.plot(XcutABOVE,YlocABOVE,'k:',linewidth=0.3)
    
    Xcut=[]
    for location in range(int(len(Yloc)/2)):
         Xcut.append(0.0)
         Xcut.append(Xmax*2)
         Xcut.append(0.0)
         Xcut.append(0.0)
    plt.plot(Xcut,YlocMIDDLE,'k-',linewidth=0.5)
    
    XcutBELOW=[]
    for location in range(int(len(Yloc)/2)):
         XcutBELOW.append(0.0)
         XcutBELOW.append(Xmax*2)
         XcutBELOW.append(0.0)
         XcutBELOW.append(0.0)
    plt.plot(XcutBELOW,YlocBELOW,'k:',linewidth=0.3)    
    
    for angle in range(len(Fxlist)):
        for loadcase in range(len(Fxlist[angle])):
            if (loadcase==0) and (angle==0):
                color='r-'
                labelname='A0 LC1'
                line=1.0
            elif (loadcase==0) and (angle==1):
                color='r-'
                labelname='A45 LC1'
                line=1.5
            elif (loadcase==1) and (angle==0):
                color='g-.'
                labelname='A0 LC2'
                line=1.0
            elif (loadcase==1) and (angle==1):
                color='g-.'
                labelname='A45 LC2'
                line=1.5
            elif (loadcase==2) and (angle==0):
                color='b--'
                labelname='A0 LC3'
                line=1.0
            elif (loadcase==2) and (angle==1):
                color='b--'
                labelname='A45 LC3'
                line=1.5
            plt.plot(Fxlist[angle][loadcase],Yloc,color,label=labelname,linewidth=line)
            
    plt.axis([Xmin,Xmax,Ymin,Ymax])
    plt.xlabel('Fx (kN)')
    plt.ylabel('Height (m)')
    plt.legend(bbox_to_anchor=(1.05,1), loc=2, borderaxespad=0.)
    plt.title('Combined Fx load distribution.png')
    plt.savefig('Jacket - Combined Fx load distribution.png',dpi=200,bbox_inches='tight')
    plt.show()
    plt.clf()
    
    #Second we create a plot for fz:
    Ymin=-1.0
    Ymax=max(Yloc)
    Xmin='?'
    Xmax='?'
    for angle in range(len(Fzlist)):
        for loadcase in range(len(Fzlist[angle])):
            for load in range(len(Fzlist[angle][loadcase])):
                if (Xmin == '?') and (Fzlist[angle][loadcase][load] != 0.0):
                    Xmin=Fzlist[angle][loadcase][load]
                if (Fzlist[angle][loadcase][load] != 0.0) and (Fzlist[angle][loadcase][load] <= Xmin):
                    Xmin=Fzlist[angle][loadcase][load]
                if (Xmax == '?') and (Fzlist[angle][loadcase][load] != 0.0):
                    Xmax=Fzlist[angle][loadcase][load]
                if (Fzlist[angle][loadcase][load] != 0.0) and (Fzlist[angle][loadcase][load] >= Xmax):
                    Xmax=Fzlist[angle][loadcase][load]
    
    Ymax=Ymax*1.05
    Xmin=Xmin*0.95
    Xmax=Xmax*1.05
    
    XcutABOVE=[]
    for location in range(int(len(Yloc)/2)):
         XcutABOVE.append(0.0)
         XcutABOVE.append(Xmax*2)
         XcutABOVE.append(0.0)
         XcutABOVE.append(0.0)
    plt.plot(XcutABOVE,YlocABOVE,'k:',linewidth=0.3)
    
    Xcut=[]
    for location in range(int(len(Yloc)/2)):
         Xcut.append(0.0)
         Xcut.append(Xmax*2)
         Xcut.append(0.0)
         Xcut.append(0.0)
    plt.plot(Xcut,YlocMIDDLE,'k-',linewidth=0.5)
    
    XcutBELOW=[]
    for location in range(int(len(Yloc)/2)):
         XcutBELOW.append(0.0)
         XcutBELOW.append(Xmax*2)
         XcutBELOW.append(0.0)
         XcutBELOW.append(0.0)
    plt.plot(XcutBELOW,YlocBELOW,'k:',linewidth=0.3)       
    
    for angle in range(len(Fzlist)):
        for loadcase in range(len(Fzlist[angle])):
            if (loadcase==0) and (angle==0):
                color='r-'
                labelname='A0 LC1'
                line=1.0
            elif (loadcase==0) and (angle==1):
                color='r-'
                labelname='A45 LC1'
                line=1.5
            elif (loadcase==1) and (angle==0):
                color='g-.'
                labelname='A0 LC2'
                line=1.0
            elif (loadcase==1) and (angle==1):
                color='g-.'
                labelname='A45 LC2'
                line=1.5
            elif (loadcase==2) and (angle==0):
                color='b--'
                labelname='A0 LC3'
                line=1.0
            elif (loadcase==2) and (angle==1):
                color='b--'
                labelname='A45 LC3'
                line=1.5
            plt.plot(Fzlist[angle][loadcase],Yloc,color,label=labelname,linewidth=line)
            
    plt.axis([Xmin,Xmax,Ymin,Ymax])
    plt.xlabel('Fz (kN)')
    plt.ylabel('Height (m)')
    plt.legend(bbox_to_anchor=(1.05,1), loc=2, borderaxespad=0.)
    plt.title('Combined Fz load distribution.png')
    plt.savefig('Jacket - Combined Fz load distribution.png',dpi=200,bbox_inches='tight')
    plt.show()
    plt.clf()
    
    #Third we create a plot for my:
    Ymin=-1.0
    Ymax=max(Yloc)
    Xmin='?'
    Xmax='?'
    for angle in range(len(Mylist)):
        for loadcase in range(len(Mylist[angle])):
            for load in range(len(Mylist[angle][loadcase])):
                if (Xmin == '?') and (Mylist[angle][loadcase][load] != 0.0):
                    Xmin=Mylist[angle][loadcase][load]
                if (Mylist[angle][loadcase][load] != 0.0) and (Mylist[angle][loadcase][load] <= Xmin):
                    Xmin=Mylist[angle][loadcase][load]
                if (Xmax == '?') and (Mylist[angle][loadcase][load] != 0.0):
                    Xmax=Mylist[angle][loadcase][load]
                if (Mylist[angle][loadcase][load] != 0.0) and (Mylist[angle][loadcase][load] >= Xmax):
                    Xmax=Mylist[angle][loadcase][load]
    
    Ymax=Ymax*1.05
    Xmin=Xmin*0.95
    Xmax=Xmax*1.05
    
    XcutABOVE=[]

    for location in range(int(len(Yloc)/2)):
         XcutABOVE.append(0.0)
         XcutABOVE.append(Xmax*2)
         XcutABOVE.append(0.0)
         XcutABOVE.append(0.0)
    plt.plot(XcutABOVE,YlocABOVE,'k:',linewidth=0.3)
    
    Xcut=[]
    for location in range(int(len(Yloc)/2)):
         Xcut.append(0.0)
         Xcut.append(Xmax*2)
         Xcut.append(0.0)
         Xcut.append(0.0)
    plt.plot(Xcut,YlocMIDDLE,'k-',linewidth=0.5)
    
    XcutBELOW=[]
    for location in range(int(len(Yloc)/2)):
         XcutBELOW.append(0.0)
         XcutBELOW.append(Xmax*2)
         XcutBELOW.append(0.0)
         XcutBELOW.append(0.0)
    plt.plot(XcutBELOW,YlocBELOW,'k:',linewidth=0.3)       
    
    for angle in range(len(Mylist)):
        for loadcase in range(len(Mylist[angle])):
            if (loadcase==0) and (angle==0):
                color='r-'
                labelname='A0 LC1'
                line=1.0
            elif (loadcase==0) and (angle==1):
                color='r-'
                labelname='A45 LC1'
                line=1.5
            elif (loadcase==1) and (angle==0):
                color='g-.'
                labelname='A0 LC2'
                line=1.0
            elif (loadcase==1) and (angle==1):
                color='g-.'
                labelname='A45 LC2'
                line=1.5
            elif (loadcase==2) and (angle==0):
                color='b--'
                labelname='A0 LC3'
                line=1.0
            elif (loadcase==2) and (angle==1):
                color='b--'
                labelname='A45 LC3'
                line=1.5
            plt.plot(Mylist[angle][loadcase],Yloc,color,label=labelname,linewidth=line)
            
    plt.axis([Xmin,Xmax,Ymin,Ymax])
    plt.xlabel('My (MNm)')
    plt.ylabel('Height (m)')
    plt.legend(bbox_to_anchor=(1.05,1), loc=2, borderaxespad=0.)
    plt.title('Combined My load distribution.png')
    plt.savefig('Jacket - Combined My load distribution.png',dpi=200,bbox_inches='tight')
    plt.show()
    plt.clf()
        
def Jacket_wireframe_loads(wireframe,member_loads):
    for LC in range(len(member_loads[0][0])):
        def propperties(Datalist):
            if Datalist[1]=='tension':
                color = 'green'
            elif Datalist[1]=='compression':
                color = 'red'
            return int(Datalist[0]/100.0)/10.0,color
            
        #first we determine locations of nodes
        Yloc=[]
        Xloc=[]
        for bay in range(len(wireframe)):
            Yloc.append([])
            Xloc.append([])
            Hbay=wireframe[bay][1]
            HbayBOT=wireframe[bay][6]
            HbayTOP=Hbay+HbayBOT
            Yloc[bay].append(HbayTOP)
            Yloc[bay].append(HbayBOT)
    
            BbayTOP=wireframe[bay][3]
            BbayBOT=wireframe[bay][4]
            Xloc[bay].append(BbayTOP)  
            Xloc[bay].append(BbayBOT)
                
        #Second we draw the wireframe of these nodes
        frame0=[]
        for bay in range(len(wireframe)):
            x1=-Xloc[bay][0]/2.0
            y1=Yloc[bay][0]
            x2=Xloc[bay][1]/2.0
            y2=Yloc[bay][1]
            x3=Xloc[bay][0]/2.0
            y3=y1
            x4=-Xloc[bay][1]/2.0
            y4=Yloc[bay][1]
            x5=x1
            y5=y1
            
            frame0.append([[x1,x2,x3,x4,x5],[y1,y2,y3,y4,y5]])
            
        xmin0=min(frame0[-1][0])*1.3
        xmax0=abs(xmin0)
        ymin0=-1
        ymax0=max(frame0[0][1])*1.1
        
        for bay in range(len(wireframe)):
            DATAleftleg=member_loads[bay][0][LC][0][0]
            DATAleftbrace=member_loads[bay][0][LC][0][1]
            DATArightleg=member_loads[bay][0][LC][1][0]
            DATArightbrace=member_loads[bay][0][LC][1][1]
            
            Fll,colorll=propperties(DATAleftleg)
            Flb,colorlb=propperties(DATAleftbrace)
            Frl,colorrl=propperties(DATArightleg)
            Frb,colorrb=propperties(DATArightbrace)
            
            
            plt.plot(frame0[bay][0],frame0[bay][1],'k')
            
            #plot left brace
            plt.text(frame0[bay][0][0]*3/4+frame0[bay][0][1]*1/4, frame0[bay][1][0]*3/4+frame0[bay][1][1]*1/4+wireframe[bay][1]*0.1, str(Flb), color=colorlb, rotation=-wireframe[bay][2]*0.5,ha='center', va='center')
            #plot right leg
            plt.text((frame0[bay][0][1]+frame0[bay][0][2])/2.+.05*wireframe[bay][4], (frame0[bay][1][1]+frame0[bay][1][2])/2.+wireframe[bay][1]*0.1, str(Frl), color=colorrl, rotation=90+degrees(wireframe[bay][15])*2,ha='center', va='center')
            #plot right brace
            plt.text(frame0[bay][0][2]*1/4+frame0[bay][0][3]*3/4, frame0[bay][1][2]*1/3+frame0[bay][1][3]*2/3, str(Frb), color=colorrb, rotation=wireframe[bay][2]*0.5,ha='center', va='center')
            #plot left leg
            plt.text((frame0[bay][0][3]+frame0[bay][0][4])/2.-.05*wireframe[bay][4], (frame0[bay][1][3]+frame0[bay][1][4])/2., str(Fll), color=colorll, rotation=90-degrees(wireframe[bay][15])*2,ha='center', va='center')
            
        plt.axis([xmin0,xmax0,ymin0,ymax0])
        plt.title('Jacket - Member loads (kN) 0 degree, loadcase '+str(LC+1))
        plt.xlabel('X-location (m)')
        plt.ylabel('Y-location (m)')
        #plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        plt.savefig('Jacket - Member loads 0 deg LC '+str(LC+1)+'.png',dpi=200,bbox_inches='tight')
        plt.show()
        plt.clf()
        
        frame45=[]
        for bay in range(len(wireframe)):
            x1=-Xloc[bay][0]*sqrt(2)/2.0
            y1=Yloc[bay][0]
            x2=0.0
            y2=Yloc[bay][1]
            x3=Xloc[bay][0]*sqrt(2)/2.0
            y3=y1
            x4=Xloc[bay][1]*sqrt(2)/2.0
            y4=y2
            x5=0.0
            y5=y1
            x6=0.0
            y6=y2
            x7=x5
            y7=y5
            x8=-Xloc[bay][1]*sqrt(2)/2.0
            y8=y2
            x9=x1
            y9=y1
            frame45.append([[x1,x2,x3,x4,x5,x6,x7,x8,x9],[y1,y2,y3,y4,y5,y6,y7,y8,y9]])
        
        xmin45=min(frame45[-1][0])*1.3
        xmax45=abs(xmin45)
        ymin45=-1
        ymax45=max(frame45[0][1])*1.1
        
        for bay in range(len(wireframe)):
            DATAleftleftleg=member_loads[bay][1][LC][0][0]
            DATAleftleftbrace=member_loads[bay][1][LC][0][1]
            DATAleftrightleg=member_loads[bay][1][LC][1][0]
            DATAleftrightbrace=member_loads[bay][1][LC][1][1]
        
            DATArightleftleg=member_loads[bay][2][LC][0][0]
            DATArightleftbrace=member_loads[bay][2][LC][0][1]
            DATArightrightleg=member_loads[bay][2][LC][1][0] 
            DATArightrightbrace=member_loads[bay][2][LC][1][1]
            
            Flll,colorlll=propperties(DATAleftleftleg)
            Fllb,colorllb=propperties(DATAleftleftbrace)
            Flrl,colorlrl=propperties(DATAleftrightleg)
            Flrb,colorlrb=propperties(DATAleftrightbrace)
            
            Frll,colorrll=propperties(DATArightleftleg)
            Frlb,colorrlb=propperties(DATArightleftbrace)
            Frrl,colorrrl=propperties(DATArightrightleg)
            Frrb,colorrrb=propperties(DATArightrightbrace)
            
            #select largest of centre leg loads
            if Flrl >= Frll:
                Fmid=Flrl
                colormid=colorlrl
                #directionmid=directionlrl
            else:
                Fmid=Frll
                colormid=colorrll
                #directionmid=directionrll
            
            plt.plot(frame45[bay][0],frame45[bay][1],'k')
            
            plt.text((1.5*frame45[bay][0][0]+frame45[bay][0][1])/2.,(frame45[bay][1][0]+frame45[bay][1][1])/2.+wireframe[bay][1]*0.4,str(Fllb), color=colorllb,rotation=-45+wireframe[bay][2]*0.1,ha='center', va='center')
            plt.text((frame45[bay][0][1]+1.25*frame45[bay][0][2])/2.,(frame45[bay][1][1]+frame45[bay][1][2])/2.+wireframe[bay][1]*0.3,str(Frrb), color=colorrrb,rotation=45-wireframe[bay][2]*0.1,ha='center', va='center')
            plt.text((frame45[bay][0][2]+frame45[bay][0][3])/2.+0.05*wireframe[bay][4],(frame45[bay][1][2]+frame45[bay][1][3])/2.,str(Frrl), color=colorrrl,rotation=degrees(wireframe[bay][15])*2.0+90,ha='center', va='center')
            plt.text((frame45[bay][0][3]+frame45[bay][0][4])/2.+0.05*wireframe[bay][4],(frame45[bay][1][3]+frame45[bay][1][4])/2.-wireframe[bay][1]*0.2,str(Frlb), color=colorrlb,rotation=-45+wireframe[bay][2]*0.2,ha='center', va='center')
            plt.text(-1.1,(frame45[bay][1][4]+frame45[bay][1][5])/2.,str(Fmid), color=colormid,rotation=90,ha='center', va='center')
            plt.text((frame45[bay][0][6]+frame45[bay][0][7]*1.5)/2.,(frame45[bay][1][6]+frame45[bay][1][7])/2.-wireframe[bay][1]*0.1,str(Flrb), color=colorlrb,rotation=45-wireframe[bay][2]*0.075,ha='center', va='center')
            plt.text((frame45[bay][0][7]+frame45[bay][0][8])/2.-0.04*wireframe[bay][4],(frame45[bay][1][7]+frame45[bay][1][8])/2.,str(Flll), color=colorlll,rotation=-degrees(wireframe[bay][15])*2.0+90,ha='center', va='center')
            
        plt.axis([xmin45,xmax45,ymin45,ymax45])
        plt.title('Jacket - Member loads (kN) 45 degree, loadcase '+str(LC+1))
        plt.xlabel('X-location (m)')
        plt.ylabel('Y-location (m)')
        #plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        plt.savefig('Jacket - Member loads 45 deg LC '+str(LC+1)+'.png',dpi=200,bbox_inches='tight')
        plt.show()
        plt.clf()
    
def Pile_loads(loads):
    
    fxLC1A0list=[]
    fxLC1A45list=[]
    fxLC2A0list=[]
    fxLC2A45list=[]
    fxLC3A0list=[]
    fxLC3A45list=[]
    fzLC1A0list=[]
    fzLC1A45list=[]
    fzLC2A0list=[]
    fzLC2A45list=[]
    fzLC3A0list=[]
    fzLC3A45list=[]
    myLC1A0list=[]
    myLC1A45list=[]
    myLC2A0list=[]
    myLC2A45list=[]
    myLC3A0list=[]
    myLC3A45list=[]
    for pile in range(len(loads[0][0])):
        for LC in range(len(loads[0])):
            for angle in range(len(loads)):
                fx=loads[angle][LC][pile][0]/1000
                fz=loads[angle][LC][pile][2]/1000
                my=loads[angle][LC][pile][4]/1000
                if (LC==0) and (angle==0):
                    fxLC1A0list.append(fx)
                    fzLC1A0list.append(fz)
                    myLC1A0list.append(my)
                elif (LC==0) and (angle==1):
                    fxLC1A45list.append(fx)
                    fzLC1A45list.append(fz)
                    myLC1A45list.append(my)
                elif (LC==1) and (angle==0):
                    fxLC2A0list.append(fx)
                    fzLC2A0list.append(fz)
                    myLC2A0list.append(my)
                elif (LC==1) and (angle==1):
                    fxLC2A45list.append(fx)
                    fzLC2A45list.append(fz)
                    myLC2A45list.append(my)
                elif (LC==2) and (angle==0):
                    fxLC3A0list.append(fx)
                    fzLC3A0list.append(fz)
                    myLC3A0list.append(my)
                elif (LC==2) and (angle==1):
                    fxLC3A45list.append(fx)
                    fzLC3A45list.append(fz)
                    myLC3A45list.append(my)
                    
    N=4
    ind=np.arange(N)   
    margin=0.025
    width=(1-2*margin)/6.0
       
    f, (fx, fz, my,) = plt.subplots(3, 1, sharex=True, figsize=(5,10))
    fx.bar(ind        , fxLC1A0list , width, color=(1.0,0.0,0.0),hatch='\\')
    fx.bar(ind+width  , fxLC1A45list, width, color=(1.0,0.5,0.0),hatch='//')
    fx.bar(ind+2*width, fxLC2A0list , width, color=(0.0,1.0,0.0),hatch='.')
    fx.bar(ind+3*width, fxLC2A45list, width, color=(0.0,1.0,0.5),hatch='o')
    fx.bar(ind+4*width, fxLC3A0list , width, color=(0.0,0.0,1.0),hatch='+')
    fx.bar(ind+5*width, fxLC3A45list, width, color=(0.0,0.5,1.0),hatch='-')
    
    fz.bar(ind        , fzLC1A0list , width, color=(1.0,0.0,0.0), label='LC 1 A0',hatch='\\')
    fz.bar(ind+width  , fzLC1A45list, width, color=(1.0,0.5,0.0), label='LC 1 A45',hatch='//')
    fz.bar(ind+2*width, fzLC2A0list , width, color=(0.0,1.0,0.0), label='LC 2 A0',hatch='.')
    fz.bar(ind+3*width, fzLC2A45list, width, color=(0.0,1.0,0.5), label='LC 2 A45',hatch='o')
    fz.bar(ind+4*width, fzLC3A0list , width, color=(0.0,0.0,1.0), label='LC 3 A0',hatch='+')
    fz.bar(ind+5*width, fzLC3A45list, width, color=(0.0,0.5,1.0), label='LC 3 A45',hatch='-')
    
    my.bar(ind        , myLC1A0list , width, color=(1.0,0.0,0.0),hatch='\\')
    my.bar(ind+width  , myLC1A45list, width, color=(1.0,0.5,0.0),hatch='//')
    my.bar(ind+2*width, myLC2A0list , width, color=(0.0,1.0,0.0),hatch='.')
    my.bar(ind+3*width, myLC2A45list, width, color=(0.0,1.0,0.5),hatch='o')
    my.bar(ind+4*width, myLC3A0list , width, color=(0.0,0.0,1.0),hatch='+')
    my.bar(ind+5*width, myLC3A45list, width, color=(0.0,0.5,1.0),hatch='-')
    
    fx.set_ylabel('Force (kN)')
    fz.set_ylabel('Force (kN)')
    my.set_ylabel('Moment (kNn)')
    
    fx.set_title('Transversal force')
    fz.set_title('Axial force')
    my.set_title('Moment')
    f.suptitle('Pile top loads',size=12)
    
    xlist=['pile 1','pile 2','pile 3','pile 4']
    fx.set_xticks(ind+width*3)
    fx.set_xticklabels(xlist)
    
    fz.legend(loc='center left', bbox_to_anchor=(1, 0.5) )
    
    plt.savefig('Piles - Top loads.png',dpi=200,bbox_inches='tight')
    plt.show()
    plt.clf()