"""
This is the place to define each of the devices in the system.
* Extron control devices (e.g. all extronlib.device objects)
* Non-control devices and services (e.g. device modules)
* User defined devices (e.g. all extronlib.interface objects or custom python coded devices)

Note: This is for definition only.  Connection and logic defined in system.py (see below).
"""

# Python imports

# Extron Library imports
from extronlib.device import ProcessorDevice, UIDevice
from extronlib.system import Timer, ProgramLog
from extronlib.interface import EthernetClientInterface, RelayInterface
# Project import
import modules.device.extr_Scaler_IN806_IN1808_Series_v1_1_6_0 as modScalar
import modules.device.epsn_vp_CB_EB_PowerLite_L630U_Series_v1_0_4_0 as Projector
import modules.device.tasc_bluray_BD_MP4K_v1_0_0_0 as Bluray
import modules.device.wolf_cs_Cynap_Core_Pure_Pro_v1_1_1_0 as Cynap

from modules.helper.ConnectionHandler import GetConnectionHandler
from modules.helper.ModuleSupport import eventEx
from modules.helper.gve_interface import gveClient

import variables as var
# Define devices
dvIPCP = ProcessorDevice('ProcessorAlias')
dvTLP = UIDevice('PanelAlias')

#TODO - work in progress, test in a room if possible 
GVEServer = gveClient('128.114.104.109', dvIPCP)

TLP_ID = 'Touchpanel'; PRJ_ID = 'Projector'; SW_ID = 'Switcher'; BLU_ID = 'Bluray'; IPCP_ID = 'IPCP'; CY_ID = 'Cynap'

dvRelay = RelayInterface(dvIPCP, 'RLY1')

dvScalar = modScalar.SSHClass('10.10.2.30', 22023, Credentials=('admin', 'wag2748'), Model='IN1808 IPCP MA 70')
dvScalar = GetConnectionHandler(dvScalar, 'Temperature', pollFrequency=30)         

@eventEx(dvScalar, ['Connected', 'Disconnected'])
def SwitcherConnectionHandler(client:EthernetClientInterface, state):
    print('Switcher on IP {0} is {1}'.format(client.IPAddress, state))
    GVEServer.SendStatus(SW_ID, 'Connection', state)
    if state is 'Connected':
        #Update Calls
        client.Update('InputSignalStatus', {'Input': '2'})
        client.Update('GroupProgramMute')
        client.Update('GroupProgramVolume')
        client.Update('GroupMicMute')
        client.Update('GroupMicVolume')
        client.SetGroupProgramVolume(var.prog_val, None)
        client.SetGroupMicVolume(var.mic_val, None)
    else:
        client.Connect(5)

dvBluray = Bluray.EthernetClass('10.10.2.70', 9030, Model='BD-MP4K')

def ConnectBluray(timer:Timer, count):
    dvBluray.Connect(5)

BlurayConnectionTimer = Timer(5, ConnectBluray)
BlurayConnectionTimer.Stop()

@eventEx(dvBluray, ['Connected', 'Disconnected'])
def BlurayConnectionHandler(client:EthernetClientInterface, state):
    print('Bluray on IP {0} is {1}'.format(client.IPAddress, state))
    GVEServer.SendStatus(BLU_ID, 'Connection', state)
    if state is 'Connected':
        client.StartKeepAlive(30, '!7?SST\r')
    else:
        client.StopKeepAlive()
        BlurayConnectionTimer.Restart()

dvPRJ = GetConnectionHandler(Projector.SerialOverEthernetClass('10.10.2.30', 2003, Model='PowerLite L630U'), 'LampUsage', pollFrequency=30)

@eventEx(dvPRJ, ['Connected', 'Disconnected'])
def ProjectorConnectionHandler(client:EthernetClientInterface, state):
    print('Projector on IP {0} is {1}'.format(client.IPAddress, state))
    GVEServer.SendStatus(PRJ_ID, 'Connection', state)
    if state is not 'Connected':
        client.Connect(5)

def LampUpdate(command, value, qualifier):
    GVEServer.SendStatus(PRJ_ID, 'Lamp 1 Hours', value)

dvPRJ.SubscribeStatus('LampUsage', None, LampUpdate)

dvCynap = Cynap.EthernetClass('128.114.159.233', 50915, Model='Cynap Pure Pro')
dvCynap = GetConnectionHandler(dvCynap, 'BYODPinDisplay', pollFrequency=30)

@eventEx(dvCynap, ['Connected', 'Disconnected'])
def CynapConnected(client:EthernetClientInterface, state):
    print('Cynap on IP {0} is {1}'.format(client.IPAddress, state))
    GVEServer.SendStatus(CY_ID, 'Connection', state)
    if state is not 'Connected':
        client.Connect(5)

device_dict = {dvTLP: TLP_ID, dvIPCP: IPCP_ID}

@eventEx([dvTLP, dvIPCP], ['Offline', 'Online'])
def TLPOff(device, state):
    GVEServer.SendStatus(device_dict[device], 'Connection', state)

