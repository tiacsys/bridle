.. _tiac_magpie_telnet-console-sample:

TELNET Console
##############

Overview
********

See :ref:`telnet-console-sample` for the original description.

.. _tiac_magpie_telnet-console-sample-requirements:

Requirements
************

- This sample application negotiate IPv4 address from a DHCPv4 server
  running everywhere in your local network.
- The 10/100 Ethernet MAC already configured in RMII/MII mode with MDIO
  using the ``&mac`` :ref:`devicetree <dt-guide>` label.

Building and Running
********************

Build and flash TELNET Console as follows:

.. zephyr-app-commands::
   :app: zephyr/samples/net/telnet
   :build-dir: telnet-tiac_magpie
   :board: tiac_magpie
   :gen-args: -DCONFIG_NET_DHCPV4=y -DCONFIG_NET_LOG=y -DCONFIG_LOG=y -DCONFIG_GPIO_SHELL=y
   :goals: build flash
   :host-os: unix

Once DHCPv4 client address negotiation completed with server, details
are shown on the console like this:

.. code-block:: none

   [00:00:00.272,000] <inf> shell_telnet: Telnet shell backend initialized
   [00:00:00.272,000] <inf> net_config: Initializing network
   [00:00:00.272,000] <inf> net_config: Waiting interface 1 (0x20021258) to be up...
   [00:00:00.762,000] <inf> net_config: Interface 1 (0x20021258) coming up
   [00:00:00.762,000] <inf> net_config: IPv4 address: 192.0.2.1
   [00:00:00.762,000] <inf> net_config: Running dhcpv4 client...
   [00:00:00.762,000] <inf> net_telnet_sample: Starting Telnet sample
   [00:00:00.762,000] <inf> net_telnet_sample: Running dhcpv4 client...
   [00:00:00.762,000] <inf> net_telnet_sample: IPv6 address: 2001:db8::1
   [00:00:00.862,000] <inf> net_config: IPv6 address: 2001:db8::1
   [00:00:00.862,000] <inf> net_config: IPv6 address: 2001:db8::1
   [00:00:00.863,000] <inf> net_config: IPv6 address: 2001:db8::1
   [00:00:04.773,000] <inf> net_dhcpv4: Received: 192.168.10.198
   [00:00:04.773,000] <inf> net_telnet_sample: IPv4 address: 192.168.10.198
   [00:00:04.773,000] <inf> net_telnet_sample: Lease time: 36000 seconds
   [00:00:04.773,000] <inf> net_telnet_sample: Subnet: 255.255.255.0
   [00:00:04.773,000] <inf> net_telnet_sample: Router: 192.168.10.1
   [00:00:04.773,000] <inf> net_config: IPv4 address: 192.168.10.198
   [00:00:04.773,000] <inf> net_config: Lease time: 36000 seconds
   [00:00:04.773,000] <inf> net_config: Subnet: 255.255.255.0
   [00:00:04.773,000] <inf> net_config: Router: 192.168.10.1

   [00:00:00.269,000] <inf> shell_telnet: Telnet shell backend initialized
   [00:00:00.269,000] <inf> net_config: Initializing network
   [00:00:00.269,000] <inf> net_config: Waiting interface 1 (0x20021098) to be up...
   [00:00:00.584,000] <inf> net_config: Interface 1 (0x20021098) coming up
   [00:00:00.584,000] <inf> net_config: IPv4 address: 192.0.2.1
   [00:00:00.584,000] <inf> net_config: Running dhcpv4 client...
   [00:00:00.584,000] <inf> net_telnet_sample: Starting Telnet sample
   [00:00:00.584,000] <inf> net_telnet_sample: Running dhcpv4 client...
   [00:00:00.584,000] <inf> net_telnet_sample: IPv6 address: 2001:db8::1
   [00:00:00.684,000] <inf> net_config: IPv6 address: 2001:db8::1
   [00:00:00.684,000] <inf> net_config: IPv6 address: 2001:db8::1
   [00:00:11.622,000] <inf> net_dhcpv4: Received: 192.168.10.184
   [00:00:11.622,000] <inf> net_telnet_sample: IPv4 address: 192.168.10.184
   [00:00:11.622,000] <inf> net_telnet_sample: Lease time: 36000 seconds
   [00:00:11.622,000] <inf> net_telnet_sample: Subnet: 255.255.255.0
   [00:00:11.622,000] <inf> net_telnet_sample: Router: 192.168.10.1
   [00:00:11.622,000] <inf> net_config: IPv4 address: 192.168.10.184
   [00:00:11.622,000] <inf> net_config: Lease time: 36000 seconds
   [00:00:11.622,000] <inf> net_config: Subnet: 255.255.255.0
   [00:00:11.622,000] <inf> net_config: Router: 192.168.10.1

