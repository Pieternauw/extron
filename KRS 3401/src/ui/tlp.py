# Python imports

# Extron Library imports
from extronlib.system import MESet
from extronlib.ui import Button, Label
from modules.helper.ModuleSupport import eventEx

#Project Imports
from devices import dvTLP

#Linking Files
import ui.tlpAdvanced as adv
import ui.tlpMainAudio as MainAudio
import variables as var

#bring in variables here for defaults (audio level, default source and what not)

# Define UI Objects

"""MAIN PAGE"""
#Source Selection  
btn_sourceHDMI = Button(dvTLP, 10)
btn_sourceWireless = Button(dvTLP, 16)
btn_sourceDocCam = Button(dvTLP, 14)
btn_sourcePC = Button(dvTLP, 12)

#mutually exclusive set for all inputs. only allows one to be selected at a time
input_set = MESet([btn_sourcePC, btn_sourceHDMI, btn_sourceWireless, btn_sourceDocCam])

#assigns states to each button in the set
for button in input_set.Objects:
    input_set.SetStates(button, 0, 1)
    
#set current to None means deselect all buttons
input_set.SetCurrent(None)
input_popup_list = ['Laptop Connected popup', 'Wireless instruction popup', 
              'Document camera instruction popup', 'BluRay control popup']


#Help Button
btn_help = Button(dvTLP, 90)

#video Mute
btn_videoMute = Button(dvTLP, 17)
        
"""HDMI Popup"""

#Connection Status Display
#definition of the objects. Control is in the sourceControl.py file
btn_laptopConnectedFeedback = Button(dvTLP, 23)
lblLaptopConnected = Label(dvTLP, 133)
        
#Help Buttons
btn_macHelp = Button(dvTLP, 131)
btn_winHelp = Button(dvTLP, 130)
btn_exitMacHelp = Button(dvTLP, 58)
btn_exitWinHelp = Button(dvTLP, 163)

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
btn_shutdown = Button(dvTLP, 8)
@eventEx(btn_shutdown, ['Pressed', 'Released'])
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

    

