"""
This control file handles the response for the up, down, and mute buttons for both program and microphone.
It utilizes the SubscribeStatus() method to keep track of states for volume mute and level. 

The basic idea is that when a button is pressed, for example the mute program button, the touchpanel 
queries the switcher for the current value. The switcher returns either 'On' or 'Off'. If the value 
is 'On' the program sets it to 'Off' and vice versa. If the command sends successfully, the switcher 
sees there's a change in the value state and calls the SubscribeStatus feedback handler which is defined 
in this file. This feedback handler sets the visual feedback of the button pressed dependent on the value 
passed by the SubscribeStatus command. 

Visual feedback done in this way means it stays consistent with the device state rather than with the 
user input. If the user presses the button but the device doesn't change state, then the button doesn't 
represent the changed state, it remains in the current state. This does add a slight delay on press
but the delay is very short. 

For volume control the inc() and dec() methods are used. This steps the level bar up and then sends the value
of the level bar to the device. There is a recorrection if the bar steps past where the last device value was
received. If the user enters commands too fast for the device to respond sometimes it won't get every inc() or
dec() command so the bar will adjust to the devices value when stabalized. 
"""

from devices import dvScalar
from modules.helper.ModuleSupport import eventEx

import ui.tlpMainAudio as tlp 

tlp.lvl_prog.SetRange(-30, 12, 1)     #In steps of 2
tlp.lvl_mic.SetRange(-30, 12, 1)
"""TODO - Check if it's Mic in or Mic in"""
@eventEx([tlp.btn_progAudioMute, tlp.btn_micAudioMute], 'Pressed')
def MuteButtonPressed(button:tlp.Button, state):
    if button is tlp.btn_progAudioMute:
        CurrentMute = dvScalar.ReadStatus('GroupProgramMute')
        dvScalar.SetGroupProgramMute('Off' if CurrentMute is 'On' else 'On', None)
    else:
        CurrentMute = dvScalar.ReadStatus('GroupMicMute')
        dvScalar.SetGroupMicMute('Off' if CurrentMute is 'On' else 'On', None)
            
def MicMuteChanged(command, value, qualifier=None):
    print(command, value, qualifier)
    tlp.btn_micAudioMute.SetState(1 if value is 'On' else 0)
        
def ProgMuteChanged(command, value, qualifier=None):
    print(command, value, qualifier)
    tlp.btn_progAudioMute.SetState(1 if value is 'On' else 0)

        
dvScalar.SubscribeStatus('GroupMicMute', None, MicMuteChanged)
dvScalar.SubscribeStatus('GroupProgramMute', None, ProgMuteChanged)
            
def MicVolumeChanged(command, value, qualifier=None):
    print(command, value, qualifier)
    tlp.lvl_mic.SetLevel(int(value))
    
def ProgVolumeChanged(command, value, qualifier=None):
    print(command, value, qualifier)
    tlp.lvl_prog.SetLevel(int(value))
    
dvScalar.SubscribeStatus('GroupMicVolume', None, MicVolumeChanged)
dvScalar.SubscribeStatus('GroupProgramVolume', None, ProgVolumeChanged)
  
mic_list = [tlp.btn_micAudioDown, tlp.btn_micAudioUp]
prog_list = [tlp.btn_progAudioDown, tlp.btn_progAudioUp]  
          
@eventEx([tlp.btn_micAudioDown, tlp.btn_micAudioUp, 
          tlp.btn_progAudioDown, tlp.btn_progAudioUp], 
         ['Pressed', 'Repeated'])
def MicControlEvent(button:tlp.Button, state):
    print(button.Name, state)
    if button in mic_list:
        if button is mic_list[0]:
            tlp.lvl_mic.Dec()
        else:
            tlp.lvl_mic.Inc()
        dvScalar.SetGroupMicVolume(tlp.lvl_mic.Level, None)
    elif button in prog_list:
        if button is prog_list[0]:
            tlp.lvl_prog.Dec()
        else:
            tlp.lvl_prog.Inc()
        dvScalar.SetGroupProgramVolume(tlp.lvl_prog.Level, None)
 