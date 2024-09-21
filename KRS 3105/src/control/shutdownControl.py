from devices import dvMatrix, dvCenterPRJ, dvRightPRJ, dvLeftPRJ, dvBiamp, dvTLPMain

from modules.helper.ModuleSupport import eventEx 
from modules.helper.MirrorUI import Button

from extronlib.system import Clock

import ui.tlp as tlp

def Startup():
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
    
    #No ties for matrix, there might already be ties in place. Plus if they reselect 
    #then ties will be made. 
    #send to room select page and open up the relay drawer
    dvTLPMain.ShowPage('room mode select')
    dvMatrix.Set('Relay', 'Close', {'Output': '4', 'Relay': '1'})
    
def Shutdown():
    #shut off projectors and update buttons with SubscribeStatus()
    dvCenterPRJ.SetAVMute('Off', None)
    dvLeftPRJ.SetAVMute('Off', None)
    dvRightPRJ.SetAVMute('Off', None)
    
    dvCenterPRJ.SetPower('Off', None)
    dvRightPRJ.SetPower('Off', None)
    dvLeftPRJ.SetPower('Off', None)
    
    dvCenterPRJ.Update('Power')
    dvRightPRJ.Update('Power')
    dvLeftPRJ.Update('Power') 
    
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
    
    for j in ['1', '2', '3']:
            dvMatrix.SetVideoMute('Off', {'Output': j})
    
    dvMatrix.SetMatrixTieCommand(None, {'Input': '2', 'Output': '9', 'Tie Type': 'Video'}) #Cynap to YuJa
    dvMatrix.SetMatrixTieCommand(None, {'Input': '2', 'Output': '10', 'Tie Type': 'Video'}) #Cynap to YuJa
    
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

Shutdown = Clock(['23:00:00'], None, ShutdownSystem)
Shutdown.Enable()