"""
The main file for the project. This file includes a lot of main page buttons such as the shutdown buttons,
the advanced settings button, and help buttons. It also includes the shutdown routine which in rev 1.0.1 will 
be moved to a control file. This is the collection point for all other touch panels as well. Any file that's 
created seperately needs to be imported into this one for the compiler to recognize it. 
"""

# Python imports
from extronlib.system import MESet, Clock
# Project imports
from modules.helper.ModuleSupport import eventEx
from modules.helper.MirrorUI import Button
from devices import dvTLPMain, dvMatrix, dvBiamp, dvLeftPRJ, dvCenterPRJ, dvRightPRJ, dvRelay

import ui.tlpAdvanced
import ui.tlpAudioMix
import ui.tlpBluray
import ui.tlpPasscode
import ui.tlpSourceSelect as tlpSourceSelect
import ui.tlpMainPageAudio as tlpMainPageAudio
# Define UI Objects

BTNEVL = ['Pressed', 'Released', 'Tapped', 'Held']

def ShutdownSystem(clock, dt):
    
    dvCenterPRJ.SetPower('Off', None)
    dvRightPRJ.SetPower('Off', None)
    dvLeftPRJ.SetPower('Off', None)
    dvCenterPRJ.Update('Power')
    dvRightPRJ.Update('Power')
    dvLeftPRJ.Update('Power')

    tlpSourceSelect.left_input_set.SetCurrent(None)
    tlpSourceSelect.right_input_set.SetCurrent(None)
    tlpSourceSelect.center_board_set.SetCurrent(None)
    tlpSourceSelect.center_input_set.SetCurrent(None)

    dvRelay.SetState('Open')

    tlpMainPageAudio.lvl_cMic.SetLevel(-18)
    tlpMainPageAudio.lvl_cProg.SetLevel(-18)
    dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelSpeech', 'Channel': '1'})
    dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelProgram', 'Channel': '1'})
        
    dvMatrix.SetMatrixTieCommand(None, {'Input': '3', 'Output': '9', 'Tie Type': 'Audio/Video'}) #Cynap
    
    for i in ['1', '2', '3', '4', '5', '12']:
        dvMatrix.SetMatrixTieCommand(None, {'Input': '0', 'Output': i, 'Tie Type': 'Audio/Video'}) 

    dvTLPMain.ShowPage('Start Page')
    dvTLPMain.HideAllPopups()

Shutdown = Clock(['23:00:00'], None, ShutdownSystem)
Shutdown.Enable()


