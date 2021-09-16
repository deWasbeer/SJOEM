# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 10:06:56 2015

@author: Johan Antonissen (windhoos@gmail.com)
"""
from parts import Input_data, Site_conditions,Elevations,Safety_factors,RNA,Tower,Jacket,Piles,Final_dimensions
import Grapher, Ansys_link, Ansys_beam

def main():
    Input_data.Ask_data()
    Site_conditions.Create_Loadcases()
    Elevations.Determine_elevations()
    Safety_factors.Calculate_safety()
    RNA.Calculate_RNA()
    Tower.Calculate_tower()
    Jacket.Calculate_jacket()
    Piles.Calculate_piles()
    Final_dimensions.dimension_collector()
    Ansys_link.ansys()
    Ansys_beam.ansys()
    Grapher.grapher()
main()