import logging

from robot_device import robot_device

logger = logging.getLogger(__name__)


class test_leds(robot_device):

    def led_on(self, led, num):
        logger.info(f'send "led on to {led} {num}" command')
        lines = self.shell.exec_command(f'led on {led} {num}')
        for line in lines:
            if "Error" in str(line):
                raise OSError(f'{line}.\nTest failed.')
        logger.info(f'response is valid.')