"""Main Page"""
btn_startScreen = Button(dvTLPMain, 19)
@eventEx(btn_startScreen, BTNEVL)
def StartScreen(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.ShowPage('Main passcode')
    elif state == 'Released':
        button.SetState(0)

selected = False
dual = False

"""Room Mode Selection Page"""
btn_singleDisplay = Button(dvTLPMain, 30)
@eventEx(btn_singleDisplay, BTNEVL)
def SingleDisplay(button:Button, state):
    global selected, dual
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.ShowPage('C Projection')
        dvTLPMain.ShowPopup('center mode confirm')
        selected = True
        dual = False
        dvRelay.SetState('Closed')
    elif state == 'Released':
        button.SetState(0)
    
btn_dualDisplay = Button(dvTLPMain, 31)
@eventEx(btn_dualDisplay, BTNEVL)
def DualDisplay(button:Button, state):
    global selected, dual
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.ShowPage('DualProjection')
        dvTLPMain.ShowPopup('dual mode confirm')
        selected = True
        dual = True
        dvRelay.SetState('Closed')
    elif state == 'Released':
        button.SetState(0)

"""confirmation button """
btn_cConfirm = Button(dvTLPMain, 46)
btn_dConfirm = Button(dvTLPMain, 17)
@eventEx([btn_cConfirm, btn_dConfirm], BTNEVL)
def CenterConfirm(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.HideAllPopups()
        dvTLPMain.ShowPage('room mode select')
        
"""Help Popup"""  
btn_cHelpPopup = Button(dvTLPMain, 90)
btn_dBottomHelp = Button(dvTLPMain, 57)
btn_dTopHelp = Button(dvTLPMain, 11)
@eventEx([btn_cHelpPopup, btn_dBottomHelp, btn_dTopHelp], BTNEVL)
def CenterHelpButton(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.ShowPopup('help popup')
    elif state == 'Released':
        button.SetState(0)
        
btn_exitHelp = Button(dvTLPMain, 225)
@eventEx(btn_exitHelp, BTNEVL)
def ExitHelpPopup(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.HidePopup('help popup')
    elif state == 'Released':
        button.SetState(0)
    
"""Shutdown Screen"""
btn_cShutdown = Button(dvTLPMain, 234)
btn_dShutdown = Button(dvTLPMain, 8)
btn_roomSelectShutdown = Button(dvTLPMain, 12)
@eventEx([btn_cShutdown, btn_dShutdown, btn_roomSelectShutdown], BTNEVL)
def ShutdownPage(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.ShowPage('Shutdown confirmation')
    elif state == 'Released':
        button.SetState(0)
        

        
btn_shutdownYes = Button(dvTLPMain, 6)
@eventEx(btn_shutdownYes, BTNEVL)
def ShutdownConfirm(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        #shut off projectors
        #shut off receivers
        #lock cabinet
        button.SetState(1)
        dvCenterPRJ.SetPower('Off', None)
        dvRightPRJ.SetPower('Off', None)
        dvLeftPRJ.SetPower('Off', None)
        dvCenterPRJ.Update('Power')
        dvRightPRJ.Update('Power')
        dvLeftPRJ.Update('Power') 

        tlpSourceSelect.left_input_set.SetCurrent(None)
        tlpSourceSelect.right_input_set.SetCurrent(None)
        tlpSourceSelect.center_board_set.SetCurrent(None)
        tlpSourceSelect.center_input_set.SetCurrent(None)

        tlpMainPageAudio.lvl_cMic.SetLevel(-18)
        tlpMainPageAudio.lvl_cProg.SetLevel(-18)
        dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelSpeech', 'Channel': '1'})
        dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelProgram', 'Channel': '1'})
        
        dvMatrix.SetMatrixTieCommand(None, {'Input': '3', 'Output': '9', 'Tie Type': 'Audio/Video'}) #Cynap

        for i in ['1', '2', '3', '4', '5', '12']:
            dvMatrix.SetMatrixTieCommand(None, {'Input': '0', 'Output': i, 'Tie Type': 'Audio/Video'}) 

        dvTLPMain.ShowPage('Start Page')
        dvTLPMain.HideAllPopups()
        
        
btn_shutdownNo = Button(dvTLPMain, 7)
@eventEx(btn_shutdownNo, 'Pressed')
def CancelShutdown(button:Button, state):
    print(button.Name, button.Host, state)
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
@eventEx(btn_macHelp, BTNEVL)
def ShowMacHelpPopup(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.ShowPopup("mac laptop & tablet help popup")
    elif state == 'Released':
        button.SetState(0)     

btn_winHelp = Button(dvTLPMain, 130)
@eventEx(btn_winHelp, BTNEVL)
def ShowMacHelpPopup(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.ShowPopup("Windows Laptop Help popup")
    elif state == 'Released':
        button.SetState(0)
        
"""Mac Help Popup"""
btn_exitMacHelp = Button(dvTLPMain, 174)
@eventEx(btn_exitMacHelp, BTNEVL)
def CloseMacHelpPopup(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.HidePopup("mac laptop & tablet help popup")
    elif state == 'Released':
        button.SetState(0)

"""Windows Help Popup"""
btn_exitWinHelp = Button(dvTLPMain, 163)
@eventEx(btn_exitWinHelp, BTNEVL)
def CloseMacHelpPopup(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.HidePopup("Windows Laptop Help popup")
    elif state == 'Released':
        button.SetState(0)
        
"""Wireless Help Popup"""
btn_wirelessMac = Button(dvTLPMain, 13)
btn_wirelessWindows = Button(dvTLPMain, 53)
btn_wirelessIpadIphone = Button(dvTLPMain, 58)
btn_wirelessAndroid = Button(dvTLPMain, 75)

wireless_set = MESet([btn_wirelessMac, btn_wirelessWindows, btn_wirelessIpadIphone, btn_wirelessAndroid])

for button in wireless_set.Objects:
    wireless_set.SetStates(button, 0, 1)
    
wireless_set.SetCurrent(None)

wireless_popup_set = ['wireless mac os popup', 'wireless windows popup', 'wireless ios popup', 'wireless android popup']
    
@eventEx(wireless_set.Objects, BTNEVL)
def WirelessHelpSelect(button:Button, state):
    print(button.Name, button.Host, state)
    dvTLPMain.HideAllPopups()
    dvTLPMain.ShowPopup('Wireless instruction popup')
    dvTLPMain.ShowPopup(wireless_popup_set[wireless_set.Objects.index(button)])
