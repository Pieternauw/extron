"""
Mirror UI module

Copyright 2018-2024, Extron. All rights reserved.
"""

from extronlib.device import UIDevice, eBUSDevice
from extronlib.ui import Button as OldButton
from extronlib.ui import Knob as OldKnob
from extronlib.ui import Label as OldLabel
from extronlib.ui import Level as OldLevel
from extronlib.ui import Slider as OldSlider

__version__ = '2.0.0'

def ModuleVersion():
    """This method returns the version of the Mirror UI Module"""
    return __version__

class MirrorHost():
    pass

class MirrorUIDevice(MirrorHost):
    """This class creates an object that contains a list of UIDevice objects
        to be used with the Button, Label, Level and Knob classes defined in
        this file.  The class object is also used in place of the UIDevice
        object for touchpanel operations such as page flips and show/hide
        popup pages.
    """
    def __init__(self, UIList):
        """Initializes the module's MirrorUIDevice in program.

        Parameters
        ----------
        UIList : list of extronlib.device.UIDevice
            List of UIDevice Objects

        Examples
        --------
        ::

            # Comment out the extronlib.ui import statement
            #from extronlib.ui import Button, Knob, Label, Level, Slider

            # Add the import statement for the MirrorUI file in System Manager
            from MirrorUI import MirrorUIDevice, Button, Knob, Label, Level, Slider

            TLP1 = UIDevice( "PanelAlias" )
            TLP2 = UIDevice( "PanelAlias_2" )

            # Add the statement defining the MirrorUIDevice and program using normal
            # methods and events
            MirroredTLPs = MirrorUIDevice([TLP1, TLP2])
        """
        if not isinstance(UIList, list):
            raise TypeError('Parameter UIList is not a list')

        self.__objects = UIList
        for i, obj in enumerate(self.__objects):
            if not isinstance(obj, UIDevice):
                raise TypeError('Object {} in UIList is not a UIDevice'.format(i))

            obj.BrightnessChanged = self.CallBrightnessChanged
            obj.HDCPStatusChanged = self.CallHDCPStatusChanged
            obj.InactivityChanged = self.CallInactivityChanged
            obj.InputPresenceChanged = self.CallInputPresenceChanged
            obj.LidChanged = self.CallLidChanged
            obj.LightChanged = self.CallLightChanged
            obj.MotionDetected = self.CallMotionDetected
            obj.SleepChanged = self.CallSleepChanged

        self.BrightnessChanged = self.__unassigned
        self.HDCPStatusChanged = self.__unassigned
        self.InactivityChanged = self.__unassigned
        self.InputPresenceChanged = self.__unassigned
        self.LidChanged = self.__unassigned
        self.LightChanged = self.__unassigned
        self.MotionDetected = self.__unassigned
        self.SleepChanged = self.__unassigned


    # Methods:
    # The methods defined here operate the same as the UIDevice methods except
    # that the parameters are passed to all of the objects defined in the
    # UIList passed to the MirrorUIDevice object.

    def Click(self, count=1, interval=None):
        """Plays the default buzzer sound on all mirrored devices.

        Parameters
        ----------
        count : int
            number of buzzer sound to play. (Default value = 1)
        interval : float
            time gap between the starts of consecutive buzzer sounds. (Default value = None)

        Notes
        -----
        If count is greater than 1, interval must be provided.
        """
        for obj in self.__objects:
            obj.Click(count, interval)

    def GetHDCPStatus(self, videoInput):
        """Returns a list of the current HDCP Status for the given input on
        all devices.

        Parameters
        ----------
        videoInput : str
            input (``'HDMI'`` or ``'XTP'``).

        Returns
        -------
        list of bool
            list of True or False
        """
        return [obj.GetHDCPStatus(videoInput) for obj in self.__objects]

    def GetInputPresence(self, videoInput):
        """Returns a list of the current Input Presence for the given input
        on all devices.

        Parameters
        ----------
        videoInput : str
            input (``'HDMI'`` or ``'XTP'``).

        Returns
        -------
        list of bool
            list of True or False
        """
        return [obj.GetInputPresence(videoInput) for obj in self.__objects]

    def GetMute(self, name):
        """Returns the current mute state for the given channel name on all
        devices.

        Parameters
        ----------
        name : str
            name of channel (``'Master'``, ``'Speaker'``, ``'Line'``, ``'Click'``, ``'Sound'``, ``'HDMI'`` and ``'XTP'``).

        Returns
        -------
        str
            ``'On'`` or ``'Off'``
        """
        return self.__objects[0].GetMute(name)

    def GetVolume(self, name):
        """Returns the current volume level for the given channel name on all
        devices.

        Parameters
        ----------
        name : str
            name of channel (``'Master'``, ``'Click'``, ``'Sound'``, ``'HDMI'`` and ``'XTP'``).

        Returns
        -------
        int
            Volume Level (0-100)
        """
        return self.__objects[0].GetVolume(name)

    def HideAllPopups(self):
        """Dismisses all popup pages on all devices."""
        for obj in self.__objects:
            obj.HideAllPopups()

    def HidePopup(self, popup):
        """Hide popup page on all devices.

        Parameters
        ----------
        popup : int, str
            popup page number or name.
        """
        for obj in self.__objects:
            obj.HidePopup(popup)

    def HidePopupGroup(self, group):
        """Hide all popup pages in a popup group on all devices.

        Parameters
        ----------
        group : int
            popup group number.
        """
        for obj in self.__objects:
            obj.HidePopupGroup(group)

    def PlaySound(self, filename):
        """Play a sound file identified by filename on all devices.

        Parameters
        ----------
        filename : str
            name of sound file.

        Notes
        -----
        * Only WAV files can be played.
        * A subsequent call will preempt the currently playing file.
        * Sound file must be added to the project file.
        """
        for obj in self.__objects:
            obj.PlaySound(filename)

    def SetAutoBrightness(self, state):
        """Set the auto brightness state on all devices. Either ``'On'`` or
        ``True`` turns on auto brightness. ``'Off'`` or ``False`` turns off
        auto brightness.

        Parameters
        ----------
        state : bool, str
            whether to enable auto brightness
        """
        for obj in self.__objects:
            obj.SetAutoBrightness(state)

    def SetBrightness(self, level):
        """Set the LCD screen brightness level on all devices.

        Parameters
        ----------
        level : int
            brightness level from 0 to 100
        """
        for obj in self.__objects:
            obj.SetBrightness(level)

    def SetDisplayTimer(self, state, timeout):
        """Enables or Disables the display timer on all devices. Either
        ``'On'`` or ``True`` enables display timer. ``'Off'`` or ``False``
        disables display timer.

        Parameters
        ----------
        state : bool, str
            whether to enable the display timer
        timeout : int
            time in seconds before turn off the display

        Notes
        -----
        Display timer is applicable to TLI only.
        """
        for obj in self.__objects:
            obj.SetDisplayTimer(state, timeout)

    def SetInactivityTime(self, times):
        """Set the inactivity times when the InactivityChanged event will
        trigger for all devices.

        Parameters
        ----------
        times : list of ints
            list of times. Each time in whole seconds
        """
        for obj in self.__objects:
            obj.SetInactivityTime(times)

    def SetInput(self, videoInput):
        """Set the video input on all devices.

        Parameters
        ----------
        videoInput : str
            input to select (``'HDMI'`` or ``'XTP'``)
        """
        for obj in self.__objects:
            obj.SetInput(videoInput)

    def SetLEDBlinking(self, ledID, rate, stateList):
        """Set the LED cycle at ADA comliant rates through a list of states
        on all devices.

        Parameters
        ----------
        ledID : int
            LED id (``65533``)
        rate : str
            ADA compliant blink rate. (``'Slow'``, ``'Medium'``, ``'Fast'``)
        stateList : list of str
            List of colors (``'Off'``, ``'Green'``, ``'Red'``)
        """
        for obj in self.__objects:
            obj.SetLEDBlinking(ledID, rate, stateList)

    def SetLEDState(self, ledID, state):
        """Make the LED to a given color on all devices.

        Parameters
        ----------
        ledID : int
            LED id (``65533``)
        state : str
            LED Color (``'Off'``, ``'Green'``, ``'Red'``)
        """
        for obj in self.__objects:
            obj.SetLEDState(ledID, state)

    def SetMotionDecayTime(self, duration):
        """Set the period of time for the MotionDetected event to trigger for
        all devices.

        Parameters
        ----------
        duration : float
            time in seconds (minimum/default value is 10)
        """
        for obj in self.__objects:
            obj.SetMotionDecayTime(duration)

    def SetMute(self, name, mute):
        """Sets the mute state for the given channel on all devices.

        Parameters
        ----------
        name : str
            name of channel (``'Master'``, ``'Speaker'``,
            ``'Line'``, ``'Click'``, ``'Sound'``, ``'HDMI'`` and ``'XTP'``).
        mute : str
            mute state (``'On'``, ``'Off'``)
        """
        for obj in self.__objects:
            obj.SetMute(name, mute)

    def SetSleepTimer(self, state, duration=None):
        """Enables or Disables the sleep timer on all devices. Either
        ``'On'`` or ``True`` enables sleep timer. ``'Off'`` or ``False``
        disables sleep timer.

        Parameters
        ----------
        state : bool, str
            whether to enable the display timer
        duration : int
            time in seconds to sleep (Default value = None)
        """
        for obj in self.__objects:
            obj.SetSleepTimer(state, duration)

    def SetVolume(self, name, level):
        """Sets the volume level for the given channel name on all devices.

        Parameters
        ----------
        name : str
            name of channel (``'Master'``, ``'Click'``, ``'Sound'``,
            ``'HDMI'`` and ``'XTP'``).
        level : int
            volume level 0 to 100
        """
        for obj in self.__objects:
            obj.SetVolume(name, level)

    def SetWakeOnMotion(self, state):
        """Enables or disables wake on motion on all devices. Either ``'On'``
        or ``True`` turns on wake on motion. ``'Off'`` or ``False`` turns off
        wake on motion.

        Parameters
        ----------
        state : bool, str
            whether to enable wake on motion
        """
        for obj in self.__objects:
            obj.SetWakeOnMotion(state)

    def ShowPage(self, page):
        """Show page on the screen on all devices.

        Parameters
        ----------
        page : int, str
            absolute page number or name
        """
        for obj in self.__objects:
            obj.ShowPage(page)

    def ShowPopup(self, popup, duration=0):
        """Display pop-up page on all devices for a period of time

        Parameters
        ----------
        popup : int, str
            absolute pop-up page number or name
        duration : float
            duration (in seconds) the pop-up remains on the
            screen. 0 means forever. (Default value = 0)

        Notes
        -----
        If a pop-up is already showing for a finite period of time,
        calling this method again with the same pop-up will replace the
        remaining period with the new period.
        """
        for obj in self.__objects:
            obj.ShowPopup(popup, duration)

    def Sleep(self):
        """Forces all devices to sleep immediately"""
        for obj in self.__objects:
            obj.Sleep()

    def StopSound(self):
        """Stop playing sound file on all devices"""
        for obj in self.__objects:
            obj.StopSound()

    def Wake(self):
        """Forces all devices to wake up immediately"""
        for obj in self.__objects:
            obj.Wake()

    def CallBrightnessChanged(self, panel, brightness):
        """Callback passed to device list to redirect event to new event call"""
        self.BrightnessChanged(panel, brightness)

    def CallHDCPStatusChanged(self, panel, state):
        """Callback passed to device list to redirect event to new event call"""
        self.HDCPStatusChanged(panel, state)

    def CallInactivityChanged(self, panel, time):
        """Callback passed to device list to redirect event to new event call"""
        self.InactivityChanged(panel, time)

    def CallInputPresenceChanged(self, panel, state):
        """Callback passed to device list to redirect event to new event call"""
        self.InputPresenceChanged(panel, state)

    def CallLidChanged(self, panel, state):
        """Callback passed to device list to redirect event to new event call"""
        self.LidChanged(panel, state)

    def CallLightChanged(self, panel, level):
        """Callback passed to device list to redirect event to new event call"""
        self.LightChanged(panel, level)

    def CallMotionDetected(self, panel, state):
        """Callback passed to device list to redirect event to new event call"""
        self.MotionDetected(panel, state)

    def CallSleepChanged(self, panel, state):
        """Callback passed to device list to redirect event to new event call"""
        self.InactivityChanged(panel, state)

    # Class Property Callbacks
    ##########################

    @property
    def AmbientLightValue(self):
        """Defined Property to pass list of Objects' AmbientLightValue
        property

        Returns
        -------
        list of int
            list of current ambient light values for all devices
        """
        return [obj.AmbientLightValue for obj in self.__objects]

    @property
    def AutoBrightness(self):
        """Defined Property to pass AutoBrightness

        Returns
        -------
        bool
            current auto brightness state for all devices
        """
        return self.__objects[0].AutoBrightness

    @property
    def Brightness(self):
        """Defined Property to pass Brightness

        Returns
        -------
        int
            current brightness level for all devices
        """
        return self.__objects[0].Brightness

    @property
    def DeviceAlias(self):
        """Defined Property to pass a list of Objects' DeviceAlias property

        Returns
        -------
        list of str
            list of the device aliases for all devices
        """
        return [obj.DeviceAlias for obj in self.__objects]

    @property
    def DisplayState(self):
        """Defined Property to pass Display State

        Returns
        -------
        str
            the current display state of the all devices (``'On'``,
            ``'Off'``)

        Notes
        -----
        Display timer is applicable to TLI only.
        """
        return self.__objects[0].DisplayState

    @property
    def DisplayTimer(self):
        """Defined Property to pass DisplayTimer

        Returns
        -------
        int
            Return list of display timer timeouts in seconds for all
            devices
        """
        return self.__objects[0].DisplayTimer

    @property
    def DisplayTimerEnabled(self):
        """Defined Property to pass DisplayTimerEnabled

        Returns
        -------
        bool
            current state of the display timer for all devices
        """
        return self.__objects[0].DisplayTimerEnabled

    @property
    def FirmwareVersion(self):
        """Defined Property to pass a list of Objects' FirmwareVersion
        property

        Returns
        -------
        list of str
            list of the firmware version for all devices
        """
        return [obj.FirmwareVersion for obj in self.__objects]

    @property
    def Hostname(self):
        """Defined Property to pass list of Objects' Hostname property

        Returns
        -------
        list of str
            list of the hostname for all devices
        """
        return [obj.Hostname for obj in self.__objects]

    @property
    def IPAddress(self):
        """Defined Property to pass a list of Objects' IPAddress property

        Returns
        -------
        list of str
            list of the IP address for all devices
        """
        return [obj.IPAddress for obj in self.__objects]

    @property
    def InactivityTime(self):
        """Defined Property to pass a list of Objects' InactivityTime
        property

        Returns
        -------
        list of int
            list of seconds since last activity for the all devices.

        Notes
        -----
        0 = Active, Nonzero = Time of inactivity.
        """
        return [obj.InactivityTime for obj in self.__objects]

    @property
    def LidState(self):
        """Defined Property to pass a list of Objects' LidState property

        Returns
        -------
        list of str
            list of the current lid state for all devices (``'Opened'``
            or ``'Closed'``)
        """
        return [obj.LidState for obj in self.__objects]

    @property
    def LightDetectedState(self):
        """Defined Property to pass a list of Objects' LightDetectedState
        property

        Returns
        -------
        list of str
            list of the state of light detection for all devices
            (``'Detected'`` or ``'Not Detected'``)
        """
        return [obj.LightDetectedState for obj in self.__objects]

    @property
    def MACAddress(self):
        """Defined Property to pass a list of Objects' MACAddress property

        Returns
        -------
        list of str
            list of the MAC address for all devices
        """
        return [obj.MACAddress for obj in self.__objects]

    @property
    def ModelName(self):
        """Defined Property to pass a list of Objects' ModelName property

        Returns
        -------
        list of str
            list of the model name for all devices
        """
        return [obj.ModelName for obj in self.__objects]

    @property
    def MotionDecayTime(self):
        """Defined Property to pass MotionDecayTime

        Returns
        -------
        int
            period of time to trigger *MotionDetected* event after last
            motion was detected for all devices. The default (and minimum)
            value is 10 seconds.
        """
        return self.__objects[0].MotionDecayTime

    @property
    def MotionState(self):
        """Defined Property to pass a list of Objects' MotionState property

        Returns
        -------
        list of str
            list of the state of the Motion sensor for all devices
            (e.g. ``'Motion'``, ``'No Motion'``)
        """
        return [obj.MotionState for obj in self.__objects]

    @property
    def Objects(self):
        """Defined Property to pass a list of Objects in the mirrored group

        Returns
        -------
        list of extronlib.device.UIDevice
            list of UIDevice objects defined in the class
        """
        return self.__objects

    @property
    def PartNumber(self):
        """Defined Property to pass a list of Objects' PartNumber property

        Returns
        -------
        list of str
            list of the part numbers for all devices
        """
        return [obj.PartNumber for obj in self.__objects]

    @property
    def SerialNumber(self):
        """Defined Property to pass a list of Objects' SerialNumber property
        Returns
        -------
        list of str
            list of the serial numbers for all devices
        """
        return [obj.SerialNumber for obj in self.__objects]

    @property
    def SleepState(self):
        """Defined Property to pass a list of Objects' SleepState property

        Returns
        -------
        list of str
            list of the current sleep state for all devices
            (e.g. ``'Asleep'``, ``'Awake'``)
        """
        return [obj.SleepState for obj in self.__objects]

    @property
    def SleepTimer(self):
        """Defined Property to pass SleepTimer

        Returns
        -------
        int
            sleep timer timeout for all devices.
        """
        return self.__objects[0].SleepTimer

    @property
    def SleepTimerEnabled(self):
        """Defined Property to pass SleepTimerEnabled

        Returns
        -------
        bool
            current state of the sleep timer for all devices. ``True`` if
            enabled. ``False`` if disabled.
        """
        return self.__objects[0].SleepTimerEnabled

    @property
    def UserUsage(self):
        """Defined Property to pass a list of Objects' UserUsage property

        Returns
        -------
        list of tuples of ints
            list of user data usage for all devices in KB ``(used, total)``.
        """
        return [obj.UserUsage for obj in self.__objects]

    @property
    def WakeOnMotion(self):
        """Defined Property to pass WakeOnMotion

        Returns
        -------
        bool
            current wake on motion state for all devices. ``True`` if
            enabled. ``False`` if disabled.
        """
        return self.__objects[0].WakeOnMotion

    # Class Event Callbacks
    #######################

    def __unassigned(self, *args):
        """If Module Events are not defined in user code, then do nothing."""
        pass

    @property
    def BrightnessChanged(self):
        """Passback the BrightnessChanged Event

        ``Event``: Triggers when LCD brightness has changed.

        The callback takes two arguments. The first one is the MirrorUIDevice
        instance triggering the event and the second one is the current
        brightness level as an integer.

        Examples
        --------
        ::

            @event(MirroredTLPs, 'BrightnessChanged')
            def HandleBrightnessChanged(mirroredtlp, brightness):
                print('{} Brightness Changed: {}'.format(mirrortlp.DeviceAlias, brightness))
        """
        def multidispatch(panel, brightness):
            self.__BrightnessChanged(self, brightness)
        return multidispatch

    @BrightnessChanged.setter
    def BrightnessChanged(self, handler):
        if callable(handler):
            self.__BrightnessChanged = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def HDCPStatusChanged(self):
        """Passback the HDCPStatusChanged Event

        ``Event``: Triggers when HDCP Status changes.

        The callback takes two arguments. The first one is the MirrorUIDevice
        instance triggering the event and state with a tuple: (``Input``,
        ``Status``).

        Examples
        --------
        ::

            @event(MirroredTLPs, 'HDCPStatusChanged')
            def HandleHDCPStatusChanged(mirroredtlp, state):
                if state[0] == 'HDMI' and not state[1]:
                    PodiumTLP.ShowPopup('No HDCP')
        """
        def multidispatch(panel, state):
            self.__HDCPStatusChanged(self, state)
        return multidispatch

    @HDCPStatusChanged.setter
    def HDCPStatusChanged(self, handler):
        if callable(handler):
            self.__HDCPStatusChanged = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def InactivityChanged(self):
        """Passback the InactivityChanged Event

        ``Event``: Triggers at times specified by SetInactivityTime() after
        state transition of inactivity timer.

        The callback takes two arguments. The first one is the MirrorUIDevice
        instance triggering the event and time with a float value of
        inactivity time in seconds.

        Examples
        --------
        ::

            @event(MirroredTLPs, 'InactivityChanged')
            def UnoccupyRoom(mirrotlp, time):
                if time == 3000:
                    ShowWarning()
                else:
                    ShutdownSystem()
        """
        def multidispatch(panel, time):
            self.__InactivityChanged(self, time)
        return multidispatch

    @InactivityChanged.setter
    def InactivityChanged(self, handler):
        if callable(handler):
            self.__InactivityChanged = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def InputPresenceChanged(self):
        """Passback the InputPresenceChanged Event

        ``Event``: Triggers when Input Presence changes.

        The callback takes two arguments. The first one is the MirrorUIDevice
        instance triggering the event and state with a tuple: (``Input``,
        ``Status``).

        Examples
        --------
        ::

            @event(MirroredTLPs, 'InputPresenceChanged')
            def HandleInputPresenceChanged(mirrotlp, state):
                if state[0] == 'HDMI' and not state[1]:
                    if mirrotlp.GetInputPresence('XTP'):
                        mirrotlp.SetInput('XTP')
                    else:
                        mirrotlp.ShowPopup('No Input Available')
        """
        def multidispatch(panel, state):
            self.__InputPresenceChanged(self, state)
        return multidispatch

    @InputPresenceChanged.setter
    def InputPresenceChanged(self, handler):
        if callable(handler):
            self.__InputPresenceChanged = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def LidChanged(self):
        """Passback the LidChanged Event

        ``Event``: Triggers when the Lid state changes.

        The callback takes two arguments. The first one is the MirrorUIDevice
        instance triggering the event and the second is the current lid state
        (``'Opened'`` or ``'Closed'``).

        Examples
        --------
        ::

            @event(MirroredTLPs, 'LidChanged')
            def HandleHDCPStatusChanged(mirroredtlp, state):
                if state == 'Closed':
                   ShutdownSystem()
        """
        def multidispatch(panel, state):
            self.__LidChanged(self, state)
        return multidispatch

    @LidChanged.setter
    def LidChanged(self, handler):
        if callable(handler):
            self.__LidChanged = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def LightChanged(self):
        """Passback the LightChanged Event

        ``Event``: Triggers when ambient light changes.

        The callback takes two arguments. The first one is the MirrorUIDevice
        instance triggering the event and the second is the ambient light
        level in the range of 0 to 255.

        Examples
        --------
        ::

            @event(MirroredTLPs, 'LightChanged')
            def HandleHDCPStatusChanged(mirroredtlp, level):
                print('{} Light Level Changed: {}'.format(mirroredtlp.DeviceAlias, level))
        """
        def multidispatch(panel, level):
            self.__LightChanged(self, level)
        return multidispatch

    @LightChanged.setter
    def LightChanged(self, handler):
        if callable(handler):
            self.__LightChanged = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def MotionDetected(self):
        """Passback the MotionDetected Event

        ``Event``: Triggers when Motion is detected.

        The callback takes two arguments. The first one is the MirrorUIDevice
        instance triggering the event and the second one is a string
        (``'Motion'`` or ``'No Motion'``).

        Examples
        --------
        ::

            @event(MirroredTLPs, 'MotionDetected')
            def HandleHDCPStatusChanged(mirroredtlp, state):
                if state == 'Motion':
                    mirroredtlp.Wake()
        """
        def multidispatch(panel, state):
            self.__MotionDetected(self, state)
        return multidispatch

    @MotionDetected.setter
    def MotionDetected(self, handler):
        if callable(handler):
            self.__MotionDetected = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def SleepChanged(self):
        """Passback the SleepChanged Event

        ``Event``: Triggers when sleep state changes.

        The callback takes two arguments. The first one is the MirrorUIDevice
        instance triggering the event and the second one is a string
        (``'Asleep'`` or ``'Awake'``).

        Examples
        --------
        ::

            @event(MirroredTLPs, 'SleepChanged')
            def HandleSleepChanged(mirrotlp, state):
                if state[0] == 'Awake' and not state[1]:
                    print('{} Sleep State Changed: {}'.format(mirrotlp.DeviceAlias, state))
        """
        def multidispatch(panel, state):
            self.__SleepChanged(self, state)
        return multidispatch

    @SleepChanged.setter
    def SleepChanged(self, handler):
        if callable(handler):
            self.__SleepChanged = handler
        else:
            raise ValueError('handler must be a function')


