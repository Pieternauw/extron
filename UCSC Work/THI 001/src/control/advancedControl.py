from devices import dvPRJ, GVEServer, dvScalar, PRJ_ID

from extronlib.system import MESet, Timer

from modules.helper.ModuleSupport import eventEx

import ui.tlpAdvanced as tlp

#Exclusive set of the power buttons
prj_set = MESet([tlp.btn_projOn, tlp.btn_projOff])
#Set button at declaration to current projector status
prj_set.SetCurrent(tlp.btn_projOn if dvPRJ.ReadStatus('Power') is 'On' else tlp.btn_projOff)

#Define a repsonse function for subscribe status
def PowerChanged(command, value, qualifier):
    print(value)
    GVEServer.SendStatus(PRJ_ID, 'Power', value)
    #If SubscribeStatus calls function with value 'On', set button to on and stop timer. 
    if value is 'On' or value is 'Off':
        prj_set.SetCurrent(tlp.btn_projOn if value == 'On' else tlp.btn_projOff)
    #If SubscribeStatus calls fucntion with value 'Off', set off button and stop timer. 
    else:
        #in the case that no response is sent, or 'Warming Up' or 'Cooling Down', blink the On button and restart the timer
        tlp.btn_projOn.SetBlinking('Medium', [0, 1])
        tlp.btn_projOff.SetBlinking('Medium', [0, 1])
        if PRJStatusTimer.Count == 0: PRJStatusTimer.Restart()
        else: PRJStatusTimer.Resume()
        

#Timer function called every time timer ends. Calls update function for projector, asking for most recent status. 
def PowerTimer(timer:Timer, count):
    print("Timer started")
    dvPRJ.Update('Power')
    if count > 11:
        timer.Stop()
        print("Timer stopped")

#5 second timer, stop after definition to prevent errors. 
PRJStatusTimer = Timer(5, PowerTimer)

#SubscribeStatus to power with callback function
dvPRJ.SubscribeStatus('Power', None, PowerChanged)

#Event to handle button press
@eventEx(prj_set.Objects, 'Pressed')
def ProjectorOnOff(button:tlp.Button, state):
    print(button, state)
    #Set current MESet to button pressed
    prj_set.SetCurrent(button)
    #If power on was pressed, send on command
    dvPRJ.SetPower('On' if button is tlp.btn_projOn else 'Off', None)
    #Update the device to trigger SubscribeStatus, allowing for visual state to correspond with device status. 
    dvPRJ.Update('Power')
    
@eventEx(tlp.btn_blankImg, 'Pressed')
def BlankImage(button:tlp.Button, state):
    print(button.Name, state)    
    button.SetState(0 if button.State is 1 else 1)
    dvPRJ.Set('AVMute', 'Off' if button.State is 0 else 'On')


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
