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
from extronlib.interface import EthernetClientInterface

# Project imports
from modules.device import extr_matrix_XTPIICrossPointSeries_v1_12_0_1 as Matrix
from modules.device import biam_dsp_TesiraSeries_v1_15_1_0 as Biamp
from modules.device import tasc_bluray_BD_MP4K_v1_0_0_0 as Bluray
"""Projector is room dependent, this is 150 seat projector"""
from modules.device import epsn_vp_CB_EB_PU100xx_PU2010x_Series_v1_0_2_0 as Projector
"""600 Seat Projector"""
from modules.helper.ConnectionHandler import GetConnectionHandler
from modules.helper.ModuleSupport import eventEx
from modules.helper.MirrorUI import MirrorUIDevice

# Define devices
dvIPCP = ProcessorDevice('ProcessorAlias')
dvTLPFront = UIDevice('MainPanel')
dvTLPBooth = UIDevice('MirroredPanel')

dvTLPMain = MirrorUIDevice([dvTLPFront, dvTLPBooth])
#TODO figure out how mirrored panels take their TLP code 

dvMatrix = Matrix.EthernetClass('10.10.2.30', 23, Model='XTP II CrossPoint 1600')

dvBiamp = Biamp.SSHClass('10.10.2.40', 22, Model='TesiraFORTE DAN AI', Credentials=('admin', 'wag2748'))   #TODO Credentials

#TODO - Change to ethernet
dvBluray = Bluray.EthernetClass('10.10.2.70', 9030, Model='BD-MPK') #4k in room

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
    if state is 'Connected':
        dvMatrix.Update('InputSignalStatusEndpoint', {'Input': '1', 'Sub Input': '1'})
        print(dvMatrix.ReadStatus('InputSignalStatusEndpoint', {'Input': '1', 'Sub Input': '1'}))
        #verify other update calls needed

def ConnectBluray(timer:Timer, count):
    result = dvBluray.Connect(5)
    print('Connection attempt result', result)
    if result in ['Connected', 'ConnectedAlready']:
        timer.Stop()
    else:
        ProgramLog('Bluray connection failure {}'.format(result), 'warning')

BlurayConnectionTimer = Timer(5, ConnectBluray)
BlurayConnectionTimer.Stop()

@eventEx(dvBluray, ['Connected', 'Disconnected'])
def BlurayConnectionHandler(client:EthernetClientInterface, state):
    print('Bluray on IP {0} is {1}'.format(client.IPAddress, state))
    if state is 'Connected':
        client.StartKeepAlive(30, '!7?SST\r')
    else:
        client.StopKeepAlive()
        BlurayConnectionTimer.Restart()

dvLeftPRJ = GetConnectionHandler(dvLeftPRJ, 'Power', pollFrequency=30)
dvCenterPRJ = GetConnectionHandler(dvCenterPRJ, 'Power', pollFrequency=10)
dvRightPRJ = GetConnectionHandler(dvRightPRJ, 'Power', pollFrequency=30)

#check if I can do client.Update('Power') instead of casting each
@eventEx([dvLeftPRJ, dvCenterPRJ, dvRightPRJ], ['Connected', 'Disconnected'])
def ProjectorConnectionHandler(client:EthernetClientInterface, state):
    print('Projector on IP {0} is {1}'.format(client.IPAddress, state))
    if state is 'Connected':
        if client is dvLeftPRJ:
            dvLeftPRJ.Update('Power')
            dvLeftPRJ.Update('AVMute') #subscribe status for the buttons
        elif client is dvCenterPRJ:
            dvCenterPRJ.Update('Power')
            dvCenterPRJ.Update('AVMute') #subscribe status for the buttons
        elif client is dvRightPRJ:
            dvRightPRJ.Update('Power')
            dvRightPRJ.Update('AVMute')

dvBiamp = GetConnectionHandler(dvBiamp, 'MuteControl', keepAliveQueryQualifier={'Instance Tag': 'MuteProgram', 'Channel': '1'}, pollFrequency=30)

@eventEx(dvBiamp, ['Connected', 'Disconnected'])
def BiampConnectionHandler(client:EthernetClientInterface, state):
    print('Biamp on IP {0} is {1}'.format(client.IPAddress, state))
    if state is 'Connected':    
        #these need to be called whenever - write an update function for whenever I need newest status in main code to return value
        dvBiamp.Update('MuteControl', {'Instance Tag': 'MuteProgram', 'Channel': '1'})
        dvBiamp.Update('MuteControl', {'Instance Tag': 'MuteSpeech', 'Channel': '1'})

