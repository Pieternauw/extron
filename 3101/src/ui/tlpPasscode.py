from modules.helper.ModuleSupport import eventEx

from extronlib.ui import Button, Label
from extronlib.system import File

from devices import dvTLP
from variables import ButtonEventList

btn_startScreen = Button(dvTLP, 19)

@eventEx(btn_startScreen, 'Pressed')
def ShowStartPage(button:Button, state):
    print(button.Name, state)
    dvTLP.ShowPage("Main passcode")
    #may want to auto this to the main page if I can't get the passcode going before deployment

"""PASSCODE SCREEN"""

"""TODO - Cancel Button needs to be added"""
#opening the passcode file
#use extron File for this - figure out how to get that onto the device

passcodeFile = File('user/passcode.txt', 'r')
passcode = str(passcodeFile.readline())
print('passcode', passcode)

PadButtons = []
for Button_IDs in range(141, 151):
    PadButtons.append(Button(dvTLP, Button_IDs))
    
LblPadString = Label(dvTLP, 140)
LblString = ''
PadString = ''

@eventEx(PadButtons, ButtonEventList)
def PadButtonPressed(button:Button, state):
    print(button.Name, state)
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
btn_passcodeEnter = Button(dvTLP, 152)
@eventEx(btn_passcodeEnter, ButtonEventList)
def BtnEnterPasscode(button:Button, state):
    print(button.Name, state)
    global PadString 
    global LblString
    if state == 'Pressed':
        button.SetState(1)
        if (PadString == '2748') or (PadString == passcode):      #whatever the current passcode is
            dvTLP.ShowPage('Main Page')
            
        PadString = ''
        LblString = ''
        LblPadString.SetText(LblString)
    elif state == 'Released':
        button.SetState(0)

btn_passcodeClear = Button(dvTLP, 151)
@eventEx(btn_passcodeClear, ButtonEventList)
def BtnClearPad(button:Button, state):
    print(button.Name, state)
    global PadString
    global LblString
    PadString = ''
    LblString = ''
    LblPadString.SetText(LblString)
    if state == 'Pressed':
        button.SetState(1)
    elif state == 'Released':
        button.SetState(0)
        