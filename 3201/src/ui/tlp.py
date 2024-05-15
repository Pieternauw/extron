"""
This is the place to put the modules for each UI in the system.  One module for each unique ui --
mirrored panels should be in the same file.
* UI object definition
* UI navigation
"""

# Python imports
from extronlib.system import MESet, Wait
# Project imports
from modules.helper.ModuleSupport import eventEx
from modules.helper.MirrorUI import Button
from devices import dvTLPMain, dvMatrix, dvBiamp, dvLeftPRJ, dvCenterPRJ, dvRightPRJ

import ui.tlpAdvanced
import ui.tlpAudioMix
import ui.tlpBluray
import ui.tlpPasscode
import ui.tlpSourceSelect
import ui.tlpMainPageAudio as tlpMainPageAudio
# Define UI Objects

BTNEVL = ['Pressed', 'Released', 'Tapped', 'Held']


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

"""Room Mode Selection Page"""
btn_singleDisplay = Button(dvTLPMain, 30)
@eventEx(btn_singleDisplay, BTNEVL)
def SingleDisplay(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.ShowPage('C Projection')
        dvTLPMain.ShowPopup('center mode confirm')
    elif state == 'Released':
        button.SetState(0)
    
btn_dualDisplay = Button(dvTLPMain, 31)
@eventEx(btn_dualDisplay, BTNEVL)
def DualDisplay(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.ShowPage('DualProjection')
        dvTLPMain.ShowPopup('dual mode confirm')
    elif state == 'Released':
        button.SetState(0)

"""confirmation button """
btn_cConfirm = Button(dvTLPMain, 46)
@eventEx(btn_cConfirm, BTNEVL)
def CenterConfirm(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.HideAllPopups()
        dvTLPMain.ShowPage('room mode select')


      
      
"""Help Popup"""  
btn_cHelpPopup = Button(dvTLPMain, 90)
@eventEx(btn_cHelpPopup, BTNEVL)
def CenterHelpButton(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.HideAllPopups()
        dvTLPMain.ShowPopup('help popup')
    elif state == 'Released':
        button.SetState(0)
        
btn_exitHelp = Button(dvTLPMain, 225)
@eventEx(btn_exitHelp, BTNEVL)
def ExitHelpPopup(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.HideAllPopups()
    elif state == 'Released':
        button.SetState(0)
    
"""Shutdown Screen"""
btn_cShutdown = Button(dvTLPMain, 234)
btn_dShutdown = Button(dvTLPMain, 8)
@eventEx([btn_cShutdown, btn_dShutdown], BTNEVL)
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
        if (dvLeftPRJ.ReadStatus('Power') == 'Warming') or (dvCenterPRJ.ReadStatus('Power') == 'Warming') or dvRightPRJ.ReadStatus('Power') == 'Warming':
            @Wait(5)
            def PrjWarming():
                dvCenterPRJ.SetPower('Off', None)
                dvRightPRJ.SetPower('Off', None)
                dvLeftPRJ.SetPower('Off', None)
        else:
            dvCenterPRJ.SetPower('Off', None)
            dvRightPRJ.SetPower('Off', None)
            dvLeftPRJ.SetPower('Off', None)

        tlpMainPageAudio.lvl_cMic.SetLevel(-18)
        tlpMainPageAudio.lvl_cProg.SetLevel(-18)
        for i in range(1, 7):  
            dvBiamp.SetLevelControl(-18, {'Instance Tag': 'Level1', 'Channel': '{}'.format(i)})

        dvMatrix.SetMatrixTieCommand(None, {'Input': '3', 'Output': '9', 'TieType': 'Video'}) #Cynap
        dvTLPMain.ShowPage('Start Page')
        dvTLPMain.HideAllPopups()
        
        
btn_shutdownNo = Button(dvTLPMain, 6)

"""Activity Timeout Cancel"""
btn_continueActivity = Button(dvTLPMain, 215)
@eventEx(btn_continueActivity, BTNEVL)
def PreventExShutdown(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLPMain.HidePopup('inactivity popup')
        #TODO - Reset Activity timer
        
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
    
@eventEx(wireless_set.Objects, BTNEVL)
def WirelessHelpSelect(button:Button, state):
    print(button.Name, button.Host, state)
    dvTLPMain.HideAllPopups()
    if button is btn_wirelessMac:
        dvTLPMain.ShowPopup('wireless mac os popup')
    elif button is btn_wirelessWindows:
        dvTLPMain.ShowPopup('wireless windows popup')
    elif button is btn_wirelessIpadIphone:
        dvTLPMain.ShowPopup('wireless ios popup')
    elif button is btn_wirelessAndroid:
        dvTLPMain.ShowPopup('wireless android popup')
    
    dvTLPMain.ShowPopup('Wireless select device')
    dvTLPMain.ShowPopup('Wireless instruction popup')
        
"""TODO FIgure out sleep """
