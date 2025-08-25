"""
This is the place to put the modules for each UI in the system.  One module for each unique ui --
mirrored panels should be in the same file.
* UI object definition
* UI navigation
"""

# Python imports

# Extron Library imports
from extronlib.ui import Button, Knob, Level
from extronlib.system import MESet

# Project imports
from modules.helper.ModuleSupport import eventEx
from devices import dvNBPA, dvNBPB

# Define UI Objects
btn_prjAOn  = Button(dvNBPA, 60021)
btn_prjAOff = Button(dvNBPA, 60022)

prjA_set = MESet([btn_prjAOff, btn_prjAOn])

for btn in prjA_set.Objects:
    prjA_set.SetStates(btn, 0, 2)

btn_prjBOn  = Button(dvNBPB, 60021)
btn_prjBOff = Button(dvNBPB, 60022)

prjB_set = MESet([btn_prjBOff, btn_prjBOn])

for btn in prjB_set.Objects:
    prjB_set.SetStates(btn, 0, 2)
    
btn_srcA1   = Button(dvNBPA, 60061)     #Laptop 
btn_srcA2   = Button(dvNBPA, 60062)     #Wireless   
btn_srcA3   = Button(dvNBPA, 60063)     #Bluray
btn_srcA4   = Button(dvNBPA, 60064)     #Posible DTP Wallplate

srcA_set = MESet([btn_srcA1, btn_srcA2, btn_srcA3, btn_srcA4])

for btn in srcA_set.Objects:
    srcA_set.SetStates(btn, 0, 2)

btn_srcB1   = Button(dvNBPB, 60061)     #Laptop
btn_srcB2   = Button(dvNBPB, 60062)     #Wirless
btn_srcB3   = Button(dvNBPB, 60063)     #Bluray
btn_srcB4   = Button(dvNBPB, 60064)     #Possible DTP Wallplate

srcB_set = MESet([btn_srcB1, btn_srcB2, btn_srcB3, btn_srcB4])

for btn in srcB_set.Objects:
    srcB_set.SetStates(btn, 0, 2)
    
prjA_set.SetCurrent(btn_prjAOff)
prjB_set.SetCurrent(btn_prjBOff)
srcA_set.SetCurrent(btn_srcA2)
srcB_set.SetCurrent(btn_srcB2)

lvl_A = Level(dvNBPA, 61011)
lvl_B = Level(dvNBPB, 61011)

lvl_A.SetRange(-40, 6)
lvl_B.SetRange(-40, 6)
lvl_A.SetLevel(-24)
lvl_B.SetLevel(-24)

kb_A = Knob(dvNBPA, 61001)
kb_B = Knob(dvNBPB, 61001)

# Define UI Object Events

#TODO define visual events for source buttons
