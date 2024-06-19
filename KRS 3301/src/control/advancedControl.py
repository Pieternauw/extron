from devices import dvPRJ

from extronlib.system import MESet, Timer

from modules.helper.ModuleSupport import eventEx

import ui.tlpAdvanced as tlp 

prj_set = MESet([tlp.btn_projOn, tlp.btn_projOff])
prj_set.SetCurrent(tlp.btn_projOn if dvPRJ.ReadStatus('Power') is 'On' else tlp.btn_projOff)

def PowerChanged(command, value, qualifier):
    if value is 'On':
        prj_set.SetCurrent(tlp.btn_projOn)
        PRJStatusTimer.Stop()
    elif value is 'Off':
        prj_set.SetCurrent(tlp.btn_projOff)
        PRJStatusTimer.Stop()
    else:
        if value is 'Warming':
            tlp.btn_projOn.SetBlinking('Medium', [0, 1])
        elif value is 'Cooling':
            tlp.btn_projOff.SetBlinking('Medium', [0, 1])
        PRJStatusTimer.Restart()


def PowerTimer(timer:Timer, count):
    print("Timer started")
    dvPRJ.Update('Power')

PRJStatusTimer = Timer(2, PowerTimer)
PRJStatusTimer.Stop()


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
    dvPRJ.Set('AVMute', 'Off' if button.State is 1 else 'On')
