"""
The passcode screen has only the passcode number pad, enter, clear, and a cancel button. The 
number pad buttons are all named for their number, allowing me to append the button's name to 
the comparison string, rather than having to do anything with logic. 

The passcode utilizes two strings and a label object to work effectively. The first string is 
the comparison string. That string is what gets checked against the passcode on the IPCP or the 
hardcoded engineering passcode. The print string is just a string of * characters, with one being 
appended every time a number gets pressed. This gets put in the label text and shown to the user
to represent how many numbers have been entered so far. 

On Enter and Clear, both variables get emptied. This prevents errors from happening if the user 
logs out and the variable wasn't cleared. Enter compares to both a hardcoded passcode, and a 
changeable passcode accessed via extron's File class. This class allows access to files stored
on the IPCP controller. Here we have a file containing one line with just the 4 numbers for the 
passcode of the quarter. This passcode gets read in and put in a varaible for comparison. 
"""

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
@eventEx(btn_passcodeClear, ['Pressed', 'Released'])
def BtnClearPad(button:Button, state):
    print(button.Name, state)
    global PadString
    global LblString
    PadString = ''
    LblString = ''
    if state == 'Pressed': LblPadString.SetText(LblString)
    button.SetState(1 if state is 'Pressed' else 0)
        
