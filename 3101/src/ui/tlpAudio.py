from modules.helper.ModuleSupport import eventEx
from extronlib.ui import Button, Slider
from devices import dvTLP

"""
The audio mix popup only contains the UI element design. It doesn't include any control.
Control is determined by the level of the slider when it gets changed. When the user 
slides up or down, the control responds by setting the volume level in the 1808 switcher
to wherever the user left the level. 
"""


"""Audio Mix Popup"""
#Sliders
sld_lavMic = Slider(dvTLP, 22)
sld_lavMic.SetRange(-18, 80, 1)
@eventEx(sld_lavMic, 'Changed')
def LavSlider(slider, state, value):
    slider.SetFill(value)

sld_handHeld = Slider(dvTLP, 28)
sld_handHeld.SetRange(-18, 80, 1)   #TODO Check these numbers
@eventEx(sld_handHeld, 'Changed')
def HandHeldSlider(slider, state, value):
    slider.SetFill(value)

sld_laptop = Slider(dvTLP, 35)
sld_laptop.SetRange(-18, 24, 0.5)     #TODO Check these numbers
@eventEx(sld_laptop, 'Changed')
def LaptopSlider(slider, state, value):
    slider.SetFill(value)

sld_wireless = Slider(dvTLP, 39)
sld_wireless.SetRange(-18, 24, 0.5)     #TODO Check numbers
@eventEx(sld_wireless, 'Changed')
def WirelessSlider(slider, state, value):
    slider.SetFill(value)

sld_bluray = Slider(dvTLP, 45)
sld_bluray.SetRange(-18, 24, 0.5)     #TODO Check numbers
@eventEx(sld_bluray, 'Changed')
def BluraySlider(slider, state, value):
    slider.SetFill(value)

sld_ampLevelOut = Slider(dvTLP, 52)
sld_ampLevelOut.SetRange(-100, 0, 1)
@eventEx(sld_ampLevelOut, 'Changed')
def AmpLevelSlider(slider, state, value):
    slider.SetFill(value)

btn_exitMix = Button(dvTLP, 76)
@eventEx(btn_exitMix, 'Pressed')
def ExitAudioMix(button:Button, state):
    print(button.Name, state)
    dvTLP.HidePopup('Audio Mix popup')

