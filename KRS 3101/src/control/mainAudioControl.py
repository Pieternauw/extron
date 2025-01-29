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
 