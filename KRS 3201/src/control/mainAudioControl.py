from devices import dvBiamp
from modules.helper.ModuleSupport import eventEx

#from extronlib.system import Timer

import ui.tlpMainPageAudio as tlp

tlp.lvl_cMic.SetRange(-40, 12, 1)      #check these range numbers, might want to be smaller as well
tlp.lvl_cProg.SetRange(-40, 12, 2)

tag_dict = {tlp.btn_cProgMute: 'MuteProgram', tlp.btn_cMicMute: 'MuteSpeech'}

@eventEx([tlp.btn_cProgMute, tlp.btn_cMicMute], 'Pressed')
def MuteButtonPressed(button:tlp.Button, state):
    print('control', button.Name, state)
    curr = dvBiamp.ReadStatus('MuteControl', {'Instance Tag': tag_dict[button], 'Channel': '1'})
    if curr is 'Off':
        dvBiamp.SetMuteControl('On', {'Instance Tag': tag_dict[button], 'Channel': '1'})
    else:
        dvBiamp.SetMuteControl('Off', {'Instance Tag': tag_dict[button], 'Channel': '1'})
    dvBiamp.Update('MuteControl', {'Instance Tag': tag_dict[button], 'Channel': '1'})

def MicMuteChanged(command, value, qualifier):
    print(command, value, qualifier)
    tlp.btn_cMicMute.SetState(1 if value is 'On' else 0)
    

def ProgMuteChanged(command, value, qualifier):
    print(command, value, qualifier)
    tlp.btn_cProgMute.SetState(1 if value is 'On' else 0)

dvBiamp.SubscribeStatus('MuteControl', {'Instance Tag': 'MuteSpeech', 'Channel': '1'}, MicMuteChanged)
dvBiamp.SubscribeStatus('MuteControl', {'Instance Tag': 'MuteProgram', 'Channel': '1'}, ProgMuteChanged)

def MicVolChanged(command, value, qualifier):
    print(command, value, qualifier)
    tlp.lvl_cMic.SetLevel(int(value))

def ProgVolChanged(command, value, qualifier):
    print(command, value, qualifier)
    tlp.lvl_cProg.SetLevel(int(value))

dvBiamp.SubscribeStatus('LevelControl', {'Instance Tag': 'LevelSpeech', 'Channel': '1'}, MicVolChanged)
dvBiamp.SubscribeStatus('LevelControl', {'Instance Tag': 'LevelProgram', 'Channel': '1'}, ProgVolChanged)

mic_list = [tlp.btn_cMicDown, tlp.btn_cMicUp]
prog_list = [tlp.btn_cProgDown, tlp.btn_cProgUp]
tot_list = [tlp.btn_cMicDown, tlp.btn_cMicUp, tlp.btn_cProgDown, tlp.btn_cProgUp]

@eventEx(tot_list, ['Pressed', 'Repeated'])
def MicControl(button:tlp.Button, state):
    print(button.Name, button.Host, state)
    if button in mic_list:
        if button is mic_list[0]:
            tlp.lvl_cMic.Dec()
        else:
            tlp.lvl_cMic.Inc()
        dvBiamp.SetLevelControl(tlp.lvl_cMic.Level, {'Instance Tag': 'LevelSpeech', 'Channel': '1'})

    else:
        if button is prog_list[0]:
            tlp.lvl_cProg.Dec()
        else:
            tlp.lvl_cProg.Inc()
        dvBiamp.SetLevelControl(tlp.lvl_cProg.Level, {'Instance Tag': 'LevelProgram', 'Channel': '1'})

"""
r = True

def FlipLabel(timer:Timer, count):
    global r
    print(r)
    tlp.lbl_micNotR.SetVisible(r)
    r = not r
    if count >= 60:
        timer.Stop()

SpeechTimer = Timer(1, FlipLabel)

def SpeechPresent(command, value, qualifier):
    print(value)
    if value == 'Signal Present':
        SpeechTimer.Stop()
        tlp.lbl_Speech.SetVisible(True)
        tlp.lbl_micNotR.SetVisible(False)
        tlp.lbl_micNotW.SetVisible(False)
    else:
        tlp.lbl_Speech.SetVisible(False)
        tlp.lbl_micNotW.SetVisible(True)
        SpeechTimer.Restart()     
    
dvBiamp.SubscribeStatus('SignalPresentMeter', {'Instance Tag': 'SpeechPresent', 'Channel': '1', 'Meter Name': 'Speech'}, SpeechPresent)
"""