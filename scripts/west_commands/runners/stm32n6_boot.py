# Copyright (c) 2026 inovex GmbH
# SPDX-License-Identifier: Apache-2.0

"""Runner for STM32N6 based boards that asserts/de-asserts the external flash
program pin via a UART-controlled helper board before and after flashing.

The STM32N6's external flash is multiplexed: it can be accessed either by the
STM32CubeProgrammer (via STLink) or by the N6 SoC itself.  A hardware "boot
pin" selects which side gets access.  This runner wraps stm32cubeprogrammer and
toggles that pin through a second board that listens for short ASCII commands
on a serial port.

The boot pin is latched at reset, so the runner power-cycles the target (via
boards/st/common/scripts/board_power_reset.sh) after every pin change.  The
full flash sequence is:

  1. assert the boot pin
  2. power-cycle the board
  3. flash with stm32cubeprogrammer
  4. de-assert the boot pin
  5. power-cycle the board again

Usage:
  west flash -r stm32n6_boot -- --boot-device=/dev/ttyACM1

Or, set it once in your west config:
  west config flash.args "--boot-device=/dev/ttyACM1"
"""

import argparse
from pathlib import Path

from runners.core import RunnerConfig
from runners.stm32cubeprogrammer import STM32CubeProgrammerBinaryRunner

try:
    import serial

    _SERIAL_MISSING = False
except ImportError:
    _SERIAL_MISSING = True