class MirroreBUSDevice(MirrorHost):
    """This class creates an object that contains a list of eBUSDevice
        objects to be used with the Button, Label, Level and Knob classes
        defined in this file.  The class object is also used in place of the
        eBUSDevice object for eBUS panel operations such as timer settings and
        mutes.
    """
    def __init__(self, eBUSList):
        """Initializes the module's MirroreBUSDevice in program.

        Parameters
        ----------
        eBUSList : list of extronlib.device.eBUSDevice
            List of eBUSDevice Objects

        Examples
        --------
        ::

            # Comment out the extronlib.ui import statement
            #from extronlib.ui import Button, Knob, Level

            # Add the import statement for the MirrorUI file in System Manager
            from MirrorUI import MirroreBUSDevice, Button, Knob, Level

            EBP1 = eBUSDevice(MainProcessor, 'eBUSAlias')
            EBP2 = eBUSDevice(MainProcessor, 'eBUSAlias_2')

            # Add the statement defining the MirroreBUSDevice and program using normal
            # methods and events
            MirroredEBPs = MirroreBUSDevice([EBP1, EBP2])
        """
        if not isinstance(eBUSList, list):
            raise TypeError('Parameter eBUSList is not a list')

        self.__objects = eBUSList
        for i, obj in enumerate(self.__objects):
            if not isinstance(obj, eBUSDevice):
                raise TypeError('Object {} in eBUSList is not an eBUSDevice'.format(i))

            obj.InactivityChanged = self.CallInactivityChanged
            obj.LidChanged = self.CallLidChanged
            obj.SleepChanged = self.CallSleepChanged

        self.InactivityChanged = self.__unassigned
        self.LidChanged = self.__unassigned
        self.SleepChanged = self.__unassigned


    # Methods:
    # The methods defined here operate the same as the eBUSDevice methods
    # except that the parameters are passed to all of the objects defined in
    # the eBUSList passed to the MirroreBUSDevice object.

    def Click(self, count=1, interval=None):
        """Play default buzzer sound on all devices

        Parameters
        ----------
        count : int
            number of buzzer sound to play. (Default value = 1)
        interval : float
            time gap between the starts of consecutive buzzer sounds. (Default value = None)

        Notes
        -----
        If count is greater than 1, interval must be provided.
        """
        for obj in self.__objects:
            obj.Click(count, interval)

    def GetMute(self, name):
        """Returns the current mute state for the given channel name on all
        devices.

        Parameters
        ----------
        name : str
            name of channel (``'Click'``).

        Returns
        -------
        str
            ``'On'`` or ``'Off'``
        """
        return self.__objects[0].GetMute(name)

    def SetInactivityTime(self, times):
        """Set the inactivity times when the InactivityChanged event will
        trigger for all devices.

        Parameters
        ----------
        times : list of ints
            list of times. Each time in whole seconds
        """
        for obj in self.__objects:
            obj.SetInactivityTime(times)

    def SetMute(self, name, mute):
        """Set the mute state for the given channel name on all devices.

        Parameters
        ----------
        name : str
            name of channel (``'Click'``).
        mute : str
            mute state (``'On'``, ``'Off'``)
        """
        for obj in self.__objects:
            obj.SetMute(name, mute)

    def SetSleepTimer(self, state, duration=None):
        """Enables or Disables the sleep timer on all devices. Either
        ``'On'`` or ``True`` enables sleep timer. ``'Off'`` or ``False``
        disables sleep timer.

        Parameters
        ----------
        state : bool, str
            whether to enable the display timer
        duration : int
            time in seconds to sleep (Default value = None)
        """
        for obj in self.__objects:
            obj.SetSleepTimer(state, duration)

    def Sleep(self):
        """Forces all devices to sleep immediately"""
        for obj in self.__objects:
            obj.Sleep()

    def Wake(self):
        """Forces all devices to wake up immediately"""
        for obj in self.__objects:
            obj.Wake()

    def CallInactivityChanged(self, panel, time):
        """Callback passed to device list to redirect event to new event call"""
        self.InactivityChanged(panel, time)

    def CallLidChanged(self, panel, state):
        """Callback passed to device list to redirect event to new event call"""
        self.LidChanged(panel, state)

    def CallSleepChanged(self, panel, state):
        """Callback passed to device list to redirect event to new event call"""
        self.InactivityChanged(panel, state)

    # Class Property Callbacks
    ##########################

    @property
    def DeviceAlias(self):
        """Defined Property to pass a list of Objects' DeviceAlias property

        Returns
        -------
        list of str
            list of the device aliases for all devices
        """
        return [obj.DeviceAlias for obj in self.__objects]

    @property
    def Host(self):
        """Defined Property to pass a list of Objects' Host property

        Returns
        -------
        list of extronlib.device.ProcessorDevice
            list of the Extron ProcessorDevice to which the eBUSDevice is
            connected for all devices.
        """
        return [obj.Host for obj in self.__objects]

    @property
    def ID(self):
        """Defined Property to pass ID

        Returns
        -------
        int
            the device's ID (set by DIP switch) for all devices
        """
        return self.__objects[0].ID

    @property
    def InactivityTime(self):
        """Defined Property to pass a list of Objects' InactivityTime
        property

        Returns
        -------
        list of int
            list of seconds since last activity for the all devices.

        Notes
        -----
        0 = Active, Nonzero = Time of inactivity.
        """
        return [obj.InactivityTime for obj in self.__objects]

    @property
    def LidState(self):
        """Defined Property to pass value of Objects[0]'s LidState property

        Returns
        -------
        list of str
            list of the current lid state for all devices (``'Opened'``
            or ``'Closed'``)
        """
        return [obj.LidState for obj in self.__objects]

    @property
    def ModelName(self):
        """Defined Property to pass a list of Objects' ModelName property
        Returns
        -------
        list of str
            list of the model name for all devices
        """
        return [obj.ModelName for obj in self.__objects]

    @property
    def Objects(self):
        """Defined Property to pass a list of Objects in the mirrored group
        Returns
        -------
        list of extronlib.device.eBUSDevice
            list of eBUSDevice objects defined in the class
        """
        return self.__objects

    @property
    def PartNumber(self):
        """Defined Property to pass a list of Objects' PartNumber property
        Returns
        -------
        list of str
            list of the part numbers for all devices
        """
        return [obj.PartNumber for obj in self.__objects]

    @property
    def SleepState(self):
        """Defined Property to pass a list of Objects' SleepState property

        Returns
        -------
        list of str
            list of the current sleep state for all devices (e.g.
            ``'Asleep'``, ``'Awake'``)
        """
        return [obj.SleepState for obj in self.__objects]

    @property
    def SleepTimer(self):
        """Defined Property to pass SleepTimer
        Returns
        -------
        int
            sleep timer timeout for all devices.
        """
        return self.__objects[0].SleepTimer

    @property
    def SleepTimerEnabled(self):
        """Defined Property to pass a list of Objects' SleepTimerEnabled
        property

        Returns
        -------
        bool
            current state of the sleep timer for all devices. ``True`` if
            enabled. ``False`` if disabled.
        """
        return self.__objects[0].SleepTimerEnabled

    # Class Event Callbacks
    #######################

    def __unassigned(self, *args):
        """If Module Events are not defined in user code, then do nothing."""
        pass

    @property
    def InactivityChanged(self):
        """Passback the InactivityChanged Event

        ``Event``: Triggers at times specified by SetInactivityTime() after
        state transition of inactivity timer.

        The callback takes two arguments. The first one is the
        MirroreBUSDevice instance triggering the event and time with a float
        value of inactivity time in seconds.

        Examples
        --------
        ::

            @event(MirroredEBPs, 'InactivityChanged')
            def HandleInactivityChanged(mirrorebp, time):
                if time == 3000:
                    ShowWarning()
                else:
                    ShutdownSystem()
        """
        def multidispatch(panel, time):
            self.__InactivityChanged(self, time)
        return multidispatch

    @InactivityChanged.setter
    def InactivityChanged(self, handler):
        if callable(handler):
            self.__InactivityChanged = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def LidChanged(self):
        """Passback the LidChanged Event

        ``Event``: Triggers when the Lid state changes.

        The callback takes two arguments. The first one is the
        MirroreBUSDevice instance triggering the event and the second is the
        current lid state (``'Opened'`` or ``'Closed'``).

        Examples
        --------
        ::

            @event(MirroredEBPs, 'LidChanged')
            def HandleLidChanged(mirrorebp, state):
                if state == 'Closed':
                   ShutdownSystem()
        """
        def multidispatch(panel, state):
            self.__LidChanged(self, state)
        return multidispatch

    @LidChanged.setter
    def LidChanged(self, handler):
        if callable(handler):
            self.__LidChanged = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def SleepChanged(self):
        """Passback the SleepChanged Event

        ``Event``: Triggers when sleep state changes.

        The callback takes two arguments. The first one is the
        MirroreBUSDevice instance triggering the event and the second one is a
        string (``'Asleep'`` or ``'Awake'``).

        Examples
        --------
        ::

            @event(MirroredEBPs, 'SleepChanged')
            def HandleSleepChanged(mirrorebp, state):
                if state[0] == 'HDMI' and not state[1]:
                    print('{} Sleep State Changed: {}'.format(mirrorebp.DeviceAlias, state))
        """
        def multidispatch(panel, state):
            self.__SleepChanged(self, state)
        return multidispatch

    @SleepChanged.setter
    def SleepChanged(self, handler):
        if callable(handler):
            self.__SleepChanged = handler
        else:
            raise ValueError('handler must be a function')


