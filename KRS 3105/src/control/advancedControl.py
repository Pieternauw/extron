from devices import dvCenterPRJ, dvRightPRJ, dvLeftPRJ

import ui.tlpAdvanced as tlp

from extronlib.system import MESet

from modules.helper.MirrorUI import Button
from modules.helper.ModuleSupport import eventEx 


prj_set = MESet([tlp.btn_projOn, tlp.btn_projOff])
prj_set.SetCurrent(tlp.btn_projOn if dvCenterPRJ.ReadStatus('Power') is 'On' else tlp.btn_projOff)

l_prj_set = MESet([tlp.btn_lPrjOn, tlp.btn_lPrjOff])
l_prj_set.SetCurrent(tlp.btn_lPrjOn if dvLeftPRJ.ReadStatus('Power') is 'On' else tlp.btn_lPrjOff)

r_prj_set = MESet([tlp.btn_rPrjOn, tlp.btn_rPrjOff])
r_prj_set.SetCurrent(tlp.btn_rPrjOn if dvRightPRJ.ReadStatus('Power') is 'On' else tlp.btn_rPrjOff)

def CenterPowerChanged(command, value, qualifier):
    prj_set.SetCurrent(tlp.btn_projOn if value == 'On' else tlp.btn_projOff)

dvCenterPRJ.SubscribeStatus('Power', None, CenterPowerChanged)

def LeftPowerChanged(command, value, qualifier):
    l_prj_set.SetCurrent(tlp.btn_lPrjOn if value == 'On' else tlp.btn_lPrjOff)

dvLeftPRJ.SubscribeStatus('Power', None, LeftPowerChanged)

def RightPowerChanged(command, value, qualifier):
    r_prj_set.SetCurrent(tlp.btn_rPrjOn if value == 'On' else tlp.btn_rPrjOff)

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
        dvRightPRJ.SetPower('On' if button is tlp.btn_rPrjOff else 'Off', None)

def CenterAVMuteChanged(command, value, qualifier):
    tlp.btn_blankImg.SetState(1 if value is 'On' else 0)

dvCenterPRJ.SubscribeStatus('AVMute', None, CenterAVMuteChanged)

def LeftAVMuteChanged(command, value, qualifier):
    tlp.btn_lBlankImg.SetState(1 if value is 'On' else 0)

dvLeftPRJ.SubscribeStatus('AVMute', None, LeftAVMuteChanged)

def RightAVMuteChanged(command, value, qualifier):
    tlp.btn_rBlankImg.SetState(1 if value is 'On' else 0)

dvRightPRJ.SubscribeStatus('AVMute', None, RightAVMuteChanged)


@eventEx(tlp.btn_blankImg, 'Pressed')
def BlankImage(button:Button, state):
    print(button.Name, button.Host, state)
    if button is tlp.btn_blankImg:
        dvCenterPRJ.Set('AVMute', 'Off' if button.State is 1 else 'On')
        dvCenterPRJ.Update('AVMute')
    elif button is tlp.btn_lBlankImg:
        dvLeftPRJ.Set('AVMute', 'Off' if button.State is 1 else 'On')
        dvLeftPRJ.Update('AVMute')
    elif button is tlp.btn_rBlankImg:
        dvRightPRJ.Set('AVMute', 'Off' if button.State is 1 else 'On')
        dvRightPRJ.Update('AVMute')