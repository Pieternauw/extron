"""
This file contains the control for the advanced settings page. Included are the instructions to the projectors 
for when the on or off button is pressed. These buttons utilize the subscribe status method to stay consistent with
the projector's power state. They are initialized with the current state at device connection via the readstatus() 
method call after their definitions. When any power command is sent (either on or off here, or on in the source 
selection page) the power status is updated using the update('power') this causes the subscribe status method 
to be activated and keeps the buttons consistent with th eactual status.

AV Mute uses a similar method but the only thing that changes the states is the advance settings blank image button. 
"""

from devices import dvCenterPRJ, dvRightPRJ, dvLeftPRJ, GVEServer, PRJL_ID, PRJC_ID, PRJR_ID

import ui.tlpAdvanced as tlp

from extronlib.system import MESet, Timer

from modules.helper.MirrorUI import Button
from modules.helper.ModuleSupport import eventEx 


prj_set = MESet([tlp.btn_projOn, tlp.btn_projOff])
prj_set.SetCurrent(tlp.btn_projOn if dvCenterPRJ.ReadStatus('Power') is 'On' else tlp.btn_projOff)

l_prj_set = MESet([tlp.btn_lPrjOn, tlp.btn_lPrjOff])
l_prj_set.SetCurrent(tlp.btn_lPrjOn if dvLeftPRJ.ReadStatus('Power') is 'On' else tlp.btn_lPrjOff)

r_prj_set = MESet([tlp.btn_rPrjOn, tlp.btn_rPrjOff])
r_prj_set.SetCurrent(tlp.btn_rPrjOn if dvRightPRJ.ReadStatus('Power') is 'On' else tlp.btn_rPrjOff)

def CenterPowerChanged(command, value, qualifier):
    GVEServer.SendStatus(PRJC_ID, 'Power', value)
    if value is 'On' or value is 'Off':
        prj_set.SetCurrent(tlp.btn_projOn if value == 'On' else tlp.btn_projOff)
        CenterPRJTimer.Stop()
    else:
        tlp.btn_projOn.SetBlinking('Medium', [0, 1])
        tlp.btn_projOff.SetState(0)
        CenterPRJTimer.Restart()

def CenterTimer(timer:Timer, count):
    print("Center Timer started")
    dvCenterPRJ.Update('Power')

CenterPRJTimer = Timer(5, CenterTimer)
CenterPRJTimer.Stop()

dvCenterPRJ.SubscribeStatus('Power', None, CenterPowerChanged)

def LeftPowerChanged(command, value, qualifier):
    GVEServer.SendStatus(PRJL_ID, 'Power', value)
    if value is 'On' or value is 'Off':
        l_prj_set.SetCurrent(tlp.btn_lPrjOn if value == 'On' else tlp.btn_lPrjOff)
        LeftPRJTimer.Stop()
        
    else:
        tlp.btn_lPrjOn.SetBlinking('Medium', [0, 1])
        tlp.btn_lPrjOff.SetState(0)
        
        LeftPRJTimer.Restart()

def LeftTimer(timer:Timer, count):
    print("Left Timer started")
    dvLeftPRJ.Update('Power')

LeftPRJTimer = Timer(5, LeftTimer)
LeftPRJTimer.Stop()

dvLeftPRJ.SubscribeStatus('Power', None, LeftPowerChanged)

def RightPowerChanged(command, value, qualifier):
    GVEServer.SendStatus(PRJR_ID, 'Power', value)
    if value is 'On' or value is 'Off':
        r_prj_set.SetCurrent(tlp.btn_rPrjOn if value == 'On' else tlp.btn_rPrjOff)
        RightPRJTimer.Stop()
        
    else:
        tlp.btn_rPrjOn.SetBlinking('Medium', [0, 1])
        tlp.btn_rPrjOff.SetState(0)
        RightPRJTimer.Restart()

def RightTimer(timer:Timer, count):
    print("Right Timer started")
    dvRightPRJ.Update('Power')

RightPRJTimer = Timer(5, RightTimer)
RightPRJTimer.Stop()

dvRightPRJ.SubscribeStatus('Power', None, RightPowerChanged)

#might need to be a list instead of *[]
prj_list = [tlp.btn_projOn, tlp.btn_projOff, 
            tlp.btn_lPrjOn, tlp.btn_lPrjOff, 
            tlp.btn_rPrjOn, tlp.btn_rPrjOff]
@eventEx(prj_list, 'Pressed')
def ProjectorOnOff(button:Button, state):
    print(button.Name, button.Host, state)
    if button in prj_set.Objects:
        dvCenterPRJ.SetPower('On' if button is tlp.btn_projOn else 'Off', None)
        dvCenterPRJ.Update('Power')
    elif button in l_prj_set.Objects:
        dvLeftPRJ.SetPower('On' if button is tlp.btn_lPrjOn else 'Off', None)
        dvLeftPRJ.Update('Power')
    elif button in r_prj_set.Objects:
        dvRightPRJ.SetPower('On' if button is tlp.btn_rPrjOn else 'Off', None)

def CenterAVMuteChanged(command, value, qualifier):
    tlp.btn_blankImg.SetState(1 if value is 'On' else 0)

dvCenterPRJ.SubscribeStatus('AVMute', None, CenterAVMuteChanged)

def LeftAVMuteChanged(command, value, qualifier):
    tlp.btn_lBlankImg.SetState(1 if value is 'On' else 0)

dvLeftPRJ.SubscribeStatus('AVMute', None, LeftAVMuteChanged)

def RightAVMuteChanged(command, value, qualifier):
    tlp.btn_rBlankImg.SetState(1 if value is 'On' else 0)

dvRightPRJ.SubscribeStatus('AVMute', None, RightAVMuteChanged)


@eventEx([tlp.btn_blankImg, tlp.btn_lBlankImg, tlp.btn_rBlankImg], 'Pressed')
def BlankImage(button:Button, state):
    print(button.Name, button.Host, state)
    if button is tlp.btn_blankImg:
        button.SetState(0 if button.State is 1 else 1)
        dvCenterPRJ.Set('AVMute', 'Off' if button.State is 0 else 'On')
    elif button is tlp.btn_lBlankImg:
        button.SetState(0 if button.State is 1 else 1)
        dvLeftPRJ.Set('AVMute', 'Off' if button.State is 0 else 'On')
    elif button is tlp.btn_rBlankImg:
        button.SetState(0 if button.State is 1 else 1)
        dvRightPRJ.Set('AVMute', 'Off' if button.State is 0 else 'On')