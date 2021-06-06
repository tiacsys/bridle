# Li-Pro.Net bridle to embedded environment

**NOT FOR PRODUCT DEVELOPMENT**

This repository presents an simple playground to evaluate Zephyr
and all they dependencies.

**Pinned on Zephyr v2.5.0**

---

## Documentation

**WARNING: THIS WILL TAKE MORE THAN 15 MINUTES TO EXECUTE**

For our Zephyr playground here in this section we will work inside the working
directory ``workspace``. **You have to had run already through section
[Setup Zephyr Build Environment](#setup-zephyr-build-environment)
at leaset once!**

Setup Zephyr source code environment, type in:

```bash
source zephyr/zephyr-env.sh
```

Patch Zephyr source code with specific 'no kconfig' hack, because we use
a shared Kconfig documentation set instead, type in:

```bash
git -C zephyr apply \
    ../bridle/scripts/patches/zephyr/0001-doc-Share-Kconfig-documentation-between-repos.patch
git -C zephyr apply \
    ../bridle/scripts/patches/zephyr/0002-doc-script-found-devicetree-bindings-recursively.patch
```

**Share Kconfig documentation between repos:**

The Kconfig reference is being turned into a separate shared documentation
set, which needs three lpn-bridle-specific Zephyr tweaks:

1. Do not build the Kconfig docs as part of the Zephyr documentation.
2. Do not link the index page of the Kconfig docs in the Zephyr documentation.
3. Pass some extra variables with output paths through to sphinx-build, so that
   they can be referenced in lpn-bridle/doc/zephyr/conf.py. They're used for
   the Intersphinx linking.

Prepare the build folder, type in:

```bash
rm -rf build/lpn-bridle-doc
west build --cmake-only -b none -d build/lpn-bridle-doc bridle/doc
```

Build the complete Li-Pro.Net bridle HTML pages in
``build/lpn-bridle-doc/html``, type in:

```bash
west build -t build-all -b none -d build/lpn-bridle-doc
```

This command will build all documentation sets. Note that this process can
take quite some time. Alternatively, if you want to build each documentation
set separately, complete the following steps:

1. Build Kconfig Reference HTML pages in
   ``build/lpn-bridle-doc/html/kconfig``, type in:

   ```bash
   west build -t kconfig-html -b none -d build/lpn-bridle-doc
   ```

2. Build Devicetree Bindings HTML pages in
   ``build/lpn-bridle-doc/html/devicetree``, type in:

   ```bash
   west build -t devicetree-html -b none -d build/lpn-bridle-doc
   ```

3. Build Zephyr Project HTML pages in
   ``build/lpn-bridle-doc/html/zephyr``, type in:

   ```bash
   west build -t zephyr -b none -d build/lpn-bridle-doc
   ```

4. Build Li-Pro.Net bridle HTML pages in
   ``build/lpn-bridle-doc/html/lpnb``, type in:

   ```bash
   west build -t lpnb -b none -d build/lpn-bridle-doc
   ```

Now you are able to open ``build/lpn-bridle-doc/html/index.html``
in any HTML browser, ex. type in:

```bash
firefox build/lpn-bridle-doc/html/index.html &
```

---

## Samples for Zephyr

For our Zephyr playground here in this section we will work inside the working
directory ``workspace``. **You have to had run already through section
[Setup Zephyr Build Environment](#setup-zephyr-build-environment)
at leaset once!**

### How to play with sample ``helloshell``

#### Play with the Zephyr embedded shell

When you have started the firmware in any runtime environment as shown below
in the next few sections you are able to play with the command line of the
Zephyer embedded shell.

After a firmware reset you will see on the console:

1. the boot banner of Zephyr
2. the short greeting message of our own example
3. the command prompt of the shell

```text
*** Booting Zephyr OS version 2.5.0  ***
Hello World! I'm THE SHELL from nucleo_f746zg


uart:~$ _
```

From now on you can enter commands. Here are some basic core commands:

```bash
uart:~$ hwinfo devid
Length: 12
ID: 0x333436353438510b00300042
```

```bash
uart:~$ kernel version
Zephyr version 2.5.0
```

```bash
uart:~$ kernel uptime
Uptime: 23703 ms
```

```bash
uart:~$ kernel stacks
0x20010568 shell_uart (real size 2048): unused 1288     usage 760 / 2048 (37 %)
0x200104b0 logging    (real size 768):  unused 664      usage 104 / 768 (13 %)
0x20010620 idle 00    (real size 320):  unused 248      usage 72 / 320 (22 %)
0x20012e80 IRQ 00     (real size 2048): unused 1520     usage 528 / 2048 (25 %)
```

```bash
uart:~$ kernel threads
Scheduler: 879 since last call
Threads:
*0x20010568 shell_uart
        options: 0x0, priority: 14 timeout: 536937956
        state: queued
        stack size 2048, unused 1104, usage 944 / 2048 (46 %)

 0x200104b0 logging
        options: 0x0, priority: 14 timeout: 536937772
        state: pending
        stack size 768, unused 664, usage 104 / 768 (13 %)

 0x20010620 idle 00
        options: 0x1, priority: 15 timeout: 536938140
        state:
        stack size 320, unused 248, usage 72 / 320 (22 %)
```

```bash
uart:~$ device list
devices:
- STM32_CLK_RCC
- stm32-exti
- UART_6
- UART_3
- sys_clock
- ADC_1
- GPIOK
- GPIOJ
- GPIOI
- GPIOH
- GPIOG
- GPIOF
- GPIOE
- GPIOD
- GPIOC
- GPIOB
- GPIOA
- FLASH_CTRL
- I2C_1
- PWM_1
```

```bash
uart:~$ log status
module_name                              | current | built-in
----------------------------------------------------------
adc_shell                                | inf     | inf
adc_stm32                                | inf     | inf
flash_stm32                              | inf     | inf
gpio_shell                               | inf     | inf
i2c                                      | inf     | inf
i2c_ll_stm32                             | inf     | inf
i2c_ll_stm32_v2                          | inf     | inf
i2c_shell                                | inf     | inf
log                                      | inf     | inf
mpu                                      | inf     | inf
os                                       | inf     | inf
pwm_stm32                                | inf     | inf
shell.shell_uart                         | inf     | inf
shell_uart                               | inf     | inf
uart_stm32                               | inf     | inf
```

Next you can try out our own ``hello`` command:

```bash
uart:~$ hello
Hello from shell.
```

Only on a real hardware, for example the ST Nucleo F746ZG board, you are
able to play with some basic I/O components. So you can setup the GPIO line
connected to a green LED on the ST Nucleo F746ZG as an output and toggle
the output level to high (1), LED on, or low (0), LED off:

```bash
uart:~$ gpio conf GPIOB 0 out
Configuring GPIOB pin 0
uart:~$ gpio set GPIOB 0 1
Writing to GPIOB pin 0
uart:~$ gpio set GPIOB 0 0
Writing to GPIOB pin 0
```

Simple read access to the internal program memory (Flash):

```bash
uart:~$ flash read FLASH_CTRL 10a40 10
00010A40: 5a 65 70 68 79 72 20 4f  53 20 76 65 72 73 69 6f |Zephyr O S versio|
```

Scan default I2C bus:

```bash
uart:~$ i2c scan I2C_1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:             -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
0 devices found on I2C_1
```

#### Running as Posix native firmware on host

Config, build, and execute, type in:

```bash
rm -rf build/helloshell-native_posix
west build -d build/helloshell-native_posix \
           -b native_posix --cmake-only \
     bridle/samples/helloshell
west build -d build/helloshell-native_posix -t all
./build/helloshell-native_posix/zephyr/zephyr.exe -attach_uart
```

#### Running as ix86 32-bit firmware in Qemu emulation

Config, build, and execute, type in:

```bash
rm -rf build/helloshell-qemu_x86
west build -d build/helloshell-qemu_x86 \
           -b qemu_x86 --cmake-only \
     bridle/samples/helloshell
west build -d build/helloshell-qemu_x86 -t all
west build -d build/helloshell-qemu_x86 -t run
```

The application stucks inside the emulator in an endless loop (the Zephyr idle
task) and can only terminated by press ``Ctrl-a`` following by ``x``.

#### Running as ARM Cortex-M3 32-bit firmware in Qemu emulation

Config, build, and execute, type in:

```bash
rm -rf build/helloshell-qemu_cortex_m3
west build -d build/helloshell-qemu_cortex_m3 \
           -b qemu_cortex_m3 --cmake-only \
     bridle/samples/helloshell
west build -d build/helloshell-qemu_cortex_m3 -t all
west build -d build/helloshell-qemu_cortex_m3 -t run
```

The application stucks inside the emulator in an endless loop (the Zephyr idle
task) and can only terminated by press ``Ctrl-a`` following by ``x``.

#### Running as ARM Cortex-M7 32-bit firmware on ST Nucleo F746ZG board

Config, build, and execute, type in:

```bash
rm -rf build/helloshell-nucleo_f746zg
west build -d build/helloshell-nucleo_f746zg \
           -b nucleo_f746zg --cmake-only \
     bridle/samples/helloshell
west build -d build/helloshell-nucleo_f746zg -t all
west flash -d build/helloshell-nucleo_f746zg
```

The terminal emulator will stuck on the serial device and can only terminated
by press ``Ctrl-a`` following by ``\`` and awnser with ``y``.

---

## Zephyr, say hello

For our Zephyr playground here in this section we will work inside the working
directory ``workspace``. **You have to had run already through section
[Setup Zephyr Build Environment](#setup-zephyr-build-environment)
at leaset once!**

### The Posix native application

Configure, build and run the simple hello world example with the help of
``west``, type in:

```bash
rm -rf build/hello_world-native_posix
west build -d build/hello_world-native_posix \
           -b native_posix --cmake-only \
     zephyr/samples/hello_world
west build -d build/hello_world-native_posix -t all
west build -d build/hello_world-native_posix -t run
```

That results in:

```text
*** Booting Zephyr OS version 2.5.0  ***
Hello World! native_posix
```

The application stucks in an endless loop (the Zephyr idle task) and can
only terminated by press ``Ctrl-c``.

### The Qemu emulated firmware

Configure, build and run the simple hello world example with the help of
``west``, type in:

#### The ix86 32-bit firmware

Type in:

```bash
rm -rf build/hello_world-qemu_x86
west build -d build/hello_world-qemu_x86 \
           -b qemu_x86 --cmake-only \
     zephyr/samples/hello_world
west build -d build/hello_world-qemu_x86 -t all
west build -d build/hello_world-qemu_x86 -t run
```

That results in:

```text
SeaBIOS (version zephyr-v1.0.0-0-g31d4e0e-dirty-20200714_234759-fv-az50-zephyr)
Booting from ROM..*** Booting Zephyr OS version 2.5.0  ***
Hello World! qemu_x86
```

The application stucks inside the emulator in an endless loop (the Zephyr idle
task) and can only terminated by press ``Ctrl-a`` following by ``x``.

#### The ARM Cortex-M3 32-bit firmware

Type in:

```bash
rm -rf build/hello_world-qemu_cortex_m3
west build -d build/hello_world-qemu_cortex_m3 \
           -b qemu_cortex_m3 --cmake-only \
     zephyr/samples/hello_world
west build -d build/hello_world-qemu_cortex_m3 -t all
west build -d build/hello_world-qemu_cortex_m3 -t run
```

That results in:

```text
*** Booting Zephyr OS version 2.5.0  ***
Hello World! qemu_cortex_m3
```

The application stucks inside the emulator in an endless loop (the Zephyr idle
task) and can only terminated by press ``Ctrl-a`` following by ``x``.

### The ARM Cortex-M7 32-bit native firmware

Configure, build and run the simple hello world example with the help of
``west``, type in:

#### The STM32F746 firmware on ST Nucleo F746ZG board

First of all, connect your ST Nucleo F746ZG board with your development
workstation via the on-board ST/Link-V2 USB connector and open the serial
line with your favorite terminal emulator. In our case we want to use the
simple ``screen`` application to open our specific serial device
``usb-STMicroelectronics_STM32_STLink_066AFF343039564157223930-if02``
with *8N1@115200Bd*, type in:

```bash
screen /dev/serial/by-id/usb-STMicroelectronics_STM32_STLink_066AFF343039564157223930-if02 \
       115200,cs8,parenb,-parodd,-cstopb
```

The terminal emulator will stuck on the serial device and can only terminated
by press ``Ctrl-a`` following by ``\`` and awnser with ``y``.

Optional clean (remove) the build directory:

```bash
rm -rf build/hello_world-nucleo_f746zg
```

Now start to config, type in:

```bash
west build -d build/hello_world-nucleo_f746zg \
           -b nucleo_f746zg --cmake-only \
     zephyr/samples/hello_world
```

The original Zephyr configuration for the ST Nucleo F746ZG board expect an
already assembled 8 MHz crystel connected to the STM32 HSE clock source. When
your board comes without this crystel you must change the clock tree
configuration by execute the ``menuconfig`` at this step, type in:

```bash
west build -d build/hello_world-nucleo_f746zg -t menuconfig
```

Got to *(Top) → Device Drivers → Hardware clock controller support
→ STM32 Reset & Clock Control* and change the configuration as shown below:

```text
(1) Clock Control Device Priority
    STM32 System Clock Source (PLL)  --->
    STM32 PLL Clock Source (HSI)  --->
(16) Division factor for PLL VCO input clock
(336) Multiplier factor for PLL VCO output clock
(4) PLL division factor for main system clock
(7) Division factor for OTG FS, SDIO and RNG clocks
(1) AHB prescaler
(2) APB1 prescaler
(1) APB2 prescaler
    STM32 MCO1 Clock Source (NOCLOCK)  --->
    STM32 MCO2 Clock Source (NOCLOCK)  --->
```

Finish the menu configuration by press ``q`` following by ``y``. Now you can
build and flash the firmware, type in:

```bash
west build -d build/hello_world-nucleo_f746zg -t all
west flash -d build/hello_world-nucleo_f746zg
```

That results in (in the terminal emulator):

```text
*** Booting Zephyr OS version 2.5.0  ***
Hello World! nucleo_f746zg
```

The application stucks inside the terminal emulator in an endless loop
(the Zephyr idle task) and can not terminated, but you are able to close
the terminal emulator.

---

## Setup Zephyr Build Environment

For the Zephyr build environment here in this description we will work inside
the new and complete empty directory ``workspace``.

To do so type in:

```bash
rm -rf workspace && mkdir workspace && cd workspace
```

**Now you have to run through section
[Setup Python Virtual Environment](#setup-python-virtual-environment) at least
once inside this folder!** At least run through the following setup steps:

1. [create and activate](#create_activate_and-update)
   your Python virtual environment
2. [install west](#install-the-zephyr-rtos-meta-tool)
   in your Python virtual environment

After this we will stay inside our working directory ``workspace``, have the
``.env`` folder in there and see the following similar shell prompt:

```bash
(workspace[Python 3.8.5]) user@host:workspace$ _
```

Now we ar able to initialize the Zephyr build environment with ``west`` as
specified by our own manifest description in ``west.yml``:

```bash
west init --manifest-url=git@github.com:tiacsys/bridle.git \
          --manifest-rev=main --manifest-file=west.yml && \
west update
```

After this we will stay inside our working directory ``workspace``, have the
``.west`` folder in there and see the following similar shell prompt:

```bash
(workspace[Python 3.8.5]) user@host:workspace$ _
```

As well we will found the Zephyr core source code in the ``zephyr`` folder
and the Li-Pro.Net bridle source code in the ``bridle`` folder. To complete
the setup, we need to extend our Python virtual environment with all the
packages that are required by Zephyr and Li-Pro.Net bridle itself, type in:

```bash
pip install --upgrade --requirement zephyr/scripts/requirements.txt
pip install --upgrade --requirement bridle/scripts/requirements.txt
```

## Setup Python Virtual Environment

**You have to had run already through section
[Setup Development Environment](#setup-development-environment)
at least once!**

### Create, Activate, and Update

Create a new and complet empty workspace directory, change into this new
folder and execute:

```bash
python3 -m venv --copies --prompt="$(basename $(pwd))[$(python3 --version)]" .env
source .env/bin/activate
pip install --upgrade pip
pip install --upgrade setuptools
```

### Install the Zephyr RTOS meta tool

| Release:    | 0.9.0 (from [PyPi.org][pypi-west])           |
| :---------- | :------------------------------------------- |
| References: | [West (Zephyr’s meta-tool)][doc-zephyr-west] |

[doc-zephyr-west]: https://docs.zephyrproject.org/2.5.0/guides/west/index.html#west-zephyr-s-meta-tool

After you have [create and activate](#create-activate-and-update) your
Python virtual environment type in:

```bash
pip install --upgrade west
which west && ($(which west) --version | head -1)
```

That results in:

```text
<YOUR_WORSPACE_FOLDER>/.env/bin/west
West version: v0.9.0
```

### Deactivate and Remove

Whenever you like to exit your Python virtual environment type in:

```bash
deactivate
```

After this you are able to remove the complete virtual environment folder:

```bash
rm -rf .env
```

Whenever you will need the Python virtual environment again,
[create and activate](#create-activate-and-update) another (new) one.

## Setup Development Environment

| OS Release: | Ubuntu 18.04 LTS (Bionic Beaver) and later |
| ----------: | :----------------------------------------- |
| References: | [Getting Started Guide][doc-zephyr-gsg]    |

[doc-zephyr-gsg]: https://docs.zephyrproject.org/2.5.0/getting_started/index.html#getting-started-guide

You have to start on a latest Ubuntu LTS that comes with a stable Python 3
release. All works were doing on Ubuntu 20.04 LTS that comes with Python 3.8.

The minimal tool requirements for the latest Zephyr release **v2.5.0** are:

| Artifacts               | minimal reuired         | provided by this guide  |
| ----------------------: | :---------------------- | :---------------------- |
| [Python][ubuntu-python] | [3.6][python-minimal]   | [3.6.9][python-install] |
| [West][pypi-west]       | [0.7.1][west-minimal]   | depends on virtual env. |
| [CMake][ubuntu-cmake]   | [3.13.1][cmake-minimal] | [3.15.5][cmake-install] |
| [DTC][ubuntu-dtc]       | [1.4.6][dtc-minimal]    | [1.5.1][dtc-install]    |
| [Zephyr SDK][zephyr-dl] | [0.11.1][zsdk-minimal]  | [0.12.3][zsdk-install]  |

[ubuntu-python]: https://packages.ubuntu.com/source/focal/python3-defaults "Interactive high-level object-oriented language (version 3.8)"
[python-minimal]: https://github.com/zephyrproject-rtos/zephyr/blob/zephyr-v2.5.0/cmake/python.cmake#L12
[python-install]: #python-3

[pypi-west]: https://pypi.org/project/west "This is the Zephyr RTOS meta tool, west."
[west-minimal]: https://github.com/zephyrproject-rtos/zephyr/blob/zephyr-v2.5.0/cmake/west.cmake#L61

[ubuntu-cmake]: https://packages.ubuntu.com/source/focal/cmake "cross-platform, open-source make system"
[cmake-minimal]: https://github.com/zephyrproject-rtos/zephyr/blob/zephyr-v2.5.0/cmake/app/boilerplate.cmake#L29
[cmake-install]: #cmake-3

[ubuntu-dtc]: https://packages.ubuntu.com/source/focal/device-tree-compiler "Device Tree Compiler for Flat Device Trees"
[dtc-minimal]: https://github.com/zephyrproject-rtos/zephyr/blob/zephyr-v2.5.0/cmake/host-tools.cmake#L13
[dtc-install]: #device-tree-compiler

[zephyr-dl]: https://github.com/zephyrproject-rtos/sdk-ng/releases "Zephyr Downloads page"
[zsdk-minimal]: https://github.com/zephyrproject-rtos/zephyr/blob/zephyr-v2.5.0/cmake/toolchain/zephyr/host-tools.cmake#L4
[zsdk-install]: #zephyr-software-development-kit

Run through the installation steps as listed below at least once:

1. [Python 3](#python-3)
2. [CMake 3](#cmake-3)
3. [Device Tree Compiler](#device-tree-compiler)
4. [Linux Host Dependencies](#linux-host-dependencies)
5. [Zephyr Software Development Kit](#zephyr-software-development-kit)

### Python 3

| Release:    | 3.8.5 (from Ubuntu 20.04 LTS)    |
| ----------: | :------------------------------- |
| References: | [Python and pip][doc-zephyr-pip] |

[doc-zephyr-pip]: https://docs.zephyrproject.org/2.5.0/getting_started/index.html#install-dependencies

**You will need root access by the command line tool ``sudo``.**

Become root and install neccessery system packages to be prepered to setup
a proper Python 3.8 (virtual) development environment on demand:

```bash
sudo -i apt-get update
sudo -i apt-get upgrade
sudo -i apt-get install python3 python3-dev python3-venv
sudo -i apt-get install python3-pip python3-setuptools
sudo -i apt-get install python3-tk python3-wheel
apt-cache policy python3.8
```

That results in:

```text
python3.8:
  Installed: 3.8.5-1~20.04.2
  Candidate: 3.8.5-1~20.04.2
  Version table:
 *** 3.8.5-1~20.04.2 500
        500 http://de.archive.ubuntu.com/ubuntu focal-updates/main amd64 Packages
        500 http://security.ubuntu.com/ubuntu focal-security/main amd64 Packages
        100 /var/lib/dpkg/status
     3.8.2-1ubuntu1 500
        500 http://de.archive.ubuntu.com/ubuntu focal/main amd64 Packages
```

#### Zephyr RTOS meta tool

The Zephyr RTOS meta tool ``west`` will be installed on demand inside your
private Python virtual environment. There is no special system installation
needed.

### CMake 3

| Release:    | 3.19.5 (from [Kitware][kitware-apt-repo])               |
| ----------: | :------------------------------------------------------ |
| References: | [Install Requirements and Dependencies][doc-zephyr-ird] |

[kitware-apt-repo]: https://apt.kitware.com/ "Kitware APT Repository"
[doc-zephyr-ird]: https://docs.zephyrproject.org/2.5.0/getting_started/index.html#install-dependencies

The system package of CMake in Ubuntu 18.04 is too old as fullfill the minimal
Zephyr requirements. To fix this issue, we have to use the APT package
repository as provided by the company behind CMake ([Kitware][kitware-apt-repo])
that will provide the latest and stable release. **You will need root access by
the command line tool ``sudo``.**

Become root, setup the Kitware APT package repository and install CMake
in a proper version for Zephyr:

``` bash
wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | sudo -i apt-key add -
sudo -i apt-add-repository 'deb https://apt.kitware.com/ubuntu/ focal main'
sudo -i apt-get update
sudo -i apt-get install kitware-archive-keyring
sudo -i apt-get install cmake
apt-cache policy cmake
```

That results in:

```text
cmake:
  Installed: 3.19.5-0kitware1ubuntu20.04.1
  Candidate: 3.19.5-0kitware1ubuntu20.04.1
  Version table:
 *** 3.19.5-0kitware1ubuntu20.04.1 500
        500 https://apt.kitware.com/ubuntu focal/main amd64 Packages
        100 /var/lib/dpkg/status
     3.19.4-0kitware1ubuntu20.04.1 500
        500 https://apt.kitware.com/ubuntu focal/main amd64 Packages
     3.19.3-0kitware1ubuntu20.04.1 500
        500 https://apt.kitware.com/ubuntu focal/main amd64 Packages
     3.19.2-0kitware1ubuntu20.04.1 500
        500 https://apt.kitware.com/ubuntu focal/main amd64 Packages
     3.19.1-0kitware1ubuntu20.04.1 500
        500 https://apt.kitware.com/ubuntu focal/main amd64 Packages
     3.19.0-0kitware1ubuntu20.04.1 500
        500 https://apt.kitware.com/ubuntu focal/main amd64 Packages
     3.18.4-0kitware1ubuntu20.04.1 500
        500 https://apt.kitware.com/ubuntu focal/main amd64 Packages
     3.18.3-0kitware1ubuntu20.04.1 500
        500 https://apt.kitware.com/ubuntu focal/main amd64 Packages
     3.18.2-0kitware1ubuntu20.04.1 500
        500 https://apt.kitware.com/ubuntu focal/main amd64 Packages
     3.18.1-0kitware1ubuntu20.04.1 500
        500 https://apt.kitware.com/ubuntu focal/main amd64 Packages
     3.18.0-0kitware1ubuntu20.04.1 500
        500 https://apt.kitware.com/ubuntu focal/main amd64 Packages
     3.17.3-0kitware1ubuntu20.04.1 500
        500 https://apt.kitware.com/ubuntu focal/main amd64 Packages
     3.17.2-0kitware1ubuntu20.04.1 500
        500 https://apt.kitware.com/ubuntu focal/main amd64 Packages
     3.16.3-1ubuntu1 500
        500 http://de.archive.ubuntu.com/ubuntu focal/main amd64 Packages
```

### Device Tree Compiler

| Release:    | 1.5.1 (from Ubuntu 20.04 LTS)        |
| ----------: | :----------------------------------- |
| References: | [Devicetree and dtc][doc-zephyr-dt]  |

[doc-zephyr-dt]: https://docs.zephyrproject.org/2.5.0/getting_started/index.html#install-dependencies

**You will need root access by the command line tool ``sudo``.**

Become root and install the Device Tree Compiler 1.5.1 for Zephyr:

```bash
sudo -i apt-get update
sudo -i apt-get upgrade
sudo -i apt-get install device-tree-compiler
apt-cache policy device-tree-compiler
```

That results in:

```text
device-tree-compiler:
  Installed: 1.5.1-1
  Candidate: 1.5.1-1
  Version table:
 *** 1.5.1-1 500
        500 http://de.archive.ubuntu.com/ubuntu focal/main amd64 Packages
        100 /var/lib/dpkg/status
```

### Linux Host Dependencies

When you have already done the installation steps for [Python 3](#python-3),
[CMake 3](#cmake-3), and the [Device Tree Compiler](#device-tree-compiler),
then you have to finish the installation of all required host tools with the
following commands. **You will need root access by the command line tool
``sudo``.**

Become root, update and upgarde the system from all APT package repositories you
have currently enabled and install all (not yet) installed host tool packages:

```bash
sudo -i apt-get update
sudo -i apt-get upgrade
sudo -i apt-get install --no-install-recommends \
  git wget cmake make ninja-build gperf \
  gcc gcc-multilib g++-multilib libsdl2-dev \
  ccache dfu-util device-tree-compiler \
  python3-dev python3-pip python3-setuptools python3-tk python3-wheel \
  xz-utils file screen doxygen mscgen
```

#### Prepare OpenOCD invocation

You will notice that Zephyr invokes open On Chip Debugger (openOCD) to flash
many boards. If you run into some issues with flashing, it porbably due to
permission issues. Add the following udev rules to fix them.

```bash
sudo -i wget -O /etc/udev/rules.d/60-openocd.rules \
        https://github.com/zephyrproject-rtos/openocd/raw/zephyr-20200722/contrib/60-openocd.rules
sudo -i udevadm control --reload-rules
sudo -i udevadm trigger
```

### Zephyr Software Development Kit

| SDK Release: | Zephyr SDK 0.12.3 – Feb 16, 2021 (about 1.06 GB)                    |
| -----------: | :------------------------------------------------------------------ |
| References:  | [Install the Zephyr Software Development Kit (SDK)][doc-zephyr-sdk] |

[doc-zephyr-sdk]: https://docs.zephyrproject.org/2.5.0/getting_started/index.html#install-a-toolchain

Opposite to the original documentation, the SDK will be installed globally
under the folder ``/opt``. **You will need root access by the command line
tool ``sudo``.**

Download the self-extracting Zephyr SDK installer, make it executable
and check the content:

```bash
wget -O /tmp/zephyr-sdk-0.12.3-x86_64-linux-setup.run \
        https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.12.3/zephyr-sdk-0.12.3-x86_64-linux-setup.run
chmod +x /tmp/zephyr-sdk-0.12.3-x86_64-linux-setup.run
/tmp/zephyr-sdk-0.12.3-x86_64-linux-setup.run --check
```

That results in:

```text
Verifying archive integrity...  100%   MD5 checksums are OK. All good.
```

Become root and execute the installation with direction to the installation folder:

```bash
sudo -i /tmp/zephyr-sdk-0.12.3-x86_64-linux-setup.run --nox11 -- -y -d /opt/zephyr-sdk-0.12.3
```

That results in:

```text
Verifying archive integrity...  100%   All good.
Uncompressing SDK for Zephyr  100%
Installing SDK to /opt/zephyr-sdk-0.12.3
Creating directory /opt/zephyr-sdk-0.12.3
Success
 [*] Installing arm tools...
 [*] Installing arm64 tools...
 [*] Installing arc tools...
 [*] Installing nios2 tools...
 [*] Installing riscv64 tools...
 [*] Installing sparc tools...
 [*] Installing mips tools...
 [*] Installing x86_64 tools...
 [*] Installing xtensa_sample_controller tools...
 [*] Installing xtensa_intel_apl_adsp tools...
 [*] Installing xtensa_intel_s1000 tools...
 [*] Installing xtensa_intel_bdw_adsp tools...
 [*] Installing xtensa_intel_byt_adsp tools...
 [*] Installing xtensa_nxp_imx_adsp tools...
 [*] Installing xtensa_nxp_imx8m_adsp tools...
 [*] Installing CMake files...
 [*] Installing additional host tools...
Success installing SDK.
SDK is ready to be used.
```

Check the installed SDK version:

```bash
cat /opt/zephyr-sdk-0.12.3/sdk_version
```

*Should result in:* **0.12.3**
