.. _magpie_f777ni_telnet-console-sample:

TELNET Console
##############

Overview
********

See :zephyr:code-sample:`zephyr:telnet-console` for the original description.

.. _magpie_f777ni_telnet-console-sample-requirements:

Requirements
************

- This sample application negotiate IPv4 address from a DHCPv4 server
  running everywhere in your local network.
- The 10/100 Ethernet MAC already configured in RMII/MII mode with MDIO
  using the ``&mac`` :ref:`devicetree <zephyr:dt-guide>` label.

Building and Running
********************

Build and flash TELNET Console as follows:

.. zephyr-app-commands::
   :app: zephyr/samples/net/telnet
   :build-dir: telnet-magpie_f777ni
   :board: magpie_f777ni
   :gen-args: -DCONFIG_NET_DHCPV4=y -DCONFIG_NET_LOG=y -DCONFIG_LOG=y -DCONFIG_GPIO_SHELL=y -DCONFIG_I2C_SHELL=y
   :west-args: -p
   :goals: flash
   :host-os: unix

Once DHCPv4 client address negotiation completed with server, details
are shown on the console like this:

.. parsed-literal::
   :class: highlight-console notranslate

   \*\*\* Booting Zephyr OS … … …\*\*\*
   [00:00:00.014,000] <inf> shell_telnet: Telnet shell backend initialized
   [00:00:00.014,000] <inf> net_config: Initializing network
   [00:00:00.014,000] <inf> net_config: Waiting interface 1 (0x200213f0) to be up...
   [00:00:00.395,000] <inf> net_config: Interface 1 (0x200213f0) coming up
   [00:00:00.395,000] <inf> net_config: IPv4 address: 192.0.2.1
   [00:00:00.395,000] <inf> net_config: Running dhcpv4 client...
   [00:00:00.396,000] :brd:`<err> net_if: Cannot join solicit node address ff02::1:ff00:1 for 1 (-12)`
   [00:00:00.397,000] <inf> net_telnet_sample: Starting Telnet sample
   [00:00:00.397,000] <inf> net_telnet_sample: Running dhcpv4 client...
   [00:00:00.398,000] <inf> net_telnet_sample: IPv6 address: 2001:db8::1
   [00:00:00.497,000] <inf> net_config: IPv6 address: fd9c:33d7:ba99:0:280:e1ff:fee1:9a39
   [00:00:09.416,000] <inf> net_dhcpv4: Received: 192.168.10.197
   [00:00:09.417,000] <inf> net_telnet_sample:    Address[1]: 192.168.10.197
   [00:00:09.417,000] <inf> net_telnet_sample:     Subnet[1]: 255.255.255.0
   [00:00:09.417,000] <inf> net_telnet_sample:     Router[1]: 192.168.10.1
   [00:00:09.417,000] <inf> net_telnet_sample: Lease time[1]: 28800 seconds
   [00:00:09.417,000] <inf> net_config: IPv4 address: 192.168.10.197
   [00:00:09.417,000] <inf> net_config: Lease time: 28800 seconds
   [00:00:09.417,000] <inf> net_config: Subnet: 255.255.255.0
   [00:00:09.417,000] <inf> net_config: Router: 192.168.10.1

To verify the Zephyr application clients are running, bind the TELNET server to
the network interface, and has received an IPv4 address by typing on Linux host:

.. parsed-literal::
   :class: highlight

   :bgn:`$` **ping -c3 192.168.10.197**
   PING 192.168.10.197 (192.168.10.197) 56(84) bytes of data.
   64 bytes from 192.168.10.197: icmp_seq=1 ttl=64 time=0.303 ms
   64 bytes from 192.168.10.197: icmp_seq=2 ttl=64 time=0.261 ms
   64 bytes from 192.168.10.197: icmp_seq=3 ttl=64 time=0.264 ms

   --- 192.168.10.197 ping statistics ---
   3 packets transmitted, 3 received, 0% packet loss, time 2052ms
   rtt min/avg/max/mdev = 0.261/0.276/0.303/0.019 ms

   :bgn:`$` **nmap -Pn 192.168.10.197**
   Starting Nmap 7.80 ( https://nmap.org ) at 2024-05-03 22:51 CEST
   Nmap scan report for 192.168.10.197
   Host is up (0.0030s latency).
   Not shown: 999 closed ports
   PORT   STATE SERVICE
   23/tcp open  telnet

   Nmap done: 1 IP address (1 host up) scanned in 8.22 seconds

At this point you should be able to connect via ``telnet`` over the network.
On your Linux host:

.. parsed-literal::
   :class: highlight

   :bgn:`$` **telnet 192.168.10.197**
   Trying 192.168.10.197...
   Connected to 192.168.10.197.
   Escape character is '^]'.

You are now connected, and as for the UART console, you can type in your
commands and get the output through your telnet client. Now type enter, the
shell prompt will appear and you can enter commands, for example ``help``
or ``kernel version``.

.. parsed-literal::
   :class: highlight-console notranslate

   :bgn:`~$` **kernel version**
   Zephyr version |zephyr_version_number_em|

   :bgn:`~$` **bridle version**
   Bridle version |version_number_em|

   :bgn:`~$` **device list**
   devices:
   - rcc\ @\ 40023800 (READY)
   - reset-controller (READY)
   - interrupt-controller\ @\ 40013c00 (READY)
   - gpio\ @\ 40022800 (READY)
   - gpio\ @\ 40022400 (READY)
   - gpio\ @\ 40022000 (READY)
   - gpio\ @\ 40021C00 (READY)
   - gpio\ @\ 40021800 (READY)
   - gpio\ @\ 40021400 (READY)
   - gpio\ @\ 40021000 (READY)
   - gpio\ @\ 40020C00 (READY)
   - gpio\ @\ 40020800 (READY)
   - gpio\ @\ 40020400 (READY)
   - gpio\ @\ 40020000 (READY)
   - rng\ @\ 50060800 (READY)
   - serial\ @\ 40007800 (READY)
   - serial\ @\ 40004c00 (READY)
   - rtc\ @\ 40002800 (READY)
   - i2c\ @\ 40006000 (READY)
   - i2c\ @\ 40005800 (READY)
   - spi\ @\ 40013400 (READY)
   - ethernet\ @\ 40028000 (READY)

Simple GPIO Operations
======================

.. rubric:: Switch user LED 2 on and off

.. parsed-literal::
   :class: highlight-console notranslate

   :bgn:`~$` **gpio get gpio@40021800 12**
   0

   :bgn:`~$` **gpio conf gpio@40021800 12 oh0**

   :bgn:`~$` **gpio set gpio@40021800 12 1**
   :bgn:`~$` **gpio set gpio@40021800 12 0**

   :bgn:`~$` **gpio blink gpio@40021800 12**
   Hit any key to exit

Simple I2C Operations
=====================

.. rubric:: Scan I2C bus 2

.. parsed-literal::
   :class: highlight-console notranslate

   :bgn:`~$` **i2c scan i2c@40005800**
        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
   00:             -- -- -- -- -- -- -- -- -- -- -- --
   10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   20: 20 21 -- -- -- -- -- -- -- -- -- -- -- -- -- --
   30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   40: 40 41 42 43 44 45 46 -- -- -- -- -- -- -- -- --
   50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   70: -- -- -- -- -- -- -- --
   9 devices found on i2c\ @\ 40005800
