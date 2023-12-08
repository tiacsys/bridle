import logging
import robot

from twister_harness.twister_harness_config import TwisterHarnessConfig
from twister_harness.device.device_adapter import DeviceAdapter

logger = logging.getLogger(__name__)


def test_sample_device_robot(twister_harness_config: TwisterHarnessConfig, dut: DeviceAdapter):
    # disconnect from device to re-open it in robot
    dut.disconnect()

    logFile = open('mylog.txt', 'w')

    ret = robot.run('bridle/samples/robot_framework/pytest/',
                    variable=[f'type:{twister_harness_config.devices[0].type}',
                              f'pathname:{twister_harness_config.devices[0].build_dir}',
                              f'serial:{twister_harness_config.devices[0].serial}',
                              f'baud:{twister_harness_config.devices[0].baud}',
                              f'timeout:{twister_harness_config.devices[0].base_timeout}'],
                    timestampoutputs=True,
                    outputdir='twister-out',
                    report='report.html',
                    log='log.html',
                    xunit='xunit.xml',
                    stdout=logFile)
    assert ret == 0, 'Robot test failed'
