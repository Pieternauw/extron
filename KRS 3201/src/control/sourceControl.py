from devices import dvMatrix, dvCenterPRJ, dvRightPRJ, dvLeftPRJ, GVEServer, PRJC_ID, PRJL_ID, PRJR_ID

from modules.helper.ModuleSupport import eventEx 
from modules.helper.MirrorUI import Button

from control.advancedControl import PRJLeftTimer, PRJCenterTimer, PRJRightTimer
import ui.tlpSourceSelect as tlp

source_list = ['LAPTOP HDMI', 'WIRELESS', 'INSTALLED PC', 'DOC CAM', 'DOC CAM', 'BLU RAY', 'CAMERA']

@eventEx([tlp.btn_cBoard1, tlp.btn_cBoard2, tlp.btn_cBoard3], 'Pressed')
def CenterBoardSelectInput(button:Button, state):
    output = tlp.center_board_set.Objects.index(button) + 9
    dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.prj_select), 'Tie Type':'Video'})
    dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.monitor_select), 'Tie Type': 'Audio/Video'})
    dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.yuja_select), 'Tie Type':'Audio/Video'})

@eventEx(tlp.input_total_list, ['Pressed'])
def SourceSelection(button:Button, state):
    print(button.Name, button.Host, state)
    #turn on projector corresponding to whichever mode was selected. Can reduce redundancy by comparing to prj_select variable instead of mode variable. 
    if tlp.prj_select == 1:
        output = tlp.left_input_set.Objects.index(button) + 1
        dvLeftPRJ.SetPower('On', None)
        PRJLeftTimer.Restart()
        GVEServer.SendStatus(PRJL_ID, 'Source', source_list[output - 1])
    elif tlp.prj_select == 2:
        output = tlp.center_input_set.Objects.index(button) + 1
        dvCenterPRJ.SetPower('On', None)
        dvCenterPRJ.Update('Power')
        PRJCenterTimer.Restart()
        GVEServer.SendStatus(PRJC_ID, 'Source', source_list[output - 1])
    elif tlp.prj_select == 3:
        output = tlp.right_input_set.Objects.index(button) + 1
        dvRightPRJ.SetPower('On', None)
        dvRightPRJ.Update('Power')
        PRJRightTimer.Restart()
        GVEServer.SendStatus(PRJR_ID, 'Source', source_list[output - 1])

    #left and right board cams special case where input value is the same as yuja value (9 for left and center, 10 for right). can be hardcoded 
    if button in [tlp.btn_lBoardCams, tlp.btn_rBoardCams]:
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(tlp.yuja_select), 'Output': '{}'.format(tlp.prj_select), 'Tie Type': 'Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(tlp.yuja_select), 'Output': '{}'.format(tlp.monitor_select),'Tie Type': 'Audio/Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(tlp.yuja_select), 'Output': '{}'.format(tlp.yuja_select),'Tie Type': 'Audio/Video'})
        #no tie to output 12 since no audio comes through (reduce error chance)
    else:
        #button pressed was not a board camera. This code works for any button left right or center, setting the input to all of the correct projectors and outputs needed to be tied. 
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.prj_select), 'Tie Type':'Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.monitor_select), 'Tie Type': 'Audio/Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.yuja_select), 'Tie Type':'Audio/Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '12', 'Tie Type': 'Audio/Video'})
        #for error prevention, tie yuja output from BluRay to a blank screen. HDCP content is not allowed to Yuja so needs to be not sent. 
        if button in [tlp.btn_cBluray, tlp.btn_lBluray, tlp.btn_rBluray]:
            dvMatrix.SetMatrixTieCommand(None, {'Input': '0', 'Output': '{}'.format(tlp.yuja_select), 'Tie Type': 'Audio/Video'})
        
    


video_mute_list = [tlp.btn_lVideoMute, tlp.btn_cVideoMute, tlp.btn_rVideoMute]
@eventEx(video_mute_list , 'Pressed')
def VideoMuteControl(button:tlp.Button, state):
    print(button.Name, button.Host, state)
    if button.State == 0:
        dvMatrix.SetVideoMute('On', {'Output': '{}'.format(video_mute_list.index(button) + 1)})
        dvMatrix.SetVideoMute('On', {'Output': '9' if button in [tlp.btn_lVideoMute, tlp.btn_cVideoMute] else '10'})
        button.SetState(1)
    else:
        dvMatrix.SetVideoMute('Off', {'Output': '{}'.format(video_mute_list.index(button) + 1)})
        dvMatrix.SetVideoMute('Off', {'Output': '9' if button in [tlp.btn_lVideoMute, tlp.btn_cVideoMute] else '10'})
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

out_tie_dict = {tlp.btn_leftSourceSound: '1', tlp.btn_rightSourceSound: '3'}

@eventEx([tlp.btn_leftSourceSound, tlp.btn_rightSourceSound], 'Pressed')
def SwitchSourceSound(button:Button, state):
    print('Switching Audo Source')
    source = dvMatrix.ReadStatus('OutputTieStatus', {'Output': '{}'.format(out_tie_dict[button]), 'Tie Type': 'Video'})
    print(source)
    dvMatrix.SetMatrixTieCommand(None, {'Input': source, 'Output': '12', 'Tie Type': 'Audio/Video'})
    tlp.btn_leftSourceSound.SetVisible(True)
    tlp.btn_rightSourceSound.SetVisible(True)
    button.SetVisible(False)
    