class Button():
    """This class takes either a singular UIDevice or eBUSDevice or a
        MirrorUIDevice or MirroreBUSDevice object and handles the properties,
        methods and events for all Button Objects created within this class.
    """
    def __init__(self, UIHost, ID, holdTime=None, repeatTime=None):
        """Representation of Hard/Soft buttons.

        Parameters
        ----------
        UIHost : see note.
            device or mirrored devices hosting this UI Object.
        ID : int, str
            ID or Name of the UIObject.
        holdTime : float
            Time for Held event.
        repeatTime : float
            Time for Repeated event.

        Notes
        -----
        * This class is a direct replacement for the extronlib.ui.Button
          class.
        * All properties, methods and events in extronlib.ui.Button are in
          this class and operate in the same fashion.
        * The UIHost parameter can take objects of type:

            * extronlib.device.eBUSDevice
            * extronlib.device.UIDevice
            * MirrorUI.MirroreBUSDevice
            * MirrorUI.MirrorUIDevice

        Examples
        --------
        ::

            # Create an instance of button ID 101 for all panels
            powerOn = Button(MirroredTLPs, 101)
        """
        self.__objects = []

        if isinstance(UIHost, MirrorHost):
            self.__objects = [OldButton(obj, ID, holdTime, repeatTime) for obj in UIHost.Objects]
        else:
            self.__objects = [OldButton(UIHost, ID, holdTime, repeatTime)]

        for obj in self.__objects:
            obj.Pressed = self.CallPressed
            obj.Released = self.CallReleased
            obj.Tapped = self.CallTapped
            obj.Held = self.CallHeld
            obj.Repeated = self.CallRepeated

        self.Pressed = self.__unassigned
        self.Released = self.__unassigned
        self.Tapped = self.__unassigned
        self.Held = self.__unassigned
        self.Repeated = self.__unassigned

    # Methods:
    # The methods defined here operate the same as the Button methods except
    # that the parameters are passed to all of the objects created from the
    # devices passed to the class.

    def CustomBlink(self, rate, stateList):
        """Makes the buttons on all devices cycle through each of the
            states provided.

        Parameters
        ----------
        rate : float
            duration of time in seconds for one visual state to stay
            until replaced by the next visual state.
        stateList : list of ints
            list of visual states that this button blinks among.
        """
        for obj in self.__objects:
            obj.CustomBlink(rate, stateList)

    def SetBlinking(self, rate, stateList):
        """Makes the buttons on all devices cycle, at ADA compliant rates,
        through each of the states provided.

        Parameters
        ----------
        rate : str
            ADA compliant blink rate. (``'Slow'``, ``'Medium'``,
            ``'Fast'``)
        stateList : list of ints
            list of visual states that this button blinks among.
        """
        for obj in self.__objects:
            obj.SetBlinking(rate, stateList)

    def SetEnable(self, enable):
        """Enable or disable a UI control object on all devices

        Parameters
        ----------
        enable : bool
            True`` to enable the object or ``False`` to disable it.
        """
        for obj in self.__objects:
            obj.SetEnable(enable)

    def SetState(self, state):
        """Set the current visual state on all devices

        Parameters
        ----------
        state : int
            visual state number.
        """
        for obj in self.__objects:
            obj.SetState(state)

    def SetText(self, text):
        """Specify text to display on the UIObject on all devices

        Parameters
        ----------
        text : str
            text to display.
        """
        for obj in self.__objects:
            obj.SetText(text)

    def SetVisible(self, visible):
        """Change the visibility of a UI control object on all devices

        Parameters
        ----------
        visible : bool
            True`` to make the object visible or ``False`` to hide it.
        """
        for obj in self.__objects:
            obj.SetVisible(visible)

    def CallPressed(self, button, state):
        """Callback passed to device list to redirect event to new event call"""
        self.Pressed(button, state)

    def CallReleased(self, button, state):
        """Callback passed to device list to redirect event to new event call"""
        self.Released(button, state)

    def CallTapped(self, button, state):
        """Callback passed to device list to redirect event to new event call"""
        self.Tapped(button, state)

    def CallHeld(self, button, state):
        """Callback passed to device list to redirect event to new event call"""
        self.Held(button, state)

    def CallRepeated(self, button, state):
        """Callback passed to device list to redirect event to new event call"""
        self.Repeated(button, state)

    # Class Property Callbacks
    ##########################

    @property
    def BlinkState(self):
        """Defined Property to pass BlinkState

        Returns
        -------
        str
            current blink state ('Not blinking' or 'Blinking') for all
            devices.
        """
        return self.__objects[0].BlinkState

    @property
    def Enabled(self):
        """Defined Property to pass Enabled

        Returns
        -------
        bool
            ``'True`` if the control object is enabled else ``False`` for all
            devices.
        """
        return self.__objects[0].Enabled

    @property
    def Host(self):
        """Defined Property to pass a list of Objects' Host property

        Returns
        -------
        list of extronlib.ui.Button
            list of the UIDevice objects that host this control object.

        Notes
        -----
        This is a deviation from the extronlib.ui.Button class.  In this
        class a list of the Hosts for each Button object created is
        returned in a list of UIDevice or eBUSDevice objects
        """
        return [obj.Host for obj in self.__objects]

    @property
    def ID(self):
        """Defined Property to pass ID

        Returns
        -------
        int
            the ID for the object on all devices
        """
        return self.__objects[0].ID

    @property
    def Objects(self):
        """Defined Property to pass a list of Objects in the mirrored group

        Returns
        -------
        list of extronlib.ui.Button
            list of Button objects defined in the class
        """
        return self.__objects

    @property
    def Name(self):
        """Defined Property to pass Name

        Returns
        -------
        str
            the object's Name on all devices
        """
        return self.__objects[0].Name

    @property
    def PressedState(self):
        """Defined Property to pass a list of Objects' PressedState property

        Returns
        -------
        bool
            the mirror device objects' pressed state.  ``True`` if and
            button in the group is pressed, else ``False``
        """
        return any([obj.PressedState for obj in self.__objects])

    @property
    def State(self):
        """Defined Property to pass State

        Returns
        -------
        int
            the object's visual state number on all devices
        """
        return self.__objects[0].State

    @property
    def Visible(self):
        """Defined Property to pass a list of Objects' Visible property

        Returns
        -------
        bool
            the object's visible state for all devices.  ``True`` if
            visible, else ``False``
        """
        return self.__objects[0].Visible

    # Class Event Callbacks
    #######################

    def __unassigned(self, *args):
        """If Module Events are not defined in user code, then do nothing."""
        pass

    @property
    def Pressed(self):
        """Passback the Pressed Event

        ``Event``: Get/Set the callback when the button is pressed

        The callback function must accept exactly two parameters, which are
        the mirrored Button that triggers the event and the state
        (e.g. 'Pressed').

        Examples
        --------
        ::

            @event(powerOn, 'Pressed')
            def PowerOn(mirrorbutton, state):
                mirrorbutton.SetBlinking('Medium', [2, 4])
                mainProjector.Send('POWER ON')
        """
        def multidispatch(button, state):
            self.__Pressed(self, state)
        return multidispatch

    @Pressed.setter
    def Pressed(self, handler):
        if callable(handler):
            self.__Pressed = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def Released(self):
        """Passback the Released Event

        ``Event``: Get/Set the callback when the button is released

        The callback function must accept exactly two parameters, which are
        the mirrored Button that triggers the event and the state
        (e.g. 'Released').

        Examples
        --------
        ::

            @event(closeSetupPage, 'Released')
            def ClosePage(mirrorbutton, state):
                MirroredTLPs.ShowPage('Main')
        """
        def multidispatch(button, state):
            self.__Released(self, state)
        return multidispatch

    @Released.setter
    def Released(self, handler):
        if callable(handler):
            self.__Released = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def Tapped(self):
        """Passback the Tapped Event

        ``Event``: Get/Set the callback when tap event is triggered

        The callback function must accept exactly two parameters, which are
        the mirrored Button that triggers the event and the state
        (e.g. 'Tapped').

        Examples
        --------
        ::

            @event(zoomIn, 'Tapped')
            def ZoomInTapped(mirrorbutton, state):
                PTZ.Send('zoom +1')   # Nudge the zoom
        """
        def multidispatch(button, state):
            self.__Tapped(self, state)
        return multidispatch

    @Tapped.setter
    def Tapped(self, handler):
        if callable(handler):
            self.__Tapped = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def Held(self):
        """Passback the Held Event

        ``Event``: Get/Set the callback when hold expire event is triggered

        The callback function must accept exactly two parameters, which are
        the mirrored Button that triggers the event and the state
        (e.g. 'Held').

        Examples
        --------
        ::

            @event(showSetupPage, 'Held')
            def ShowSetupPage(mirrorbutton, state):
                MirroredTLPs.ShowPage('Setup Page')
        """
        def multidispatch(button, state):
            self.__Held(self, state)
        return multidispatch

    @Held.setter
    def Held(self, handler):
        if callable(handler):
            self.__Held = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def Repeated(self):
        """Passback the Repeated Event

        ``Event``: Get/Set the callback when repeat event is triggered

        The callback function must accept exactly two parameters, which are
        the mirrored Button that triggers the event and the state
        (e.g. 'Repeated').

        Examples
        --------
        ::

            @event(volumeUp, 'Repeated')
            def VolUp(mirrorbutton, state):
                global VolLevel
                if VolLevel < 20:
                    VolLevel += 1
                    mainProjector.Send('VOLUME {}'.format(VolLevel))
        """
        def multidispatch(button, state):
            self.__Repeated(self, state)
        return multidispatch

    @Repeated.setter
    def Repeated(self, handler):
        if callable(handler):
            self.__Repeated = handler
        else:
            raise ValueError('handler must be a function')


