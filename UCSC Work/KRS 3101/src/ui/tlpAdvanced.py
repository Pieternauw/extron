from modules.helper.ModuleSupport import eventEx
from extronlib.system import MESet
from extronlib.ui import Button, Label, Slider

from devices import dvTLP
from variables import ButtonEventList

#advanced settings
btn_advSettings = Button(dvTLP, 47)
@eventEx(btn_advSettings, ButtonEventList)
def ShowAdvancedSettingsPopup(button:Button, state):
    print(button.Name, state)
    button.SetState(1 if state is 'Pressed' else 0)
    dvTLP.ShowPopup("Advanced Settings")
    

#Activity Timeout
btn_actTimeout = Button(dvTLP, 155)
btn_actTimeout.SetVisible(False)

btn_projOn = Button(dvTLP, 24)
btn_projOff = Button(dvTLP, 25)

btn_blankImg = Button(dvTLP, 21)

TechButtons = []
for Button_IDs in range(107, 117):
    TechButtons.append(Button(dvTLP, Button_IDs))
    
LblTechString = Label(dvTLP, 20)
techstr = ''
techlblstr = ''

@eventEx(TechButtons, ButtonEventList)
def TechButtonPressed(button:Button, state):
    button.SetState(1 if state is 'Pressed' else 0)
    if state is 'Pressed':
        print(button.Name, state)
        global techstr 
        global techlblstr
        techstr += button.Name
        techlblstr += '*'
        LblTechString.SetText(techlblstr)
    
btn_techClear = Button(dvTLP, 117)
btn_techEnter = Button(dvTLP, 118)

def blank_str():
    global techstr, techlblstr
    techstr = ''
    techlblstr = ''
    LblTechString.SetText(techlblstr)

@eventEx([btn_techClear, btn_techEnter], ButtonEventList)
def BtnEnterTech(button:Button, state):
    print(button.Name, state)
    global techstr
    button.SetState(1 if state is 'Pressed' else 0)
    if button is btn_techEnter and techstr == '2748':
        dvTLP.ShowPopup('Audio Mix popup')
    blank_str()
    
#Advanced Exit 
btn_advSettingsExit = Button(dvTLP, 56)
@eventEx(btn_advSettingsExit, ButtonEventList)
def ExitAdvancedSettingsPopup(button:Button, state):
    print(button.Name, state)
    button.SetState(1 if state is 'Pressed' else 0)
    blank_str()        #clear the passcode before closing the page so it's empty when the user returns 
    dvTLP.HidePopup("Advanced Settings")

sld_lavMic = Slider(dvTLP, 22)
sld_lavMic.SetRange(-18, 80, 1)

sld_handHeld = Slider(dvTLP, 28)
sld_handHeld.SetRange(-18, 80, 1) 

sld_laptop = Slider(dvTLP, 35)
sld_laptop.SetRange(-18, 24, 0.5)  

sld_wireless = Slider(dvTLP, 39)
sld_wireless.SetRange(-18, 24, 0.5)     #TODO Check numbers

sld_bluray = Slider(dvTLP, 45)
sld_bluray.SetRange(-18, 24, 0.5)     #TODO Check numbers

sld_ampLevelOut = Slider(dvTLP, 52)
sld_ampLevelOut.SetRange(-100, 0, 1)

slider_list = [sld_lavMic, sld_handHeld, sld_laptop, sld_wireless, sld_bluray, sld_ampLevelOut]
@eventEx(slider_list, 'Changed')
def SliderFills(slider:Slider, state, value):
    slider.SetFill(value)
    
btn_exitMix = Button(dvTLP, 76)
@eventEx(btn_exitMix, 'Pressed')
def ExitAudioMix(button:Button, state):
    print(button.Name, state)
    dvTLP.HidePopup('Audio Mix popup')

