#Extron Imports 
from modules.helper.ModuleSupport import eventEx
from modules.helper.MirrorUI import Button, Label, Slider

from devices import dvTLPMain

#advanced settings
btn_dAdvSettings = Button(dvTLPMain, 41)
btn_cAdvSettings = Button(dvTLPMain, 235)
@eventEx([btn_dAdvSettings, btn_cAdvSettings], ['Pressed', 'Released'])
def ShowAdvancedSettingsPopup(button:Button, state):
    print(button.Name, button.Host, state)
    button.SetState(1 if state is 'Pressed' else 0)
    if state == 'Pressed': dvTLPMain.ShowPopup("Advanced Settings")

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
    button.SetState(1 if state is 'Pressed' else 0)
    if state is 'Pressed':
        print(button.Name, state)
        global techstr, techlblstr
        techstr += button.Name
        techlblstr += '*'
        LblTechString.SetText(techlblstr)
    
btn_techClear = Button(dvTLPMain, 117)
btn_techEnter = Button(dvTLPMain, 118)

def blank_str():
    global techstr, techlblstr
    techstr = techlblstr = ''
    LblTechString.SetText(techlblstr)

@eventEx([btn_techClear, btn_techEnter], ['Pressed', 'Released'])
def BtnEnterTech(button:Button, state):
    print(button.Name, state)
    global techstr
    button.SetState(1 if state is 'Pressed' else 0)
    if button is btn_techEnter and techstr == '2748':
        dvTLPMain.ShowPopup('Audio Mix popup')
    blank_str()
    
#Advanced Exit 
btn_advSettingsExit = Button(dvTLPMain, 56)
@eventEx(btn_advSettingsExit, ['Pressed', 'Released'])
def ExitAdvancedSettingsPopup(button:Button, state):
    print(button.Name, state)
    button.SetState(1 if state is 'Pressed' else 0)
    blank_str()        #clear the passcode before closing the page so it's empty when the user returns 
    dvTLPMain.HidePopup("Advanced Settings")

btn_Inactivity = Button(dvTLPMain, 155)
btn_Inactivity.SetVisible(False)

sld_lavMic = Slider(dvTLPMain, 22)
sld_lavMic.SetRange(-18, 80, 1)

sld_handHeld = Slider(dvTLPMain, 28)
sld_handHeld.SetRange(-18, 80, 1) 

sld_laptop = Slider(dvTLPMain, 35)
sld_laptop.SetRange(-18, 24, 0.5)  

sld_wireless = Slider(dvTLPMain, 39)
sld_wireless.SetRange(-18, 24, 0.5)     #TODO Check numbers

sld_bluray = Slider(dvTLPMain, 45)
sld_bluray.SetRange(-18, 24, 0.5)     #TODO Check numbers

sld_ampLevelOut = Slider(dvTLPMain, 52)
sld_ampLevelOut.SetRange(-100, 0, 1)

slider_list = [sld_lavMic, sld_handHeld, sld_laptop, sld_wireless, sld_bluray, sld_ampLevelOut]
@eventEx(slider_list, 'Changed')
def SliderFills(slider:Slider, state, value):
    slider.SetFill(value)
    
btn_exitMix = Button(dvTLPMain, 76)
@eventEx(btn_exitMix, 'Pressed')
def ExitAudioMix(button:Button, state):
    print(button.Name, state)
    dvTLPMain.HidePopup('Audio Mix popup')
