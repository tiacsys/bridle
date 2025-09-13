.. _helloshell-sample:

Hello Shell
###########

**This is a derived work from the original Zephyr "Hello World" example!**
**Most of the stuff in this README file needs to be redesigned and changed!**

Overview
********

A simple Hello World example that can be used with any supported board and
prints 'Hello World! I'm THE SHELL' to the console. This application can be
built into modes:

* basic command set
* fancy command set, with default enabled :kconfig:option:`CONFIG_BRIDLE_CMD_HELLO`

Requirements
************

.. zephyr-keep-sorted-start re(^\s+\* \|\w)

* One of the following development boards:

  * |bridle:board:seeeduino_cm0|
  * |bridle:board:seeeduino_lotus|
  * |bridle:board:waveshare_rp2040|
  * |zephyr:board:arduino_zero| or Bridle's |bridle:board:arduino_zero|
  * |zephyr:board:mimxrt1010_evk|
  * |zephyr:board:mimxrt1060_evk|
  * |zephyr:board:native_sim|
  * |zephyr:board:nucleo_f303re| (NUCLEO-F303RE)
  * |zephyr:board:nucleo_f401re| (NUCLEO-F401RE)
  * |zephyr:board:nucleo_f413zh| (NUCLEO-F413ZH)
  * |zephyr:board:nucleo_f746zg| (NUCLEO-F746ZG)
  * |zephyr:board:nucleo_f767zi| (NUCLEO-F767ZI)
  * |zephyr:board:qemu_arc|
  * ARM Cortex-A9 Emulation (``qemu_cortex_a9``)
  * |zephyr:board:qemu_cortex_a53|
  * |zephyr:board:qemu_cortex_m0|
  * |zephyr:board:qemu_cortex_m3|
  * |zephyr:board:qemu_cortex_r5|
  * |zephyr:board:qemu_kvm_arm64|
  * |zephyr:board:qemu_leon3|
  * |zephyr:board:qemu_malta|
  * |zephyr:board:qemu_riscv32e|
  * |zephyr:board:qemu_riscv32|
  * |zephyr:board:qemu_riscv64|
  * |zephyr:board:qemu_x86|
  * |zephyr:board:qemu_xtensa|
  * |zephyr:board:rpi_pico|
  * |zephyr:board:seeeduino_xiao| or Bridle's |bridle:board:xiao_samd21|

.. zephyr-keep-sorted-stop

Building and Running
********************

This project outputs 'Hello World! I'm THE SHELL' to the console. It can be
built and executed as emulation in |zephyr:board:qemu_x86| as follows:

.. zephyr-app-commands::
   :app: bridle/samples/helloshell
   :build-dir: helloshell-qemu_x86
   :board: qemu_x86
   :west-args: -p
   :goals: run
   :host-os: unix

.. hint:: Exit QEMU by pressing :kbd:`CTRL+A` :kbd:`x`.

Also it can be built and executed on following targets:

* As |zephyr:board:native_sim|, fancy command set mode:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-native_sim
     :board: native_sim
     :west-args: -p
     :goals: run
     :host-os: unix

  .. hint:: Connect a terminal emulator to the given pseudotty or start the
     application directly with the autoconnect argument:

     .. code-block:: console

        ./build/helloshell-native_sim/zephyr/zephyr.exe -attach_uart

* As emulation in |zephyr:board:qemu_cortex_m3|, fancy command set mode:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-qemu_cortex_m3
     :board: qemu_cortex_m3
     :west-args: -p
     :goals: run
     :host-os: unix

  .. hint:: Exit QEMU by pressing :kbd:`CTRL+A` :kbd:`x`.

* On |zephyr:board:nucleo_f746zg| board, fancy command set mode:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-nucleo_f746zg
     :board: nucleo_f746zg
     :west-args: -p
     :goals: flash
     :host-os: unix

Further you can deside either to run in a basic or fancy command set
mode:

* On |zephyr:board:nucleo_f746zg| board, tiny command set mode for
  an absolutely minimal environment (lowest memory footprint):

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-nucleo_f746zg
     :gen-args: -DEXTRA_CONF_FILE="prj-tiny.conf"
     :board: nucleo_f746zg
     :west-args: -p
     :goals: flash
     :host-os: unix

