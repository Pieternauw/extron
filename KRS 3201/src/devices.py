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
from extronlib.system import Timer, File
from extronlib.interface import EthernetClientInterface

# Project imports
from modules.device import extr_matrix_XTPIICrossPointSeries_v1_12_0_1 as Matrix
from modules.device import biam_dsp_TesiraSeries_v1_15_1_0 as Biamp
from modules.device import tasc_bluray_BD_MP4K_v1_0_0_0 as Bluray
from modules.device import epsn_vp_CB_EB_PU_21xxW_22xxB_Series_v1_0_0_0 as Projector
from modules.device import wolf_cs_Cynap_Core_Pure_Pro_v1_1_1_0 as Cynap
from modules.helper.ConnectionHandler import GetConnectionHandler
from modules.helper.ModuleSupport import eventEx
from modules.helper.MirrorUI import MirrorUIDevice
from modules.helper.gve_interface import gveClient

# Define devices
dvIPCP = ProcessorDevice('ProcessorAlias')
dvTLPFront = UIDevice('MainPanel')
dvTLPBooth = UIDevice('MirroredPanel')

dvTLPMain = MirrorUIDevice([dvTLPFront, dvTLPBooth])

passwordFile = File('user/password.txt', 'r')
password = str(passwordFile.readline())

newpswfile = File('user/newpsw.txt', 'r')
newpsw = str(newpswfile.readline())

GVEServer = gveClient('128.114.104.109', dvIPCP)

TLPF_ID = 'TLPF'; TLPB_ID = 'TLPB'; PRJL_ID = 'PRJL'; PRJC_ID = 'PRJC'; PRJR_ID = 'PRJR'; BMP_ID = 'Biamp'; BLU_ID = 'Bluray'; SW_ID = 'Matrix'; IPCP_ID = 'IPCP'; CY_ID = 'Cynap'

dvMatrix = Matrix.EthernetClass('10.10.2.30', 23, Model='XTP II CrossPoint 1600')

dvBiamp = Biamp.SSHClass('128.114.159.243', 22, Model='TesiraFORTE DAN AI', Credentials=('admin', newpsw))

dvBluray = Bluray.EthernetClass('10.10.2.70', 9030, Model='BD-MP4K') #4k in room
# dvBluray = Bluray.SerialClass(dvIPCP, 'COM1', Model='BD-MP4K')

#dvBoardCam1 = BoardCam.SerialClass(dvIPCP, 'COM2', Model='AT-HDVS-CAM')
#dvBoardCam2 = BoardCam.SerialClass(dvIPCP, 'COM1', Model='AT-HDVS-CAM')

"""150 Seat Projectors"""
dvLeftPRJ = Projector.SerialOverEthernetClass('10.10.2.30', 2033, Model='CB-PU2010B')       #for 150 and 600 there are two different models
dvCenterPRJ = Projector.SerialOverEthernetClass('10.10.2.30', 2034, Model='CB-PU2010B')
dvRightPRJ = Projector.SerialOverEthernetClass('10.10.2.30', 2035, Model='CB-PU2010B')

"""NOTE Device Connections - Using my own written method for bluray. 
        Once completed test the projector updates and subscribe status for button feedbacks"""

dvMatrix = GetConnectionHandler(dvMatrix, 'HDCPInputStatus', pollFrequency=30)

@eventEx(dvMatrix, ['Connected', 'Disconnected'])
def MatricConnectionHandler(client:EthernetClientInterface, state):
    print('Matrix on IP {0} is {1}'.format(client.IPAddress, state))
    GVEServer.SendStatus(SW_ID, 'Connection', state)
    if state is 'Connected':
        dvMatrix.Update('InputSignalStatusEndpoint', {'Input': '1', 'Sub Input': '1'})
        print(dvMatrix.ReadStatus('InputSignalStatusEndpoint', {'Input': '1', 'Sub Input': '1'}))
        #verify other update calls needed
    else:
        client.Connect(5)

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
        print('Bluray attempt reconnect')
        BlurayConnectionTimer.Restart()

