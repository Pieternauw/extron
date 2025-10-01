from devices import dvMatrix, dvBiamp, dvTLPMain, dvCenterPRJ, dvRightPRJ, dvLeftPRJ, GVEServer, dvCynap, PRJC_ID, PRJL_ID, PRJR_ID # , dvBluray
from control.advancedControl import PRJCenterTimer, PRJLeftTimer, PRJRightTimer

from modules.helper.ModuleSupport import eventEx 
from modules.helper.MirrorUI import Button, Label
from extronlib.system import File

from extronlib.system import Clock, Wait

import ui.tlp as tlp

def DefaultCalls():
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
    
    tlp.tlpSourceSelect.left_input_set.SetCurrent(None)
    tlp.tlpSourceSelect.right_input_set.SetCurrent(None)
    tlp.tlpSourceSelect.center_board_set.SetCurrent(None)
    tlp.tlpSourceSelect.center_input_set.SetCurrent(None)
    tlp.tlpSourceSelect.btn_cBoardCams.SetState(0)

def Startup():
    DefaultCalls()
    
    print('Startup running')
    #default audio levels set, turn off mute buttons. Visual feedback handled by SubscribeStatus()
    
    dvTLPMain.HidePopup('Login')
    
    #No ties for matrix, there might already be ties in place. Plus if they reselect 
    #then ties will be made. 
    #send to room select page and open up the relay drawer
    dvTLPMain.ShowPage('room mode select')
    dvMatrix.Set('Relay', 'Close', {'Output': '4', 'Relay': '1'})
    
def Shutdown(): 
    DefaultCalls()
    
    def PRJShutoff():
        dvCenterPRJ.SetPower('Off', None)
        dvRightPRJ.SetPower('Off', None)
        dvLeftPRJ.SetPower('Off', None)
    
        PRJCenterTimer.Restart()
        PRJRightTimer.Restart()
        PRJLeftTimer.Restart()
        
    PRJ_Shutoff = Wait(2, PRJShutoff)

    dvCynap.Set('EndPresentation', None, {'Delete Recordings Folder': 'Yes', 'Delete Snapshots Folder': 'Yes', 'Power Off Mode': 'New Presentation'})

    #Tie all outputs to 0 except Yuja, handled lower (ties to cynap)
    for i in ['1', '2', '3', '4', '5', '12']:
        dvMatrix.SetMatrixTieCommand(None, {'Input': '0', 'Output': i, 'Tie Type': 'Audio/Video'}) 
    
    dvMatrix.SetMatrixTieCommand(None, {'Input': '2', 'Output': '9', 'Tie Type': 'Audio/Video'}) #Cynap to YuJa
    dvMatrix.SetMatrixTieCommand(None, {'Input': '2', 'Output': '10', 'Tie Type': 'Audio/Video'}) #Cynap to YuJa
    
    GVEServer.SendStatus(PRJC_ID, 'Source', 'SYSTEM OFF')
    GVEServer.SendStatus(PRJL_ID, 'Source', 'SYSTEM OFF')
    GVEServer.SendStatus(PRJR_ID, 'Source', 'SYSTEM OFF')
    
    #Show the start page and lock the drawer. Hides popups
    dvTLPMain.ShowPage('Start Page')
    dvMatrix.Set('Relay', 'Open', {'Output': '4', 'Relay': '1'})
    dvTLPMain.HideAllPopups()
    # dvBluray.Set('Power', 'Off')

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

passcodeFile = File('user/passcode.txt', 'r')
passcode = str(passcodeFile.readline())
print('passcode', passcode)

PadButtons = []
for Button_IDs in range(141, 151):
    PadButtons.append(Button(dvTLPMain, Button_IDs))
    
LblPadString = Label(dvTLPMain, 140)
LblString = PadString = ''
def clear_code():
    global PadString, LblString
    PadString = LblString = ''
    LblPadString.SetText(LblString)

@eventEx(PadButtons, ['Pressed', 'Released'])
def PadButtonPressed(button:Button, state):
    button.SetState(1 if state is 'Pressed' else 0)
    if state is 'Pressed':
        print(button.Name, state, "Control")
        global PadString, LblString
        PadString += button.Name
        LblString += '*'
        LblPadString.SetText(LblString)

#enter and clear
btn_passcodeEnter = Button(dvTLPMain, 152)
btn_passcodeClear = Button(dvTLPMain, 151)
btn_passcodeCancel = Button(dvTLPMain, 153)
@eventEx([btn_passcodeEnter, btn_passcodeClear, btn_passcodeCancel], ['Pressed', 'Released'])
def BtnEnterPasscode(button:Button, state):
    print(button.Name, state)
    global PadString 
    button.SetState(1 if state is 'Pressed' else 0)
    if (button is btn_passcodeEnter) and ((PadString == '2748') or (PadString == passcode)):      #whatever the current passcode is
        print('startup running')
        dvTLPMain.ShowPopup('Login')
        StartupWait = Wait(1, Startup)
    elif (button is btn_passcodeCancel):
        dvTLPMain.ShowPage('Start Page')
    clear_code()
