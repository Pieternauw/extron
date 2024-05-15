from devices import dvTLPMain
from modules.helper.ModuleSupport import eventEx
from modules.helper.MirrorUI import Button, Label

from extronlib.system import MESet

BTNEVL = ['Pressed', 'Released', 'Tapped', 'Held']

"""Center Sets"""
btn_cHDMI = Button(dvTLPMain, 247)
btn_cWireless = Button(dvTLPMain, 250)
btn_cMac = Button(dvTLPMain, 253)
btn_cBluray = Button(dvTLPMain, 248)
btn_cDoc1 = Button(dvTLPMain, 249)
btn_cDoc2 = Button(dvTLPMain, 252)
btn_cBoardCams = Button(dvTLPMain, 254)

center_input_set = MESet([btn_cHDMI, btn_cWireless, btn_cMac, btn_cDoc1, btn_cDoc2, btn_cBluray])
for button in center_input_set.Objects:
    center_input_set.SetStates(button, 0, 1)
    
center_input_set.SetCurrent(None)

"""Left Sets"""
btn_lHDMI = Button(dvTLPMain, 229)
btn_lWireless = Button(dvTLPMain, 232)
btn_lMac = Button(dvTLPMain, 258)
btn_lBluray = Button(dvTLPMain, 230)
btn_lDocCam1 = Button(dvTLPMain, 231)
btn_lDocCam2 = Button(dvTLPMain, 257)
btn_lBoardCams = Button(dvTLPMain, 266)

left_input_set = MESet([btn_lHDMI, btn_lWireless, btn_lMac, btn_lDocCam1, btn_lDocCam2, btn_lBluray, btn_lBoardCams])

for button in left_input_set.Objects:
    left_input_set.SetStates(button, 0, 1)

left_input_set.SetCurrent(None)

"""Right Sets"""
btn_rHDMI = Button(dvTLPMain, 259)
btn_rWireless = Button(dvTLPMain, 262)
btn_rMac = Button(dvTLPMain, 265)
btn_rBluray = Button(dvTLPMain, 260)
btn_rDocCam1 = Button(dvTLPMain, 261)
btn_rDocCam2 = Button(dvTLPMain, 264)
btn_rBoardCams = Button(dvTLPMain, 267)

right_input_set = MESet([btn_rHDMI, btn_rWireless, btn_rMac, btn_rDocCam1, btn_rDocCam2, btn_rBluray, btn_rBoardCams])

for button in right_input_set.Objects:
    right_input_set.SetStates(button, 0, 1)

right_input_set.SetCurrent(None)

"""NOTE buttons aren't used so commented out for now until I know if they're needed"""
#Center Board Camera

btn_cBoard1 = Button(dvTLPMain, 186)
btn_cBoard2 = Button(dvTLPMain, 185)
btn_cBoard3 = Button(dvTLPMain, 184)
btn_cBoard3.SetVisible(False)

center_board_set = MESet([btn_cBoard1, btn_cBoard2, btn_cBoard3])

for button in center_board_set.Objects:
    center_board_set.SetStates(button, 0, 1)

center_board_set.SetCurrent(None)
    
"""
#Left Board Cams 

btn_lBoard1 = Button(dvTLPMain, 207)
btn_lBoard2 = Button(dvTLPMain, 205)
btn_lBoard3 = Button(dvTLPMain, 201)

left_board_set = MESet([btn_lBoard1, btn_lBoard2, btn_lBoard3])

for button in left_board_set.Objects:
    left_board_set.SetStates(button, 0, 1)

left_board_set.SetCurrent(None)

#Right Board Cams

btn_rBoard1 = Button(dvTLPMain, 204)
btn_rBoard2 = Button(dvTLPMain, 203)
btn_rBoard3 = Button(dvTLPMain, 202)

right_board_set = MESet([btn_rBoard1, btn_rBoard2, btn_rBoard3])

for button in right_board_set.Objects:
    right_board_set.SetStates(button, 0, 1)

right_board_set.SetCurrent(None)
"""

"""Video Mute"""    
btn_cVideoMute = Button(dvTLPMain, 255)

"""NOTE Laptop Feedback"""
btn_laptopConnectedFeedback = Button(dvTLPMain, 23)
lblLaptopConnected = Label(dvTLPMain, 133)


"""Global variables for matrix tie commands"""
prj_select = 2
monitor_select = 4
yuja_select = 9
mode = 'Center'

#TODO check names
popup_list = ['Laptop Connected popup', 'Wireless instruction popup', 'Installed mac', 
              'Document camera instruction popup', 'Document camera instruction popup', 
              'BluRay control popup']

input_total_list = [btn_cHDMI, btn_cWireless, btn_cMac, btn_cBluray, btn_cDoc1, btn_cDoc2, 
                    btn_lHDMI, btn_lWireless, btn_lMac, btn_lDocCam1, btn_lDocCam2, btn_lBluray, btn_lBoardCams, 
                    btn_rHDMI, btn_rWireless, btn_rMac, btn_rBluray, btn_rDocCam1, btn_rDocCam2, btn_rBoardCams, 
                    btn_cBoard1, btn_cBoard2, btn_cBoard3]

#TODO - Check MatrixTieeventEx call for list 
@eventEx(input_total_list, 'Pressed')
def SwitchInput(button:Button, state):
    global prj_select, monitor_select, yuja_select, mode
    print(button.Name, button.Host, state)
    dvTLPMain.HideAllPopups()
    btn_cBoardCams.SetState(0)
    if button in [btn_cWireless, btn_lWireless, btn_rWireless]:
        dvTLPMain.ShowPopup('Wireless select device')
    
    if button in center_input_set.Objects:
        prj_select = 2
        monitor_select = 4
        yuja_select = 9
        mode = 'Center'
        dvTLPMain.ShowPopup(popup_list[center_input_set.Objects.index(button)])
        center_input_set.SetCurrent(button)
    elif button is btn_cBoardCams:
        prj_select = 2; monitor_select = 4; yuja_select = 9; mode = 'Center'
        dvTLPMain.ShowPopup('Center board camera selection')
        button.SetState(1)
    elif button in left_input_set.Objects:
        prj_select = 1
        monitor_select = 4
        yuja_select = 9
        mode = 'Left'
        dvTLPMain.ShowPopup(popup_list[left_input_set.Objects.index(button)])
        left_input_set.SetCurrent(button)

    elif button in right_input_set.Objects:
        prj_select = 3
        monitor_select = 5
        yuja_select = 10
        mode = 'Right'  
        dvTLPMain.ShowPopup(popup_list[right_input_set.Objects.index(button)])
        right_input_set.SetCurrent(button)
        