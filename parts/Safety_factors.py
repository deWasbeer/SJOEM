# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 12:31:26 2015

@author: Johan Antonissen (windhoos@gmail.com)
"""

class stored_data:
    def __init__(self):
        self.DAF = 0.0
        self.fatigue_safety_factor = 0.0
        self.partial_safety_env_loads = 0.0
        self.partial_safety_gravity = 0.0
        self.partial_safety_material_uls = 0.0
        self.ScombENV = 0.0
        self.ScombGRAV = 0.0
        
def Calculate_safety():
    DAF = 1.0
    fatigue_safety_factor = 1.5
    partial_safety_env_loads = 1.35
    partial_safety_gravity = 1.1
    partial_safety_material_uls = 1.1
    
    stored_data.DAF = DAF*1.0
    stored_data.fatigue_safety_factor = fatigue_safety_factor*1.0
    stored_data.partial_safety_env_loads = partial_safety_env_loads*1.0
    stored_data.partial_safety_gravity = partial_safety_gravity*1.0
    stored_data.partial_safety_material_uls = partial_safety_material_uls*1.0
    
    stored_data.ScombENV = DAF*fatigue_safety_factor*partial_safety_env_loads*partial_safety_material_uls
    stored_data.ScombGRAV = DAF*fatigue_safety_factor*partial_safety_gravity*partial_safety_material_uls
    
    text=open('Data-Safety_factors.txt','w')
    text.truncate()
    text.write('Stored data'+'\n')
    text.write('DAF '+str(stored_data.DAF)+'\n')
    text.write('fatigue safety factor '+str(stored_data.fatigue_safety_factor)+'\n')
    text.write('partial safety factor env loads '+str(stored_data.partial_safety_env_loads)+'\n')
    text.write('partial safety factor gravity '+str(stored_data.partial_safety_gravity)+'\n')
    text.write('partial safety material ULS '+str(stored_data.partial_safety_material_uls)+'\n')
    text.write('ScombENV '+str(stored_data.ScombENV)+'\n')
    text.write('ScombGRAV '+str(stored_data.ScombGRAV)+'\n')
    text.close()
      
    