dvLeftPRJ = GetConnectionHandler(dvLeftPRJ, 'LampUsage', pollFrequency=10)
dvCenterPRJ = GetConnectionHandler(dvCenterPRJ, 'LampUsage', pollFrequency=10)
dvRightPRJ = GetConnectionHandler(dvRightPRJ, 'LampUsage', pollFrequency=10)

PRJ_DICT = {dvLeftPRJ: PRJL_ID, dvCenterPRJ: PRJC_ID, dvRightPRJ: PRJR_ID}

#check if I can do client.Update('Power') instead of casting each
@eventEx([dvLeftPRJ, dvCenterPRJ, dvRightPRJ], ['Connected', 'Disconnected'])
def ProjectorConnectionHandler(client:EthernetClientInterface, state):
    print('Projector on IP {0} is {1}'.format(client.IPAddress, state))
    GVEServer.SendStatus(PRJ_DICT[client], 'Connection', state)
    if state is 'Connected':
        client.Update('Power')
        client.Update('AVMute')
        client.Update('LampUsage')
    else:
        client.Connect(5)

def LampUpdateL(command, value, qualifier):
    GVEServer.SendStatus(PRJL_ID, 'Lamp 1 Hours', value)

def LampUpdateC(command, value, qualifier):
    GVEServer.SendStatus(PRJC_ID, 'Lamp 1 Hours', value)

def LampUpdateR(command, value, qualifier):
    GVEServer.SendStatus(PRJR_ID, 'Lamp 1 Hours', value)

dvLeftPRJ.SubscribeStatus('LampUsage', None, LampUpdateL)
dvCenterPRJ.SubscribeStatus('LampUsage', None, LampUpdateC)
dvRightPRJ.SubscribeStatus('LampUsage', None, LampUpdateR)

dvCynap = Cynap.EthernetClass('128.114.159.235', 50915, Model='Cynap Pure Pro')
dvCynap.deviceUsername = 'admin'
dvCynap.devicePassword = newpsw

dvCynap = GetConnectionHandler(dvCynap, 'BYODPinDisplay', pollFrequency=30)

@eventEx(dvCynap, ['Connected', 'Disconnected'])
def CynapConnected(client:EthernetClientInterface, state):
    print('Cynap on IP {0} is {1}'.format(client.IPAddress, state))
    GVEServer.SendStatus(CY_ID, 'Connection', state)
    if state is not 'Connected':
        client.Connect(5)


# dvBiamp = GetConnectionHandler(dvBiamp, 'MuteControl', keepAliveQueryQualifier={'Instance Tag': 'MuteProgram', 'Channel': '1'}, pollFrequency=30)
dvBiamp = GetConnectionHandler(dvBiamp, 'SignalPresentMeter', keepAliveQueryQualifier={'Instance Tag': 'SpeechPresent', 'Channel': '1', 'Meter Name': 'Speech'})

@eventEx(dvBiamp, ['Connected', 'Disconnected'])
def BiampConnectionHandler(client:EthernetClientInterface, state):
    print('Biamp on IP {0} is {1}'.format(client.IPAddress, state))
    GVEServer.SendStatus(BMP_ID, 'Connection', state)
    if state is 'Connected':    
        #these need to be called whenever - write an update function for whenever I need newest status in main code to return value
        dvBiamp.Update('MuteControl', {'Instance Tag': 'MuteProgram', 'Channel': '1'})
        dvBiamp.Update('MuteControl', {'Instance Tag': 'MuteSpeech', 'Channel': '1'})
    else:
        client.Connect(5)

device_dict = {dvTLPFront: TLPF_ID, dvTLPBooth: TLPB_ID, dvIPCP: IPCP_ID}

@eventEx([dvTLPFront, dvTLPBooth, dvIPCP], ['Offline', 'Online'])
def TLPOff(device, state):
    GVEServer.SendStatus(device_dict[device], 'Connection', state)
