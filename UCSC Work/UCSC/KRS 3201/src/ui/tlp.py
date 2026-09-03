# Python imports
from extronlib.system import MESet
# Project imports
from modules.helper.ModuleSupport import eventEx
from modules.helper.MirrorUI import Button
from devices import dvTLPMain

import ui.tlpAdvanced as adv
import ui.tlpBluray
import ui.tlpSourceSelect as tlpSourceSelect
import ui.tlpMainPageAudio as tlpMainPageAudio
# Define UI Objects

BTNEVL = ['Pressed', 'Released', 'Tapped', 'Held']


"""Main Page"""
btn_startScreen = Button(dvTLPMain, 19)
@eventEx(btn_startScreen, BTNEVL)
def StartScreen(button:Button, state):
    print(button.Name, button.Host, state)
    button.SetState(1 if state is 'Pressed' else 0)
    if state == 'Pressed': dvTLPMain.ShowPage('Main passcode')
    

selected = False
dual = False

"""Room Mode Selection Page"""
btn_singleDisplay = Button(dvTLPMain, 30)
@eventEx(btn_singleDisplay, BTNEVL)
def SingleDisplay(button:Button, state):
    global selected, dual
    print(button.Name, button.Host, state)
    button.SetState(1 if state is 'Pressed' else 0)
    if state == 'Pressed':
        dvTLPMain.ShowPage('C Projection')
        dvTLPMain.ShowPopup('center mode confirm')
        selected = True
        dual = False
    
btn_dualDisplay = Button(dvTLPMain, 31)
@eventEx(btn_dualDisplay, BTNEVL)
def DualDisplay(button:Button, state):
    global selected, dual
    print(button.Name, button.Host, state)
    button.SetState(1 if state is 'Pressed' else 0)
    if state == 'Pressed':
        dvTLPMain.ShowPage('DualProjection')
        dvTLPMain.ShowPopup('dual mode confirm')
        selected = True
        dual = True

"""confirmation button """
btn_cConfirm = Button(dvTLPMain, 46)
btn_dConfirm = Button(dvTLPMain, 17)
@eventEx([btn_cConfirm, btn_dConfirm], BTNEVL)
def CenterConfirm(button:Button, state):
    print(button.Name, button.Host, state)
    button.SetState(1 if state is 'Pressed' else 0)
    if state == 'Pressed':
        dvTLPMain.HideAllPopups()
        dvTLPMain.ShowPage('room mode select')
        
"""Help Popup"""  
btn_cHelpPopup = Button(dvTLPMain, 90)
btn_dBottomHelp = Button(dvTLPMain, 57)
btn_dTopHelp = Button(dvTLPMain, 11)
@eventEx([btn_cHelpPopup, btn_dBottomHelp, btn_dTopHelp], BTNEVL)
def CenterHelpButton(button:Button, state):
    print(button.Name, button.Host, state)
    button.SetState(1 if state is 'Pressed' else 0)
    if state == 'Pressed':
        dvTLPMain.ShowPopup('help popup')
    
btn_exitHelp = Button(dvTLPMain, 225)
@eventEx(btn_exitHelp, BTNEVL)
def ExitHelpPopup(button:Button, state):
    print(button.Name, button.Host, state)
    button.SetState(1 if state is 'Pressed' else 0)
    if state == 'Pressed':
        dvTLPMain.HidePopup('help popup')
    
"""Shutdown Screen"""
btn_cShutdown = Button(dvTLPMain, 234)
btn_dShutdown = Button(dvTLPMain, 8)
btn_roomSelectShutdown = Button(dvTLPMain, 12)
@eventEx([btn_cShutdown, btn_dShutdown, btn_roomSelectShutdown], BTNEVL)
def ShutdownPage(button:Button, state):
    print(button.Name, button.Host, state)
    button.SetState(1 if state is 'Pressed' else 0)
    if state == 'Pressed':
        dvTLPMain.ShowPage('Shutdown confirmation')

btn_shutdownYes = Button(dvTLPMain, 6)
        
btn_shutdownNo = Button(dvTLPMain, 7)
@eventEx(btn_shutdownNo, 'Pressed')
def CancelShutdown(button:Button, state):
    print(button.Name, button.Host, state)
    button.SetState(1 if state is 'Pressed' else 0)
    global selected, dual
    if selected:
        if dual:
            dvTLPMain.ShowPage('DualProjection')
        else:
            dvTLPMain.ShowPage('C Projection')
    else:
        dvTLPMain.ShowPage('room mode select')
        
#Help Buttons
btn_macHelp = Button(dvTLPMain, 131)
btn_winHelp = Button(dvTLPMain, 130)
btn_exitMacHelp = Button(dvTLPMain, 174)
btn_exitWinHelp = Button(dvTLPMain, 163)

help_set = [btn_macHelp, btn_winHelp]
close_help = [btn_exitMacHelp, btn_exitWinHelp]
help_popup = ["mac laptop & tablet help popup", "Windows Laptop Help popup"]

@eventEx([btn_macHelp, btn_winHelp, btn_exitMacHelp, btn_exitWinHelp], ['Pressed', 'Released'])
def HelpPopups(button:Button, state):
    print(button.Name, state)
    button.SetState(1 if state is 'Pressed' else 0)
    if button in help_set:
        dvTLPMain.ShowPopup(help_popup[help_set.index(button)])
        dvTLPMain.HidePopup('Laptop Connected popup')
    else: 
        dvTLPMain.HidePopup(help_popup[close_help.index(button)])
        dvTLPMain.ShowPopup('Laptop Connected popup')
        
"""Wireless Help Popup"""
btn_wirelessMac = Button(dvTLPMain, 13)
btn_wirelessWindows = Button(dvTLPMain, 53)
btn_wirelessIpadIphone = Button(dvTLPMain, 58)
btn_wirelessAndroid = Button(dvTLPMain, 75)

wireless_set = MESet([btn_wirelessMac, btn_wirelessWindows, btn_wirelessIpadIphone, btn_wirelessAndroid])

for button in wireless_set.Objects:
    wireless_set.SetStates(button, 0, 1)
    
wireless_set.SetCurrent(None)

wireless_popup_set = {btn_wirelessMac: 'wireless mac os popup', btn_wirelessWindows: 'wireless windows popup',
                      btn_wirelessIpadIphone: 'wireless ios popup', btn_wirelessAndroid: 'wireless android popup'}
    
prev_popup = ''

@eventEx(wireless_set.Objects, BTNEVL)
def WirelessHelpSelect(button:Button, state):
    print(button.Name, button.Host, state)
    global prev_popup
    dvTLPMain.HidePopup('wireless select device')
    dvTLPMain.HidePopup(prev_popup)
    prev_popup = wireless_popup_set[button]
    dvTLPMain.ShowPopup(wireless_popup_set[button])
    wireless_set.SetCurrent(button)
