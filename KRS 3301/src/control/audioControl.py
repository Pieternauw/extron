"""
This file defines the control for the advanced settings sliders. Depending on which slider gets changed, 
the scalar gets told the value it was changed to. The user moves the slider where they want it and that 
value is passed in the set function. On startup, default values are set and the sliders are filled to 
a certain level. 
"""

from modules.helper.ModuleSupport import eventEx
import ui.tlpAudio as tlp 
from devices import dvScalar 
import variables as var

mic_slider_list = [tlp.sld_lavMic, tlp.sld_handHeld]
prg_slider_list = [tlp.sld_laptop, tlp.sld_wireless, tlp.sld_bluray]

@eventEx([tlp.sld_lavMic, tlp.sld_handHeld, tlp.sld_laptop, tlp.sld_wireless, tlp.sld_bluray, tlp.sld_ampLevelOut], 'Changed')
def SliderChanged(slider:tlp.Slider, state, value):
    print(slider.Name, 'Control')
    if slider in mic_slider_list:
        dvScalar.SetMicLineInputGain(value, {'Input': '{}'.format(mic_slider_list.index(slider) + 1)})  #TODO check these input numbers
    elif slider in prg_slider_list:
        dvScalar.SetEmbeddedInputGain(value, {'Input': '{}'.format(prg_slider_list.index(slider)+ 1)})
    elif slider is tlp.sld_ampLevelOut:
        dvScalar.SetOutputAttenuation(value, {'Output': 'Amp Out'})
    
def Startup():
    tlp.sld_lavMic.SetFill(var.lav_mic_sld)
    tlp.sld_handHeld.SetFill(var.hand_mic_sld)
    tlp.sld_laptop.SetFill(var.laptop_prg_sld)
    tlp.sld_wireless.SetFill(var.wireless_prg_sld)
    tlp.sld_bluray.SetFill(var.bluray_prg_sld)
    tlp.sld_ampLevelOut.SetFill(var.amp_sld)
    dvScalar.SetMicLineInputGain(var.lav_mic_sld, {'Input': '1'})  #TODO check these input numbers
    dvScalar.SetMicLineInputGain(var.hand_mic_sld, {'Input': '2'})  #TODO check these input numbers
    dvScalar.SetEmbeddedInputGain(var.laptop_prg_sld, {'Input': '1'})  #TODO check these input numbers
    dvScalar.SetEmbeddedInputGain(var.wireless_prg_sld, {'Input': '2'})  #TODO check these input numbers
    dvScalar.SetEmbeddedInputGain(var.bluray_prg_sld, {'Input': '3'})  #TODO check these input numbers
    dvScalar.SetOutputAttenuation(var.amp_sld, {'Output': 'Amp Out'})
    
@eventEx(dvScalar, 'Connected')
def SetSliderValues(client, data):
    Startup()