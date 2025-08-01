#extron Import
from modules.helper.ModuleSupport import eventEx 

#Project Import 
import ui.tlp as tlp 
import variables as var
import control.advancedControl as adv

#Device Imports
from devices import dvScalar, dvPRJ, GVEServer, PRJ_ID

input_popup_list = ['Laptop Connected popup', 'wireless popup', 
              'Document camera instruction popup', 'Mac Help popup', 'BluRay control popup']

source_list = ['LAPTOP HDMI', 'WIRELESS', 'DOC CAM', 'INSTRUCTOR PC', 'BLU RAY']

@eventEx(tlp.input_set.Objects, 'Pressed')
def ControlInput(button:tlp.Button, state):
    print(button.Name, state, 'Control')
    dvScalar.SetInput('{}'.format(tlp.input_set.Objects.index(button) + 2), {'Type': 'Audio/Video'})
    dvScalar.SetVideoMute('Off', {'Output': '1A'})
    dvPRJ.SetPower('On', None) 
    tlp.dvTLP.HideAllPopups()
    tlp.dvTLP.ShowPopup(input_popup_list[tlp.input_set.Objects.index(button)])
    if button is tlp.btn_sourceWireless: tlp.dvTLP.ShowPopup('wireless select device')
    tlp.input_set.SetCurrent(button)
    adv.PRJStatusTimer.Restart()
    tlp.wireless_btn_help_set.SetCurrent(None)
    GVEServer.SendStatus(PRJ_ID, 'Source', source_list[tlp.input_set.Objects.index(button)])
    
@eventEx(tlp.btn_videoMute, 'Pressed')
def VideoMuteControl(button:tlp.Button, state):
    if button.State == 0:
        dvScalar.SetVideoMute('On', {'Output': '1B'})
        button.SetState(1)
    else:
        dvScalar.SetVideoMute('Off', {'Output': '1B'})
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
