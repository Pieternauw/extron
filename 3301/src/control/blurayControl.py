import ui.tlpBluray as tlp 

from devices import dvBluray

from extronlib.system import Wait 
from modules.helper.ModuleSupport import eventEx 

transport_set = [tlp.btn_blurayStop, tlp.btn_blurayPlay, tlp.btn_blurayPause, 
                 tlp.btn_blurayRTrack, tlp.btn_blurayFTrack, tlp.btn_blurayRewind, 
                 tlp.btn_blurayFForward]

menu_set = [tlp.btn_blurayDown, tlp.btn_blurayRight, tlp.btn_blurayUp, 
            tlp.btn_blurayLeft, tlp.btn_blurayEnter, tlp.btn_blurayReturn, 
            tlp.btn_blurayHome, tlp.btn_blurayOption, tlp.btn_blurayMenu]


@eventEx([tlp.btn_blurayStop, tlp.btn_blurayPlay, tlp.btn_blurayPause, 
          tlp.btn_blurayRTrack, tlp.btn_blurayFTrack, tlp.btn_blurayDown, 
          tlp.btn_blurayRight, tlp.btn_blurayUp, 
          tlp.btn_blurayLeft, tlp.btn_blurayEnter, tlp.btn_blurayReturn, 
          tlp.btn_blurayHome, tlp.btn_blurayOption, tlp.btn_blurayMenu, 
          tlp.btn_blurayRewind, tlp.btn_blurayFForward, tlp.btn_blurayEject, 
          tlp.btn_bluraySub], 'Pressed')
def TransportEvent(button:tlp.Button, state):
    print(button.Name, state, 'Control')
    if button in transport_set:
        dvBluray.SetTransport(button.Name, None)
    elif button in menu_set:
        dvBluray.SetMenuControl(button.Name, None)
    elif button is tlp.btn_bluraySub:
        dvBluray.SetSubtitle(None, None)
    elif button is tlp.btn_blurayEject:
        response = dvBluray.SendAndWait('!7?MST\r', 2)
        print(response)
        if response:
            blurayResp = response.decode()
            if 'TTO' in blurayResp:
                dvBluray.SetDiscTray('Close', None)
            else:
                dvBluray.SetDiscTray('Open',None)