* On |zephyr:board:nucleo_f746zg| board, minimal command set mode for
  basic system operations:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-nucleo_f746zg
     :gen-args: -DEXTRA_CONF_FILE="prj-minimal.conf"
     :board: nucleo_f746zg
     :west-args: -p
     :goals: flash
     :host-os: unix

* On |zephyr:board:nucleo_f746zg| board, helpful command set mode for
  hardware startups and bug hunting:

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-nucleo_f746zg
     :gen-args: -DEXTRA_CONF_FILE="prj-hwstartup.conf"
     :board: nucleo_f746zg
     :west-args: -p
     :goals: flash
     :host-os: unix

* On |zephyr:board:nucleo_f746zg| board, fancy command set mode
  (implies :file:`prj.conf` merged with board specific configuration):

  .. zephyr-app-commands::
     :app: bridle/samples/helloshell
     :build-dir: helloshell-nucleo_f746zg
     :board: nucleo_f746zg
     :west-args: -p
     :goals: flash
     :host-os: unix

Sample Output
=============

(text in bold is a command input, text in angle brackets are keys to press)

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      Hello World! I'm THE SHELL from nucleo_f746zg


      :bgn:`uart:~$` **<Tab>**
        :bcy:`adc        bridle     clear      dac        device     devmem     eeprom`
        :bcy:`flash      gpio       hello      help       history    hwinfo     i2c`
        :bcy:`kernel     led        log        pwm        regulator  rem        resize`
        :bcy:`retval     rtc        sensor     shell      timer`

      :bgn:`uart:~$` **help**
      Please press the <Tab> button to see all available commands.
      You can also use the <Tab> button to prompt or auto-complete all commands or its subcommands.
      You can try to call commands with <-h> or <--help> parameter for more information.

      Shell supports following meta-keys:
        Ctrl + (a key from: abcdefklnpuw)
        Alt  + (a key from: bf)
      Please refer to shell documentation for more details.

      Available commands:
        adc        : ADC commands
        bridle     : Bridle commands.
        clear      : Clear screen.
        dac        : DAC shell commands
        device     : Device commands
        devmem     : Read/write physical memory
                     Usage:
                     Read memory at address with optional width:
                     devmem address [width]
                     Write memory at address with mandatory width and value:
                     devmem address <width> <value>
        eeprom     : EEPROM shell commands
        flash      : Flash shell commands
        gpio       : GPIO commands
        hello      : say hello
        help       : Prints the help message.
        history    : Command history.
        hwinfo     : HWINFO commands
        i2c        : I2C commands
        kernel     : Kernel commands
        led        : LED commands
        log        : Commands for controlling logger
        pwm        : PWM shell commands
        regulator  : Regulator playground
        rem        : Ignore lines beginning with 'rem '
        resize     : Console gets terminal screen size or assumes default in case the
                     readout fails. It must be executed after each terminal width
                     change to ensure correct text display.
        retval     : Print return value of most recent command
        sensor     : Sensor commands
        shell      : Useful, not Unix-like shell commands.
        timer      : Timer commands

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **hello -h**
      hello - say hello
      :bgn:`uart:~$` **hello**
      Hello from shell.

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **kernel version**
      Zephyr version |zephyr_version_number_em|

      :bgn:`uart:~$` **bridle version**
      Bridle version |shortversion_number_em|

      :bgn:`uart:~$` **bridle version long**
      Bridle version |longversion_number_em|

      :bgn:`uart:~$` **bridle info**
      Zephyr: |zephyr_release_number_em|
      Bridle: |release_number_em|

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **kernel uptime**
      Uptime: 327750 ms

      :bgn:`uart:~$` **kernel cycles**
      cycles: 3586181929 hw cycles

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **kernel thread list**
      Scheduler: 498 since last call
      Threads:
       0x20010e80
              options: 0x0, priority: -16 timeout: 0
              state: pending, entry: 0x800231d
              stack size 2048, unused 1920, usage 128 / 2048 (6 %)

      \*0x20010ae8 shell_uart
              options: 0x0, priority: 14 timeout: 0
              state: queued, entry: 0x8004ba1
              stack size 2048, unused 960, usage 1088 / 2048 (53 %)

       0x20011750 sysworkq
              options: 0x1, priority: -1 timeout: 0
              state: pending, entry: 0x800ec3d
              stack size 1024, unused 848, usage 176 / 1024 (17 %)

       0x200105e8 logging
              options: 0x0, priority: 14 timeout: 0
              state: pending, entry: 0x8002a29
              stack size 768, unused 584, usage 184 / 768 (23 %)

       0x200114f0 idle
              options: 0x1, priority: 15 timeout: 0
              state: , entry: 0x801481d
              stack size 320, unused 256, usage 64 / 320 (20 %)

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`uart:~$` **kernel thread stacks**
      0x20010e80                                  (real size 2048):   unused 1920     usage  128 / 2048 ( 6 %)
      0x20010ae8 shell_uart                       (real size 2048):   unused  960     usage 1088 / 2048 (53 %)
      0x20011750 sysworkq                         (real size 1024):   unused  848     usage  176 / 1024 (17 %)
      0x200105e8 logging                          (real size  768):   unused  584     usage  184 /  768 (23 %)
      0x200114f0 idle                             (real size  320):   unused  256     usage   64 /  320 (20 %)
      0x20015e80 IRQ 00                           (real size 2048):   unused 1816     usage  232 / 2048 (11 %)

