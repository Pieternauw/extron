from devices import dvPRJ

from extronlib.system import MESet 

from modules.helper.ModuleSupport import eventEx

import ui.tlpAdvanced as tlp 

prj_set = MESet([tlp.btn_projOn, tlp.btn_projOff])
prj_set.SetCurrent(tlp.btn_projOn if dvPRJ.ReadStatus('Power') is 'On' else tlp.btn_projOff)

def PowerChanged(command, value, qualifier):
    prj_set.SetCurrent(tlp.btn_projOn if value == 'On' else tlp.btn_projOff)

dvPRJ.SubscribeStatus('Power', None, PowerChanged)

@eventEx(prj_set.Objects, 'Pressed')
def ProjectorOnOff(button:tlp.Button, state):
    print(button, state)
    prj_set.SetCurrent(button)
    dvPRJ.SetPower('On' if button is tlp.btn_projOn else 'Off', None)
    dvPRJ.Update('Power')
    
@eventEx(tlp.btn_blankImg, 'Pressed')
def BlankImage(button:tlp.Button, state):
    print(button.Name, state)    
    button.SetState(0 if button.State is 1 else 1)
    dvPRJ.Set('AVMute', 'Off' if button.State is 1 else 0)
