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
from extronlib.interface import EthernetClientInterface, RelayInterface, SerialInterface
# Project import
import modules.device.extr_Scaler_IN806_IN1808_Series_v1_1_6_0 as modScalar
import modules.device.epsn_vp_CB_EB_PU100xx_PU2010x_Series_v1_0_2_0 as Projector
import modules.device.tasc_bluray_BD_MP1_v1_2_0_0 as Bluray
from modules.device import biam_dsp_TesiraSeries_v1_15_1_0 as Biamp

from modules.helper.ConnectionHandler import GetConnectionHandler
from modules.helper.ModuleSupport import eventEx
from modules.helper.gve_interface import gveClient

import variables as var
# Define devices
dvIPCP = ProcessorDevice('ProcessorAlias')
dvTLP = UIDevice('PanelAlias')

GVEServer = gveClient('128.114.104.109', dvIPCP)

TLP_ID = 'Touchpanel'; PRJ_ID = 'Projector'; SW_ID = 'Switcher'; BLU_ID = 'Bluray'; IPCP_ID = 'IPCP'; BMP_ID = 'Biamp'

dvRelay = RelayInterface(dvIPCP, 'RLY1')

dvBiamp = Biamp.SerialClass(dvIPCP, 'COM1', Baud=115200, Model='TesiraFORTE DAN AI')

dvScalar = modScalar.SSHClass('10.10.2.30', 22023, Credentials=('admin', 'wag2748'), Model='IN1806')
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

dvBluray = Bluray.EthernetClass('10.10.2.70', 9030, Model='BD-MP1')

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

dvPRJ = GetConnectionHandler(Projector.SerialOverEthernetClass('10.10.2.30', 2003, Model='EB-PU1008B'), 'LampUsage', pollFrequency=30)

@eventEx(dvPRJ, ['Connected', 'Disconnected'])
def ProjectorConnectionHandler(client:EthernetClientInterface, state):
    print('Projector on IP {0} is {1}'.format(client.IPAddress, state))
    GVEServer.SendStatus(PRJ_ID, 'Connection', state)

    if state is not 'Connected':
        client.Connect(5)

dvBiamp = GetConnectionHandler(dvBiamp, 'MuteControl', keepAliveQueryQualifier={'Instance Tag': 'MuteProgram', 'Channel': '1'}, pollFrequency=30)

@eventEx(dvBiamp, ['Connected', 'Disconnected'])
def BiampConnectionHandler(client:SerialInterface, state):
    GVEServer.SendStatus(BMP_ID, 'Connection', state)
    if state is 'Connected':    
        #these need to be called whenever - write an update function for whenever I need newest status in main code to return value
        dvBiamp.Update('MuteControl', {'Instance Tag': 'MuteProgram', 'Channel': '1'})
        dvBiamp.Update('MuteControl', {'Instance Tag': 'MuteSpeech', 'Channel': '1'})
    else:
        client.Connect(5)


def LampUpdate(command, value, qualifier):
    GVEServer.SendStatus(PRJ_ID, 'Lamp 1 Hours', value)

dvPRJ.SubscribeStatus('LampUsage', None, LampUpdate)

device_dict = {dvTLP: TLP_ID, dvIPCP: IPCP_ID}

@eventEx([dvTLP, dvIPCP], ['Offline', 'Online'])
def TLPOff(device, state):
    GVEServer.SendStatus(device_dict[device], 'Connection', state)     
