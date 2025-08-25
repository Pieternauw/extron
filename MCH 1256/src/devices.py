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
from extronlib.interface import EthernetClientInterface

# Project imports
import modules.device.epsn_vp_BrightLink_BrightLinkPro_CB_EB_69x_14x as PRJ
import modules.device.extr_scaler_IN2004_Series_v1_0_0_0 as Scaler

from modules.helper.ConnectionHandler import GetConnectionHandler
from modules.helper.ModuleSupport import eventEx
from modules.helper.gve_interface import gveClient


# Define devices

dvIPCP = ProcessorDevice('ProcessorAlias')
dvNBPA = UIDevice('PanelA')
dvNBPB = UIDevice('PanelB')

dvSW = Scaler.SerialOverEthernetClass('128.114.0.4', 22023, Credentials=('admin', '100%Becknerized'), Model='DTP3 IN2004 DI/DO')
dvSW = GetConnectionHandler(dvSW, 'Temperature', pollFrequency=30)         


dvPRJA = GetConnectionHandler(PRJ.SerialOverEthernetClass('128.114.0.4', 2003, Model='EB-690U'), 'LampUsage', pollFrequency=30)
dvPRJB = GetConnectionHandler(PRJ.SerialClass(dvIPCP, 'COM1', Model='EB-690U'), 'LampUsage', pollFrequency=30)

IPCP_ID = 'IPCP'; NBPA_ID = 'NBPA'; NBPB_ID = 'NBPB'; SW_ID = 'SW'; PRJA_ID = 'PRJA'; PRJB_ID = 'PRJB'

GVEServer = gveClient('128.114.104.109', dvIPCP)

@eventEx(dvSW, ['Connected', 'Disconnected'])
def SwitcherConnectionHandler(client:EthernetClientInterface, state):
    print('Switcher on IP {0} is {1}'.format(client.IPAddress, state))
    GVEServer.SendStatus(SW_ID, 'Connection', state)
    if state is 'Connected':
        #Update Calls
        for cmd in ['GroupProgramMute', 'GroupProgramVolume', 'GroupMicMute', 'GroupMicVolume', 'Input']:
            client.Update(cmd)
        client.SetGroupProgramVolume(-24, None)
        client.SetGroupMicVolume(-24, None)
    else:
        client.Connect(5)
        
prj_list = {dvPRJA: PRJA_ID, dvPRJB: PRJB_ID}

@eventEx([dvPRJA, dvPRJB], ['Connected', 'Disconnected'])
def ProjectorConnectionHandler(client, state):
    GVEServer.SendStatus(prj_list[client], 'Connection', state)
    if state is not 'Connected':
        client.Connect(5)
def LampUpdateA(command, value, qualifier):
    GVEServer.SendStatus(PRJA_ID, 'Lamp 1 Hours', value)
   
dvPRJA.SubscribeStatus('LampUsage', None, LampUpdateA)

def LampUpdateB(command, value, qualifier):
    GVEServer.SendStatus(PRJB_ID, 'Lamp 1 Hours', value)

dvPRJB.SubscribeStatus('LampUsage', None, LampUpdateB)

device_dict = {dvNBPA: NBPA_ID, dvNBPB: NBPB_ID, dvIPCP: IPCP_ID}

@eventEx([dvNBPA, dvNBPB, dvIPCP], ['Offline', 'Online'])
def TLPOff(device, state):
    GVEServer.SendStatus(device_dict[device], 'Connection', state)


