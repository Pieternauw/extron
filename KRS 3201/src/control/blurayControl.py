import ui.tlpBluray as tlp 

from devices import dvBluray

from modules.helper.ModuleSupport import eventEx 

transport_set = {tlp.btn_blurayStop: 'Stop', tlp.btn_blurayPlay:'Play', 
                   tlp.btn_blurayPause: 'Play Pause', tlp.btn_blurayRTrack: 'Track Skip Previous', 
                   tlp.btn_blurayFTrack: 'Track Skip Next', tlp.btn_blurayRewind: 'Rewind', 
                   tlp.btn_blurayFForward: 'Fast Forward'}

menu_set = {tlp.btn_blurayDown: 'Down', tlp.btn_blurayRight: 'Right', tlp.btn_blurayUp: 'Up', 
              tlp.btn_blurayLeft: 'Left', tlp.btn_blurayEnter: 'Enter', tlp.btn_blurayReturn: 'Return', 
              tlp.btn_blurayHome: 'Home', tlp.btn_blurayOption: 'Option Menu', tlp.btn_blurayMenu: 'Setup Menu'}

#Defines an event for every single button on the bluray page.
@eventEx([tlp.btn_blurayStop, tlp.btn_blurayPlay, tlp.btn_blurayPause, 
    tlp.btn_blurayRTrack, tlp.btn_blurayFTrack, tlp.btn_blurayDown, 
    tlp.btn_blurayRight, tlp.btn_blurayUp, 
    tlp.btn_blurayLeft, tlp.btn_blurayEnter, tlp.btn_blurayReturn, 
    tlp.btn_blurayHome, tlp.btn_blurayOption, tlp.btn_blurayMenu, 
    tlp.btn_blurayRewind, tlp.btn_blurayFForward, tlp.btn_blurayEject, 
    tlp.btn_bluraySub], 'Pressed')
def TransportEvent(button:tlp.Button, state):
    print(button.Name, state, 'Control')
    #Transport set corresponds to buttons sent using SetTransport('<command>') in the device module
    if button in transport_set:
        dvBluray.SetTransport(transport_set[button], None)
    #Menu set corresponds to buttons sent using SetMenu('<command>') in the device module 
    elif button in menu_set:
        dvBluray.SetMenu(menu_set[button], None)
    #The SetSubtitle() command was created by us in our device module. For future projects always use a BluRay module included in one of the project folders to have access to the SetSubtitle command.
    elif button is tlp.btn_bluraySub:
        dvBluray.SetSubtitle(None, None)
    elif button is tlp.btn_blurayEject:
        #Response contains the device's binary response to the command sent. SendAndWait() sends the commmand and waits 2 seconds before continuing. 
        response = dvBluray.SendAndWait('!7?MST\r', 2)
        print(response)
        if response:
            #if a response was received, decode it into a string. 
            blurayResp = response.decode()
            #TTO is a piece of the command corresponding to if the disk tray is open. If it is, send command to close it. The whole response is longer than just TTO but that is the only piece that changes depending on state. 
            if 'TTO' in blurayResp:
                dvBluray.SetDiskTray('Close', None)
            else:
                dvBluray.SetDiskTray('Open', None)
    