class Knob():
    """This class takes either a singular UIDevice or eBUSDevice or a
        MirrorUIDevice or MirroreBUSDevice object and handles the properties,
        methods and events for all Knob Objects created within this class.
    """

    def __init__(self, UIHost, ID, holdTime=None, repeatTime=None):
        """Knob is a rotary control that has 36 steps for a full revolution.

        Parameters
        ----------
        UIHost : see note.
            device or mirrored devices hosting this UI Object.
        ID : int, str
            ID or Name of the UIObject.

        Notes
        -----
        * This class is a direct replacement for the extronlib.ui.Knob
          class.
        * All properties, methods and events in extronlib.ui.Knob are in
          this class and operate in the same fashion.
        * The UIHost parameter can take objects of type:

            * extronlib.device.eBUSDevice
            * extronlib.device.UIDevice
            * MirrorUI.MirroreBUSDevice
            * MirrorUI.MirrorUIDevice

        Examples
        --------
        ::

            # Creates an instance of the knob for all eBUS panels
            EBPKnob = Knob(MirroredEBPs, 61001)
        """
        self.__objects = []

        if isinstance(UIHost, MirrorHost):
            self.__objects = [OldKnob(obj, ID) for obj in UIHost.Objects]
        else:
            self.__objects = [OldKnob(UIHost, ID)]

        for obj in self.__objects:
            obj.Turned = self.CallTurned

        self.Turned = self.__unassigned

    # Methods:
    # The methods defined here operate the same as the Knob methods except
    # that the parameters are passed to all of the objects created from the
    # devices passed to the class.

    def CallTurned(self, knob, direction):
        """Callback passed to device list to redirect event to new event call"""
        self.Turned(knob, direction)

    # Class Property Callbacks
    ##########################

    @property
    def Host(self):
        """Defined Property to pass a list of Objects' Host property

        Returns
        -------
        list of extronlib.ui.Knob
            list of the UIDevice objects that host this control object.

        Notes
        -----
        This is a deviation from the extronlib.ui.Knob class.  In this
        class a list of the Hosts for each Knob object created is returned
        in a list of UIDevice or eBUSDevice objects

        """
        return [obj.Host for obj in self.__objects]

    @property
    def ID(self):
        """Defined Property to pass ID

        Returns
        -------
        int
            the ID for the object on all devices
        """
        return self.__objects[0].ID

    @property
    def Objects(self):
        """Defined Property to pass a list of Objects in the mirrored group

        Returns
        -------
        list of extronlib.ui.Knob
            list of Knob objects defined in the class
        """
        return self.__objects

    # Class Event Callbacks
    #######################

    def __unassigned(self, *args):
        """If Module Events are not defined in user code, then do nothing."""
        pass

    @property
    def Turned(self):
        """Passback the Turned Event

        ``Event``: Get/Set callback when knob is turned

        The callback takes two parameters. The first one is the mirrored Knob
        itself and the second one is a signed integer indicating steps that
        was turned. Positive values indicate clockwise rotation.

        Examples
        --------
        ::

            @event(mainKnob, 'Turned')
            def handleMainKnob(mirrorknob, direction):
                if direction > 0:
                    for i in range(direction):
                        mainProjector.Send('VOLUME UP')
                else:
                    for i in range(direction, 0):
                        mainProjector.Send('VOLUME DOWN')
        """
        def multidispatch(knob, direction):
            self.__Turned(self, direction)
        return multidispatch

    @Turned.setter
    def Turned(self, handler):
        if callable(handler):
            self.__Turned = handler
        else:
            raise ValueError('handler must be a function')


