'''
GVE Interface module.

Copyright 2015-2022, Extron. All rights reserved.
'''

__version__ = '2.2.0'

## Begin Python Import ---------------------------------------------------------
import re
import time

## End Python Import ---------------------------------------------------------
##
## Begin ControlScript Import --------------------------------------------------
from extronlib.interface import EthernetClientInterface, EthernetServerInterfaceEx
from extronlib.system import Wait, Timer


## End ControlScript Import ----------------------------------------------------

class gveClient:
    """
    GVE Client Interface Class

    This module implements the GS to GVE interface protocol.  The module
    manages the connections to send and receive commands to and from the GVE
    Server, and maintains a heartbeat to maintain the connection to the GVE
    Server.
    """

    matchCommand = re.compile('GSTR([0-9a-fA-F]{12})([0-9]{0,3})(\[.*\])*')
    matchDevice = re.compile('\[([0-9a-zA-Z]{1,50})(~([0-9]{1,2})=(.*))*')
    matchAction = re.compile('([0-9]{1,2})=(.*)')

    def __init__(self, Hostname, HostDevice, IPPort=5555, Interface='Any'):
        """
        :param Hostname: GVE Server Host Name/IP Address
        :type Hostname: string
        :param HostDevice: Primary Processor
        :type HostDevice: extronlib.device.ProcessorDevice
        :param IPPort: IP Port Number used for TCP and UDP Communications
        :type IPPort: int
        :param Interface: Defines the network interface on which to listen
            ('Any', 'LAN', or 'AVLAN')
        :type Interface: string
        """

        self.Hostname = Hostname
        self.MACAddress = HostDevice.MACAddress.replace('-', '').upper()
        self.IPPort = IPPort
        self.GVEStatus = {}

        self.__sequence = 0
        self.__canCommunicate = True
        self.__dataBuffer = ''

        # Event handlers
        self.__DiagnosticSendText = self.__unassigned
        self.__DiagnosticReceiveText = self.__unassigned
        self.__GVEServerConnected = self.__unassigned
        self.__GVEServerDisconnected = self.__unassigned
        self.__ReceiveGVECommand = self.__unassigned

        self.__TCPListen = EthernetServerInterfaceEx(self.IPPort, 'TCP', Interface=Interface)

        time.sleep(2)
        self.__TCPListen.Connected = self.__GVEServerConnected_handler
        self.__TCPListen.Disconnected = self.__GVEServerDisconnected_handler
        self.__TCPListen.ReceiveData = self.__ReceiveData
        res = self.__TCPListen.StartListen()
        if 'Listening' not in res:
            raise RuntimeError('Unable to start GVE Listener. {}'.format(res))

        self.__UDPSender = EthernetClientInterface(self.Hostname, self.IPPort, 'UDP')

        @Wait(3.0)
        def StartKeepAlive():
            self.__SendHeartBeat(None, None)
            Timer(20, self.__SendHeartBeat)

    def __GVEServerConnected_handler(self, _, state):
        self.__GVEServerConnected(self, state)

    def __GVEServerDisconnected_handler(self, _, state):
        self.__GVEServerDisconnected(self, state)

    def __CreateCommandString(self, command=None):
        """ Command String Builder

        Assembles Command String with Header, MAC Address, Sequence, and ETX
        byte.
        """
        header = 'GSTR{0}{1:03d}'.format(
            self.MACAddress,
            self.__sequence
            )

        if self.__sequence == 255:
            self.__sequence = 0
        else:
            self.__sequence += 1

        return header + command + '\x03' if command else header + '\x03'

    def __UDPSend(self, data):
        try:
            self.__UDPSender.Send(data)
        except Exception:
            # gaierror is the only known exception.  Unable to import gaierror
            # from disallowed non-built-in module socket.
            self.__DiagnosticSendText(self, 'Cannot send: network error')

    def __SendHeartBeat(self, timer, count):
        """ Send Hearbeat Message

        Recursive Loop that sends heartbeat every 20.0 seconds.
        """
        SendString = self.__CreateCommandString()
        self.__DiagnosticSendText(self, SendString)
        self.__UDPSend(SendString)

    def __SendFullUpdate(self):
        """ Send Full System Update Message

        Assembles and sends the system update message.
        """
        cmdString = ''

        for key in self.GVEStatus:
            cmdString += '[{0}]'.format(key)

            for subkey in self.GVEStatus[key]:
                cmdString = cmdString[:-1] + \
                        '~{0}={1}]'.format(subkey, self.GVEStatus[key][subkey])

        if cmdString and self.__canCommunicate:
            SendString = self.__CreateCommandString(cmdString)
            self.__DiagnosticSendText(self, SendString)
            self.__UDPSend(SendString)

    def __ExecuteCommand(self, device, actionID, actionState):
        """ Execute Command from GVE Server

        Internal function that interprets commands received from the GVE Server
        """
        ActionDict = {
            0: 'Update',
            17: 'Power',
            22: 'Device Status',
            38: 'Room Event',
            }
        StateDict = {
            '0': 'Off',
            '1': 'On',
            }

        if device == '0' and ActionDict[actionID] == 'Update':
            if actionState == '1':
                self.__canCommunicate = True
                self.__SendFullUpdate()
            elif actionState == '0':
                self.__canCommunicate = False
        elif device == '0' and ActionDict[actionID] == 'Room Event':
            RoomEventData = actionState.split('_')
            self.__ReceiveGVERoomEvent(self,
                    (device, int(RoomEventData[0]), RoomEventData[1]))
        else:
            if ActionDict[actionID] == 'Power':
                self.__ReceiveGVECommand(self,
                        (device, 'Power', StateDict[actionState]))
            else:
                self.__ReceiveGVECommand(self,
                        (device, ActionDict[actionID], actionState))

    def __ReceiveData(self, interface, data):
        """ Receive Data

        Internal event processor for data received from the GVE Server.
        Processes incoming data and validates commands that match MAC Address
        """
        tempBuffer = self.__dataBuffer + data.decode()

        if tempBuffer[-1] != '\x03':
            last = tempBuffer.rfind('\x03')
            self.__dataBuffer = tempBuffer[last+1:]
            tempBuffer = tempBuffer[:last]
        else:
            self.__dataBuffer = ''

        dataLines = tempBuffer.split('\x03')[:-1]

        for rcvCmd in dataLines:
            self.__DiagnosticReceiveText(self, rcvCmd)

            # See if Valid Commmand is received
            found = self.matchCommand.match(rcvCmd)

            if found:
                rcvMAC = found.group(1).upper()

                # Check if MAC matches processor
                if rcvMAC == self.MACAddress:
                    rcvSequence = found.group(2)

                    if found.group(3):
                        rcvCommands = found.group(3).split(']')
                    else:
                        rcvCommands = []

                    # Check what commands received from GVE Server
                    for rcvCommand in rcvCommands:
                        # Parse which device
                        foundDevice = self.matchDevice.match(rcvCommand)
                        if foundDevice is not None:
                            cmdDevice = foundDevice.group(1)
                            cmdActions = foundDevice.group(2).split('~')
                            # Parse which commands and parameters
                            for cmdAction in cmdActions:
                                foundAction = self.matchAction.match(cmdAction)
                                if foundAction:
                                    ActionID = int(foundAction.group(1))
                                    ActionState = str(foundAction.group(2))
                                    escapeChars = {
                                        '\7E': '~',
                                        '\3D': '=',
                                        '\5C': '\\',
                                        '\5B': '[',
                                        '\5D': ']',
                                    }
                                    for k, v in escapeChars.items():
                                        if k in ActionState:
                                            ActionState = ActionState.replace(k, v)

                                    self.__ExecuteCommand(cmdDevice, ActionID,
                                            ActionState)
                else:
                    self.__DiagnosticReceiveText(self,
                            'Receive Command with incorrect MAC')

    def SendStatus(self, device, command, value):
        """
        Send Status to GVE Server

        External Method that interprets and assembles commands to send to GVE
        Server.  See the :ref:`ref-SendStatus` table in the appendix for
        available commands.

        :param device: device ID assigned in GVE Server
        :type device: string
        :param command: friendly name for command sent to GVE Server
        :type command: string
        :param value: command values to set on GVE Server
        :type value: string
        """
        CommandDict = {
            'Power': 17,
            'Source': 18,
            'Connection': 19,
            'Lamp 1 Hours': 20,
            'Lamp 2 Hours': 29,
            'Lamp 3 Hours': 30,
            'Lamp 4 Hours': 31,
            'Filter Hours': 21,
            'Device Status': 44,
            }
        StringStatusCommand = [
            'Source', 'Lamp 1 Hours', 'Lamp 2 Hours', 'Lamp 3 Hours',
            'Lamp 4 Hours', 'Filter Hours',
            ]
        PowerDict = {
            'Unknown': -1,
            'Off': 0,
            'On': 1,
            'Cooling Down': 2,
            'Warming Up': 3,
            }
        StatusDict = {
            'Unknown': -1,
            'Disconnected': 0,
            'Connected': 1,
            'Online': 1,
            'Offline': 0,
            }
        cmdString = ''
        if command in CommandDict:
            if not isinstance(device, str):
                raise TypeError('device must be an alphanumeric string.')

            if not device in self.GVEStatus:
                self.GVEStatus[device] = {}

            if command == 'Power' and value in PowerDict:
                cmdString = '[{0}~{1}={2}]'.format(device,
                        CommandDict[command], PowerDict[value])
                self.GVEStatus[device][CommandDict[command]] = PowerDict[value]
            elif command == 'Connection' and value in StatusDict:
                cmdString = '[{0}~{1}={2}]'.format(device,
                        CommandDict[command], StatusDict[value])
                self.GVEStatus[device][CommandDict[command]] = StatusDict[value]
            elif command == 'Device Status':
                cmdString = '[{0}~{1}={2}]'.format(device,
                        CommandDict[command], value)
                self.GVEStatus[device][CommandDict[command]] = value
            elif command in StringStatusCommand:
                escapeChars = {
                    '~': '\7E',
                    '=': '\3D',
                    '\\': '\5C',
                    '[': '\5B',
                    ']': '\5D',
                }
                for k, v in escapeChars.items():
                    if k in str(value):
                        value = str(value).replace(k, v)

                cmdString = '[{0}~{1}={2}]'.format(
                            device, CommandDict[command], value)
                self.GVEStatus[device][CommandDict[command]] = value
            else:
                self.__DiagnosticReceiveText(self,
                        'GVE> Invalid Status Received')

            if cmdString and self.__canCommunicate:
                SendString = self.__CreateCommandString(cmdString)
                self.__DiagnosticSendText(self, SendString)
                self.__UDPSend(SendString)

    def SendSecondaryProcessorStatus(self, device, value):
        """
        Send Secondary Processor Status to GVE Server

        External Method that sends Secondary Processor Connection Status to GVE
        Server

        :param device: Secondary Processor added in GVE
        :type device: extronlib.device.ProcessorDevice
        :param value: 'Unknown', 'Connected', 'Disconnected', 'Online' or 'Offline'
        :type value: string
        """
        StatusDict = {
            'Unknown': -1,
            'Disconnected': 0,
            'Connected': 1,
            'Offline': 0,
            'Online': 1,
            }

        if device.MACAddress is not None:
            macaddr = device.MACAddress.replace('-', '')

            if value in StatusDict:
                if not macaddr in self.GVEStatus:
                    self.GVEStatus[macaddr] = {}

                cmdString = '[{0}~19={1}]'.format(macaddr, StatusDict[value])
                self.GVEStatus[macaddr][19] = StatusDict[value]

                if self.__canCommunicate:
                    SendString = self.__CreateCommandString(cmdString)
                    self.__DiagnosticSendText(self, SendString)
                    self.__UDPSend(SendString)
        else:
            self.__DiagnosticSendText(self, 'GVE> Invalid MAC Address')

    ## Class Event Callbacks
    ##########
    def __unassigned(self, *args):
        pass

    @property
    def DiagnosticSendText(self):
        """
        ``Event:`` Triggers when data is sent to the GVE server.

        The callback function must accept exactly two parameters, which are
        the :py:class:`~gve_interface.gveClient` that triggers the event and
        the string that was sent.
        """
        return self.__DiagnosticSendText

    @DiagnosticSendText.setter
    def DiagnosticSendText(self, handler):
        if callable(handler):
            self.__DiagnosticSendText = handler
        else:
            raise TypeError("'handler' is not callable")

    @property
    def DiagnosticReceiveText(self):
        """
        ``Event:`` Triggers when data is received from the GVE server.

        The callback function must accept exactly two parameters, which are
        the :py:class:`~gve_interface.gveClient` that triggers the event and
        the string that was received.
        """
        return self.__DiagnosticReceiveText

    @DiagnosticReceiveText.setter
    def DiagnosticReceiveText(self, handler):
        if callable(handler):
            self.__DiagnosticReceiveText = handler
        else:
            raise TypeError("'handler' is not callable")

    @property
    def GVEServerConnected(self):
        """
        ``Event:`` Triggers when a connection to the GVE server is
        established.

        The callback function must accept exactly two parameters, which are
        the :py:class:`~gve_interface.gveClient` that triggers the event and a
        string (``'Connected'``).
        """
        return self.__GVEServerConnected

    @GVEServerConnected.setter
    def GVEServerConnected(self, handler):
        if callable(handler):
            self.__GVEServerConnected = handler
        else:
            raise TypeError("'handler' is not callable")

    @property
    def GVEServerDisconnected(self):
        """
        ``Event:`` Triggers when a connection to the GVE server is closed.

        The callback function must accept exactly two parameters, which are
        the :py:class:`~gve_interface.gveClient` that triggers the event and a
        string (``'Disconnected'``).
        """
        return self.__GVEServerDisconnected

    @GVEServerDisconnected.setter
    def GVEServerDisconnected(self, handler):
        if callable(handler):
            self.__GVEServerDisconnected = handler
        else:
            raise TypeError("'handler' is not callable")

    @property
    def ReceiveGVECommand(self):
        """
        ``Event:`` Triggers when a command is received from the GVE server.

        The callback function must accept exactly two parameters, which are
        the :py:class:`~gve_interface.gveClient` that triggers the event and a
        tuple ``(deviceID, command, parameter)``.  See the
        :ref:`ref-ReceiveGVECommand` in the appendix for the possible
        commands.
        """
        return self.__ReceiveGVECommand

    @ReceiveGVECommand.setter
    def ReceiveGVECommand(self, handler):
        if callable(handler):
            self.__ReceiveGVECommand = handler
        else:
            raise TypeError("'handler' is not callable")

    @property
    def ReceiveGVERoomEvent(self):
        """
        ``Event:`` Triggers when a room event action is received from the GVE
        server.

        The callback function must accept exactly two parameters, which are
        the :py:class:`~gve_interface.gveClient` that triggers the event and a
        tuple ``(deviceID, room, eventName)``.  See the
        :ref:`ref-ReceiveGVERoomEvent` in the appendix for the possible room
        events.
        """
        return self.__ReceiveGVERoomEvent

    @ReceiveGVERoomEvent.setter
    def ReceiveGVERoomEvent(self, handler):
        if callable(handler):
            self.__ReceiveGVERoomEvent = handler
        else:
            raise TypeError("'handler' is not callable")
