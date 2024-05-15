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
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(tlp.yuja_select), 'Output': '{}'.format(tlp.monitor_select), 'Tie Type': 'Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(tlp.yuja_select), 'Output': '{}'.format(tlp.yuja_select), 'Tie Type': 'Audio/Video'})
    elif button in tlp.center_board_set.Objects:
        output = tlp.center_board_set.Objects.index(button) + 9
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.prj_select), 'Tie Type': 'Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.monitor_select), 'Tie Type': 'Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.yuja_select), 'Tie Type': 'Audio/Video'})
    else:
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.prj_select), 'Tie Type': 'Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.monitor_select), 'Tie Type': 'Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.yuja_select), 'Tie Type': 'Audio/Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '12', 'Tie Type': 'Audio/Video'})
        
    if button in [tlp.btn_cBluray, tlp.btn_lBluray, tlp.btn_rBluray]:
        dvMatrix.SetMatrixTieCommand(None, {'Input': '0', 'Output': '{}'.format(tlp.yuja_select), 'Tie Type': 'Audio/Vieo'})

#Video Mute - TODO define left and right buttons 
@eventEx([tlp.btn_cVideoMute] , 'Pressed')
def VideoMuteControl(button:tlp.Button, state):
    print(button.Name, button.Host, state)
    if button.State == 0:
        dvMatrix.SetGlobalVideoMute('On', None)
        tlp.btn_cVideoMute.SetState(1)
        #tlp.btn_lVideoMute.SetState(1)
        #tlp.btn_rVideoMute.SetState(1)
    else:
        dvMatrix.SetGlobalVideoMute('Off', None)
        tlp.btn_cVideoMute.SetState(0)
        #tlp.btn_lVideoMute.SetState(0)
        #tlp.btn_rVideoMute.SetState(0)

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