TCP/IP Network over Wi-Fi on the RPi Pico W
===========================================

This project provides an extended board-specific configuration for the
|RPi Pico W| with a pre-activated :external+zephyr:ref:`TCP/IP network stack
<network_stack_architecture>` via the Wi-Fi chip made by Infineon. It have to
build at least with the Zephyr upstream :external+zephyr:ref:`snippet-wifi-ip`
and optional with the Bridle :ref:`snippet-usb-console`:

   .. zephyr-app-commands::
      :app: bridle/samples/helloshell
      :build-dir: helloshell-rpi_pico_w
      :board: rpi_pico/rp2040/w
      :snippets: "usb-console wifi-ip"
      :west-args: -p
      :flash-args: -r uf2
      :goals: flash
      :host-os: unix
      :compact:

You should see the following message on the console:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         WLAN MAC Address : 29:F7:28:FC:67:1C
         WLAN Firmware    : wl0: Jun  5 2024 06:33:59 version 7.95.88 (cf1d613 CY) FWID 01-7b7cf51a
         WLAN CLM         : API: 12.2 Data: 9.10.39 Compiler: 1.29.4 ClmImport: 1.36.3 Creation: 2024-04-16 21:20:55
         WHD VERSION      : 3.3.2.25168 : v3.3.2 : GCC 12.2 : 2024-12-06 06:53:17 +0000

         \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
         [00:00:04.113,000] :byl:`<wrn> udc_rpi: BUS RESET`
         [00:00:04.192,000] :byl:`<wrn> udc_rpi: BUS RESET`
         \*\*\* Booting Zephyr OS build v\ |zephyr_version_number_em| \*\*\*
         Hello World! I'm THE SHELL from rpi_pico
         [00:00:07.834,000] <inf> net_config: Initializing network
         [00:00:07.834,000] <inf> net_config: Waiting interface 1 (0x20001940) to be up...
         [00:00:07.834,000] <inf> net_config: Running dhcpv4 client...
         [00:00:07.834,000] <inf> net_config: Running dhcpv6 client...

Simple test execution on target
-------------------------------

