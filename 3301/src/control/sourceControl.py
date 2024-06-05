#extron Import
from modules.helper.ModuleSupport import eventEx 

#Project Import 
import ui.tlp as tlp 

#Device Imports
from devices import dvScalar, dvPRJ

input_popup_list = ['Laptop Connected popup', 'Wireless insturction popup', 
              'Document camera instruction popup', 'BluRay control popup']

@eventEx(tlp.input_set.Objects, 'Pressed')
def ControlInput(button:tlp.Button, state):
    print(button.Name, state, 'Control')
    dvScalar.SetInput('{}'.format(tlp.input_set.Objects.index(button) + 2), {'Type': 'Audio/Video'})
    dvPRJ.Set('Power', 'On') 
    tlp.dvTLP.HideAllPopups()
    tlp.dvTLP.ShowPopup(input_popup_list[tlp.input_set.Objects.index(button)])
    tlp.input_set.SetCurrent(button)
    
@eventEx(tlp.btn_videoMute, 'Pressed')
def VideoMuteControl(button:tlp.Button, state):
    if button.State == 0:
        dvScalar.SetGlobalVideoMute('On', None)
        button.SetState(1)
    else:
        dvScalar.SetGlobalVideoMute('Off', None)
        button.SetState(0)   
     
def LaptopConnectedFeedback(command, value, qualifier):
    print(command, value, qualifier)
    if value == 'Active':
        tlp.btn_laptopConnectedFeedback.SetState(1)
        tlp.lblLaptopConnected.SetText('Connected')
    else:
        tlp.btn_laptopConnectedFeedback.SetState(0)
        tlp.lblLaptopConnected.SetText('Not Connected')
        
    
dvScalar.SubscribeStatus('InputSignalStatus', {'Input': '2'}, LaptopConnectedFeedback)

@eventEx(tlp.btn_shdnYes, 'Pressed')
def ShutdownControl(button:tlp.Button, state):
    dvScalar.SetInput('3', {'Type': 'Audio/Video'})
    dvPRJ.SetPower('Off', None)
    tlp.input_set.SetCurrent(None)