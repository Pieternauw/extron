from devices import dvMatrix, dvCenterPRJ, dvRightPRJ, dvLeftPRJ, dvBiamp, dvTLPMain

from modules.helper.ModuleSupport import eventEx 
from modules.helper.MirrorUI import Button

from extronlib.system import Clock

import ui.tlp as tlp

@eventEx(tlp.btn_shutdownYes, 'Pressed')
def ShutdownConfirm(button:Button, state):
    print(button.Name, button.Host, state)
    if state == 'Pressed':
        #shut off projectors
        #shut off receivers
        #lock cabinet
        button.SetState(1)
        dvCenterPRJ.SetPower('Off', None)
        dvRightPRJ.SetPower('Off', None)
        dvLeftPRJ.SetPower('Off', None)
        dvCenterPRJ.Update('Power')
        dvRightPRJ.Update('Power')
        dvLeftPRJ.Update('Power') 
        
        dvMatrix.Set('Relay', 'Open', {'Output': '4', 'Relay': '1'})

        tlp.tlpSourceSelect.left_input_set.SetCurrent(None)
        tlp.tlpSourceSelect.right_input_set.SetCurrent(None)
        tlp.tlpSourceSelect.center_board_set.SetCurrent(None)
        tlp.tlpSourceSelect.center_input_set.SetCurrent(None)

        tlp.tlpMainPageAudio.lvl_cMic.SetLevel(-18)
        tlp.tlpMainPageAudio.lvl_cProg.SetLevel(-18)
        dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelSpeech', 'Channel': '1'})
        dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelProgram', 'Channel': '1'})
        
        dvMatrix.SetMatrixTieCommand(None, {'Input': '3', 'Output': '9', 'Tie Type': 'Audio/Video'}) #Cynap

        for i in ['1', '2', '3', '4', '5', '12']:
            dvMatrix.SetMatrixTieCommand(None, {'Input': '0', 'Output': i, 'Tie Type': 'Audio/Video'}) 

        dvTLPMain.ShowPage('Start Page')
        dvTLPMain.HideAllPopups()
        
def ShutdownSystem(clock, dt):
    
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

    dvMatrix.Set('Relay', 'Open', {'Output': '4', 'Relay': '1'})

    tlp.tlpMainPageAudio.lvl_cMic.SetLevel(-18)
    tlp.tlpMainPageAudio.lvl_cProg.SetLevel(-18)
    dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelSpeech', 'Channel': '1'})
    dvBiamp.SetLevelControl(-18, {'Instance Tag': 'LevelProgram', 'Channel': '1'})
        
    dvMatrix.SetMatrixTieCommand(None, {'Input': '3', 'Output': '9', 'Tie Type': 'Audio/Video'}) #Cynap
    
    for i in ['1', '2', '3', '4', '5', '12']:
        dvMatrix.SetMatrixTieCommand(None, {'Input': '0', 'Output': i, 'Tie Type': 'Audio/Video'}) 

    dvTLPMain.ShowPage('Start Page')
    dvTLPMain.HideAllPopups()

Shutdown = Clock(['23:00:00'], None, ShutdownSystem)
Shutdown.Enable()