# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 15:14:59 2015

@author: Johan Antonissen (windhoos@gmail.com)
"""
from parts import Tower,Jacket,Piles


def dimension_collector():
    Tower_dimensions=Tower.stored_data.Tower_dimensions
    Jacket_dimensions=Jacket.stored_data.Jacket_dimensions
    Wireframe=Jacket.stored_data.wireframe
    Sleeve_dimensions=Jacket.stored_data.Sleeve_dimensions
    Pile_dimensions=Piles.stored_data.pile_dimensions
    
    print()
    print('*** TOWER DIMENSIONS ***')
    for segment in range(len(Tower_dimensions)):
        print('H=',int(Tower_dimensions[segment][0]*1000.0)/1000.0,' , ',int(Tower_dimensions[segment][1]*1000.0)/1000.0,' , ',int(Tower_dimensions[segment][2]*1000.0)/1000.0)
    print('[Height,Diameter, Wall Thickness]')
    print('Total tower weight:',int(Tower.stored_data.weight),'Newton')
    print()
    print('*** JACKET DIMENSIONS ***')
    for bay in range(len(Jacket_dimensions)):
        print('Bay=',bay+1,'Leg:  ',int(Jacket_dimensions[bay][0]*1000.0)/1000.0,' , ',int(Jacket_dimensions[bay][2]*100000.0)/100000.0,' , ',int(Wireframe[bay][1]*(1.0+Wireframe[bay][15])*1000.0)/1000.0,' , ',int(Sleeve_dimensions[bay][0]*100000.0)/100000.0,' , ',int(Sleeve_dimensions[bay][2]*1000.0)/1000.0)
        print('       Brace:',int(Jacket_dimensions[bay][1]*1000.0)/1000.0,' , ',int(Jacket_dimensions[bay][3]*100000.0)/100000.0,' , ',int(Wireframe[bay][5]*1000.0)/1000.0,' , ',int(Sleeve_dimensions[bay][1]*100000.0)/100000.0,' , ',int(Sleeve_dimensions[bay][3]*1000.0)/1000.0)
    print('[Diameter, Wall thickness, Length, Additonal sleeve thickness, Sleeve length]')
    print('Total jacket weight:',int(Jacket.stored_data.weight),'Newton')
    print()
    print('*** PILE DIMENSIONS ***')
    print(int(Pile_dimensions[0]*1000.0)/1000.0,' , ',int(Pile_dimensions[1]*100000.0)/100000.0,' , ',int(Pile_dimensions[2]*1000.0)/1000.0)
    print('[Diameter, Wall thickness, Length]')
    print('Total piles weight:',int(Piles.stored_data.weight),' Newton')
    print()
    print('Total strudture weight is estimated at:', int(Tower.stored_data.weight+Jacket.stored_data.weight+Piles.stored_data.weight),'Newton')
    print()
    print('Thank you for using this program')
    
    text=open('Data-Final_dimensions.txt' , 'w')
    text.truncate()
    text.write('*** TOWER DIMENSIONS ***'+'\n')
    for segment in range(len(Tower_dimensions)):
        text.write('H='+str(int(Tower_dimensions[segment][0]*1000.0)/1000.0)+' , '+str(int(Tower_dimensions[segment][1]*1000.0)/1000.0)+' , '+str(int(Tower_dimensions[segment][2]*1000.0)/1000.0)+'\n')
    text.write('[Diameter, Wall Thickness]'+'\n')
    text.write('Total tower weight: '+str(int(Tower.stored_data.weight))+' Newton'+'\n'+'\n')
    
    text.write('*** JACKET DIMENSIONS ***'+'\n')
    for bay in range(len(Jacket_dimensions)):
        text.write('Bay='+str(bay+1)+' Leg:  '+str(int(Jacket_dimensions[bay][0]*1000.0)/1000.0)+' , '+str(int(Jacket_dimensions[bay][2]*100000.0)/100000.0)+' , '+str(int(Wireframe[bay][1]*(1.0+Wireframe[bay][15])*1000.0)/1000.0)+' , '+str(int(Sleeve_dimensions[bay][0]*100000.0)/100000.0)+' , '+str(int(Sleeve_dimensions[bay][2]*1000.0)/1000.0)+'\n')
        text.write('       Brace:'+str(int(Jacket_dimensions[bay][1]*1000.0)/1000.0)+' , '+str(int(Jacket_dimensions[bay][3]*100000.0)/100000.0)+' , '+str(int(Wireframe[bay][5]*1000.0)/1000.0)+' , '+str(int(Sleeve_dimensions[bay][1]*100000.0)/100000.0)+' , '+str(int(Sleeve_dimensions[bay][3]*1000.0)/1000.0)+'\n')
    text.write('[Diameter, Wall thickness, Length, Additonal sleeve thickness, Sleeve length]'+'\n')
    text.write('Total jacket weight: '+str(int(Jacket.stored_data.weight))+' Newton'+'\n'+'\n')
    
    text.write('*** PILE DIMENSIONS ***'+'\n')
    text.write(str(int(Pile_dimensions[0]*1000.0)/1000.0)+' , '+str(int(Pile_dimensions[1]*100000.0)/100000.0)+' , '+str(int(Pile_dimensions[2]*1000.0)/1000.0)+'\n')
    text.write('[Diameter, Wall thickness, Length]'+'\n')
    text.write('Total piles weight: '+str(int(Piles.stored_data.weight))+' Newton'+'\n'+'\n')
    
    text.write('Total strudture weight is estimated at: '+str(int(Tower.stored_data.weight+Jacket.stored_data.weight+Piles.stored_data.weight))+' Newton'+'\n'+'\n')
    
    text.write('Thank you for using this program'+'\n')
    text.close()