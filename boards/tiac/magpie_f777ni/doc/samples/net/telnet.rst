.. _magpie_f777ni_telnet-console-sample:

TELNET Console
##############

Overview
********

See :external+zephyr:zephyr:code-sample:`telnet-console` for the
original description.

.. _magpie_f777ni_telnet-console-sample-requirements:

Requirements
************

- This sample application negotiate IPv4 address from a DHCPv4 server
  running everywhere in your local network.
- The 10/100 Ethernet MAC already configured in RMII/MII mode with MDIO
  using the ``&mac`` :external+zephyr:ref:`devicetree <dt-guide>` label.

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

.. container:: highlight highlight-console notranslate no-copybutton

   .. parsed-literal::

      [00:00:00.050,000] <inf> phy_mii: PHY (0) ID 221560
      \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* \*\*\*
      [00:00:00.060,000] <inf> shell_telnet: Telnet shell backend initialized
      [00:00:00.060,000] <inf> net_config: Initializing network
      [00:00:00.060,000] <inf> net_config: Waiting interface 1 (0x20021440) to be up...
      [00:00:02.652,000] <inf> phy_mii: PHY (0) Link speed **100 Mb**, **full duplex**
      [00:00:02.658,000] <inf> net_config: Interface 1 (0x20021440) coming up
      [00:00:02.658,000] <inf> net_config: IPv4 address: 192.0.2.1
      [00:00:02.658,000] <inf> net_config: Running dhcpv4 client...
      [00:00:02.659,000] <inf> net_telnet_sample: Starting Telnet sample
      [00:00:02.759,000] <inf> net_config: IPv6 address: 2001:db8::1
      [00:00:03.680,000] <inf> net_dhcpv4: Received: **192.168.10.197**
      [00:00:03.680,000] <inf> net_config: IPv4 address: 192.168.10.197
      [00:00:03.680,000] <inf> net_config: Lease time: 28800 seconds
      [00:00:03.680,000] <inf> net_config: Subnet: 255.255.255.0
      [00:00:03.680,000] <inf> net_config: Router: 192.168.10.1
      [00:00:03.760,000] <inf> net_config: IPv6 address: 2001:db8::1

To verify the Zephyr application clients are running, bind the TELNET server to
the network interface, and has received an IPv4 address by typing on Linux host:

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`$` **ping -c3 192.168.10.197**
      PING 192.168.10.197 (192.168.10.197) 56(84) bytes of data.
      64 bytes from 192.168.10.197: icmp_seq=1 ttl=64 time=0.808 ms
      64 bytes from 192.168.10.197: icmp_seq=2 ttl=64 time=0.396 ms
      64 bytes from 192.168.10.197: icmp_seq=3 ttl=64 time=0.501 ms

      --- 192.168.10.197 ping statistics ---
      3 packets transmitted, 3 received, 0% packet loss, time 2060ms
      rtt min/avg/max/mdev = 0.396/0.568/0.808/0.174 ms

      :bgn:`$` **nmap -Pn 192.168.10.197**
      Starting Nmap 7.80 ( https://nmap.org ) at … … …
      Nmap scan report for 192.168.10.197
      Host is up (0.00083s latency).
      Not shown: 999 closed ports
      PORT   STATE SERVICE
      23/tcp open  telnet

      Nmap done: 1 IP address (1 host up) scanned in 4.99 seconds

At this point you should be able to connect via ``telnet`` over the network.
On your Linux host:

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`$` **telnet 192.168.10.197**
      Trying 192.168.10.197...
      Connected to **192.168.10.197**.
      Escape character is '^]'.

You are now connected, and as for the UART console, you can type in your
commands and get the output through your telnet client. Now type enter, the
shell prompt will appear and you can enter commands, for example ``help``
or ``kernel version``.

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`~$` **kernel version**
      Zephyr version |zephyr_version_number_em|

      :bgn:`~$` **bridle version**
      Bridle version |shortversion_number_em|

      :bgn:`~$` **device list**
      devices:
      - rcc\ @\ 40023800 (READY)
        DT node labels: rcc
      - reset-controller (READY)
        DT node labels: rctl
      - interrupt-controller\ @\ 40013c00 (READY)
        DT node labels: exti
      - gpio\ @\ 40022800 (READY)
        DT node labels: gpiok
      - gpio\ @\ 40022400 (READY)
        DT node labels: gpioj
      - gpio\ @\ 40022000 (READY)
        DT node labels: gpioi
      - gpio\ @\ 40021C00 (READY)
        DT node labels: gpioh
      - gpio\ @\ 40021800 (READY)
        DT node labels: gpiog
      - gpio\ @\ 40021400 (READY)
        DT node labels: gpiof
      - gpio\ @\ 40021000 (READY)
        DT node labels: gpioe
      - gpio\ @\ 40020C00 (READY)
        DT node labels: gpiod
      - gpio\ @\ 40020800 (READY)
        DT node labels: gpioc
      - gpio\ @\ 40020400 (READY)
        DT node labels: gpiob
      - gpio\ @\ 40020000 (READY)
        DT node labels: gpioa
      - rng\ @\ 50060800 (READY)
        DT node labels: rng
      - serial\ @\ 40007800 (READY)
        DT node labels: uart7
      - serial\ @\ 40004c00 (READY)
        DT node labels: uart4 tmph_serial1 tmph_serial
      - rtc\ @\ 40002800 (READY)
        DT node labels: rtc
      - i2c\ @\ 40006000 (READY)
        DT node labels: i2c4 tmph_i2c1 tmph_i2c
      - i2c\ @\ 40005800 (READY)
        DT node labels: i2c2
      - spi\ @\ 40013400 (READY)
        DT node labels: spi4 tmph_spi1 tmph_spi
      - mdio (READY)
        DT node labels: mdio
      - ethernet-phy\ @\ 0 (READY)
        DT node labels: eth_phy
      - ethernet (READY)
        DT node labels: mac

Simple GPIO Operations
======================

.. rubric:: Switch user LED 2 on and off

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`~$` **gpio get gpiog 12**
      0

      :bgn:`~$` **gpio conf gpiog 12 oh0**

      :bgn:`~$` **gpio set gpiog 12 1**
      :bgn:`~$` **gpio set gpiog 12 0**

      :bgn:`~$` **gpio blink gpiog 12**
      Hit any key to exit

Simple I2C Operations
=====================

.. rubric:: Scan I2C bus 2

.. container:: highlight highlight-console notranslate

   .. parsed-literal::

      :bgn:`~$` **i2c scan i2c2**
           0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
      00:             -- -- -- -- -- -- -- -- -- -- -- --
      10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      20: 20 21 -- -- -- -- -- -- -- -- -- -- -- -- -- --
      30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      40: 40 41 42 43 44 45 46 -- -- -- -- -- -- -- -- --
      50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      70: -- -- -- -- -- -- -- --
      9 devices found on i2c2
