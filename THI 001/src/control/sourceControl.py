"""
The source control file handles switching inputs based on button input. It also takes in a popup list
and switches popups depending on what input was selected. It also includes the laptop feedback which 
informs the user if their laptop was detected or not. This feedback also uses the SubscribeStatus() 
function to keep track of the input signal status on input 2 where the winder cable terminates. 

In this file is also shutdown control instructions, telling the projector to turn off and telling 
the switcher to swap to input 3 (the cynap) which is the default in all room shutdown processes. 
In the next revision there will be relay commands on shutdown to handle the mic drawer closing. 
"""

#extron Import
from modules.helper.ModuleSupport import eventEx 

#Project Import 
import ui.tlp as tlp 
import variables as var
import control.advancedControl as adv

#Device Imports
from devices import dvScalar, dvPRJ

input_popup_list = ['Laptop Connected popup', 'wireless popup', 
              'Document camera instruction popup', 'Mac Help popup', 'BluRay control popup']

@eventEx(tlp.input_set.Objects, 'Pressed')
def ControlInput(button:tlp.Button, state):
    print(button.Name, state, 'Control')
    dvScalar.SetInput('{}'.format(tlp.input_set.Objects.index(button) + 2), {'Type': 'Audio/Video'})
    dvPRJ.SetPower('On', None) 
    tlp.dvTLP.HideAllPopups()
    tlp.dvTLP.ShowPopup(input_popup_list[tlp.input_set.Objects.index(button)])
    if button is tlp.btn_sourceWireless: tlp.dvTLP.ShowPopup('wireless select device')
    tlp.input_set.SetCurrent(button)
    adv.PRJStatusTimer.Restart()
    tlp.wireless_btn_help_set.SetCurrent(None)
    
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
