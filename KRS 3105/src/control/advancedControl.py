from devices import dvCenterPRJ, dvRightPRJ, dvLeftPRJ, GVEServer, PRJC_ID, PRJL_ID,  PRJR_ID

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
    else:
        tlp.btn_projOn.SetBlinking('Medium', [0, 1])
        tlp.btn_projOff.SetBlinking('Medium', [0, 1])

dvCenterPRJ.SubscribeStatus('Power', None, CenterPowerChanged)

def LeftPowerChanged(command, value, qualifier):
    GVEServer.SendStatus(PRJL_ID, 'Power', value)
    if value is 'On' or value is 'Off':
        l_prj_set.SetCurrent(tlp.btn_lPrjOn if value == 'On' else tlp.btn_lPrjOff)     
    else:
        tlp.btn_lPrjOn.SetBlinking('Medium', [0, 1])
        tlp.btn_lPrjOff.SetBlinking('Medium', [0, 1])

dvLeftPRJ.SubscribeStatus('Power', None, LeftPowerChanged)

def RightPowerChanged(command, value, qualifier):
    GVEServer.SendStatus(PRJR_ID, 'Power', value)
    if value is 'On' or value is 'Off':
        r_prj_set.SetCurrent(tlp.btn_rPrjOn if value == 'On' else tlp.btn_rPrjOff) 
    else:
        tlp.btn_rPrjOn.SetBlinking('Medium', [0, 1])
        tlp.btn_rPrjOff.SetBlinking('Medium', [0, 1])
        
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
        dvRightPRJ.Update('Power')
    button.SetBlinking('Medium', [0, 1])

def CenterAVMuteChanged(command, value, qualifier):
    tlp.btn_blankImg.SetState(1 if value is 'On' else 0)

dvCenterPRJ.SubscribeStatus('AVMute', None, CenterAVMuteChanged)

def LeftAVMuteChanged(command, value, qualifier):
    tlp.btn_lBlankImg.SetState(1 if value is 'On' else 0)

dvLeftPRJ.SubscribeStatus('AVMute', None, LeftAVMuteChanged)

def RightAVMuteChanged(command, value, qualifier):
    tlp.btn_rBlankImg.SetState(1 if value is 'On' else 0)

dvRightPRJ.SubscribeStatus('AVMute', None, RightAVMuteChanged)


@eventEx([tlp.btn_blankImg, tlp.btn_lBlankImg, tlp.btn_rBlankImg], 
         'Pressed')
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

"""NO AUDIO SLIDERS DEFINED YET"""