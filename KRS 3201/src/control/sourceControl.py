"""
This file takes in the variables assigned values in the previous tlp file and makes all of the matrix tie commands.
The structure is as follows:
1. turn on the correct projector. Update the state for visual feedback in advanced settings. Output variable is the 
corresponding index of the button pressed from within the left right or center set. + 1 is added because index 0 
represents input 1 on the matrix. 
2. If the left or right board cams were selected, tie yuja (9 for left 10 for right) to projector, monitor, and yuja.
Yuja is used because left cam is on input 9 and right is on input 10
3. If the button is one of the center board cam set, add 9 to the index (0 or 1) and tie it to the same things
4. Otherwise it's one of the other inputs. Tie the output assigned to the projector, monitor, yuja, and surround sound
5. Finally, if the button is a bluray button, tie yuja to input 0 to handle errors caused by trying to send HDCP 
content to the yuja device. 

There is also the laptop connected feedback which is a SubscribeStatus() method call following the enpoint status 
of input 1. This changes the button to green and the text to connected when there's a connection made at the 
winder cable. Sub input 1 refers to input 1 on the transmitter box which is where the HDMI cable is plugged in. 
"""

from devices import dvMatrix, dvCenterPRJ, dvRightPRJ, dvLeftPRJ

from modules.helper.ModuleSupport import eventEx 
from modules.helper.MirrorUI import Button

import ui.tlpSourceSelect as tlp

@eventEx(tlp.input_total_list, ['Pressed'])
def SourceSelection(button:Button, state):
    print(button.Name, button.Host, state)
    #turn on projector corresponding to whichever mode was selected. Can reduce redundancy by comparing to prj_select variable instead of mode variable. 
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
    
    #left and right board cams special case where input value is the same as yuja value (9 for left and center, 10 for right). can be hardcoded 
    if button in [tlp.btn_lBoardCams, tlp.btn_rBoardCams]:
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(tlp.yuja_select), 'Output': '{}'.format(tlp.prj_select), 'Tie Type': 'Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(tlp.yuja_select), 'Output': '{}'.format(tlp.monitor_select),'Tie Type': 'Audio/Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(tlp.yuja_select), 'Output': '{}'.format(tlp.yuja_select),'Tie Type': 'Audio/Video'})
        #no tie to output 12 since no audio comes through (reduce error chance)
    elif button in tlp.center_board_set.Objects:
        #center board cams have two buttons for either left or right camera, so button index + 9 (0 + 9, 1 + 9) 
        output = tlp.center_board_set.Objects.index(button) + 9
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.prj_select), 'Tie Type':'Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.monitor_select), 'Tie Type': 'Audio/Video'})
        dvMatrix.SetMatrixTieCommand(None, {'Input': '{}'.format(output), 'Output': '{}'.format(tlp.yuja_select), 'Tie Type':'Audio/Video'})
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

@eventEx([tlp.btn_leftSourceSound, tlp.btn_rightSourceSound], 'Pressed')
def SwitchSourceSound(button:Button, state):
    print('Switching Audo Source')
    if button is tlp.btn_leftSourceSound:
        source = dvMatrix.ReadStatus('OutputTieStatus', {'Output': '1', 'Tie Type': 'Video'})
        print(source)
        dvMatrix.SetMatrixTieCommand(None, {'Input': source, 'Output': '12', 'Tie Type': 'Audio/Video'})
        button.SetVisible(False)
        tlp.btn_rightSourceSound.SetVisible(True)
    else:
        source = dvMatrix.ReadStatus('OutputTieStatus', {'Output': '3', 'Tie Type': 'Video'})
        print(source)
        dvMatrix.SetMatrixTieCommand(None, {'Input': source, 'Output': '12', 'Tie Type': 'Audio/Video'})
        button.SetVisible(False)
        tlp.btn_leftSourceSound.SetVisible(True)