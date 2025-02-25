from devices import dvBiamp
from modules.helper.ModuleSupport import eventEx

import ui.tlpMainAudio as tlp 

tlp.lvl_prog.SetRange(-40, 6, 2)     #In steps of 2
tlp.lvl_mic.SetRange(-20, 0, 1)
"""TODO - Check if it's Mic in or Mic in"""
tag_dict = {tlp.btn_progAudioMute: 'MuteProgram', tlp.btn_micAudioMute: 'MuteSpeech'}

@eventEx([tlp.btn_cProgMute, tlp.btn_cMicMute], 'Pressed')
def MuteButtonPressed(button:tlp.Button, state):
    print('control', button.Name, state)
    curr = dvBiamp.ReadStatus('MuteControl', {'Instance Tag': tag_dict[button], 'Channel': '1'})
    if curr is 'Off':
        dvBiamp.SetMuteControl('On', {'Instance Tag': tag_dict[button], 'Channel': '1'})
    else:
        dvBiamp.SetMuteControl('Off', {'Instance Tag': tag_dict[button], 'Channel': '1'})
    dvBiamp.Update('MuteControl', {'Instance Tag': tag_dict[button], 'Channel': '1'})
            
def MicMuteChanged(command, value, qualifier=None):
    print(command, value, qualifier)
    tlp.btn_micAudioMute.SetState(1 if value is 'On' else 0)
        
def ProgMuteChanged(command, value, qualifier=None):
    print(command, value, qualifier)
    tlp.btn_progAudioMute.SetState(1 if value is 'On' else 0)

        
dvBiamp.SubscribeStatus('MuteControl', {'Instance Tag': 'MuteSpeech', 'Channel': '1'}, MicMuteChanged)
dvBiamp.SubscribeStatus('MuteControl', {'Instance Tag': 'MuteProgram', 'Channel': '1'}, ProgMuteChanged)
            
def MicVolumeChanged(command, value, qualifier=None):
    print(command, value, qualifier)
    tlp.lvl_mic.SetLevel(int(value))
    
def ProgVolumeChanged(command, value, qualifier=None):
    print(command, value, qualifier)
    tlp.lvl_prog.SetLevel(int(value))
    
dvBiamp.SubscribeStatus('LevelControl', {'Instance Tag': 'LevelSpeech', 'Channel': '1'}, MicVolumeChanged)
dvBiamp.SubscribeStatus('LevelControl', {'Instance Tag': 'LevelProgram', 'Channel': '1'}, ProgVolumeChanged)
  
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
        dvBiamp.SetLevelControl(tlp.lvl_mic.Level, {'Instance Tag': 'LevelSpeech', 'Channel': '1'})
    elif button in prog_list:
        if button is prog_list[0]:
            tlp.lvl_prog.Dec()
        else:
            tlp.lvl_prog.Inc()
        dvBiamp.SetLevelControl(tlp.lvl_prog.Level, {'Instance Tag': 'LevelProgram', 'Channel': '1'})
 