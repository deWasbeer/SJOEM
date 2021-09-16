# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:22:03 2015

@author: Johan Antonissen (windhoos@gmail.com)
"""
from math import radians

class stored_data:
    def __init__(self):
        self.Drotor = 0.0
        self.Mrna = 0.0
        self.Cdrotoridling = 0.0
        self.Vrated = 0.0
        self.Wscale = 0.0
        self.Wshape = 0.0
        self.Href = 0.0
        self.ShearExp = 0.0
        self.Hdepth = 0.0
        self.HAT = 0.0
        self.Surge = 0.0
        self.H1 = 0.0
        self.H50 = 0.0
        self.RHOwater = 0.0
        self.PHIsoil = 0.0
        self.RHOsoil = 0.0
        self.sigmY = 0.0
        self.Ed = 0.0

def Ask_data():
    #Ask general inout data
    print("Welcome to SJOEM, Simple Jacket Optimization Engineering Model")
    print('   _______   ________     _______     _________  ____    ____')
    print('  /                  |   /       \   |           |   \  /    |')
    print(' /                   |  /         \  |           |    \/     |')
    print(' |                   |  |         |  |           |           |')
    print(' \                   |  |         |  |           |           |')
    print('  \______            |  |         |  |——————     |           |')
    print('         \           |  |         |  |           |           |')
    print('          \          |  |         |  |           |           |')
    print('          |          |  |         |  |           |           |')
    print('          /  \       /  \         /  |           |           |')
    print(' ________/    \_____/    \_______/   |_________  |           |')
    print()
    print("Would you like to input your own information?")
    print()
    print("If no data is entered please choose one of the following farms:")
    print('1) Alpha Ventus:     Farm just outside the Dutch-German border, north of Groningen')
    print('                     Turbine: REpower (5MW), Depth: 30m, H50max: 16 m')
    print('2) Princes Amalia:   Farm just off the coast of Amsterdam')
    print('                     Turbine: Vestas (2MW), Depth: 22m, H50max: 12 m')
    print('3) SJOEM:            Imaginary farm located at the outermost north-west patch of Dutch territory')
    print('                     Turbine: Siemens (6MW), Depth: 50m, H50max: 20 m')
    execute = input('Yes (Y) / Alpha Ventus (AV) / Princes Amalia (PA) / SJOEM (SJ)? ')
    while (execute != 'Y') and (execute != 'AV') and (execute != 'PA') and (execute != 'SJ'):
        execute = input(' Please enter: Yes (Y) / Alpha Ventus (AV) / Princes Amalia (PA) / SJOEM (SJ)? ')
    #execute = 'n'
    print()
    if execute == 'Y':
        print("Please give in the following data:")
        print()
        #Turbine data
        Turbine = 'Costum'
        Drotor= eval(input('Diameter rotor (m) '))
        Mrna= eval(input('Mass RNA assembly (kg) '))
        Cdrotoridling= eval(input('Drag coefficient blades (-) '))
        Vrated= eval(input('Rated wind speed to calculate maximum thrust (m/s) '))
        #Site data
            #Aerodynamic
        Wscale= eval(input('Weibull scale factor (m/s) '))
        Wshape= eval(input('Weibull shape factor (-) '))
        Href= eval(input('Reference wind speed height from SWL (m) '))
        ShearExp= eval(input('Wind sear exponent (-) '))
            #Hydrodynamic
        Hdepth= eval(input('Depth at deepest point (m) '))
        HAT= eval(input('Hightest astronomical tide (m) '))
        Surge= eval(input('Surge level (m) '))
        H1= eval(input('1 year significant wave height (m) '))
        H50= eval(input('50 year significant wave height (m) '))
        RHOwater= eval(input('Density of water (kg/m3) '))
            #Geodynamic
        PHIsoil = eval(input('Soil friction angle (deg) '))
        RHOsoil = eval(input('Sebmerged soil unit weight (N/m3) '))
            #Material propperties
        sigmY=eval(input('Yield strength steel (Mpa) '))
        sigmY=sigmY*10**6
        Ed=eval(input('Elasticity steel (Gpa) '))
        Ed=Ed*10**9
    elif execute == 'AV':
        print("Calculations made for Alpha Ventus farm")
        print()
        #Turbine data
        Turbine= 'REpower 5M'
        Drotor= 126 #m Diameter rotor
        Mrna= 440000 #kg Mass RNA assembly
        Cdrotoridling= 0.4 #- Drag coefficient blades
        Vrated= 13 #m/s Rated wind speed to calculate maximum thrust
        #Site data
            #Aerodynamic
        Wscale= 10.5 #m/s Weibull scale factor
        Wshape= 2.4 #- Weibull shape factor
        Href= 90.0 #m Reference wind speed height from SWL
        ShearExp= 0.07 #- Wind sear exponent
            #Hydrodynamic
        Hdepth= 30. #m #Depth at deepest point
        HAT= 2. #m Hightest astronomical tide
        Surge= 2.25 #m Surge level
        H50max = 16.
        H50= H50max /2.5 #m 50 year significant wave height
        H1=  H50/1.86 #m 1y significant wave height
        RHOwater= 1025 #kg/m3 density of water
            #Geodynamic (Gravel + sand)
        PHIsoil = 40. #deg Soil friction angle (gravel)
        RHOsoil = 21000. #N/m3 sebmerged soil unit weight (gravel)
            #Material propperties
        sigmY = 250*10**6 #N/m2 Yield strength steel
        Ed = 210*10**9 #N/m2 Elasticity steel
    elif execute == 'PA':
        print("Calculations made for Princes Amalia farm")
        print()
        #Turbine data
        Turbine= 'Vestas V90'
        Drotor= 80. #m Diameter rotor
        Mrna= 129000. #kg Mass RNA assembly
        Cdrotoridling= 0.4 #- Drag coefficient blades
        Vrated= 14 #m/s Rated wind speed to calculate maximum thrust
        #Site data
            #Aerodynamic
        Wscale= 10. #m/s Weibull scale factor
        Wshape= 2.1 #- Weibull shape factor
        Href= 90.0 #m Reference wind speed height from SWL
        ShearExp= 0.1 #- Wind sear exponent
            #Hydrodynamic
        Hdepth= 22. #m #Depth at deepest point
        HAT= 1.5 #m Hightest astronomical tide
        Surge= 3. #m Surge level
        H50max = 12.
        H50= H50max /2.5 #m 50 year significant wave height
        H1=  H50/1.86 #m 1y significant wave height
        RHOwater= 1025 #kg/m3 density of water
            #Geodynamic
        PHIsoil = 35. #deg Soil friction angle (sand)
        RHOsoil = 19000 #N/m3 sebmerged soil unit weight (sand)
            #Material propperties
        sigmY = 250*10**6 #N/m2 Yield strength steel
        Ed = 210*10**9 #N/m2 Elasticity steel
    elif execute == 'SJ':
        print("Calculations made for SJOEM far-shore farm")
        print()
        #Turbine data
        Turbine= 'Siemens SWT6'
        Drotor= 154. #m Diameter rotor
        Mrna= 360000. #kg Mass RNA assembly
        Cdrotoridling= 0.4 #- Drag coefficient blades
        Vrated= 12. #m/s Rated wind speed to calculate maximum thrust
        #Site data
            #Aerodynamic
        Wscale= 11. #m/s Weibull scale factor
        Wshape= 2.3 #- Weibull shape factor
        Href= 90.0 #m Reference wind speed height from SWL
        ShearExp= 0.05 #- Wind sear exponent
            #Hydrodynamic
        Hdepth= 50. #m #Depth at deepest point
        HAT= 1. #m Hightest astronomical tide
        Surge= 2. #m Surge level
        H50max = 20.
        H50= H50max /2.5 #m 50 year significant wave height
        H1=  H50/1.86 #m 1y significant wave height
        RHOwater= 1025 #kg/m3 density of water
            #Geodynamic
        PHIsoil = 25. #deg Soil friction angle (mud)
        RHOsoil = 18000 #N/m3 sebmerged soil unit weight (mud)
            #Material propperties
        sigmY = 250*10**6 #N/m2 Yield strength steel
        Ed = 210*10**9 #N/m2 Elasticity steel
    else:
        print("Calculations made with example input")
        print()
        #Turbine data
        Turbine='Vestas V90'
        Drotor= 90 #m Diameter rotor
        Mrna= 111000 #kg Mass RNA assembly
        Cdrotoridling= 0.4 #- Drag coefficient blades
        Vrated= 15 #m/s Rated wind speed to calculate maximum thrust
        #Site data
            #Aerodynamic
        Wscale= 10.83 #m/s Weibull scale factor
        Wshape= 2.35 #- Weibull shape factor
        Href= 60.0 #m Reference wind speed height from SWL
        ShearExp= 0.7 #- Wind sear exponent
            #Hydrodynamic
        Hdepth= 20 #m #Depth at deepest point
        HAT= 0.8 #m Hightest astronomical tide
        Surge= 2.5 #m Surge level
        H1= 3.3 #m 1y significant wave height
        H50= 9.5 #m 50 year significant wave height
        RHOwater= 1025 #kg/m3 density of water
            #Geodynamic
        PHIsoil = 35.0 #deg Soil friction angle
        RHOsoil = 10000 #N/m3 sebmerged soil unit weight
            #Material propperties
        sigmY = 250*10**6 #N/m2 Yield strength steel
        Ed = 210*10**9 #N/m2 Elasticity steel
        
    print('#Turbine data')
    print('     Turbine=       %s' %(Turbine))
    print('     Drotor=        %f #m Diameter rotor' %(Drotor))
    print('     Mrna=          %f #kg Mass RNA assembly' %(Mrna))
    print('     Cdrotoridling= %f #- Drag coefficient blades' %(Cdrotoridling))
    print('     Vrated=        %f #m/s Rated wind speed to calculate maximum thrust' %(Vrated))
    print()
    print('#Site data')
    print('    #Aerodynamic')
    print('     Wscale=        %f #m/s Weibull scale factor' %(Wscale))
    print('     Wshape=        %f #- Weibull shape factor' %(Wshape))
    print('     Href=          %f #m Reference wind speed height from SWL' %(Href))
    print('     ShearExp=      %f #- Wind sear exponent' %(ShearExp))
    print('    #Hydrodynamic')
    print('     Hdepth=        %f #m #Depth at deepest point' %(Hdepth))
    print('     HAT=           %f #m Hightest astronomical tide' %(HAT))
    print('     Surge=         %f #m Surge level' %(Surge))
    print('     H1=            %f #m 1y significant wave height' %(H1))
    print('     H50=           %f #m 50 year significant wave height' %(H50))
    print('     RHOwater=      %f #kg/m3 density of water' %(RHOwater))
    print('    #Geodynamic')
    print('     PHIsoil=       %f #deg Soil friction angle' %(PHIsoil))
    print('     RHOsoil=       %f #N/m3 sebmerged soil unit weight' %(RHOsoil))
    print('    #Material propperties')
    print('     sigmY =        %f #N/m2 Yield strength steel' %(sigmY))
    print('     Ed =           %f #N/m2 Elasticity steel' %(Ed))
    print()
    
    text=open('Data-Input_data.txt','w')
    text.truncate()
    
    text.write('#Turbine data'+'\n')
    text.write('     Turbine =      %s '%(Turbine)+'\n')
    text.write('     Drotor=        %f #m Diameter rotor'%(Drotor)+'\n')
    text.write('     Mrna=          %f #kg Mass RNA assembly'%(Mrna)+'\n') 
    text.write('     Cdrotoridling= %f #- Drag coefficient blades'%(Cdrotoridling)+'\n') 
    text.write('     Vrated=        %f #m/s Rated wind speed to calculate maximum thrust'%(Vrated)+'\n') 
    text.write('\n')
    text.write('#Site data'+'\n')
    text.write('    #Aerodynamic'+'\n')
    text.write('     Wscale=        %f #m/s Weibull scale factor'%(Wscale)+'\n') 
    text.write('     Wshape=        %f #- Weibull shape factor'%(Wshape)+'\n') 
    text.write('     Href=          %f #m Reference wind speed height from SWL'%(Href)+'\n') 
    text.write('     ShearExp=      %f #- Wind sear exponent'%(ShearExp)+'\n') 
    text.write('    #Hydrodynamic'+'\n')
    text.write('     Hdepth=        %f #m #Depth at deepest point'%(Hdepth)+'\n') 
    text.write('     HAT=           %f #m Hightest astronomical tide'%(HAT)+'\n') 
    text.write('     Surge=         %f #m Surge level'%(Surge)+'\n') 
    text.write('     H1=            %f #m 1y significant wave height' %(H1)+'\n')
    text.write('     H50=           %f #m 50 year significant wave height'%(H50)+'\n') 
    text.write('     RHOwater=      %f #kg/m3 density of water'%(RHOwater)+'\n') 
    text.write('    #Geodynamic'+'\n') 
    text.write('     PHIsoil=       %f #deg Soil friction angle'%(PHIsoil)+'\n') 
    text.write('     RHOsoil=       %f #N/m3 sebmerged soil unit weight' %(RHOsoil)+'\n')
    text.write('    #Material propperties'+'\n')
    text.write('     sigmY =        %f #N/m2 Yield strength steel'%(sigmY)+'\n') 
    text.write('     Ed =           %f #N/m2 Elasticity steel'%(Ed)+'\n') 
    text.close()
    
    stored_data.Drotor=Drotor
    stored_data.Mrna=Mrna
    stored_data.Cdrotoridling=Cdrotoridling
    stored_data.Vrated=Vrated
    stored_data.Wscale=Wscale
    stored_data.Wshape=Wshape
    stored_data.Href=Href
    stored_data.ShearExp=ShearExp
    stored_data.Hdepth=Hdepth
    stored_data.HAT=HAT
    stored_data.Surge=Surge
    stored_data.H1=H1
    stored_data.H50=H50
    stored_data.RHOwater=RHOwater
    stored_data.PHIsoil=radians(PHIsoil)
    stored_data.RHOsoil=RHOsoil
    stored_data.sigmY=sigmY
    stored_data.Ed=Ed