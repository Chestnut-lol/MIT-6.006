# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 19:10:30 2020

@author: LH
"""

import algorithms
import peak

array = []
with open("array.txt","r") as f:
    for line in f:
        line = line.strip().split(" ")
        row = list(map(int,line))
        array.append(row)

print(array)
    

problem = peak.createProblem(array)

print(algorithms.algorithm3(problem))