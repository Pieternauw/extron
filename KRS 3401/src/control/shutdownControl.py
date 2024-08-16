from devices import dvScalar, dvPRJBack, dvPRJFront, dvTLP, dvRelay

from modules.helper.ModuleSupport import eventEx 

from extronlib.system import Clock 

import ui.tlp as tlp

def ShutdownRoutine():
    dvPRJBack.SetPower('Off', None)
    dvPRJFront.SetPower('Off', None)
    dvPRJFront.Update('Power')
    
    dvRelay.SetState('Open')
    
    tlp.input_set.SetCurrent(None)
    
    tlp.MainAudio.lvl_mic.SetLevel(-18)
    tlp.MainAudio.lvl_prog.SetLevel(-18)
    
    dvScalar.SetGroupProgramVolume(-18, None)
    dvScalar.SetGroupMicVolume(-18, None)
    
    dvScalar.SetInput('3', {'Type': 'Audio/Video'})
    
    dvTLP.ShowPage('Start Page')
    dvTLP.HideAllPopups()
    
@eventEx(tlp.btn_shdnYes, 'Pressed')
def ShutdownControl(button:tlp.Button, state):
    ShutdownRoutine()
    
def ShutdownSystem(clock, dt):
    ShutdownRoutine()
    
Shutdown = Clock(['23:00:00'], None, ShutdownSystem)
Shutdown.Enable()