class STM32N6BootBinaryRunner(STM32CubeProgrammerBinaryRunner):
    """Thin wrapper around stm32cubeprogrammer that toggles the N6 boot pin."""

    def __init__(
        self,
        cfg: RunnerConfig,
        # stm32cubeprogrammer args (forwarded to parent)
        port: str,
        dev_id: str | None,
        frequency: int | None,
        reset_mode: str | None,
        download_address: int | None,
        download_modifiers: list[str],
        start_address: int | None,
        start_modifiers: list[str],
        conn_modifiers: str | None,
        cli: Path | None,
        use_elf: bool,
        erase: bool,
        reset_system: bool,
        extload: str | None,
        tool_opt: list[str],
        # boot pin controller args
        boot_device: str | None,
        boot_baud: int,
        boot_assert_cmd: str,
        boot_deassert_cmd: str,
        boot_response_timeout: float,
        # board power reset args
        power_reset_script: str | None,
    ) -> None:
        super().__init__(
            cfg,
            port=port,
            dev_id=dev_id,
            frequency=frequency,
            reset_mode=reset_mode,
            download_address=download_address,
            download_modifiers=download_modifiers,
            start_address=start_address,
            start_modifiers=start_modifiers,
            conn_modifiers=conn_modifiers,
            cli=cli,
            use_elf=use_elf,
            erase=erase,
            reset_system=reset_system,
            extload=extload,
            tool_opt=tool_opt,
        )
        self._boot_device = boot_device
        self._boot_baud = boot_baud
        self._boot_assert_cmd = boot_assert_cmd
        self._boot_deassert_cmd = boot_deassert_cmd
        self._boot_response_timeout = boot_response_timeout
        self._power_reset_script = power_reset_script

    @classmethod
    def name(cls) -> str:
        return "stm32n6_boot"

    @classmethod
    def do_add_parser(cls, parser: argparse.ArgumentParser) -> None:
        super().do_add_parser(parser)
        parser.add_argument(
            "--boot-device",
            type=str,
            required=False,
            default=None,
            help=(
                "Serial device of the boot pin controller board "
                "(e.g. /dev/ttyACM1). "
                "Can also be set via the N6_BOOT_CTRL_DEVICE environment variable."
            ),
        )
        parser.add_argument(
            "--boot-baud",
            type=int,
            default=115200,
            help="Baud rate for the boot pin controller (default: 115200)",
        )
        parser.add_argument(
            "--boot-assert-cmd",
            type=str,
            default="assert\n",
            help=("Command string sent to assert the boot pin (default: 'assert\\n')"),
        )
        parser.add_argument(
            "--boot-deassert-cmd",
            type=str,
            default="deassert\n",
            help=("Command string sent to de-assert the boot pin (default: 'deassert\\n')"),
        )
        parser.add_argument(
            "--boot-response-timeout",
            type=float,
            default=5.0,
            metavar="SECONDS",
            help=("Seconds to wait for a response from the boot pin controller (default: 5.0)"),
        )
        parser.add_argument(
            "--power-reset-script",
            type=str,
            default=None,
            metavar="PATH",
            help=(
                "Path to the board power reset script that is run after the "
                "boot pin is toggled. Defaults to "
                "$ZEPHYR_BASE/boards/st/common/scripts/board_power_reset.sh."
            ),
        )

    @classmethod
    def do_create(cls, cfg: RunnerConfig, args: argparse.Namespace) -> "STM32N6BootBinaryRunner":
        import os

        boot_device = args.boot_device or os.environ.get("N6_BOOT_CTRL_DEVICE")

        power_reset_script = args.power_reset_script
        if power_reset_script is None:
            zephyr_base = os.environ.get("ZEPHYR_BASE")
            if zephyr_base:
                power_reset_script = str(
                    Path(zephyr_base)
                    / "boards"
                    / "st"
                    / "common"
                    / "scripts"
                    / "board_power_reset.sh"
                )

        return cls(
            cfg,
            port=args.port,
            dev_id=args.dev_id,
            frequency=args.frequency,
            reset_mode=args.reset_type,
            download_address=args.download_address,
            download_modifiers=args.download_modifiers,
            start_address=args.start_address,
            start_modifiers=args.start_modifiers,
            conn_modifiers=args.conn_modifiers,
            cli=args.cli,
            use_elf=args.use_elf,
            erase=args.erase,
            reset_system=args.reset,
            extload=args.extload,
            tool_opt=args.tool_opt,
            boot_device=boot_device,
            boot_baud=args.boot_baud,
            boot_assert_cmd=args.boot_assert_cmd,
            boot_deassert_cmd=args.boot_deassert_cmd,
            boot_response_timeout=args.boot_response_timeout,
            power_reset_script=power_reset_script,
        )

    def _send_boot_pin_cmd(self, cmd: str) -> None:
        """Send cmd to the boot pin controller over UART and log any response."""
        if _SERIAL_MISSING:
            raise RuntimeError(
                "pyserial is required for the stm32n6_boot runner; "
                "install it with: pip install pyserial"
            )
        self.logger.info(
            "boot pin ctrl: %r -> %s (baud %d)",
            cmd.strip(),
            self._boot_device,
            self._boot_baud,
        )
        with serial.Serial(
            self._boot_device,
            baudrate=self._boot_baud,
            timeout=self._boot_response_timeout,
        ) as ser:
            ser.write(cmd.encode())
            ser.flush()
            response = ser.readline().decode(errors="replace").strip()
            if response:
                self.logger.debug("boot pin ctrl response: %r", response)

    def _power_reset(self) -> None:
        """Power-cycle the target board via the board power reset script."""
        if not self._power_reset_script:
            raise RuntimeError(
                "stm32n6_boot runner: power reset script could not be located.\n"
                "Set ZEPHYR_BASE, or pass the path explicitly:\n"
                "  west flash -- --power-reset-script=/path/to/board_power_reset.sh"
            )
        if not Path(self._power_reset_script).is_file():
            raise RuntimeError(
                f"stm32n6_boot runner: power reset script not found at {self._power_reset_script}"
            )
        self.logger.info("board power reset: %s", self._power_reset_script)
        self.check_call(["bash", self._power_reset_script])

    def flash(self, **kwargs) -> None:
        if not self._boot_device:
            raise RuntimeError(
                "stm32n6_boot runner: --boot-device is required.\n"
                "Pass it on the command line:\n"
                "  west flash -- --boot-device=/dev/ttyACM1\n"
                "Or set the N6_BOOT_CTRL_DEVICE environment variable."
            )
        # Assert the boot pin and power-cycle so the SoC comes up with the
        # BOOT1 pin asserted
        self._send_boot_pin_cmd(self._boot_assert_cmd)
        self._power_reset()
        try:
            super().flash(**kwargs)
        finally:
            # De-assert the boot pin and power-cycle again so the board boots
            # the freshly programmed image
            self._send_boot_pin_cmd(self._boot_deassert_cmd)
            self._power_reset()
