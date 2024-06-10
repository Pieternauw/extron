"""
This is the advanced settings page. It contains the references to the 3 projector control buttons
as well as the number pad to access the advanced audio sliders page. Projector buttons are defined 
in the control file matching this one. The subscribe status method is used to keep the visual 
feedback consistent throughout the whole UI. 
"""

#Extron Imports 
from modules.helper.ModuleSupport import eventEx
from modules.helper.MirrorUI import Button, Label

from devices import dvTLPMain

#advanced settings
btn_dAdvSettings = Button(dvTLPMain, 41)
btn_cAdvSettings = Button(dvTLPMain, 235)
@eventEx([btn_dAdvSettings, btn_cAdvSettings], ['Pressed', 'Released'])
def ShowAdvancedSettingsPopup(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.ShowPopup("Advanced Settings")
    elif state == 'Released':
        button.SetState(0)

#Projector
"""Center Projector"""
btn_projOn = Button(dvTLPMain, 24)
btn_projOff = Button(dvTLPMain, 25)

btn_lPrjOn = Button(dvTLPMain, 219)
btn_lPrjOff = Button(dvTLPMain, 221)

btn_rPrjOn = Button(dvTLPMain, 216)
btn_rPrjOff = Button(dvTLPMain, 218)
    
btn_blankImg = Button(dvTLPMain, 21)
btn_lBlankImg = Button(dvTLPMain, 220)
btn_rBlankImg = Button(dvTLPMain, 217)

#Technician Access Code
TechButtons = []
for Button_IDs in range(107, 117):
    TechButtons.append(Button(dvTLPMain, Button_IDs))
    
LblTechString = Label(dvTLPMain, 20)
techstr = ''
techlblstr = ''

@eventEx(TechButtons, ['Pressed', 'Released'])
def TechButtonPressed(button:Button, state):
    print(button.Name, button.Host, state)
    global techstr 
    global techlblstr
    if state == 'Pressed':
        button.SetState(1)
        techstr += button.Name
        techlblstr += '*'
        LblTechString.SetText(techlblstr)
    elif state == 'Released':
        button.SetState(0)

btn_techClear = Button(dvTLPMain, 117)
@eventEx(btn_techClear, ['Pressed', 'Released'])
def BtnClearTech(button:Button, state):
    print(button.Name, button.Host, state)
    global techstr 
    global techlblstr
    if state == 'Pressed':
        button.SetState(1)
        techstr = ''
        techlblstr = ''
        LblTechString.SetText(techlblstr)
    elif state == 'Released':
        button.SetState(0)
        
btn_techEnter = Button(dvTLPMain, 118)
@eventEx(btn_techEnter, ['Pressed', 'Released'])
def BtnEnterTech(button:Button, state):
    print(button.Name, button.Host, state)
    global techstr 
    global techlblstr
    if state == 'Pressed':
        button.SetState(1)
        if techstr == '2748':
            techstr = '' 
            techlblstr = ''
            LblTechString.SetText(techlblstr)
            dvTLPMain.ShowPopup('Audio Mix popup')
        else:
            techstr = ''
            techlblstr = ''
            LblTechString.SetText(techlblstr)
    elif state == 'Released':
        button.SetState(0)

#Advanced Exit 
btn_advSettingsExit = Button(dvTLPMain, 56)
@eventEx(btn_advSettingsExit, ['Pressed', 'Released'])
def ExitAdvancedSettingsPopup(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        global techstr
        global techlblstr
        button.SetState(1)
        techstr = ''
        techlblstr = ''
        LblTechString.SetText(techstr)          #clear the passcode before closing the page so it's empty when the user returns 
        dvTLPMain.HidePopup("Advanced Settings")
    elif state == 'Released':
        button.SetState(0)
