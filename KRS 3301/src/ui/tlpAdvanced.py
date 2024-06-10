"""
Advanced Settings Page

The advanced settings popup has a lot of buttons on it that I decided to make seperate from the main page.
It includes a passcode for the advanced audio settings and projector controls
The passcode runs the same structure as the main page passcode except that it only compares to the hardcoded passcode and not the SFTP passcode

Button definitions follow the same structure as any otherfile and the import statements are mostly the same

The current method of projector control ignores status returned by the projector. 
Rev 1.0.2 will change this to be more similar to the method used in the 3105 or 3201 room. 
That method utilizes the SubscribeStatus() function to affect visual change to a projector on a button press. 
The button in the tlp file will only be its definition and not its control. All control will be in the Control file corresponding to this one
"""

#Extron Imports 
from modules.helper.ModuleSupport import eventEx
from extronlib.system import MESet
from extronlib.ui import Button, Label

from devices import dvTLP, dvPRJ
from variables import ButtonEventList

#advanced settings
btn_advSettings = Button(dvTLP, 47)
@eventEx(btn_advSettings, ButtonEventList)
def ShowAdvancedSettingsPopup(button:Button, state):
    print(button.Name, state)
    if state == 'Pressed':
        button.SetState(1)
        dvTLP.ShowPopup("Advanced Settings")
    elif state == 'Released':
        button.SetState(0)

#Activity Timeout
btn_actTimeout = Button(dvTLP, 155)
btn_actTimeout.SetVisible(False)

""" Projector Control uses a mutual set to make sure only one button gets highlighted when the projector is on or off
    The new revision allows the button definition to set the state of the projector then call the update. Button feedback then 
    will reflect the current state of the projector so if the command didn't work, it's easy to tell the state of the projector
    and press the button again if it didn't stick. It also follows the state of the projector constatly, so if it gets turned on by 
    the user selcting a source, the button will stay consistent. The same method will be used for Blank Image"""
btn_projOn = Button(dvTLP, 24)
btn_projOff = Button(dvTLP, 25)

prj_set = MESet([btn_projOn, btn_projOff])

@eventEx(prj_set.Objects, 'Pressed')
def ProjectorOnOff(button:Button, state):
    print(button, state)
    prj_set.SetCurrent(button)
    if button is btn_projOn:
        dvPRJ.Set('Power', 'On')
    else:
        dvPRJ.Set('Power', 'Off')

btn_blankImg = Button(dvTLP, 21)
@eventEx(btn_blankImg, 'Pressed')
def BlankImage(button:Button, state):
    print(button.Name, state)    
    if button.State == 1:
        button.SetState(0)
        dvPRJ.Set('AVMute', 'Off')
    else:
        button.SetState(1)
        dvPRJ.Set('AVMute', 'On')

""" Technician Access Code takes only 1 password. It again uses a set of buttons with the names 0-9 to append to a string for comparison
    A dictionary could be used with the original button names, but because the names don't need to be unique I can have mutltiple buttons
    with the same name so long as they have distinct ID numbers. The technician passcode is seperate from the main page pascode by a number 
    if ID numbers, meaning it can use the exact same structure but with different variable names.
    
    The Buttons get added to a list. I have two blank strings, one for the comparison and one for the * when a button is pressed. Every button 
    in the list has the same fucntion associated with it. That function appends the button name to the comparison string and appends a * to the 
    print string. It sets the text of the label on the UI then waits for the user to press another button. 
    
    On pressing Clear, the program checks if the comparison string matches the code string. If it does, the page gets swapped and both variables
    get cleared. If it doesn't both variables get cleared but no page is shown. The clear button uses the same method when pressed. Every time 
    enter is pressed, the variables need to be cleared in order for the user to re-attempt if they get it wrong, or enter the code again if 
    they exit back to the main page. 
    
    When exiting advanced settings, the passcode variables get cleared again, just in case the user typed some numbers but didn't press enter 
    or clear. This is just to prevent any possible errors."""
TechButtons = []
for Button_IDs in range(107, 117):
    TechButtons.append(Button(dvTLP, Button_IDs))
    
LblTechString = Label(dvTLP, 20)
techstr = ''
techlblstr = ''

@eventEx(TechButtons, ButtonEventList)
def TechButtonPressed(button:Button, state):
    print(button.Name, state)
    global techstr 
    global techlblstr
    if state == 'Pressed':
        button.SetState(1)
        techstr += button.Name
        techlblstr += '*'
        LblTechString.SetText(techlblstr)
    elif state == 'Released':
        button.SetState(0)

btn_techClear = Button(dvTLP, 117)
@eventEx(btn_techClear, ButtonEventList)
def BtnClearTech(button:Button, state):
    print(button.Name, state)
    global techstr 
    global techlblstr
    if state == 'Pressed':
        button.SetState(1)
        techstr = ''
        techlblstr = ''
        LblTechString.SetText(techlblstr)
    elif state == 'Released':
        button.SetState(0)
        
btn_techEnter = Button(dvTLP, 118)
@eventEx(btn_techEnter, ButtonEventList)
def BtnEnterTech(button:Button, state):
    print(button.Name, state)
    global techstr 
    global techlblstr
    if state == 'Pressed':
        button.SetState(1)
        if techstr == '2748':
            techstr = '' 
            techlblstr = ''
            LblTechString.SetText(techlblstr)
            dvTLP.ShowPopup('Audio Mix popup')
        else:
            techstr = ''
            techlblstr = ''
            LblTechString.SetText(techlblstr)
    elif state == 'Released':
        button.SetState(0)

#Advanced Exit 
btn_advSettingsExit = Button(dvTLP, 56)
@eventEx(btn_advSettingsExit, ButtonEventList)
def ExitAdvancedSettingsPopup(button:Button, state):
    print(button.Name, state)
    if state == 'Pressed':
        global techstr
        global techlblstr
        button.SetState(1)
        techstr = ''
        techlblstr = ''
        LblTechString.SetText(techstr)          #clear the passcode before closing the page so it's empty when the user returns 
        dvTLP.HidePopup("Advanced Settings")
    elif state == 'Released':
        button.SetState(0)
