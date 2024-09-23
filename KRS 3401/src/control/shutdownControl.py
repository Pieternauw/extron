from devices import dvScalar, dvPRJBack, dvPRJFront, dvTLP, dvRelay

from modules.helper.ModuleSupport import eventEx 

from extronlib.system import Clock 

import ui.tlp as tlp

def Startup():
    #set default mic and prog volume levels
    tlp.MainAudio.lvl_mic.SetLevel(-18)
    tlp.MainAudio.lvl_prog.SetLevel(-18)
    dvScalar.SetGroupProgramVolume(-18, None)
    dvScalar.SetGroupMicVolume(-18, None)
    
    #turn off mic and program mutes
    #visual feedback handled by SubscribeStatus()
    dvScalar.SetGroupProgramMute('Off', None)
    dvScalar.SetGroupMicMute('Off', None)
    
    #turn off video mute
    dvScalar.SetGlobalVideoMute('Off', None)
    tlp.btn_videoMute.SetState(0)   

    dvPRJBack.Set('AVMute', 'Off')
    dvPRJFront.Set('AVMute', 'Off')
    dvPRJFront.Update('AVMute')
    
    #main page shown, function called after successful passcode entry
    dvTLP.ShowPage('Main Page')
    #unlock drawer
    dvRelay.SetState('Close')
    
def Shutdown():
    dvPRJBack.SetPower('Off', None)
    dvPRJFront.SetPower('Off', None)
    dvPRJFront.Update('Power')
        
    tlp.input_set.SetCurrent(None)
    dvScalar.SetInput('3', {'Type': 'Audio/Video'})
    
    tlp.MainAudio.lvl_mic.SetLevel(-18)
    tlp.MainAudio.lvl_prog.SetLevel(-18)
    
    dvScalar.SetGroupProgramVolume(-18, None)
    dvScalar.SetGroupMicVolume(-18, None)
    
    dvScalar.SetGlobalVideoMute('Off', None)
    tlp.btn_videoMute.SetState(0)   

    dvPRJBack.Set('AVMute', 'Off')
    dvPRJFront.Set('AVMute', 'Off')
    dvPRJFront.Update('AVMute')
    
    dvTLP.HideAllPopups()
    dvTLP.ShowPage('Start Page')
    dvRelay.SetState('Open')
    
@eventEx(tlp.btn_shdnYes, 'Pressed')
def ShutdownControl(button:tlp.Button, state):
    Shutdown()
    
def ShutdownSystem(clock, dt):
    Shutdown()
    
Shutdown = Clock(['23:00:00'], None, ShutdownSystem)
Shutdown.Enable()