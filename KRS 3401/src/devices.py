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
from extronlib.interface import EthernetClientInterface, RelayInterface
# Project import
import modules.device.extr_Scaler_IN806_IN1808_Series_v1_1_6_0 as modScalar
import modules.device.epsn_vp_CB_EB_PowerLite_L630U_Series_v1_0_4_0 as Projector

from modules.helper.ConnectionHandler import GetConnectionHandler
from modules.helper.ModuleSupport import eventEx
from modules.helper.gve_interface import gveClient

import variables as var
# Define devices
dvIPCP = ProcessorDevice('ProcessorAlias')
dvTLP = UIDevice('PanelAlias')

GVEServer = gveClient('128.114.104.109', dvIPCP)

TLP_ID = 'Touchpanel'; PRJF_ID = 'ProjectorFront'; PRJB_ID = 'ProjectorBack'; SW_ID = 'Switcher'; BLU_ID = 'Bluray'; IPCP_ID = 'IPCP'

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

dvPRJFront = GetConnectionHandler(Projector.SerialOverEthernetClass('10.10.2.30', 2003, Model='PowerLite L630U'), 'Power', pollFrequency=30)
dvPRJBack = GetConnectionHandler(Projector.SerialClass(dvIPCP, 'COM1', Model='Powerlite L630U'), 'Power', pollFrequency=30)

prj_dict = {dvPRJFront: PRJF_ID, dvPRJBack: PRJB_ID}

@eventEx([dvPRJFront, dvPRJBack], ['Connected', 'Disconnected'])
def ProjectorConnectionHandler(client:EthernetClientInterface, state):
    print('Projector on IP {0} is {1}'.format(client.IPAddress, state))
    GVEServer.SendStatus(prj_dict[client], 'Connection', state)
    if state is not 'Connected':
        client.Connect(5) 

device_dict = {dvTLP: TLP_ID, dvIPCP: IPCP_ID}

@eventEx([dvTLP, dvIPCP], ['Offline', 'Online'])
def TLPOff(device, state):
    GVEServer.SendStatus(device_dict[device], 'Connection', state)