class Label():
    """This class takes either a singular UIDevice or eBUSDevice or a
        MirrorUIDevice or MirroreBUSDevice object and handles the properties
        and methods for all Label Objects created within this class.
    """

    def __init__(self, UIHost, ID):
        """Label object displays text string on the screen.

        Parameters
        ----------
        UIHost : see note.
            device or mirrored devices hosting this UI Object.
        ID : int, str
            ID or Name of the UIObject.

        Notes
        -----
        * This class is a direct replacement for the extronlib.ui.Label
          class.
        * All properties, methods and events in extronlib.ui.Label are in
          this class and operate in the same fashion.
        * The UIHost parameter can take objects of type:

            * extronlib.device.UIDevice
            * MirrorUI.MirrorUIDevice

        Examples
        --------
        ::

            # Creates an instance of label ID 3001 for all panels
            RoomLabel = Label(MirroredTLPs, 3001)
        """
        self.__objects = []

        if isinstance(UIHost, MirrorHost):
            self.__objects = [OldLabel(obj, ID) for obj in UIHost.Objects]
        else:
            self.__objects = [OldLabel(UIHost, ID)]

    # Methods:
    # The methods defined here operate the same as the Label methods except
    # that the parameters are passed to all of the objects created from the
    # devices passed to the class.

    def SetText(self, text):
        """Specify text to display on the UIObject for all devices.

        Parameters
        ----------
        text : str
            text to display.
        """
        for obj in self.__objects:
            obj.SetText(text)

    def SetVisible(self, visible):
        """Change the visibility of a UI control object on all devices

        Parameters
        ----------
        visible : bool
            True`` to make the object visible or ``False`` to
            hide it.
        """
        for obj in self.__objects:
            obj.SetVisible(visible)

    # Class Property Callbacks
    ##########################

    @property
    def Host(self):
        """Defined Property to pass a list of Objects' Host property

        Returns
        -------
        list of extronlib.device.UIDevice, extronlib.device.eBUSDevice
            list of the UIDevice and eBUSDevice objects that host this
            control object.

        Notes
        -----
        This is a deviation from the extronlib.ui.Label class.  In this
        class a list of the Hosts for each Label object created is
        returned in a list of UIDevice and/or eBUSDevice objects.
        """
        return [obj.Host for obj in self.__objects]

    @property
    def ID(self):
        """Defined Property to pass ID

        Returns
        -------
        list of int
            list of the ID for the object on all devices
        """
        return self.__objects[0].ID

    @property
    def Name(self):
        """Defined Property to pass Name

        Returns
        -------
        str
            the object's Name on all devices
        """
        return self.__objects[0].Name

    @property
    def Objects(self):
        """Defined Property to pass a list of Objects in the mirrored group

        Returns
        -------
        list of extronlib.ui.Label
            list of Label objects defined in the class
        """
        return self.__objects

    @property
    def Visible(self):
        """Defined Property to pass Visible

        Returns
        -------
        bool
            the object's visible state for all devices.  ``True`` if
            visible, else ``False``
        """
        return self.__objects[0].Visible


