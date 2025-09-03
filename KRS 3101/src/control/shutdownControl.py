from devices import dvScalar, dvPRJ, dvTLP, dvRelay, GVEServer, PRJ_ID, dvCynap

from modules.helper.ModuleSupport import eventEx 

from extronlib.system import Clock, Wait
from extronlib.ui import Button, Label
from extronlib.system import File

import ui.tlp as tlp

def SharedCommands():
    dvPRJ.SetAVMute('Off', None)
    tlp.adv.btn_blankImg.SetState(0)
    
    tlp.MainAudio.lvl_mic.SetLevel(-18)
    tlp.MainAudio.lvl_prog.SetLevel(-18)
    dvScalar.SetGroupProgramVolume(-18, None)
    dvScalar.SetGroupMicVolume(-18, None)
    
    dvScalar.SetGlobalVideoMute('Off', None)
    tlp.btn_videoMute.SetState(0)   
    
def Startup():
    SharedCommands()
    #turn off mic and program mutes
    #visual feedback handled by SubscribeStatus()
    dvScalar.SetGroupProgramMute('Off', None)
    dvScalar.SetGroupMicMute('Off', None)
    print(dvScalar.ReadStatus('GroupProgramMute')) 
    
    dvTLP.HidePopup('Login')
    
    #main page shown, function called after successful passcode entry
    dvTLP.ShowPage('Main Page')
    #unlock drawer
    dvRelay.SetState('Close')
    
def Shutdown():
    SharedCommands()
    
    dvPRJ.SetPower('Off', None)
    dvPRJ.Update('Power')
    
    dvCynap.Set('EndPresentation', None, {'Deete Recordings Folder': 'Yes', 'Delete Snapshots Folder': 'Yes', 'Power Off Mode': 'New Presentation'})
        
    tlp.input_set.SetCurrent(None)
    dvScalar.SetInput('3', {'Type': 'Audio/Video'})
    GVEServer.SendStatus(PRJ_ID, 'Source', 'SYSTEM OFF')
    
    dvTLP.HideAllPopups()
    dvTLP.ShowPage('Start Page')
    dvRelay.SetState('Open')
    
@eventEx(tlp.btn_shdnYes, 'Pressed')
def ShutdownControl(button:tlp.Button, state):
    Shutdown()
    
def ShutdownSystem(clock, dt):
    Shutdown()
    
ShutdownClock = Clock(['23:00:00'], None, ShutdownSystem)
ShutdownClock.Enable()

btn_startScreen = Button(dvTLP, 19)

@eventEx(btn_startScreen, 'Pressed')
def ShowStartPage(button:Button, state):
    print(button.Name, state)
    dvTLP.ShowPage("Main passcode")
    #may want to auto this to the main page if I can't get the passcode going before deployment

"""PASSCODE SCREEN"""

"""TODO - Cancel Button needs to be added"""

#port 22022 in cyberduck
passcodeFile = File('user/passcode.txt', 'r')
passcode = str(passcodeFile.readline())

PadButtons = []
for Button_IDs in range(141, 151):
    PadButtons.append(Button(dvTLP, Button_IDs))
    
LblPadString = Label(dvTLP, 140)
LblString = ''
PadString = ''

def clear_code():
    global PadString
    global LblString
    PadString = ''
    LblString = ''
    LblPadString.SetText(LblString)

@eventEx(PadButtons, ['Pressed', 'Released'])
def PadButtonPressed(button:Button, state):
    button.SetState(1 if state is 'Pressed' else 0)
    if state is 'Pressed':
        print(button.Name, state, "Control")
        global PadString 
        global LblString
        PadString += button.Name
        LblString += '*'
        LblPadString.SetText(LblString)
    
#enter and clear
btn_passcodeEnter = Button(dvTLP, 152)
btn_passcodeClear = Button(dvTLP, 151)
@eventEx([btn_passcodeEnter, btn_passcodeClear], ['Pressed', 'Released'])
def BtnEnterPasscode(button:Button, state):
    print(button.Name, state)
    global PadString 
    button.SetState(1 if state is 'Pressed' else 0)
    if (button is btn_passcodeEnter) and ((PadString == '2748') or (PadString == passcode)):      #whatever the current passcode is
        print('startup running')
        dvTLP.ShowPopup('Login')
        StartupWait = Wait(3, Startup)
    clear_code()
        
btn_passcodeCancel = Button(dvTLP, 153)
@eventEx(btn_passcodeCancel, ['Pressed', 'Released'])
def CancelPasscode(button:Button, state):
    print(button.Name, state)
    clear_code()
    button.SetState(1 if state is 'Pressed' else 0)
    dvTLP.ShowPage('Start Page')