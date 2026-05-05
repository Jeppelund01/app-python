#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 09:47:55 2026

@author: jeppelund
"""

import pandas as pd

import spacy
nlp = spacy.load("da_core_news_sm")


tal = 4

# lister
mylist=list()
mylist.append("jeppe")
mylist.append("viggo")

# loop
for elem in mylist:
    print(elem)
    
[print(elem) for elem in mylist if elem.startswith("L")]


# funktioner
def myfun(x,y):
    retval = x+y
    return(retval)

myfun(5, 6)

