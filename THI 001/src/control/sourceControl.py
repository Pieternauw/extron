#extron Import
from modules.helper.ModuleSupport import eventEx 

#Project Import 
import ui.tlp as tlp 
import variables as var
import control.advancedControl as adv

#Device Imports
from devices import dvScalar, dvPRJ, dvCynap, GVEServer, PRJ_ID # , dvBluray

input_popup_list = ['Laptop Connected popup', 'wireless popup', 
              'Document camera instruction popup', 'Mac Help popup', 'BluRay control popup']

source_list = ['LAPTOP HDMI', 'WIRELESS', 'DOC CAM', 'INSTRUCTOR PC', 'BLU RAY']

@eventEx(tlp.input_set.Objects, 'Pressed')
def ControlInput(button:tlp.Button, state):
    print(button.Name, state, 'Control')
    ID = tlp.input_set.Objects.index(button)
    dvScalar.SetInput('{}'.format(ID + 2), {'Type': 'Audio/Video'})
    dvScalar.SetVideoMute('Off', {'Output': '1A'})
    dvPRJ.SetPower('On', None) 
    tlp.dvTLP.HideAllPopups()
    tlp.dvTLP.ShowPopup(input_popup_list[ID])
    if button is tlp.btn_sourceWireless: tlp.dvTLP.ShowPopup('wireless select device')
    tlp.input_set.SetCurrent(ID)
    adv.PRJStatusTimer.Restart()
    tlp.wireless_btn_help_set.SetCurrent(None)
    GVEServer.SendStatus(PRJ_ID, 'Source', source_list[ID])
    # if button is tlp.btn_sourceBluray: dvBluray.Set('Power', 'On')
    
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

@eventEx(tlp.btn_wirelessDisconnect, ['Pressed', 'Released'])
def DisconnectPresentation(button:tlp.Button, state):
    button.SetState(1 if state is 'Pressed' else 0)
    dvCynap.Set('EndPresentation', None, {'Delete Recordings Folder': 'Yes', 'Delete Snapshots Folder': 'Yes', 'Power Off Mode': 'New Presentation'})
    