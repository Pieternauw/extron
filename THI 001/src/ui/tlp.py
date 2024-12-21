"""
This is the place to put the modules for each UI in the system.  One module for each unique ui --
mirrored panels should be in the same file.
* UI object definition
* UI navigation
"""

"""
Version 1.0.1 - Pre-deployment in Kresge 3101 w/ Organizational changes

--- Code Structure ---

Import statements:
System for MESet - used to group the input buttons together
UI for Button and Label - define all UI objects referenced including text objects
Module Support for eventEx - allows user defined functions to control devices and do actions

Device imports - Touchpanel for UI interaction and the 1808 switcher for source and audio control - Audio may be removed at later revision
Variables - A list of button event types allowing for different responses based on button state

UI Files - Where other sections of the UI are defined such as BluRay control, the Advanced Settings popup, and the passcode page
UI is split between different files for organizaitional purposes. Having multiple files for UI objects makes each file smaller and easier to handle
Control for these UI objects is included in the Control folder where a majority of the external device interaction is defined. 
The only remaining control is the 1808 switcher's audio control on shutdown routine which will be moved soon

MAIN PAGE
This is where all main page buttons are defined including source selection buttons, shutdown buttons, and the advanced settings popup.
This section also includes help popups from different selected sources and the overall help button (still undefined). 

The nightly shutdown function will be included in revision 1.0.2

Rev 1.2.1:
-- Removed multiple shutdown functions
-- Created one function called by both button press and nightly timer
-- Implemented 11:00pm shu

"""

# Python imports

# Extron Library imports
from extronlib.system import MESet
from extronlib.ui import Button, Label
from modules.helper.ModuleSupport import eventEx

#Project Imports
from devices import dvTLP
from variables import ButtonEventList

#Linking Files
import ui.tlpBluray
import ui.tlpAdvanced as adv
import ui.tlpAudio
import ui.tlpMainAudio as MainAudio
import variables as var

#bring in variables here for defaults (audio level, default source and what not)

# Define UI Objects

#Tap to start

"""MAIN PAGE"""
#Source Selection  
btn_sourceHDMI = Button(dvTLP, 247)
btn_sourceWireless = Button(dvTLP, 250)
btn_sourceMac = Button(dvTLP, 253) 
btn_sourceBluray = Button(dvTLP, 248)
btn_sourceDocCam = Button(dvTLP, 249)

#mutually exclusive set for all inputs. only allows one to be selected at a time
input_set = MESet([btn_sourceHDMI, btn_sourceWireless, btn_sourceDocCam, btn_sourceMac, btn_sourceBluray])

#assigns states to each button in the set
for button in input_set.Objects:
    input_set.SetStates(button, 0, 1)
    
#set current to None means deselect all buttons
input_set.SetCurrent(None)


#Help Button
btn_help = Button(dvTLP, 90)
btn_exit_help = Button(dvTLP, 225)

@eventEx(btn_help, ['Pressed', 'Released'])
def ShowHelp(button:Button, state):
    button.SetState(1 if state is 'Pressed' else 0)
    dvTLP.ShowPopup('help popup')
    
@eventEx(btn_exit_help, ['Pressed', 'Released'])
def ExitHelp(button:Button, state):
    button.SetState(1 if state is 'Pressed' else 0)
    dvTLP.HidePopup('help popup')

#video Mute
btn_videoMute = Button(dvTLP, 255)
        
"""HDMI Popup"""

#Connection Status Display
#definition of the objects. Control is in the sourceControl.py file
btn_laptopConnectedFeedback = Button(dvTLP, 23)
lblLaptopConnected = Label(dvTLP, 133)
        
#Help Buttons
btn_macHelp = Button(dvTLP, 131)
btn_winHelp = Button(dvTLP, 130)
btn_exitMacHelp = Button(dvTLP, 174)
btn_exitWinHelp = Button(dvTLP, 163)

btn_wirelessMac = Button(dvTLP, 13)
btn_wirelessWindows = Button(dvTLP, 53)
btn_wirelessIPhone = Button(dvTLP, 58)
btn_wirelessAndroid = Button(dvTLP, 75)

wireless_btn_help_set = MESet([btn_wirelessMac, btn_wirelessWindows, btn_wirelessIPhone, btn_wirelessAndroid])

for button in wireless_btn_help_set.Objects:
    wireless_btn_help_set.SetStates(button, 0, 1)
    
wireless_btn_help_set.SetCurrent(None)

prev_popup = ''

wireless_help_set = {btn_wirelessMac: 'wireless mac os', btn_wirelessWindows: 'wireless windows', btn_wirelessIPhone: 'wireless ios', btn_wirelessAndroid: 'wireless android'}
@eventEx(wireless_btn_help_set.Objects, 'Pressed')
def WirelessHelpSelect(button:Button, state):
    global prev_popup
    dvTLP.HidePopup('wireless select device')
    dvTLP.HidePopup(prev_popup)
    dvTLP.ShowPopup(wireless_help_set[button])
    prev_popup = wireless_help_set[button]
    wireless_btn_help_set.SetCurrent(button)

help_set = [btn_macHelp, btn_winHelp]
close_help = [btn_exitMacHelp, btn_exitWinHelp]
help_popup = ["mac laptop & tablet help popup", "Windows Laptop Help popup"]

@eventEx(help_set, ['Pressed', 'Released'])
def ShowHelp(button:Button, state):
    print(button.Name, state)
    button.SetState(1 if state is 'Pressed' else 0)
    if state is 'Pressed': dvTLP.ShowPopup(help_popup[help_set.index(button)])

@eventEx(close_help, ['Pressed', 'Released'])
def CloseHelp(button:Button, state):
    print(button.Name, state)
    button.SetState(1 if state is 'Pressed' else 0)
    if state is 'Pressed': dvTLP.HidePopup(help_popup[close_help.index(button)])

#Shutdown button
btn_shutdown = Button(dvTLP, 234)
@eventEx(btn_shutdown, ButtonEventList)
def ShowShutdownPage(button:Button, state):
    print(button.Name, state)
    button.SetState(1 if state is 'Pressed' else 0)
    if state is 'Pressed': dvTLP.ShowPage("Shutdown confirmation")

btn_shdnYes = Button(dvTLP, 6)

btn_shdnNo = Button(dvTLP, 7)
@eventEx(btn_shdnNo, 'Pressed')
def ShutdownNo(button:Button, state):
    print(button.Name, state)
    dvTLP.ShowPage("Main Page")

    

