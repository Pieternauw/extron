"""
The main audio file defines the UI objects for the main page audio. This includes the 
speech volume, program volume, and mute buttons. Control for the up and down buttons
and mute control and feedback are in the mainAudioControl.py file. This file just
creates the objects being controlled and assigns status to the up and down button.
Mute status is based on response from the scalar after the button is pressed. 
"""

from extronlib.ui import Button, Level
# Project imports
from devices import dvTLP
from modules.helper.ModuleSupport import eventEx

#Program Audio
btn_progAudioUp = Button(dvTLP, 84, repeatTime=0.2)
btn_progAudioDown = Button(dvTLP, 82, repeatTime=0.2)
btn_progAudioMute = Button(dvTLP, 83)

#Microphone Audio
btn_micAudioUp = Button(dvTLP, 87, repeatTime=0.2)
btn_micAudioDown = Button(dvTLP, 12, repeatTime=0.2)
btn_micAudioMute = Button(dvTLP, 88)

#level bar
lvl_prog = Level(dvTLP, 18)
lvl_mic = Level(dvTLP, 85)

@eventEx([btn_micAudioMute, btn_progAudioMute], 'Pressed')
def MutePressedEvent(button:Button, state):
    print(button.Name, state)
    
@eventEx([btn_micAudioDown, btn_micAudioUp,
         btn_progAudioDown, btn_progAudioUp], ['Pressed', 'Released'])
def VolumeChange(button:Button, state):
    print(button.Name, state)
    button.SetState(1 if state is 'Pressed' else 0)