(text in bold is a command input)

   .. admonition:: Network connect over Wi-Fi chip with system date before and after
      :class: note dropdown toggle-shown

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **date get**
            1970-01-01 00:00:29 UTC

      :brd:`Replace` the values :command:`<key_management>`, :command:`<SSID>`
      and :command:`<passphrase>` with your own, e.g. :command:`-k 1` for
      :emphasis:`WPA2-PSK`! Use the command :command:`wifi connect` without
      parameters to see online help with more details.

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **wifi connect -s <SSID> -k <key_management> -p <passphrase>**
            Connected
            Connection requested
            [00:04:57.840,000] <inf> net_dhcpv4: Received: 192.168.10.197
            [00:04:57.841,000] <inf> net_config: IPv4 address: 192.168.10.197
            [00:04:57.841,000] <inf> net_config: Lease time: 28800 seconds
            [00:04:57.841,000] <inf> net_config: Subnet: 255.255.255.0
            [00:04:57.842,000] <inf> net_config: Router: 192.168.10.1
            [00:04:59.480,000] :brd:`<err> net_dhcpv6: Failed to configure DHCPv6 address`

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **date get**
            2025-08-31 18:28:26 UTC

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **net iface**
            Default interface: 1


            Interface wlan0 (0x20001940) (WiFi) [1]
            ===============================
            Link addr : 29:F7:28:FC:67:1C
            MTU       : 1500
            Flags     : AUTO_START,IPv4,IPv6
            Device    : airoc-wifi\ @\ 0 (0x1004d1f0)
            Status    : oper=UP, admin=UP, carrier=ON
            Ethernet capabilities supported:
                    MAC address filtering
            Ethernet PHY device: <none> (0)
            IPv6 unicast addresses (max 2):
                    fe80::2acd:c1ff:fe02:74f4 autoconf preferred infinite
                    fd9c:33d7:ba99:0:2acd:c1ff:fe02:74f4 autoconf preferred infinite
            IPv6 multicast addresses (max 3):
                    ff02::1
                    ff02::1:ff02:74f4
            IPv6 prefixes (max 2):
                    fd9c:33d7:ba99::/64 infinite
            IPv6 hop limit           : 64
            IPv6 base reachable time : 30000
            IPv6 reachable time      : 20783
            IPv6 retransmit timer    : 0
            DHCPv6 state             : disabled
            IPv4 unicast addresses (max 1):
                    192.168.10.197/255.255.255.0 DHCP preferred
            IPv4 multicast addresses (max 2):
                    224.0.0.1
            IPv4 gateway : 192.168.10.1
            DHCPv4 lease time : 28800
            DHCPv4 renew time : 14400
            DHCPv4 server     : 192.168.10.10
            DHCPv4 requested  : 192.168.10.197
            DHCPv4 state      : bound
            DHCPv4 attempts   : 2
            DHCPv4 state      : bound

   .. admonition:: DNS server list and name lookup query
      :class: note dropdown

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **net dns**
            DNS servers:
                    192.168.10.10:53 via wlan0 (DHCP)
                    192.168.10.20:53 via wlan0 (DHCP)
                    [fd9c:33d7:ba99::1]:53 via wlan0 (IPv6 RA)
            Pending queries:

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **net dns query google.com**
            Query for 'google.com' sent.
            dns: 142.250.185.142
            dns: All results received

   .. admonition:: ICMP/Ping check in WAN and LAN
      :class: note dropdown

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **net ping 142.250.185.142**
            PING 142.250.185.142
            28 bytes from 142.250.185.142 to 192.168.10.197: icmp_seq=1 ttl=118 time=28 ms
            28 bytes from 142.250.185.142 to 192.168.10.197: icmp_seq=2 ttl=118 time=27 ms
            28 bytes from 142.250.185.142 to 192.168.10.197: icmp_seq=3 ttl=118 time=28 ms

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **net ping 192.168.10.1**
            PING 192.168.10.1
            28 bytes from 192.168.10.1 to 192.168.10.197: icmp_seq=1 ttl=64 time=15 ms
            28 bytes from 192.168.10.1 to 192.168.10.197: icmp_seq=2 ttl=64 time=8 ms
            28 bytes from 192.168.10.1 to 192.168.10.197: icmp_seq=3 ttl=64 time=9 ms

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **net ping fd9c:33d7:ba99::1**
            PING fd9c:33d7:ba99::1
            8 bytes from fd9c:33d7:ba99::1 to fd9c:33d7:ba99:0:2acd:c1ff:fe02:74f4: icmp_seq=1 ttl=64 time=10 ms
            8 bytes from fd9c:33d7:ba99::1 to fd9c:33d7:ba99:0:2acd:c1ff:fe02:74f4: icmp_seq=2 ttl=64 time=9 ms
            8 bytes from fd9c:33d7:ba99::1 to fd9c:33d7:ba99:0:2acd:c1ff:fe02:74f4: icmp_seq=3 ttl=64 time=9 ms

   .. admonition:: ARP list, list of connections, and interface statistics
      :class: note dropdown

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **net arp**
                 Interface  Link              Address
            [ 0] 1          BC:EE:7B:32:E5:D0 192.168.10.1
            [ 1] 1          00:80:77:84:BF:81 192.168.10.10

         .. parsed-literal::

            :bgn:`uart:~$` **net conn**
                 Context    Iface  Flags            Local             Remote
            [ 1] 0x20005c8c 1      4DU      0.0.0.0:42759          0.0.0.0:0
            [ 2] 0x20005d3c 1      4DU      0.0.0.0:38313          0.0.0.0:0
            [ 3] 0x20005dec 1      6DU         [::]:38774             [::]:0

                 Handler    Callback  Proto            Local                  Remote
            [ 1] 0x20006510 0x10024b79  UDP       [::]:38774                  [::]:0
            [ 2] 0x200065a0 0x10024b79  UDP    0.0.0.0:38313               0.0.0.0:0
            [ 3] 0x20006558 0x10024b79  UDP    0.0.0.0:42759               0.0.0.0:0
            [ 4] 0x200065e8 0x10030165  UDP         [::]:546                  [::]:0
            [ 5] 0x20006630 0x100310d9  UDP       0.0.0.0:68               0.0.0.0:0

            TCP        Context   Src port Dst port   Send-Seq   Send-Ack  MSS    State
            No TCP connections
            :bgn:`Set CONFIG_NET_TCP_LOG_LEVEL_DBG to enable TCP debugging support.`

         .. parsed-literal::

            :bgn:`uart:~$` **net stats**

            Interface 0x20001940 (WiFi) [1]
            ===============================
            IPv6 recv      34       sent    38      drop    3       forwarded       0
            IPv6 ND recv   21       sent    22      drop    1
            IPv6 MLD recv  0        sent    2       drop    0
            IPv4 recv      40       sent    39      drop    2       forwarded       0
            IP vhlerr      49       hblener 0       lblener 0
            IP fragerr     0        chkerr  0       protoer 49
            ICMP recv      61       sent    64      drop    0
            ICMP typeer    0        chkerr  0
            IGMP recv      0        sent    0       drop    0
            UDP recv       8        sent    8       drop    5
            UDP chkerr     0
            TCP bytes recv 0        sent    0       resent  0
            TCP seg recv   0        sent    0       drop    0
            TCP seg resent 0        chkerr  0       ackerr  0
            TCP seg rsterr 0        rst     0
            TCP conn drop  0        connrst 0
            TCP pkt drop   0
            DNS recv       3        sent    4       drop    1
            Bytes received 42752
            Bytes sent     6278
            Processing err 11

   .. admonition:: Wi-Fi interface statistics and SSID scan
      :class: note dropdown

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **wifi statistics**
            Statistics for Wi-Fi interface 0x20001940 [1]
            Bytes received   : 45148
            Bytes sent       : 6622
            Packets received : 163
            Packets sent     : 96
            Receive errors   : 0
            Send errors      : 0
            Bcast received   : 0
            Bcast sent       : 0
            Mcast received   : 0
            Mcast sent       : 0
            Beacons received : 0
            Beacons missed   : 0
            Unicast received : 0
            Unicast sent     : 0
            Overrun count    : 0

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **wifi scan**
            Scan requested

            Num | SSID               (len) | Chan (Band)   | RSSI | Security         | BSSID             | MFP
            1   | PYUR Community     14    | 1    (2.4GHz) | -77  | WPA2 Enterprise  | B5:7F:4F:4E:05:AC | Disable
            2   | PYUR B6672         10    | 1    (2.4GHz) | -75  | WPA2-PSK         | 0B:A2:AB:0C:C6:A1 | Disable
            3   | FRITZ!Box 7430 XR  17    | 1    (2.4GHz) | -82  | WPA2-PSK         | A8:34:B0:1E:D9:79 | Disable
            4   | o2-WLAN65          9     | 2    (2.4GHz) | -82  | WPA2-PSK         | 5A:8B:47:4C:80:9C | Disable
            5   | Fluchtweg          9     | 6    (2.4GHz) | -50  | WPA2-PSK         | 44:12:1A:18:24:C5 | Disable
            6   | Hekatoncheiren     14    | 6    (2.4GHz) | -50  | WPA2-PSK         | B2:05:A9:B0:DB:9A | Disable
            7   | FRITZ!Box 7430 SH  17    | 11   (2.4GHz) | -77  | WPA2-PSK         | 34:3B:8A:C0:B3:37 | Disable
            8   | Fallschirm         10    | 11   (2.4GHz) | -70  | WPA2-PSK         | F9:15:89:6C:7D:59 | Disable
            9   | Fallschirm Gast    15    | 11   (2.4GHz) | -71  | WPA2-PSK         | 14:AD:F1:A0:07:F1 | Disable
            Scan request done

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **wifi status**
            :byl:`Status request failed`
