from devices import dvMatrix, dvCenterPRJ, dvRightPRJ, dvLeftPRJ

from modules.helper.ModuleSupport import eventEx 
from modules.helper.MirrorUI import Button

import ui.tlpSourceSelect as tlp

@eventEx(tlp.input_total_list, ['Pressed'])
def SourceSelection(button:Button, state):
    print(button.Name, button.Host, state)
    if tlp.mode == 'Center':
        output = tlp.center_input_set.Objects.index(button) + 1
        dvCenterPRJ.SetPower('On', None)
        dvCenterPRJ.Update('Power')
    elif tlp.mode == 'Left':
        output = tlp.left_input_set.Objects.index(button) + 1
        dvLeftPRJ.SetPower('On', None)
        dvLeftPRJ.Update('Power')
    elif tlp.mode == 'Right':
        output = tlp.right_input_set.Objects.index(button) + 1
        dvRightPRJ.SetPower('On', None)
        dvRightPRJ.Update('Power')
    
    if button in [tlp.btn_lBoardCams, tlp.btn_rBoardCams]:
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(tlp.yuja_select), 'Output': '{}'.format(tlp.prj_select), 'Tie Type': 'Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(tlp.yuja_select), 'Output': '{}'.format(tlp.monitor_select), 'Tie Type': 'Audio/Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(tlp.yuja_select), 'Output': '{}'.format(tlp.yuja_select), 'Tie Type': 'Audio/Video'})
    elif button in tlp.center_board_set.Objects:
        output = tlp.center_board_set.Objects.index(button) + 9
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.prj_select), 'Tie Type': 'Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.monitor_select), 'Tie Type': 'Audio/Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.yuja_select), 'Tie Type': 'Audio/Video'})
    else:
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.prj_select), 'Tie Type': 'Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.monitor_select), 'Tie Type': 'Audio/Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.yuja_select), 'Tie Type': 'Audio/Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '12', 'Tie Type': 'Audio/Video'})
        
    if button in [tlp.btn_cBluray, tlp.btn_lBluray, tlp.btn_rBluray]:
        dvMatrix.SetMatrixTieCommand(None, {'Input': '0', 'Output': '{}'.format(tlp.yuja_select), 'Tie Type': 'Audio/Vieo'})

#Video Mute - TODO define left and right buttons 
video_mute_list = [tlp.btn_lVideoMute, tlp.btn_cVideoMute, tlp.btn_rVideoMute]
@eventEx(video_mute_list , 'Pressed')
def VideoMuteControl(button:tlp.Button, state):
    print(button.Name, button.Host, state)
    if button.State == 0:
        dvMatrix.SetVideoMute('On', {'Output': '{}'.format(video_mute_list.index(button) + 1)})
        button.SetState(1)
    else:
        dvMatrix.SetVideoMute('Off', {'Output': '{}'.format(video_mute_list.index(button) + 1)})
        button.SetState(0)

#Laptop Feedback
def LaptopConnectedFeedback(command, value, qualifier):
    print(command, value, qualifier)
    if value == 'Active':
        tlp.btn_laptopConnectedFeedback.SetState(1)
        tlp.lblLaptopConnected.SetText('Connected')
    else:
        tlp.btn_laptopConnectedFeedback.SetState(0)
        tlp.lblLaptopConnected.SetText('Not Connected')
    
dvMatrix.SubscribeStatus('InputSignalStatusEndpoint', {'Input': '1', 'Sub Input': '1'}, LaptopConnectedFeedback)

@eventEx([tlp.btn_leftSourceSound, tlp.btn_rightSourceSound], 'Pressed')
def SwitchSourceSound(button:Button, state):
    print('Switching Audo Source')
    if button is tlp.btn_leftSourceSound:
        source = dvMatrix.ReadStatus('OutputTieStatus', {'Output': '1', 'Tie Type': 'Video'})
        print(source)
        dvMatrix.SetMatrixTieCommand(None, {'Input': source, 'Output': '12', 'Tie Type': 'Audio'})
        button.SetVisible(False)
        tlp.btn_rightSourceSound.SetVisible(True)
    else:
        source = dvMatrix.ReadStatus('OutputTieStatus', {'Output': '3', 'Tie Type': 'Video'})
        print(source)
        dvMatrix.SetMatrixTieCommand(None, {'Input': source, 'Output': '12', 'Tie Type': 'Audio'})
        button.SetVisible(False)
        tlp.btn_leftSourceSound.SetVisible(True)