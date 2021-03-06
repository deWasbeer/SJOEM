# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 12:00:13 2015

@author: Johan Antonissen (windhoos@gmail.com)
"""

from math import gamma,sqrt,pi,sinh,tanh
from scipy.optimize import newton
from . import Input_data

class stored_data:
    def __init_(self):
        self.Vaverage = 0.0
        self.Vreference = 0.0
        self.Vmax_50_year = 0.0
        self.Vred_50_year = 0.0
        
        self.Hmax_50_year = 0.0
        self.Tmax_50_year = 0.0
        self.kmax_50_year = 0.0
        self.Tpeak_50_year = 0.0
        self.Uw_50_year = 0.0
        
        self.Hred_50_year = 0.0
        self.Tred_50_year = 0.0
        self.kred_50_year = 0.0
        
        self.Hmax_1_year = 0.0
        self.Tmax_1_year = 0.0
        self.kmax_1_year = 0.0
        self.max_crest = 0.0
        
        self.LCcompilation=[]

class aerodynamic:
    def __init__(self,Vrated,Wscale,Wshape,Href,ShearExp):
        self.Vrated=Vrated
        self.scale=Wscale
        self.shape=Wshape
        self.Href=Href
        self.alpha=ShearExp
        self.g=9.81
        self.rho=1.225
        
        self.Vaverage = 0.0
        self.Vreference = 0.0
        self.Vmax_50_year = 0.0
        self.Vred_50_year = 0.0
        
    def aerodynamic_conditions(self):
        #All winds calculated at reference height for length and scale factor
        self.Vaverage = self.scale*gamma(1.0 + 1.0/self.shape)
        self.Vreference = self.Vaverage * 5.0
        self.Vmax_50_year = 1.2 * self.Vreference  
        self.Vred_50_year = (1.2 / 1.1) * self.Vreference
        
        stored_data.Vaverage=self.Vaverage
        stored_data.Vreference=self.Vreference
        stored_data.Vmax_50_year=self.Vmax_50_year
        stored_data.Vred_50_year=self.Vred_50_year
        
        return [self.Vrated,self.Vred_50_year,self.Vmax_50_year]
        
def get_wind_speed_at_height(wind_speed_ref, height):
    return wind_speed_ref * (height / Input_data.stored_data.Href)**Input_data.stored_data.ShearExp
        
class hydrodynamic:
    def __init__(self,Hdepth,HAT,Surge,H1,H50,RHOwater):
        self.Hdepth=Hdepth
        self.HAT=HAT
        self.Surge=Surge
        self.H1=H1
        self.H50=H50
        self.rho=RHOwater
        self.g=9.81
        
        self.Hmax_50_year = 0.0
        self.Tmax_50_year = 0.0
        self.kmax_50_year = 0.0
        self.Tpeak_50_year = 0.0
        self.Uw_50_year = 0.0
        
        self.Hred_50_year = 0.0
        self.Tred_50_year = 0.0
        self.kred_50_year = 0.0
        
        self.Hmax_1_year = 0.0
        self.Tmax_1_year = 0.0
        self.kmax_1_year = 0.0
        self.max_crest = 0.0
        #self.min_crest = 0.0
        
    def hydrodynamic_conditions(self):
        self.Hmax_50_year = 1.86 * self.H50
        self.Tmax_50_year = 11.1 * sqrt(self.Hmax_50_year / self.g)
        self.kmax_50_year = self.get_wave_number(self.Tmax_50_year)
        self.Hmax_50_year = min(self.Hmax_50_year, self.wave_limit(self.kmax_50_year))
        self.Tpeak_50_year = 1.4 * 11.1 * sqrt(self.H50 / self.g)
        self.Uw_50_year = (pi * self.H50 / (self.Tpeak_50_year * sinh(self.get_wave_number(self.Tpeak_50_year) * self.Hdepth)))
                                              
        self.Hred_50_year = 1.32 * self.H50
        self.Tred_50_year = 11.1 * sqrt(self.Hred_50_year / self.g)
        self.kred_50_year = self.get_wave_number(self.Tred_50_year)
        self.Hred_50_year = min(self.Hred_50_year, self.wave_limit(self.kred_50_year))
        
        self.Hmax_1_year = 1.86 * self.H1
        self.Tmax_1_year = 11.1 * sqrt(self.Hmax_1_year / self.g)
        self.kmax_1_year = self.get_wave_number(self.Tmax_1_year)
        self.Hmax_1_year = min(self.Hmax_1_year, self.wave_limit(self.kmax_1_year))
        self.max_crest = self.HAT + self.Surge + 0.55 * self.Hmax_50_year 
        #self.min_crest = self.LAT + self.Surge - 0.45 * self.Hmax_50_year
        
        stored_data.Hmax_50_year=self.Hmax_50_year
        stored_data.Tmax_50_year=self.Tmax_50_year
        stored_data.kmax_50_year=self.kmax_50_year
        stored_data.Tpeak_50_year=self.Tpeak_50_year
        stored_data.Uw_50_year=self.Uw_50_year
        
        stored_data.Hred_50_year=self.Hred_50_year
        stored_data.Tred_50_year=self.Tred_50_year
        stored_data.kred_50_year=self.kred_50_year
        
        stored_data.Hmax_1_year=self.Hmax_1_year
        stored_data.Tmax_1_year=self.Tmax_1_year
        stored_data.kmax_1_year=self.kmax_1_year
        stored_data.max_crest=self.max_crest
        
        return [self.Hmax_1_year,self.kmax_1_year,self.Hmax_50_year,self.kmax_50_year,self.Hred_50_year,self.kred_50_year]
    
    def get_wave_number(self, period):
        omega = 2 * pi / period
        
        start_k = omega**2 / self.g
        return newton(self.dispersion, start_k, args = (omega, ), tol = 0.001)
    
    def dispersion(self, d, *args):
        k = d
        omega = args[0]
        
        return omega**2 - self.g * k * tanh(k * self.Hdepth)
    
    def wave_limit(self, k):
        shallow_water_limit = 0.78 * self.Hdepth
        deep_water_limit = 0.142 * 2.0 * pi /k
        return min(shallow_water_limit, deep_water_limit)
        
class create_LC:
    def __init__(self,LCwind,LCwater):
        self.LCwind=LCwind
        self.LCwater=LCwater
        self.LCcompilation=[]
    
    def conductor(self):
        for i in range(3):
            self.LCcompilation.append([0.0,0.0,0.0])
            self.LCcompilation[i][0]=self.LCwind[i]
            self.LCcompilation[i][1]=self.LCwater[2*i]
            self.LCcompilation[i][2]=self.LCwater[2*i+1]
            
        stored_data.LCcompilation=self.LCcompilation
        
def Create_Loadcases():
    print('The following loadcases are created')
    print('LC 1: operation, rated wind speed, maximum wave in one-year extreme sea state')
    print('LC 2: parked, reduced gust in 50-year average wind speed, maximum wave in 50-year extreme sea state')
    print('LC 3: parked, maximum gust in 50-year average wind speed, reduced wave in 50-year extreme sea state')
    print()
    
    text=open('Data-Site_conditions.txt','w')
    text.truncate()
    text.write('The following loadcases are created'+'\n')
    text.write('LC 1: operation, rated wind speed, maximum wave in one-year extreme sea state'+'\n')
    text.write('LC 2: parked, reduced gust in 50-year average wind speed, maximum wave in 50-year extreme sea state'+'\n')
    text.write('LC 3: parked, maximum gust in 50-year average wind speed, reduced wave in 50-year extreme sea state'+'\n')
    text.write('\n')
    
    wind=aerodynamic(Input_data.stored_data.Vrated,Input_data.stored_data.Wscale,Input_data.stored_data.Wshape,Input_data.stored_data.Href,Input_data.stored_data.ShearExp)    
    LCwind=wind.aerodynamic_conditions()
    
    water=hydrodynamic(Input_data.stored_data.Hdepth,Input_data.stored_data.HAT,Input_data.stored_data.Surge,Input_data.stored_data.H1,Input_data.stored_data.H50,Input_data.stored_data.RHOwater)
    LCwater=water.hydrodynamic_conditions()
    
    Loadcase=create_LC(LCwind,LCwater)
    Loadcase.conductor()

    print('List of loadcase information containing per loadcase: ')
    print('[Vhub (m/s), Wave height (m), Wave number (-)]')
    for i in range(len(stored_data.LCcompilation)):
        print('LC',i+1,stored_data.LCcompilation[i])
    print()
    
    text.write('List of loadcase information containing per loadcase: '+'\n')
    text.write('[Vhub (m/s), Wave height (m), Wave number (-)]'+'\n')
    for i in range(len(stored_data.LCcompilation)):
        text.write('LC '+str(i+1)+' '+str(stored_data.LCcompilation[i])+'\n')
        
    text.write('\n'+'stored data'+'\n')
    text.write('Vaverage '+str(stored_data.Vaverage)+'\n')
    text.write('Vreference '+str(stored_data.Vreference)+'\n')
    text.write('Vmax_50_year '+str(stored_data.Vmax_50_year)+'\n')
    text.write('Vred_50_year '+str(stored_data.Vred_50_year)+'\n')
    
    text.write('Hmax_50_year '+str(stored_data.Hmax_50_year)+'\n')
    text.write('Tmax_50_year '+str(stored_data.Tmax_50_year)+'\n')
    text.write('kmax_50_year '+str(stored_data.kmax_50_year)+'\n')
    text.write('Tpeak_50_year '+str(stored_data.Tpeak_50_year)+'\n')
    text.write('Uw_50_year '+str(stored_data.Uw_50_year)+'\n')
    
    text.write('Hred_50_year '+str(stored_data.Hred_50_year)+'\n')
    text.write('Tred_50_year '+str(stored_data.Tred_50_year)+'\n')
    text.write('kred_50_year '+str(stored_data.kred_50_year)+'\n')
    
    text.write('Hmax_1_year '+str(stored_data.Hmax_1_year)+'\n')
    text.write('Tmax_1_year '+str(stored_data.Tmax_1_year)+'\n')
    text.write('kmax_1_year '+str(stored_data.kmax_1_year)+'\n')
    text.write('max_crest '+str(stored_data.max_crest)+'\n')
    
    text.write('LCcompilation '+'\n'+str(stored_data.LCcompilation)+'\n')    
    text.close()