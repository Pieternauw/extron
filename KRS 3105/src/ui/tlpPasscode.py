"""
The main passcode has two possible codes that work. The first is the hard-coded MSE passcode.
The second is the passcode located on the IPCP itself. This passcode is changed quarterly so
reading it off of a file means it can be changed without needing to change any of the code itself. 
The number pad numbers have their UI names set as the number the represent. When a number button 
gets pressed, that name gets appended to a comparison string. When the user presses enter that
string gets compared to both passcodes and if it matches, it's cleared and the main page is shown.
If it's wrong, the clear routine gets called where both the visual feedback (string of * representing
numbers entered) gets refreshed as well as the comparison string. 
"""

from modules.helper.ModuleSupport import eventEx
from modules.helper.MirrorUI import Button, Label

from extronlib.system import File

from devices import dvTLPMain  

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
            dvTLPMain.ShowPage('room mode select')
            
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
    