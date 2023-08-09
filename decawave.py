import platform
import time
from typing import Callable

import serial
import serial.tools.list_ports


class DecawaveModule:
    """
    Decawave UWB module class.

    Decawave DWM1001 modules contain a pre-built firmware library called
    "Positioning And Networking Stack" (PANS), which provides Application
    Programming Interface (API) to communicate with the modules.

    :param bool debug: If true, print debug information to the terminal.

    Usage example:

    >>> dwm = DecawaveModule()
    >>> dwm.open()
    >>> dwm.les()
    >>> dwm.les()
    >>> dwm.close()

    """
    def __init__(self, debug: bool = True) -> None:
        self.debug = debug
        
        self.ser = None
        self.stop_reading = False


    def _find_portname(self) -> str:
        """Find the port name of the module."""
        portname = None
        comports = serial.tools.list_ports.comports()
        for comport in comports:
            # SEGGER Embedded Studio is used for the software development
            # of the Decawave modules.
            if comport.manufacturer == "SEGGER":
                portname = comport.name
                break
        if portname is None:
            raise RuntimeError("DWM: No serial port found")
        if platform.system() == "Linux":
            portname = f"/dev/{portname}"
        return portname


    def _write(self, shell_command: str):
        """Write a shell command."""
        self.ser.write(shell_command.encode())
        self.ser.write(b'\n')


    def _read(self, datahandler: Callable = None, **kwargs):
        """Read the output of the shell command."""
        while True:
            try:
                if self.stop_reading:
                    break
                data = self.ser.readline(1024)
                if len(data) == 0:
                    break
                if self.debug:
                    print(data)
                if not datahandler:
                    continue
                datahandler(data, **kwargs)
            except KeyboardInterrupt:
                break
        self.stop_reading = False


    def _shell_mode_on(self, delay: int = 0):
        """Go to the shell mode by writing ENTER twice."""
        if delay > 0:
            time.sleep(delay)
        self.ser.write(b'\r\r')
        self._read()


    def _shell_mode_off(self):
        """Exit the shell mode and go the generic mode."""
        self._write("quit")
        self._read()


    def open(self):
        """Open the serial port of the module."""
        portname = self._find_portname()
        # Specify a timeout since the readline() could block forever if
        # no newline character is received.
        self.ser = serial.Serial(portname, baudrate=115200, timeout=1)
        if self.debug:
            print(f"DWM: Serial port {portname} opened")
        self._shell_mode_on()


    def close(self):
        """Close the serial port of the module."""
        if self.ser is None:
            return
        self._shell_mode_off()
        self.ser.close()
        if self.debug:
            print("DWM: Serial port closed")


    def stop(self):
        """Stop reading the output of the shell command."""
        self.stop_reading = True


    # -----------------------------------------------------------------
    # PANS API command group: BASE
    # -----------------------------------------------------------------
    def help(self):
        """Show help."""
        self._write("help")
        self._read()


    # -----------------------------------------------------------------
    # PANS API command group: SYS
    # -----------------------------------------------------------------
    def system_free_memory(self):
        """Show free memory on the heap."""
        self._write("f")
        self._read()


    def system_reset(self):
        """Reboot the system."""
        self._write("reset")
        # The system will restart in the generic mode by default, thus
        # switch back to the shell mode.
        self._shell_mode_on(delay=2)


    def system_info(self):
        """Show system info"""
        self._write("si")
        self._read()


    def system_uptime(self):
        """Show device uptime."""
        self._write("ut")
        self._read()


    def system_factory_reset(self):
        """Perform a factory reset for the system."""
        self._write("frst")
        self._shell_mode_on(delay=5)


    # -----------------------------------------------------------------
    # PANS API command group: SENS
    # -----------------------------------------------------------------
    def sens_aid(self):
        """Read ACC device ID."""
        self._write("aid")
        self._read()


    def sens_av(self):
        """Read ACC values."""
        self._write("av")
        self._read()


    # -----------------------------------------------------------------
    # PANS API command group: LE
    # -----------------------------------------------------------------
    def les(self, datahandler: Callable = None, **kwargs):
        """Show range measurements and position.

        Show distances to ranging anchors and the position if location
        engine is enabled. Sending this command multiple times will
        turn on/off this functionality.

        :param Callable datahandler: Function which handles the output data.

        """
        self._write("les")
        self._read(datahandler, **kwargs)


    def lec(self, datahandler: Callable = None, **kwargs):
        """Show range measurements and position in CSV.

        Show distances to ranging anchors and the position if location
        engine is enabled in CSV format. Sending this command multiple
        times will turn on/off this functionality.

        :param Callable datahandler: Function which handles the output data.

        """
        self._write("lec")
        self._read(datahandler, **kwargs)


    def lep(self, datahandler: Callable = None, **kwargs):
        """Show position in CSV.

        Show position in CSV format. Sending this command multiple
        times will turn on/off this functionality.

        :param Callable datahandler: Function which handles the output data.

        """
        self._write("lep")
        self._read(datahandler, **kwargs)


    # -----------------------------------------------------------------
    # PANS API command group: UWBMAC
    # -----------------------------------------------------------------
    def show_anchor_list(self):
        """Show AN (anchor node) list."""
        self._write("la")
        self._read()


    def show_bridge_list(self):
        """Show BN (bridge node) list."""
        self._write("lb")
        self._read()


    def get_mode(self):
        """Get node mode."""
        self._write("nmg")
        self._read()


    def set_mode_an(self):
        """Set mode to AN (anchor node) and reset the node."""
        self._write("nma")
        self._shell_mode_on(delay=2)


    def set_mode_ain(self):
        """Set mode to AIN (initiator anchor node) and reset the node."""
        self._write("nmi")
        self._shell_mode_on(delay=2)


    def set_mode_tn(self):
        """Set mode to active TN (tag node) and reset the node."""
        self._write("nmt")
        self._shell_mode_on(delay=2)


    def set_mode_tnlp(self):
        """Set mode to low power TN (tag node) and reset the node."""
        self._write("nmtl")
        self._shell_mode_on(delay=2)


    def set_mode_bn(self):
        """Set mode to BN (bridge node)."""
        self._write("nmb")
        self._shell_mode_on(delay=2)


    def show_iot_data(self):
        """Show the incoming IoT data.

        Sending this command multiple times will turn on/off this 
        functionality.

        """
        self._write("udi")
        self._read()
