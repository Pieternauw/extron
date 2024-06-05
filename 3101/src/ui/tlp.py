"""
This is the place to put the modules for each UI in the system.  One module for each unique ui --
mirrored panels should be in the same file.
* UI object definition
* UI navigation
"""

# Python imports

# Extron Library imports
from extronlib.system import MESet, Wait, Timer
from extronlib.ui import Button, Label
from modules.helper.ModuleSupport import eventEx

#Project Imports
from devices import dvTLP, dvScalar
from variables import ButtonEventList

#Linking Files
import ui.tlpBluray
import ui.tlpAdvanced
import ui.tlpAudio
import ui.tlpPasscode
import ui.tlpMainAudio as MainAudio
import variables as var

#bring in variables here for defaults (audio level, default source and what not)

# Define UI Objects

#Tap to start

"""MAIN PAGE"""
#Source Selection  
btn_sourceHDMI = Button(dvTLP, 10)
btn_sourceWireless = Button(dvTLP, 16)
btn_sourceDocCam = Button(dvTLP, 14)
btn_sourceBluray = Button(dvTLP, 11)

input_set = MESet([btn_sourceHDMI, btn_sourceWireless, btn_sourceDocCam, btn_sourceBluray])

for button in input_set.Objects:
    input_set.SetStates(button, 0, 1)
    
input_set.SetCurrent(None)
input_popup_list = ['Laptop Connected popup', 'Wireless instruction popup', 
              'Document camera instruction popup', 'BluRay control popup']


#Help Button
btn_help = Button(dvTLP, 90)

#video Mute
btn_videoMute = Button(dvTLP, 17)
        
"""HDMI Popup

TODO needs to be fixed so that when InputSignalStatus changes, the visual feedback changes"""
#Connection Status Display
btn_laptopConnectedFeedback = Button(dvTLP, 23)
lblLaptopConnected = Label(dvTLP, 133)
        
#Help Buttons
btn_macHelp = Button(dvTLP, 131)
@eventEx(btn_macHelp, ButtonEventList)
def ShowMacHelpPopup(button:Button, state):
    print(button.Name, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLP.ShowPopup("mac laptop & tablet help popup")
    elif state == 'Released':
        button.SetState(0)
        

btn_winHelp = Button(dvTLP, 130)
@eventEx(btn_winHelp, ButtonEventList)
def ShowMacHelpPopup(button:Button, state):
    print(button.Name, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLP.ShowPopup("Windows Laptop Help popup")
    elif state == 'Released':
        button.SetState(0)
        
"""Mac Help Popup"""
btn_exitMacHelp = Button(dvTLP, 58)
@eventEx(btn_exitMacHelp, ButtonEventList)
def CloseMacHelpPopup(button:Button, state):
    print(button.Name, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLP.HidePopup("mac laptop & tablet help popup")
    elif state == 'Released':
        button.SetState(0)

"""Windows Help Popup"""
btn_exitWinHelp = Button(dvTLP, 163)
@eventEx(btn_exitWinHelp, ButtonEventList)
def CloseMacHelpPopup(button:Button, state):
    print(button.Name, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLP.HidePopup("Windows Laptop Help popup")
    elif state == 'Released':
        button.SetState(0)
        

#Shutdown button
btn_shutdown = Button(dvTLP, 8)
@eventEx(btn_shutdown, ButtonEventList)
def ShowShutdownPage(button:Button, state):
    print(button.Name, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLP.ShowPage("Shutdown confirmation")
    elif state == 'Released':
        button.SetState(0)

btn_shdnYes = Button(dvTLP, 6)
@eventEx(btn_shdnYes, ButtonEventList)
def ShutdownYes(button:Button, state):
    print(button.Name, state)
    if state == 'Pressed':
        button.SetState(1)
    
        #lock drawer with control? 
        #turn off projector
        #Set Audio levels back to defaults

        MainAudio.lvl_mic.SetLevel(var.mic_val)
        dvScalar.SetGroupMicVolume(var.mic_val, None)

        MainAudio.lvl_prog.SetLevel(var.prog_val)
        dvScalar.SetGroupProgramVolume(var.prog_val, None)

        #set Cynap as input
        
        #switch to start page
        dvTLP.ShowPage("Start Page")
        dvTLP.HideAllPopups()
        
    elif state == 'Released':
        button.SetState(0)

btn_shdnNo = Button(dvTLP, 7)
@eventEx(btn_shdnNo, 'Pressed')
def ShutdownNo(button:Button, state):
    print(button.Name, state)
    dvTLP.ShowPage("Main Page")


        
#Sleep timer
"""TODO The sleep timer seems to be related to a button press. I don't want to 
        sleep on a buton press I want an inactivity timeout. 
        
        When innactive for certain time - check page we're on. If it's the start page 
        then trigger sleep event. """

#change sleep state event 
"""TODO I don't know if this routine will work properly on a tap if it's off. 
        I think I still need a sleep timer which should go above here
@eventEx(dvTLP, 'SleepChanged')
def HandleSleepChange(tlp, state):
    if state is 'Awake':
        tlp.Wake()
        tlp.ShowPage('Start Page')
    else:
        tlp.Sleep()
""" #Commented out for now
# Define UI Object Events

    

