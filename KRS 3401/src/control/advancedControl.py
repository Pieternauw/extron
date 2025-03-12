from devices import dvPRJFront, dvPRJBack, GVEServer, dvScalar, PRJF_ID, PRJB_ID

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
    elif value is 'Off':
        prj_set.SetCurrent(tlp.btn_projOff)
    else:
        tlp.btn_projOn.SetBlinking('Slow', [0, 1])


def PowerTimer(timer:Timer, count):
    print("Timer started")
    dvPRJFront.Update('Power')

PRJStatusTimer = Timer(10, PowerTimer)

dvPRJFront.SubscribeStatus('Power', None, PowerChanged)


@eventEx(prj_set.Objects, 'Pressed')
def ProjectorOnOff(button:tlp.Button, state):
    print(button, state)
    prj_set.SetCurrent(button)
    dvPRJFront.SetPower('On' if button is tlp.btn_projOn else 'Off', None)
    dvPRJBack.SetPower('On' if button is tlp.btn_projOn else 'Off', None)
    dvPRJFront.Update('Power')
    dvPRJBack.Update('Power')

@eventEx(tlp.btn_blankImg, 'Pressed')
def BlankImage(button:tlp.Button, state):
    print(button.Name, state)    
    button.SetState(0 if button.State is 1 else 1)
    dvPRJFront.Set('AVMute', 'Off' if button.State is 0 else 'On')
    dvPRJBack.Set('AVMute', 'Off' if button.State is 0 else 'On')

mic_slider_list = [tlp.sld_lavMic, tlp.sld_handHeld]
prg_slider_list = [tlp.sld_wireless, tlp.sld_laptop, tlp.sld_bluray]

@eventEx([tlp.sld_lavMic, tlp.sld_handHeld, tlp.sld_laptop, tlp.sld_wireless, tlp.sld_bluray, tlp.sld_ampLevelOut], 'Changed')
def SliderChanged(slider:tlp.Slider, state, value):
    print(slider.Name, 'Control')
    if slider in mic_slider_list:
        dvScalar.SetMicLineInputGain(value, {'Input': '{}'.format(mic_slider_list.index(slider) + 1)})  #TODO check these input numbers
    elif slider in prg_slider_list:
        dvScalar.SetEmbeddedInputGain(value, {'Input': '{}'.format(prg_slider_list.index(slider)+ 1)})
    elif slider is tlp.sld_ampLevelOut:
        dvScalar.SetOutputAttenuation(value, {'Output': 'Amp Out'})