from devices import dvMatrix, dvCenterPRJ, dvRightPRJ, dvLeftPRJ, dvBiamp, dvTLPMain

from modules.helper.ModuleSupport import eventEx 
from modules.helper.MirrorUI import Button, Label
from extronlib.system import File

from extronlib.system import Clock, Wait

from control.advancedControl import PRJLeftTimer, PRJCenterTimer, PRJRightTimer
import ui.tlp as tlp 

def Startup():
    print('Startup running')
    #default audio levels set, turn off mute buttons. Visual feedback handled by SubscribeStatus()
    tlp.tlpMainPageAudio.lvl_cMic.SetLevel(-18)
    tlp.tlpMainPageAudio.lvl_cProg.SetLevel(-18)
    dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelSpeech', 'Channel': '1'})
    dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelProgram', 'Channel': '1'})        
    dvBiamp.SetMuteControl('Off', {'Instance Tag': 'MuteProgram', 'Channel': '1'})
    dvBiamp.Update('MuteControl', {'Instance Tag': 'MuteProgram', 'Channel': '1'})
    dvBiamp.SetMuteControl('Off', {'Instance Tag': 'MuteSpeech', 'Channel': '1'})
    dvBiamp.Update('MuteControl', {'Instance Tag': 'MuteSpeech', 'Channel': '1'})

    dvCenterPRJ.SetAVMute('Off', None)
    tlp.adv.btn_blankImg.SetState(0)
    dvLeftPRJ.SetAVMute('Off', None)
    tlp.adv.btn_lBlankImg.SetState(0)
    dvRightPRJ.SetAVMute('Off', None)
    tlp.adv.btn_rBlankImg.SetState(0)

    for j in ['1', '2', '3', '9', '10']:
        dvMatrix.SetVideoMute('Off', {'Output': j})
        
    tlp.tlpSourceSelect.btn_cVideoMute.SetState(0)
    tlp.tlpSourceSelect.btn_lVideoMute.SetState(0)
    tlp.tlpSourceSelect.btn_rVideoMute.SetState(0)
    
    dvTLPMain.HidePopup('Login')
    
    #No ties for matrix, there might already be ties in place. Plus if they reselect 
    #then ties will be made. 
    #send to room select page and open up the relay drawer
    dvTLPMain.ShowPage('room mode select')
    dvMatrix.Set('Relay', 'Close', {'Output': '4', 'Relay': '1'})
    
def Shutdown():
    #shut off projectors and update buttons with SubscribeStatus()
    dvCenterPRJ.SetAVMute('Off', None)
    tlp.adv.btn_blankImg.SetState(0)
    dvLeftPRJ.SetAVMute('Off', None)
    tlp.adv.btn_lBlankImg.SetState(0)
    dvRightPRJ.SetAVMute('Off', None)
    tlp.adv.btn_rBlankImg.SetState(0)
    
    
    def PRJShutoff():
        dvCenterPRJ.SetPower('Off', None)
        dvRightPRJ.SetPower('Off', None)
        dvLeftPRJ.SetPower('Off', None)
        PRJLeftTimer.Restart()
        PRJCenterTimer.Restart()
        PRJRightTimer.Restart()
    
    PRJ_Shutoff = Wait(2, PRJShutoff)
    
    #set source buttons to all be deselected
    tlp.tlpSourceSelect.left_input_set.SetCurrent(None)
    tlp.tlpSourceSelect.right_input_set.SetCurrent(None)
    tlp.tlpSourceSelect.center_board_set.SetCurrent(None)
    tlp.tlpSourceSelect.center_input_set.SetCurrent(None)
    tlp.tlpSourceSelect.btn_cBoardCams.SetState(0)

    #default audio levels set, turn off mute buttons. Visual feedback handled by SubscribeStatus()
    tlp.tlpMainPageAudio.lvl_cMic.SetLevel(-18)
    tlp.tlpMainPageAudio.lvl_cProg.SetLevel(-18)
    dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelSpeech', 'Channel': '1'})
    dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelProgram', 'Channel': '1'})        
    dvBiamp.SetMuteControl('Off', {'Instance Tag': 'MuteProgram', 'Channel': '1'})
    dvBiamp.Update('MuteControl', {'Instance Tag': 'MuteProgram', 'Channel': '1'})
    dvBiamp.SetMuteControl('Off', {'Instance Tag': 'MuteSpeech', 'Channel': '1'})
    dvBiamp.Update('MuteControl', {'Instance Tag': 'MuteSpeech', 'Channel': '1'})
    
    #Tie all outputs to 0 except Yuja, handled lower (ties to cynap)
    for i in ['1', '2', '3', '4', '5', '12']:
        dvMatrix.SetMatrixTieCommand(None, {'Input': '0', 'Output': i, 'Tie Type': 'Audio/Video'}) 
    
    for j in ['1', '2', '3', '9', '10']:
            dvMatrix.SetVideoMute('Off', {'Output': j})
    tlp.tlpSourceSelect.btn_cVideoMute.SetState(0)
    tlp.tlpSourceSelect.btn_lVideoMute.SetState(0)
    tlp.tlpSourceSelect.btn_rVideoMute.SetState(0)
    
    dvMatrix.SetMatrixTieCommand(None, {'Input': '2', 'Output': '9', 'Tie Type': 'Audio/Video'}) #Cynap to YuJa
    dvMatrix.SetMatrixTieCommand(None, {'Input': '2', 'Output': '10', 'Tie Type': 'Audio/Video'}) #Cynap to YuJa
    
    #Show the start page and lock the drawer. Hides popups
    dvTLPMain.ShowPage('Start Page')
    dvMatrix.Set('Relay', 'Open', {'Output': '4', 'Relay': '1'})
    dvTLPMain.HideAllPopups()

@eventEx(tlp.btn_shutdownYes, 'Pressed')
def ShutdownConfirm(button:Button, state):
    print(button.Name, button.Host, state)
    Shutdown()
    
        
def ShutdownSystem(clock, dt):
    Shutdown()

ShutdownClock = Clock(['23:00:00'], None, ShutdownSystem)
ShutdownClock.Enable()

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
btn_passcodeEnter = Button(dvTLPMain, 152)
btn_passcodeClear = Button(dvTLPMain, 151)
@eventEx([btn_passcodeEnter, btn_passcodeClear], ['Pressed', 'Released'])
def BtnEnterPasscode(button:Button, state):
    print(button.Name, state)
    global PadString 
    button.SetState(1 if state is 'Pressed' else 0)
    if (button is btn_passcodeEnter) and ((PadString == '2748') or (PadString == passcode)):      #whatever the current passcode is
        print('startup running')
        dvTLPMain.ShowPopup('Login')
        StartupWait = Wait(1, Startup)
    clear_code()
        
btn_passcodeCancel = Button(dvTLPMain, 153)
@eventEx(btn_passcodeCancel, ['Pressed', 'Released'])
def CancelPasscode(button:Button, state):
    print(button.Name, state)
    clear_code()
    button.SetState(1 if state is 'Pressed' else 0)
    dvTLPMain.ShowPage('Start Page')
    