To verify the Zephyr application clients are running, bind the TELNET server to
the network interface, and has received an IPv4 address by typing on Linux host:

.. code-block:: console

   $ ping -c3 192.168.10.184
   PING 192.168.10.184 (192.168.10.184) 56(84) bytes of data.
   64 bytes from 192.168.10.184: icmp_seq=1 ttl=64 time=0.303 ms
   64 bytes from 192.168.10.184: icmp_seq=2 ttl=64 time=0.261 ms
   64 bytes from 192.168.10.184: icmp_seq=3 ttl=64 time=0.264 ms

   --- 192.168.10.184 ping statistics ---
   3 packets transmitted, 3 received, 0% packet loss, time 2052ms
   rtt min/avg/max/mdev = 0.261/0.276/0.303/0.019 ms

   $ nmap 192.168.10.184
   Starting Nmap 7.80 ( https://nmap.org ) at 2021-04-05 19:01 CEST
   Nmap scan report for 192.168.10.184
   Host is up (0.00043s latency).
   Not shown: 999 closed ports
   PORT   STATE SERVICE
   23/tcp open  telnet

   Nmap done: 1 IP address (1 host up) scanned in 3.77 seconds

At this point you should be able to connect via ``telnet`` over the network.
On your Linux host:

.. code-block:: console

   $ telnet 192.168.10.184
   Trying 192.168.10.184...
   Connected to 192.168.10.184.
   Escape character is '^]'.

You are now connected, and as for the UART console, you can type in your
commands and get the output through your telnet client. Now type enter, the
shell prompt will appear and you can enter commands, for example ``help``
or ``kernel version``.

.. code-block:: console

   ~$ kernel version
   Zephyr version 3.0.0

   ~$ device list
   devices:
   - rcc@40023800 (READY)
   - GPIOK (READY)
     requires: rcc@40023800
   - GPIOJ (READY)
     requires: rcc@40023800
   - GPIOI (READY)
     requires: rcc@40023800
   - GPIOH (READY)
     requires: rcc@40023800
   - GPIOG (READY)
     requires: rcc@40023800
   - GPIOF (READY)
     requires: rcc@40023800
   - GPIOE (READY)
     requires: rcc@40023800
   - GPIOD (READY)
     requires: rcc@40023800
   - GPIOC (READY)
     requires: rcc@40023800
   - GPIOB (READY)
     requires: rcc@40023800
   - GPIOA (READY)
     requires: rcc@40023800
   - interrupt-controller@40013c00 (READY)
   - RTC_0 (READY)
     requires: rcc@40023800
   - RNG (READY)
     requires: rcc@40023800
   - UART_7 (READY)
     requires: rcc@40023800
   - UART_4 (READY)
     requires: rcc@40023800
   - I2C_4 (READY)
     requires: rcc@40023800
   - I2C_2 (READY)
     requires: rcc@40023800
   - SPI_4 (READY)
     requires: rcc@40023800
   - ETH_0 (READY)
     requires: rcc@40023800

Simple GPIO Operations
======================

.. rubric:: Switch user LED 2 on and off

.. code-block:: console

   ~$ gpio get GPIOG 12
   Reading GPIOG pin 12
   Value 0
   ~$ gpio conf GPIOG 12 out
   Configuring GPIOG pin 12
   ~$ gpio set GPIOG 12 1
   Writing to GPIOG pin 12
   ~$ gpio set GPIOG 12 0
   Writing to GPIOG pin 12

Simple I2C Operations
=====================

.. rubric:: Scan I2C bus 2

.. code-block:: console

   ~$ i2c scan I2C_2
   i2c scan I2C_2
        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
   00:             -- -- -- -- -- -- -- -- -- -- -- --
   10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   20: 20 21 -- -- -- -- -- -- -- -- -- -- -- -- -- --
   30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   40: 40 41 42 43 44 45 46 -- -- -- -- -- -- -- -- --
   50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   70: -- -- -- -- -- -- -- --
   9 devices found on I2C_2
