from devices import dvMatrix, dvCenterPRJ, dvRightPRJ, dvLeftPRJ, dvBiamp, dvTLPMain

from modules.helper.ModuleSupport import eventEx 
from modules.helper.MirrorUI import Button

from extronlib.system import Clock

import ui.tlp as tlp

def StartupAndShutdown():
        #shut off projectors
        #lock cabinet
        #tie matrix and audio outputs
        dvCenterPRJ.SetAVMute('Off', None)
        dvLeftPRJ.SetAVMute('Off', None)
        dvRightPRJ.SetAVMute('Off', None)
        
        dvCenterPRJ.SetPower('Off', None)
        dvRightPRJ.SetPower('Off', None)
        dvLeftPRJ.SetPower('Off', None)
        dvCenterPRJ.Update('Power')
        dvRightPRJ.Update('Power')
        dvLeftPRJ.Update('Power') 

        tlp.tlpSourceSelect.left_input_set.SetCurrent(None)
        tlp.tlpSourceSelect.right_input_set.SetCurrent(None)
        tlp.tlpSourceSelect.center_board_set.SetCurrent(None)
        tlp.tlpSourceSelect.center_input_set.SetCurrent(None)

        tlp.tlpMainPageAudio.lvl_cMic.SetLevel(-18)
        tlp.tlpMainPageAudio.lvl_cProg.SetLevel(-18)
        dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelSpeech', 'Channel': '1'})
        dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelProgram', 'Channel': '1'})
    
        for i in ['1', '2', '3', '4', '5', '12']:
            dvMatrix.SetMatrixTieCommand(None, {'Input': '0', 'Output': i, 'Tie Type': 'Audio/Video'}) 
            
        for j in ['1', '2', '3']:
            dvMatrix.SetVideoMute('Off', {'Output': j})
            
        tlp.tlpSourceSelect.btn_cVideoMute.SetState(0)
        tlp.tlpSourceSelect.btn_lVideoMute.SetState(0)
        tlp.tlpSourceSelect.btn_rVideoMute.SetState(0)
        tlp.tlpSourceSelect.btn_cBoardCams.SetState(0)
        tlp.tlpSourceSelect.btn_lBoardCams.SetState(0)
        tlp.tlpSourceSelect.btn_rBoardCams.SetState(0)
        
        dvMatrix.SetMatrixTieCommand(None, {'Input': '2', 'Output': '9', 'Tie Type': 'Audio/Video'}) #Cynap to YuJa
        dvMatrix.SetMatrixTieCommand(None, {'Input': '2', 'Output': '10', 'Tie Type': 'Audio/Video'}) #Cynap to YuJa
        
        dvTLPMain.HideAllPopups()


@eventEx(tlp.btn_shutdownYes, 'Pressed')
def ShutdownConfirm(button:Button, state):
    print(button.Name, button.Host, state)
    StartupAndShutdown()
    dvMatrix.Set('Relay', 'Open', {'Output': '4', 'Relay': '1'})
    dvTLPMain.ShowPage('Start Page')
        
def ShutdownSystem(clock, dt):
    StartupAndShutdown()
    dvMatrix.Set('Relay', 'Open', {'Output': '4', 'Relay': '1'})
    dvTLPMain.ShowPage('Start Page')

Shutdown = Clock(['23:00:00'], None, ShutdownSystem)
Shutdown.Enable()