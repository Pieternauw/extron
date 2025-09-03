"""
This is the place to put control code for various types of systems (e.g. AV, Building Management).
The core purpose is for separation of concerns. Each concern should be as isolated as possible,
taking advantage of the framework structure and helper modules.

Examples:

* AV devices
* Building management systems
  * Lighting
  * HVAC
* Cloud Services
"""

# Python imports

# Extron Library imports
from modules.helper.ModuleSupport import eventEx 
from devices import dvSW, dvPRJA, dvPRJB, dvCynap, GVEServer, PRJA_ID, PRJB_ID

import ui.nbp as nbp

"""
Requirements
- 4 source buttons. Both panels must display same highlights for sources
- NBPA buttons turn on/off PRJA, NBPB buttons turn on/off PRJB
- Audio levels must be tied together. 
- Projector On must enable either audio in 1 or 2 depending on which NBP selected
- In 5 might be camera + audio feed for yuja (?)
"""

#TODO define source switching logic
#TODO define projector on/off logic

# Project imports

src_list = ['LAPTOP', 'WIRELESS', 'BLURAY']

prgVol = -24

@eventEx(nbp.srcA_set.Objects, ['Pressed', 'Released'])
def ASourcePressed(button:nbp.Button, state):
    ID = nbp.srcA_set.Objects.index(button)
    dvSW.Set('Input', '{}'.format(ID + 1))
    nbp.srcA_set.SetCurrent(ID)
    nbp.srcB_set.SetCurrent(ID)
    
@eventEx(nbp.srcB_set.Objects, ['Pressed', 'Released'])
def BSourcePressed(button:nbp.Button, state):
    ID = nbp.srcB_set.Objects.index(button)
    dvSW.Set('Input', '{}'.format(ID + 1))
    nbp.srcA_set.SetCurrent(ID)
    nbp.srcB_set.SetCurrent(ID)
    
@eventEx(nbp.prjA_set.Objects, ['Pressed', 'Released'])
def APRJPressed(button:nbp.Button, state):
    pwr = 'On' if button is nbp.btn_prjAOn else 'Off'
    dvPRJA.Set('Power', pwr)
    GVEServer.SendStatus(PRJA_ID, 'Power', pwr)
    nbp.prjA_set.SetCurrent(button)    
    
@eventEx(nbp.prjB_set.Objects, ['Pressed', 'Released'])
def BPRJPressed(button:nbp.Button, state):
    pwr = 'On' if button is nbp.btn_prjBOn else 'Off'
    dvPRJB.Set('Power', pwr)
    GVEServer.SendStatus(PRJB_ID, 'Power', pwr)
    nbp.prjB_set.SetCurrent(button)    
    
@eventEx([nbp.btn_srcA2, nbp.btn_srcB2], 'Held')
def WirelessDisconnect(button:nbp.Button, state):
    dvCynap.Set('EndPresentation', None, {'Deete Recordings Folder': 'Yes', 'Delete Snapshots Folder': 'Yes', 'Power Off Mode': 'New Presentation'})
    
@eventEx([nbp.kb_A, nbp.kb_B], 'Turned')
def KnobATurned(knob:nbp.Knob, direction):
    global prgVol
    if direction > 0:
        for i in range(direction):
            prgVol += 1
    else:
        for i in range(direction):
            prgVol -= 1
    dvSW.Set('GroupProgramVolume', prgVol)
    nbp.lvl_A.SetLevel(prgVol)
    nbp.lvl_B.SetLevel(prgVol)
    
def ProjectorPowerA(command, value, qualifier):
    source = dvSW.ReadStatus('Input')
    GVEServer.SendStatus(PRJA_ID, 'Source', src_list[source - 1] if value is 'On' else 'SYSTEM OFF')
    GVEServer.SendStatus(PRJA_ID, command, value)
    
        
def ProjectorPowerB(command, value, qualifier):
    source = dvSW.ReadStatus('Input')
    GVEServer.SendStatus(PRJB_ID, 'Source', src_list[source - 1] if value is 'On' else 'SYSTEM OFF')
    GVEServer.SendStatus(PRJB_ID, command, value)

    
dvPRJA.SubscribeStatus('Power', None, ProjectorPowerA)
dvPRJB.SubscribeStatus('Power', None, ProjectorPowerB)