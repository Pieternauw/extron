from devices import dvPRJFront, dvPRJBack, GVEServer, PRJF_ID, PRJB_ID

from extronlib.system import MESet, Timer

from modules.helper.ModuleSupport import eventEx

import ui.tlpAdvanced as tlp 

prj_set = MESet([tlp.btn_projOn, tlp.btn_projOff])
prj_set.SetCurrent(tlp.btn_projOn if dvPRJFront.ReadStatus('Power') is 'On' else tlp.btn_projOff)

def PowerChanged(command, value, qualifier):
    print(value)
    GVEServer.SendStatus(PRJF_ID, 'Power', value)
    GVEServer.SendStatus(PRJB_ID, 'Power', value)
    if value is 'On':
        prj_set.SetCurrent(tlp.btn_projOn)
        PRJStatusTimer.Stop()
    elif value is 'Off':
        prj_set.SetCurrent(tlp.btn_projOff)
        PRJStatusTimer.Stop()
    else:
        tlp.btn_projOn.SetBlinking('Slow', [0, 1])
        PRJStatusTimer.Restart()


def PowerTimer(timer:Timer, count):
    print("Timer started")
    dvPRJFront.Update('Power')


PRJStatusTimer = Timer(5, PowerTimer)
PRJStatusTimer.Stop()

dvPRJFront.SubscribeStatus('Power', None, PowerChanged)


@eventEx(prj_set.Objects, 'Pressed')
def ProjectorOnOff(button:tlp.Button, state):
    print(button, state)
    prj_set.SetCurrent(button)
    dvPRJFront.SetPower('On' if button is tlp.btn_projOn else 'Off', None)
    dvPRJBack.SetPower('On' if button is tlp.btn_projOn else 'Off', None)
    dvPRJFront.Update('Power')
    dvPRJBack.Update('Power')
    dvPRJFront.Update('LampUsage')

@eventEx(tlp.btn_blankImg, 'Pressed')
def BlankImage(button:tlp.Button, state):
    print(button.Name, state)    
    button.SetState(0 if button.State is 1 else 1)
    dvPRJFront.Set('AVMute', 'Off' if button.State is 0 else 'On')
    dvPRJBack.Set('AVMute', 'Off' if button.State is 0 else 'On')
