"""
This file is the definiton of every source selection button. It includes both center, left, and right 
input sets and uses the MESet class to combine them all. With the MESet, only one of the groups buttons
can be selected at a time. This allows for visual feedback to acurately represent the current selcted 
source. 

The final piece of this is the event when any button is pressed. Depending on which set its in, different 
variables are set for the control file. The variables include:
1. prj_select -> referneces which projector to tie inputs too. Also determines wich to turn on and what set 
to pull the button index from for source selection
2. monitor_select -> refers to the confidence monitor on the podium. Center and left use the same monitor
3. yuja_select -> refers to which yuja input gets tied to the input source. Center and left use the same 
number. Also used for board camera selection as of rev 1.0.0

These numbers are used in the control file matching this one. This method simplifies the logic needed in 
switching sources and allows me to treat all input buttons as one big set of buttons. That way only one 
method is needed to control any input button selection. 
"""

from modules.helper.ModuleSupport import eventEx
from modules.helper.MirrorUI import Button, Label

from control.shutdownControl import Startup

from extronlib.system import File

from devices import dvTLPMain, dvMatrix

btn_startScreen = Button(dvTLPMain, 19)

@eventEx(btn_startScreen, 'Pressed')
def ShowStartPage(button:Button, state):
    print(button.Name, button.Host, state)
    dvTLPMain.ShowPage("Main passcode")
    #may want to auto this to the main page if I can't get the passcode going before deployment


passcodeFile = File('user/passcode.txt', 'r')
passcode = str(passcodeFile.readline())
print('passcode', passcode)

PadButtons = []
for Button_IDs in range(141, 151):
    PadButtons.append(Button(dvTLPMain, Button_IDs))
    
LblPadString = Label(dvTLPMain, 140)
LblString = ''
PadString = ''

@eventEx(PadButtons, ['Pressed', 'Released'])
def PadButtonPressed(button:Button, state):
    print(button.Name, button.Host, state)
    global PadString 
    global LblString
    if state == 'Pressed':
        button.SetState(1)
        PadString += button.Name
        LblString += '*'
        LblPadString.SetText(LblString)
    elif state == 'Released':
        button.SetState(0)

#enter and clear
btn_passcodeEnter = Button(dvTLPMain, 152)
@eventEx(btn_passcodeEnter, ['Pressed', 'Released'])
def BtnEnterPasscode(button:Button, state):
    print(button.Name, button.Host, state)
    global PadString 
    global LblString
    if state == 'Pressed':
        button.SetState(1)
        if (PadString == '2748') or (PadString == passcode):      #whatever the current passcode is
            Startup()
        PadString = ''
        LblString = ''
        LblPadString.SetText(LblString)
    elif state == 'Released':
        button.SetState(0)

btn_passcodeClear = Button(dvTLPMain, 151)
@eventEx(btn_passcodeClear, ['Pressed', 'Released'])
def BtnClearPad(button:Button, state):
    print(button.Name, button.Host, state)
    global PadString
    global LblString
    PadString = ''
    LblString = ''
    LblPadString.SetText(LblString)
    if state == 'Pressed':
        button.SetState(1)
    elif state == 'Released':
        button.SetState(0)

btn_passcodeCancel = Button(dvTLPMain, 153)
@eventEx(btn_passcodeCancel, ['Pressed', 'Released'])
def CancelPasscode(button:Button, state):
    button.SetState(1 if state == 'Pressed' else 0)
    print(button.Name, state)
    if state is 'Pressed':
        dvTLPMain.ShowPage('Start Page')
    