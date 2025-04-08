from modules.helper.MirrorUI import Button, Level #, Label

from modules.helper.ModuleSupport import eventEx
from devices import dvTLPMain

BTNEVL = ['Pressed', 'Released']

btn_cProgUp = Button(dvTLPMain, 238, repeatTime=0.2)
btn_cProgMute = Button(dvTLPMain, 237)
btn_cProgDown = Button(dvTLPMain, 236, repeatTime=0.2)

btn_cMicDown = Button(dvTLPMain, 241, repeatTime=0.2)
btn_cMicMute = Button(dvTLPMain, 240)
btn_cMicUp = Button(dvTLPMain, 239, repeatTime=0.2)

lvl_cMic = Level(dvTLPMain, 242)
lvl_cProg = Level(dvTLPMain, 244)

"""
lbl_Speech = Label(dvTLPMain, )
lbl_micNotW = Label(dvTLPMain, )
lbl_micNotR = Label(dvTLPMain, )
"""

@eventEx([btn_cMicMute, btn_cProgMute], 'Pressed')
def MutePressedEvent(button:Button, state):
    print(button.Name, button.Host, state)

@eventEx([btn_cMicUp, btn_cMicDown, btn_cProgUp, btn_cProgDown], BTNEVL)
def VolumeChangeCenter(button:Button, state):
    print(button.Name, button.Host, state)
    button.SetState(1 if state is 'Pressed' or state is 'Held' else 0)

