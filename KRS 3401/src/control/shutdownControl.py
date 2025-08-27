from devices import dvScalar, dvPRJBack, dvPRJFront, dvTLP, dvRelay, GVEServer, PRJF_ID, PRJB_ID

from modules.helper.ModuleSupport import eventEx 

from extronlib.system import Clock, Wait
from extronlib.ui import Button

import ui.tlp as tlp
from control.advancedControl import PRJTimer

def DefaultCalls():
    dvPRJBack.Set('AVMute', 'Off')
    dvPRJFront.Set('AVMute', 'Off')
    tlp.adv.btn_blankImg.SetState(0)

    tlp.MainAudio.lvl_mic.SetLevel(-18)
    tlp.MainAudio.lvl_prog.SetLevel(-18)
    dvScalar.SetGroupProgramVolume(-18, None)
    dvScalar.SetGroupMicVolume(-18, None)
        
    tlp.btn_videoMute.SetState(0)   

def Startup():
    DefaultCalls()
    
    print('Startup running')
    #turn off mic and program mutes
    #visual feedback handled by SubscribeStatus()
    dvScalar.SetGroupProgramMute('Off', None)
    dvScalar.SetGroupMicMute('Off', None)
    
    #turn off video mute
    dvScalar.SetVideoMute('Off', {'Output': '1B'})
    dvScalar.SetVideoMute('Off', {'Output': '1A'})
    
    
    #main page shown, function called after successful passcode entry
    dvTLP.ShowPage('Main Page')
    
    #unlock drawer
    dvRelay.SetState('Close')
    
def Shutdown():
    DefaultCalls()
    
    dvPRJBack.SetPower('Off', None)
    dvPRJFront.SetPower('Off', None)
    PRJTimer.Restart()
        
    tlp.input_set.SetCurrent(None)
    dvScalar.SetInput('3', {'Type': 'Audio/Video'})
    
    GVEServer.SendStatus(PRJF_ID, 'Source', 'SYSTEM OFF')
    GVEServer.SendStatus(PRJB_ID, 'Source', 'SYSTEM OFF')
    
    dvScalar.SetVideoMute('On', {'Output': '1B'})
    dvScalar.SetVideoMute('Off', {'Output': '1A'})
    
    dvTLP.HideAllPopups()
    dvTLP.ShowPage('Start Page')
    dvRelay.SetState('Open')
    
@eventEx(tlp.btn_shdnYes, 'Pressed')
def ShutdownControl(button:tlp.Button, state):
    Shutdown()
    
def ShutdownSystem(clock, dt):
    Shutdown()
    
ShutdownClock = Clock(['23:00:00'], None, ShutdownSystem)
ShutdownClock.Enable()

btn_start = Button(dvTLP, 19)
@eventEx(btn_start, 'Pressed')
def ShowMain(button:Button, state):
    Startup()