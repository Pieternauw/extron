#extron Import
from modules.helper.ModuleSupport import eventEx 

#Project Import 
import ui.tlp as tlp 
import variables as var
import control.advancedControl as adv

#Device Imports
from devices import dvScalar, dvPRJ, PRJ_ID, GVEServer

input_popup_list = ['Laptop Connected popup', 'Wireless insturction popup', 
              'Document camera instruction popup', 'BluRay control popup']

source_list = ['LAPTOP HDMI', 'WIRELESS', 'DOC CAM', 'BLU RAY']

@eventEx(tlp.input_set.Objects, 'Pressed')
def ControlInput(button:tlp.Button, state):
    print(button.Name, state, 'Control')
    ID = tlp.input_set.Objects.index(button)
    dvScalar.SetInput('{}'.format(ID + 2), {'Type': 'Audio/Video'})
    dvPRJ.SetPower('On', None) 
    tlp.dvTLP.HideAllPopups()
    tlp.dvTLP.ShowPopup(input_popup_list[ID])
    tlp.input_set.SetCurrent(ID)
    adv.PRJStatusTimer.Restart()
    GVEServer.SendStatus(PRJ_ID, 'Source', source_list[ID])
    
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

tlp.btn_laptopConnectedFeedback.SetState(1 if dvScalar.ReadStatus('InputSignalStatus', {'Inpt': '1'}) is 'Active' else 0)
tlp.lblLaptopConnected.SetText('Connected' if dvScalar.ReadStatus('InputSignalStatus', {'Inpt': '1'}) is 'Active' else 'Not Connected')
        
dvScalar.SubscribeStatus('InputSignalStatus', {'Input': '2'}, LaptopConnectedFeedback)
