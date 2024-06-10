"""
This file only creates every button object and assigns the basic feedback on 
press and release to every button. 
"""

from modules.helper.MirrorUI import Button 
from modules.helper.ModuleSupport import eventEx
from devices import dvTLPMain

"""Bluray Popup"""

btn_blurayStop = Button(dvTLPMain, 51)
btn_blurayPlay = Button(dvTLPMain, 60)
btn_blurayPause = Button(dvTLPMain, 66)
btn_blurayRTrack = Button(dvTLPMain, 62)
btn_blurayFTrack = Button(dvTLPMain, 1066)
btn_blurayRewind = Button(dvTLPMain, 47)
btn_blurayFForward = Button(dvTLPMain, 68)
btn_blurayLeft = Button(dvTLPMain, 78)
btn_blurayUp = Button(dvTLPMain, 80)
btn_blurayDown = Button(dvTLPMain, 79)
btn_blurayRight = Button(dvTLPMain, 77)
btn_blurayEnter = Button(dvTLPMain, 154)
btn_blurayReturn = Button(dvTLPMain, 38)
btn_blurayHome = Button(dvTLPMain,70)
btn_blurayOption = Button(dvTLPMain, 73)
btn_blurayMenu = Button(dvTLPMain, 71)
btn_bluraySub = Button(dvTLPMain, 74)   

#Same as MP4k code so make sure this works
btn_blurayEject = Button(dvTLPMain, 134)

button_set = [btn_blurayStop, btn_blurayPlay, btn_blurayPause, btn_blurayRTrack, btn_blurayFTrack, 
              btn_blurayDown, btn_blurayRight, btn_blurayUp, btn_blurayLeft, btn_blurayEnter, 
              btn_blurayReturn, btn_blurayHome, btn_blurayOption, btn_blurayMenu, btn_blurayRewind, 
              btn_blurayFForward, btn_bluraySub, btn_blurayEject]

@eventEx(button_set, ['Pressed', 'Released'])
def ButtonPressedEvent(button:Button, state):
    print(button.Name, button.Host, state)
    button.SetState(1 if state is 'Pressed' else 0)
    