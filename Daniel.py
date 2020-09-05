# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 13:05:34 2020

@author: blake
"""

def danielsucks(daniel):
    if daniel == "sucks":
        print("Daniel", daniel)
        
daniel = "cool"
question = input("Does daniel suck? ")
question = question.lower()
if question == "yes" or question == "y":
    daniel = "sucks"
else:
    print("He definitely sucks idk what you mean.")
danielsucks(daniel)
        