class Level():
    """This class takes either a singular UIDevice or eBUSDevice or a
        MirrorUIDevice or MirroreBUSDevice object and handles the properties
        and methods for all Level Objects created within this class.
    """

    def __init__(self, UIHost, ID):
        """This module defines interfaces of Level UI.

        Parameters
        ----------
        UIHost : see note.
            device or mirrored devices hosting this UI Object.
        ID : int, str
            ID or Name of the UIObject.

        Notes
        -----
        * This class is a direct replacement for the extronlib.ui.Level
          class.
        * All properties, methods and events in extronlib.ui.Level are in
          this class and operate in the same fashion.
        * The UIHost parameter can take objects of type:

            * extronlib.device.eBUSDevice
            * extronlib.device.UIDevice
            * MirrorUI.MirroreBUSDevice
            * MirrorUI.MirrorUIDevice

        Examples
        --------
        ::

            # Creates an instance of level ID 4001 for all panels
            VolumeLevel = Level(MirroredTLPs, 4001)
        """
        self.__objects = []

        if isinstance(UIHost, MirrorHost):
            self.__objects = [OldLevel(obj, ID) for obj in UIHost.Objects]
        else:
            self.__objects = [OldLevel(UIHost, ID)]

    # Methods:
    # The methods defined here operate the same as the Level methods except
    # that the parameters are passed to all of the objects created from the
    # devices passed to the class.

    def Dec(self):
        """Nudge the level down a step for all devices"""
        for obj in self.__objects:
            obj.Dec()

    def Inc(self):
        """Nudge the level up a step for all devices"""
        for obj in self.__objects:
            obj.Inc()

    def SetLevel(self, level):
        """Set the current level for all devices

        Parameters
        ----------
        level : int
            Discrete value of the level object.
        """
        for obj in self.__objects:
            obj.SetLevel(level)

    def SetRange(self, Min, Max, Step=1):
        """Set level object's allowed range and the step size for all devices

        Parameters
        ----------
        Min : int
            Minimum level
        Max : int
            Maximum level
        Step : int
            Optional step size for Inc() and Dec(). (Default value = 1)

        Notes
        -----
        * The default range is 0 - 100 with a step size of 1.
        * For multi-state levels, you must set the level range to match
          the number of states in the level.
        """
        for obj in self.__objects:
            obj.SetRange(Min, Max, Step)

    def SetVisible(self, visible):
        """Change the visibility of a UI control object for all devices

        Parameters
        ----------
        visible : bool
            True`` to make the object visible or ``False`` to
            hide it.
        """
        for obj in self.__objects:
            obj.SetVisible(visible)

    # Class Property Callbacks
    ##########################

    @property
    def Host(self):
        """Defined Property to pass a list of Objects' Host property

        Returns
        -------
        list of extronlib.device.UIDevice, extronlib.device.eBUSDevice
            list of the UIDevice and eBUSDevice objects that host this
            control object.

        Notes
        -----
        This is a deviation from the extronlib.ui.Level class.  In this
        class a list of the Hosts for each Level object created is
        returned in a list of UIDevice and eBUSDevice objects.
        """
        return [obj.Host for obj in self.__objects]

    @property
    def ID(self):
        """Defined Property to pass ID

        Returns
        -------
        int
            the ID for the object on all devices
        """
        return self.__objects[0].ID

    @property
    def Level(self):
        """Defined Property to pass Level

        Returns
        -------
        int
            the object's current level for all devices
        """
        return self.__objects[0].Level

    @property
    def Max(self):
        """Defined Property to pass Max

        Returns
        -------
        int
            the object's upper bound of the level for all devices
        """
        return self.__objects[0].Max

    @property
    def Min(self):
        """Defined Property to pass Min

        Returns
        -------
        int
            the object's lower bound of the level for all devices
        """
        return self.__objects[0].Min

    @property
    def Name(self):
        """Defined Property to pass Name

        Returns
        -------
        str
            the object's Name on all devices
        """
        return self.__objects[0].Name

    @property
    def Objects(self):
        """Defined Property to pass a list of Objects in the mirrored group

        Returns
        -------
        list of extronlib.ui.Level
            list of Label objects defined in the class
        """
        return self.__objects

    @property
    def Visible(self):
        """Defined Property to pass Visible

        Returns
        -------
        bool
            the object's visible state for all devices.  ``True`` if
            visible, else ``False``
        """
        return self.__objects[0].Visible


