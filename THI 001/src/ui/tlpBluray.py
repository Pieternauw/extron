from extronlib.ui import Button 
from modules.helper.ModuleSupport import eventEx
from devices import dvTLP

"""
Bluray Popup defines all of the UI buttons in the bluray popup.
It uses one list to set state of buttons when pressed. Otherwise
all control is handled in the blurayControl.py file.  
"""

btn_blurayStop = Button(dvTLP, 51)
btn_blurayPlay = Button(dvTLP, 60)
btn_blurayPause = Button(dvTLP, 66)
btn_blurayRTrack = Button(dvTLP, 62)
btn_blurayFTrack = Button(dvTLP, 1066)
btn_blurayRewind = Button(dvTLP, 1047)
btn_blurayFForward = Button(dvTLP, 68)
btn_blurayLeft = Button(dvTLP, 78)
btn_blurayUp = Button(dvTLP, 80)
btn_blurayDown = Button(dvTLP, 79)
btn_blurayRight = Button(dvTLP, 77)
btn_blurayEnter = Button(dvTLP, 154)
btn_blurayReturn = Button(dvTLP, 38)
btn_blurayHome = Button(dvTLP, 70)
btn_blurayOption = Button(dvTLP, 73)
btn_blurayMenu = Button(dvTLP, 71)
btn_bluraySub = Button(dvTLP, 74)   

#Same as MP4k code so make sure this works
btn_blurayEject = Button(dvTLP, 134)

button_set = [btn_blurayStop, btn_blurayPlay, btn_blurayPause, btn_blurayRTrack, btn_blurayFTrack, 
              btn_blurayDown, btn_blurayRight, btn_blurayUp, btn_blurayLeft, btn_blurayEnter, 
              btn_blurayReturn, btn_blurayHome, btn_blurayOption, btn_blurayMenu, btn_blurayRewind, 
              btn_blurayFForward, btn_bluraySub, btn_blurayEject]

@eventEx(button_set, ['Pressed', 'Released'])
def ButtonPressedEvent(button:Button, state):
    print(button.Name, state)
    button.SetState(1 if state is 'Pressed' else 0)
    
    