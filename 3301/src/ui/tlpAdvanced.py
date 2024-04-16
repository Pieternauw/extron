#Extron Imports 
from modules.helper.ModuleSupport import eventEx
from extronlib.system import MESet
from extronlib.ui import Button, Label

from devices import dvTLP, dvPRJ
from variables import ButtonEventList

#advanced settings
btn_advSettings = Button(dvTLP, 47)
@eventEx(btn_advSettings, ButtonEventList)
def ShowAdvancedSettingsPopup(button:Button, state):
    print(button.Name, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLP.ShowPopup("Advanced Settings")
    elif state == 'Released':
        button.SetState(0)

#Activity Timeout
btn_actTimeout = Button(dvTLP, 155)
@eventEx(btn_actTimeout, ButtonEventList)
def DisableActivityTimeout(button:Button, state):
    print(button.Name, state)
    if state == 'Pressed':
        button.SetState(1)
        #TODO - get timeout setup - do something with the system to disable said act timeout.
        print("something to disable errors\n") 
    elif state == 'Released':
        button.SetState(0)

#Projector
"""TODO might want to do a subscribe status to keep visual feedback consistent"""
btn_projOn = Button(dvTLP, 24)
btn_projOff = Button(dvTLP, 25)

prj_set = MESet([btn_projOn, btn_projOff])

@eventEx(prj_set.Objects, 'Pressed')
def ProjectorOnOff(button:Button, state):
    print(button, state)
    prj_set.SetCurrent(button)
    if button is btn_projOn:
        dvPRJ.Set('Power', 'On')
    else:
        dvPRJ.Set('Power', 'Off')

btn_blankImg = Button(dvTLP, 21)
@eventEx(btn_blankImg, 'Pressed')
def BlankImage(button:Button, state):
    print(button.Name, state)    
    if button.State == 1:
        button.SetState(0)
        dvPRJ.Set('AVMute', 'Off')
    else:
        button.SetState(1)
        dvPRJ.Set('AVMute', 'On')

#Technician Access Code
TechButtons = []
for Button_IDs in range(107, 117):
    TechButtons.append(Button(dvTLP, Button_IDs))
    
LblTechString = Label(dvTLP, 20)
techstr = ''
techlblstr = ''

@eventEx(TechButtons, ButtonEventList)
def TechButtonPressed(button:Button, state):
    print(button.Name, state)
    global techstr 
    global techlblstr
    if state == 'Pressed':
        button.SetState(1)
        techstr += button.Name
        techlblstr += '*'
        LblTechString.SetText(techlblstr)
    elif state == 'Released':
        button.SetState(0)

btn_techClear = Button(dvTLP, 117)
@eventEx(btn_techClear, ButtonEventList)
def BtnClearTech(button:Button, state):
    print(button.Name, state)
    global techstr 
    global techlblstr
    if state == 'Pressed':
        button.SetState(1)
        techstr = ''
        techlblstr = ''
        LblTechString.SetText(techlblstr)
    elif state == 'Released':
        button.SetState(0)
        
btn_techEnter = Button(dvTLP, 118)
@eventEx(btn_techEnter, ButtonEventList)
def BtnEnterTech(button:Button, state):
    print(button.Name, state)
    global techstr 
    global techlblstr
    if state == 'Pressed':
        button.SetState(1)
        if techstr == '2748':
            techstr = '' 
            techlblstr = ''
            LblTechString.SetText(techlblstr)
            dvTLP.ShowPopup('Audio Mix popup')
        else:
            techstr = ''
            techlblstr = ''
            LblTechString.SetText(techlblstr)
    elif state == 'Released':
        button.SetState(0)

#Advanced Exit 
btn_advSettingsExit = Button(dvTLP, 56)
@eventEx(btn_advSettingsExit, ButtonEventList)
def ExitAdvancedSettingsPopup(button:Button, state):
    print(button.Name, state)
    if state == 'Pressed':
        global techstr
        global techlblstr
        button.SetState(1)
        techstr = ''
        techlblstr = ''
        LblTechString.SetText(techstr)          #clear the passcode before closing the page so it's empty when the user returns 
        dvTLP.HidePopup("Advanced Settings")
    elif state == 'Released':
        button.SetState(0)