class Slider():
    """This class takes either a singular UIDevice or a
        MirrorUIDevice object and handles the properties
        and methods for all Level Objects created within this class.
    """

    def __init__(self, UIHost, ID):
        """This module defines interfaces of Slider UI.

        Parameters
        ----------
        UIHost : see note.
            device or mirrored devices hosting this UI Object.
        ID : int, str
            ID or Name of the UIObject.

        Notes
        -----
        * This class is a direct replacement for the extronlib.ui.Slider
          class.
        * All properties, methods and events in extronlib.ui.Slider are in
          this class and operate in the same fashion.
        * The UIHost parameter can take objects of type:

            * extronlib.device.UIDevice
            * MirrorUI.MirrorUIDevice

        Examples
        --------
        ::

            # Creates an instance of Slider ID 4001 for all panels
            VolumeSlider = Slider(MirroredTLPs, 4001)
        """
        self.__objects = []

        if isinstance(UIHost, MirrorHost):
            self.__objects = [OldSlider(obj, ID) for obj in UIHost.Objects]
        else:
            self.__objects = [OldSlider(UIHost, ID)]

        for obj in self.__objects:
            obj.Changed = self.CallChanged
            obj.Pressed = self.CallPressed
            obj.Released = self.CallReleased

        self.Changed = self.__unassigned
        self.Pressed = self.__unassigned
        self.Released = self.__unassigned

    # Methods:
    # The methods defined here operate the same as the Level methods except
    # that the parameters are passed to all of the objects created from the
    # devices passed to the class.

    def SetEnable(self, enable):
        """Enable or disable a UI control object on all devices

        Parameters
        ----------
        enable : bool
            True`` to enable the object or ``False`` to disable
            it.
        """
        for obj in self.__objects:
            obj.SetEnable(enable)

    def SetFill(self, Fill):
        """Set the current fill level for all devices

        Parameters
        ----------
        Fill : int
            Discrete value of the slider object.
        """
        for obj in self.__objects:
            obj.SetFill(Fill)

    def SetRange(self, Min, Max, Step=1):
        """Set slider object's allowed range and the step size for all
        devices

        Parameters
        ----------
        Min : int
            Minimum fill
        Max : int
            Maximum fill
        Step : int
            Optional step size for Inc() and Dec(). (Default value = 1)

        Notes
        -----
        The default range is 0 - 100 with a step size of 1.
        """
        for obj in self.__objects:
            obj.SetRange(Min, Max, Step)

    def SetVisible(self, visible):
        """Change the visibility of a UI control object for all devices

        Parameters
        ----------
        visible : bool
            True`` to make the object visible or ``False`` to
            hide it.
        """
        for obj in self.__objects:
            obj.SetVisible(visible)

    def CallChanged(self, slider, state, value):
        """Callback passed to device list to redirect event to new event call"""
        self.Changed(slider, state, value)

    def CallPressed(self, slider, state, value):
        """Callback passed to device list to redirect event to new event call"""
        self.Pressed(slider, state, value)

    def CallReleased(self, slider, state, value):
        """Callback passed to device list to redirect event to new event call"""
        self.Released(slider, state, value)

    # Class Property Callbacks
    ##########################

    @property
    def Enabled(self):
        """Defined Property to pass Enabled

        Returns
        -------
        int
            the object's current Enabled for all devices
        """
        return self.__objects[0].Enabled

    @property
    def Fill(self):
        """Defined Property to pass Fill

        Returns
        -------
        int
            the object's current Fill for all devices
        """
        return self.__objects[0].Fill

    @property
    def Host(self):
        """Defined Property to pass a list of Objects' Host property

        Returns
        -------
        list of extronlib.device.UIDevice, extronlib.device.eBUSDevice
            list of the UIDevice and eBUSDevice objects that host this
            control object.

        Notes
        -----
        This is a deviation from the extronlib.ui.Slider class.  In this
        class a list of the Hosts for each Slider object created is
        returned in a list of UIDevice and eBUSDevice objects.
        """
        return [obj.Host for obj in self.__objects]

    @property
    def ID(self):
        """Defined Property to pass ID

        Returns
        -------
        int
            the ID for the object on all devices
        """
        return self.__objects[0].ID

    @property
    def Max(self):
        """Defined Property to pass Max

        Returns
        -------
        int
            the object's upper bound of the fill for all devices
        """
        return self.__objects[0].Max

    @property
    def Min(self):
        """Defined Property to pass Min

        Returns
        -------
        int
            the object's lower bound of the fill for all devices
        """
        return self.__objects[0].Min

    @property
    def Name(self):
        """Defined Property to pass Name

        Returns
        -------
        str
            the object's Name on all devices
        """
        return self.__objects[0].Name

    @property
    def Objects(self):
        """Defined Property to pass a list of Objects in the mirrored group

        Returns
        -------
        list of extronlib.ui.Slider
            list of Slider objects defined in the class
        """
        return self.__objects

    @property
    def Step(self):
        """Defined Property to pass Step

        Returns
        -------
        int
            the object's Step on all devices
        """
        return self.__objects[0].Step

    @property
    def Visible(self):
        """Defined Property to pass Visible

        Returns
        -------
        bool
            the object's visible state for all devices.  ``True`` if
            visible, else ``False``
        """
        return self.__objects[0].Visible

    # Class Event Callbacks
    #######################

    def __unassigned(self, *args):
        """If Module Events are not defined in user code, then do nothing."""
        pass

    @property
    def Changed(self):
        """Passback the Changed Event

        ``Event``: Get/Set the callback when the slider thumb postion is
        changed.

        The callback takes three arguments. The first is the mirrored Slider
        instance triggering the event, the second is the state, and the third
        is the new slider value.

        Examples
        --------
        ::

            @event(ProgramAudio, 'Changed')
            def handleProgramAudio(mirrorslider, state, value):
                if state == 'Changed':
                    # Send new program audio level
        """
        def multidispatch(slider, state, value):
            self.__Changed(self, state, value)
        return multidispatch

    @Changed.setter
    def Changed(self, handler):
        if callable(handler):
            self.__Changed = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def Pressed(self):
        """Passback the Pressed Event

        ``Event``: Get/Set the callback when the slider is pressed.

        The callback takes three arguments. The first is the mirrored Slider
        instance triggering the event, the second is the state, and the third
        is the new slider value.

        Examples
        --------
        ::

            @event(ProgramAudio, 'Pressed')
            def handleProgramAudio(mirrorslider, state, value):
                if state == 'Pressed':
                    # Send new program audio level
        """
        def multidispatch(slider, state, value):
            self.__Pressed(self, state, value)
        return multidispatch

    @Pressed.setter
    def Pressed(self, handler):
        if callable(handler):
            self.__Pressed = handler
        else:
            raise ValueError('handler must be a function')

    @property
    def Released(self):
        """Passback the Released Event

        ``Event``: Get/Set the callback when the slider is released.

        The callback takes three arguments. The first is the mirrored Slider
        instance triggering the event, the second is the state, and the third
        is the new slider value.

        Examples
        --------
        ::

            @event(ProgramAudio, 'Released')
            def handleProgramAudio(mirrorslider, state, value):
                if state == 'Released':
                    # Send new program audio level
        """
        def multidispatch(slider, state, value):
            self.__Released(self, state, value)
        return multidispatch

    @Released.setter
    def Released(self, handler):
        if callable(handler):
            self.__Released = handler
        else:
            raise ValueError('handler must be a function')
