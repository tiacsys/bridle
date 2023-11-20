import logging
import pathlib

from twister_harness import Shell
from twister_harness.twister_harness_config import DeviceConfig
from twister_harness.device.hardware_adapter import HardwareAdapter

logger = logging.getLogger(__name__)

pytest_plugins = (
    'twister_harness.fixtures'
)


class robot_device():
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, type, pathname, serial, baud, timeout) -> None:
        device_config = DeviceConfig(
            type=type,
            build_dir=pathlib.Path(pathname),
            base_timeout=float(timeout),
            platform=None,
            serial=serial,
            baud=baud,
            runner=None,
            id=None,
            product=None,
            serial_pty=None,
            west_flash_extra_args="",
            pre_script=None,
            post_script=None,
            post_flash_script=None,
        )
        self.device = HardwareAdapter(device_config)

        # use here the function launch() if we found a way to
        # get the device config values without calling a test
        # function in main.py
        self.device.close()
        self.device._clear_internal_resources()

        # prepare the HardwareAdapter for connection
        self.device._device_run.set()
        self.device._start_reader_thread()

        self.shell = Shell(self.device, timeout=20.0)
        self.lines: str = None

    def __del__(self) -> None:
        self.device.close()
        self.device._clear_internal_resources()

    def connect_device(self):
        logger.info('connect to device')
        self.device.connect()

    def disconnect_device(self):
        logger.info('disconnect from device')
        self.device.disconnect()
