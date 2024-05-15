from modules.helper.MirrorUI import Slider, Button
from modules.helper.ModuleSupport import eventEx

from devices import dvTLPMain

      
"""Audio Mix"""

"""TODO - This hasn't been implemented in any of it so I have no idea how to code it
        - Check with Scott or Tosh about how they want this to work
        - Most likely something to do with the Biamp"""

sld_lavMic = Slider(dvTLPMain, 22)
sld_lavMic.SetRange(-18, 80, 1)
@eventEx(sld_lavMic, 'Changed')
def LavSlider(slider, state, value):
    if state == 'Changed':
        slider.SetFill(value)


sld_handHeld = Slider(dvTLPMain, 28)
sld_handHeld.SetRange(-18, 80, 1)   #TODO Check these numbers
@eventEx(sld_handHeld, 'Changed')
def HandHeldSlider(slider, state, value):
    if state == 'Changed':
        slider.SetFill(value)

sld_laptop = Slider(dvTLPMain, 35)
sld_laptop.SetRange(-18, 24, 0.5)     #TODO Check these numbers
@eventEx(sld_laptop, 'Changed')
def LaptopSlider(slider, state, value):
    if state == 'Changed':
        slider.SetFill(value)

sld_wireless = Slider(dvTLPMain, 39)
sld_wireless.SetRange(-18, 24, 0.5)     #TODO Check numbers
@eventEx(sld_wireless, 'Changed')
def WirelessSlider(slider, state, value):
    if state == 'Changed':
        slider.SetFill(value)

sld_bluray = Slider(dvTLPMain, 45)
sld_bluray.SetRange(-18, 24, 0.5)     #TODO Check numbers
@eventEx(sld_bluray, 'Changed')
def BluraySlider(slider, state, value):
    if state == 'Changed':
        slider.SetFill(value)

sld_ampLevelOut = Slider(dvTLPMain, 52)
sld_ampLevelOut.SetRange(-100, 0, 1)
@eventEx(sld_ampLevelOut, 'Changed')
def AmpLevelSlider(slider, state, value):
    if state == 'Changed':
        slider.SetFill(value)

btn_exitMix = Button(dvTLPMain, 76)
@eventEx(btn_exitMix, 'Pressed')
def ExitAudioMix(button:Button, state):
    print(button.Name, button.Host, state)
    dvTLPMain.HidePopup('Audio Mix popup')

