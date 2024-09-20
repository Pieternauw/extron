from devices import dvMatrix, dvCenterPRJ, dvRightPRJ, dvLeftPRJ, dvBiamp, dvTLPMain

from modules.helper.ModuleSupport import eventEx 
from modules.helper.MirrorUI import Button

from extronlib.system import Clock

import ui.tlp as tlp

def StartupAndShutdown():
        #shut off projectors
        #lock cabinet
        #tie matrix and audio outputs
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

        dvMatrix.SetMatrixTieCommand(None, {'Input': '2', 'Output': '9', 'Tie Type': 'Video'}) #Cynap to YuJa
        dvMatrix.SetMatrixTieCommand(None, {'Input': '2', 'Output': '10', 'Tie Type': 'Video'}) #Cynap to YuJa

        dvTLPMain.ShowPage('Start Page')
        dvTLPMain.HideAllPopups()

@eventEx(tlp.btn_shutdownYes, 'Pressed')
def ShutdownConfirm(button:Button, state):
    print(button.Name, button.Host, state)
    StartupAndShutdown()
    dvMatrix.Set('Relay', 'Open', {'Output': '4', 'Relay': '1'})
    
        
def ShutdownSystem(clock, dt):
    StartupAndShutdown()

Shutdown = Clock(['23:00:00'], None, ShutdownSystem)
Shutdown.Enable()