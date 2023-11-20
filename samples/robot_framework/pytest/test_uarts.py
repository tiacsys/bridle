import logging

from robot_device import robot_device

logger = logging.getLogger(__name__)


class test_uarts(robot_device):

    def write_line_to_uart(self, cmd):
        self.lines = ""
        logger.info(f'send "{cmd}" command')
        self.lines = self.shell.exec_command(cmd)

    def wait_for_line_on_uart(self, expected_response):
        logger.info(f'check response: {expected_response}')
        assert any([expected_response in line for line in self.lines]), \
            'expected response not found'
        logger.info('response is valid')
        self.lines = ""
