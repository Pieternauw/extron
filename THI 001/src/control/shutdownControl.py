from devices import dvScalar, dvPRJ, dvTLP, dvRelay, dvBiamp

from modules.helper.ModuleSupport import eventEx 

from extronlib.system import Clock, Wait
from extronlib.ui import Button, Label
from extronlib.system import File

import ui.tlp as tlp

def Startup():
    print('Startup running')
    #set input set to nothing
    #Don't set scalar b/c instructor might be displaying something we want to keep up while system starts up 
    dvPRJ.SetAVMute('Off', None)
    tlp.adv.btn_blankImg.SetState(0)
    
    #set default mic and prog volume levels
    tlp.MainAudio.lvl_mic.SetLevel(-18)
    tlp.MainAudio.lvl_prog.SetLevel(-18)
    dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelSpeech', 'Channel': '1'})
    dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelProgram', 'Channel': '1'})        
    dvBiamp.SetMuteControl('Off', {'Instance Tag': 'MuteProgram', 'Channel': '1'})
    dvBiamp.Update('MuteControl', {'Instance Tag': 'MuteProgram', 'Channel': '1'})
    dvBiamp.SetMuteControl('Off', {'Instance Tag': 'MuteSpeech', 'Channel': '1'})
    dvBiamp.Update('MuteControl', {'Instance Tag': 'MuteSpeech', 'Channel': '1'})    
    
    #turn off video mute
    dvScalar.SetVideoMute('Off', {'Output': '1A'})
    dvScalar.SetVideoMute('Off', {'Output': '1B'})
    dvScalar.SetVideoMute('Off', {'Output': 'Loop Out'})
    tlp.btn_videoMute.SetState(0)   

    dvPRJ.SetAVMute('Off', None)
    tlp.adv.btn_blankImg.SetState(0)
    
    #main page shown, function called after successful passcode entry
    #TODO - make this center page from dual popup
    dvTLP.ShowPage('C Projection')
    #unlock drawer
    dvRelay.SetState('Close')
    
def Shutdown():
    dvPRJ.SetAVMute('Off', None)
    dvPRJ.SetPower('Off', None)
    dvPRJ.Update('Power')

    tlp.adv.btn_blankImg.SetState(0)
        
    tlp.input_set.SetCurrent(None)
    dvScalar.SetInput('3', {'Type': 'Audio/Video'})
    tlp.wireless_btn_help_set.SetCurrent(None)
    
    tlp.MainAudio.lvl_mic.SetLevel(-18)
    tlp.MainAudio.lvl_prog.SetLevel(-18)
    
    dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelSpeech', 'Channel': '1'})
    dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelProgram', 'Channel': '1'})        
    dvBiamp.SetMuteControl('Off', {'Instance Tag': 'MuteProgram', 'Channel': '1'})
    dvBiamp.Update('MuteControl', {'Instance Tag': 'MuteProgram', 'Channel': '1'})
    dvBiamp.SetMuteControl('Off', {'Instance Tag': 'MuteSpeech', 'Channel': '1'})
    dvBiamp.Update('MuteControl', {'Instance Tag': 'MuteSpeech', 'Channel': '1'})
    
    dvScalar.SetVideoMute('On', {'Output': '1A'})
    dvScalar.SetVideoMute('Off', {'Output': '1B'})
    dvScalar.SetVideoMute('On', {'Output': 'Loop Out'})
    tlp.btn_videoMute.SetState(0)   
    
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

@eventEx(PadButtons, ['Pressed', 'Released'])
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
@eventEx(btn_passcodeEnter, ['Pressed', 'Released'])
def BtnEnterPasscode(button:Button, state):
    print(button.Name, state)
    global PadString 
    global LblString
    if state == 'Pressed':
        button.SetState(1)
        if (PadString == '2748') or (PadString == passcode):      #whatever the current passcode is
            dvTLP.ShowPopup('Login')
            StartupWait = Wait(1, Startup)
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
        
btn_passcodeCancel = Button(dvTLP, 153)
@eventEx(btn_passcodeCancel, ['Pressed', 'Released'])
def CancelPasscode(button:Button, state):
    print(button.Name, state)
    global PadString, LblString
    PadString = LblString = ''
    if state == 'Pressed': LblPadString.SetText('')
    button.SetState(1 if 'Pressed' else 0)
    dvTLP.ShowPage('Start Page')