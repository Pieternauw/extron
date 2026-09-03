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
from devices import dvDPRJDoor, dvDPRJWall

import ui.nbp as nbp

@eventEx(nbp.door_set.Objects, 'Pressed')
def DoorPRJ(button:nbp.Button, state):
	dvDPRJDoor.SetPower('On' if button is nbp.btn_doorOn else 'Off')
	dvDPRJDoor.Update('Power')

def DoorPowerState(command, value, qualifier):
	nbp.door_set.SetCurrent(nbp.btn_doorOn if value == 'On' else nbp.btn_doorOff)

dvDPRJDoor.SubscribeStatus('Power', None, DoorPowerState)

@eventEx(nbp.wall_set.Objects, 'Pressed')
def DoorPRJ(button:nbp.Button, state):
	dvDPRJWall.SetPower('On' if button is nbp.btn_wallOn else 'Off')
	dvDPRJWall.Update('Power')

def WallPowerState(command, value, qualifier):
	nbp.wall_set.SetCurrent(nbp.btn_wallOn if value == 'On' else nbp.btn_wallOff)

dvDPRJWall.SubscribeStatus('Power', None, WallPowerState)

@eventEx(nbp.btn_doorMute, 'Pressed')
def DoorMute(button:nbp.Button, state):
	dvDPRJDoor.SetAVMute('On' if button.State is 0 else 'Off', None)
	dvDPRJDoor.Update('AVMute')

def DoorMuteResponse(command, value, qualifier):
	nbp.btn_doorMute.SetState(1 if value is 'On' else 0)

dvDPRJDoor.SubscribeStatus('AVMute', None, DoorMuteResponse)
	
@eventEx(nbp.btn_wallMute, 'Pressed')
def WallMute(button:nbp.Button, state):
	dvDPRJWall.SetAVMute('On' if button.State is 0 else 'Off', None)
	dvDPRJWall.Update('AVMute')

def WallMuteResponse(command, value, qualifier):
	nbp.btn_wallMute.SetState(1 if value is 'On' else 0)

dvDPRJWall.SubscribeStatus('AVMute', None, WallMuteResponse)
