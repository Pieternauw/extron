"""
This file defines the BluRay control response. When a button is pressed, the matching command
is sent out. Buttons are named by commands to simplify the logic. Certain set commands take 
different arguments such as SetTransport() or SetMenuControl(). Using button names simplifies
the program and allows me to define different lists of buttons. If a matching button is found, 
it takes the name of that button and sends the command. The same goes for subtitle with my own defined 
SetSubtitle() command in the module file for the BluRay device. 

The disk tray is a special case. There is only an open and close command, but no way for me to know 
if the tray is already open or closed in the extron module. To work around this I define my own 
Tray commands, using the disk tray commands provided but based on status the device sends me. 

Using SendAndWait() I can ask the device for its status on some command, and assign the response to a variable. 
By decoding the variable I can check if a certain string is in the response and do something if it is. 
In this case if the tray is open, the device sends back a string with TTO included. There are more parts to the
string but that's the only difference between open and closed. Closed responds TTC. If the string returned 
has TTO in it, I send the tray command to close. Otherwise, I send the open command. 
"""

import ui.tlpBluray as tlp 

from devices import dvBluray

from modules.helper.ModuleSupport import eventEx 

transport_set = [tlp.btn_blurayStop, tlp.btn_blurayPlay, tlp.btn_blurayPause, 
                 tlp.btn_blurayRTrack, tlp.btn_blurayFTrack]

menu_set = [tlp.btn_blurayDown, tlp.btn_blurayRight, tlp.btn_blurayUp, 
            tlp.btn_blurayLeft, tlp.btn_blurayEnter, tlp.btn_blurayReturn, 
            tlp.btn_blurayHome, tlp.btn_blurayOption, tlp.btn_blurayMenu]

scan_set = [tlp.btn_blurayRewind, tlp.btn_blurayFForward]

@eventEx([tlp.btn_blurayStop, tlp.btn_blurayPlay, tlp.btn_blurayPause, 
          tlp.btn_blurayRTrack, tlp.btn_blurayFTrack, tlp.btn_blurayDown, 
          tlp.btn_blurayRight, tlp.btn_blurayUp, 
          tlp.btn_blurayLeft, tlp.btn_blurayEnter, tlp.btn_blurayReturn, 
          tlp.btn_blurayHome, tlp.btn_blurayOption, tlp.btn_blurayMenu, 
          tlp.btn_blurayRewind, tlp.btn_blurayFForward, tlp.btn_blurayEject, 
          tlp.btn_bluraySub], 'Pressed')
def TransportEvent(button:tlp.Button, state):
    print(button.Name, button.Host, state, 'Control')
    if button in transport_set:
        dvBluray.SetTransport(button.Name, None)
    elif button in menu_set:
        dvBluray.SetMenuControl(button.Name, None)
    elif button in scan_set:
        dvBluray.SetScan('{}'.format(button.Name), {'Speed': 'Slow'})
    elif button is tlp.btn_bluraySub:
        dvBluray.SetSubtitle(None, None)
    elif button is tlp.btn_blurayEject:
        #TODO -  Send bluray command - a receiveData event will be triggered and that's where I'll handle the control
        response = dvBluray.SendAndWait('!7?MST\r', 2)
        print(response)
        if response:
            blurayResp = response.decode()
            if 'TTO' in blurayResp:
                dvBluray.SetDiscTray('Close', None)
            else:
                dvBluray.SetDiscTray('Open',None)
