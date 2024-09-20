from devices import dvScalar, dvPRJ, dvTLP, dvRelay

from modules.helper.ModuleSupport import eventEx 

from extronlib.system import Clock 

import ui.tlp as tlp

def StartupAndShutdown():
    dvPRJ.SetPower('Off', None)
    dvPRJ.Update('Power')
        
    tlp.input_set.SetCurrent(None)
    
    tlp.MainAudio.lvl_mic.SetLevel(-18)
    tlp.MainAudio.lvl_prog.SetLevel(-18)
    
    dvScalar.SetGroupProgramVolume(-18, None)
    dvScalar.SetGroupMicVolume(-18, None)
    
    dvScalar.SetInput('3', {'Type': 'Audio/Video'})
    dvTLP.HideAllPopups()
    
@eventEx(tlp.btn_shdnYes, 'Pressed')
def ShutdownControl(button:tlp.Button, state):
    StartupAndShutdown()
    dvTLP.ShowPage('Start Page')
    dvRelay.SetState('Open')
    
def ShutdownSystem(clock, dt):
    StartupAndShutdown()
    dvTLP.ShowPage('Start Page')
    dvRelay.SetState('Open')
    
Shutdown = Clock(['23:00:00'], None, ShutdownSystem)
Shutdown.Enable()