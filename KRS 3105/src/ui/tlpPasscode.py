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
    