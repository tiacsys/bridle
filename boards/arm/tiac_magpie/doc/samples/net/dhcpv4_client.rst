.. _tiac_magpie_dhcpv4-client-sample:

DHCPv4 Client
#############

Overview
********

See :doc:`zephyr:samples/net/dhcpv4_client/README` for the original description.

.. _tiac_magpie_dhcpv4-client-sample-requirements:

Requirements
************

- This sample application negotiate IPv4 address from a DHCPv4 server
  running everywhere in your local network.
- The 10/100 Ethernet MAC already configured in RMII/MII mode with MDIO
  using the ``&mac`` :ref:`devicetree <zephyr:dt-guide>` label.

Building and Running
********************

Build and flash DHCPv4 Client as follows:

.. zephyr-app-commands::
   :app: zephyr/samples/net/dhcpv4_client
   :build-dir: dhcpv4_client-tiac_magpie
   :board: tiac_magpie
   :west-args: -p
   :goals: flash
   :host-os: unix

Once DHCPv4 client address negotiation completed with server, details
are shown on the console like this:

.. code-block:: none

   [00:00:00.011,000] <inf> net_dhcpv4_client_sample: Run dhcpv4 client
   [00:00:00.011,000] <inf> net_dhcpv4_client_sample: Start on ethernet@40028000: index=1
   [00:00:03.084,000] <inf> net_dhcpv4_client_sample: DHCP Option 42: 192.168.10.10
   [00:00:03.084,000] <inf> net_dhcpv4: Received: 192.168.10.197
   [00:00:03.084,000] <inf> net_dhcpv4_client_sample:    Address[1]: 192.168.10.197
   [00:00:03.084,000] <inf> net_dhcpv4_client_sample:     Subnet[1]: 255.255.255.0
   [00:00:03.084,000] <inf> net_dhcpv4_client_sample:     Router[1]: 192.168.10.1
   [00:00:03.084,000] <inf> net_dhcpv4_client_sample: Lease time[1]: 28800 seconds

To verify the Zephyr application client is running and has received
an IPv4 address by typing on Linux host:

.. code-block:: console

   $ ping -c3 192.168.10.197
   PING 192.168.10.197 (192.168.10.197) 56(84) bytes of data.
   64 bytes from 192.168.10.197: icmp_seq=1 ttl=64 time=0.333 ms
   64 bytes from 192.168.10.197: icmp_seq=2 ttl=64 time=0.264 ms
   64 bytes from 192.168.10.197: icmp_seq=3 ttl=64 time=0.274 ms

   --- 192.168.10.197 ping statistics ---
   3 packets transmitted, 3 received, 0% packet loss, time 2043ms
   rtt min/avg/max/mdev = 0.264/0.290/0.333/0.030 ms

On Zephyr, Shell command line:

.. code-block:: none

   uart:~$ net iface show 1

   Interface eth0 (0x20020cb8) (Ethernet) [1]
   ===================================
   Link addr : 02:80:E1:4F:98:16
   MTU       : 1500
   Flags     : AUTO_START,IPv4
   Ethernet capabilities supported:
	   10 Mbits
	   100 Mbits
   IPv4 unicast addresses (max 1):
	   192.168.10.197 DHCP preferred
   IPv4 multicast addresses (max 1):
	   <none>
   IPv4 gateway : 192.168.10.1
   IPv4 netmask : 255.255.255.0
   DHCPv4 lease time : 28800
   DHCPv4 renew time : 14400
   DHCPv4 server     : 192.168.10.10
   DHCPv4 requested  : 192.168.10.197
   DHCPv4 state      : bound
   DHCPv4 attempts   : 1

   uart:~$ net ping 192.168.10.1

   PING 192.168.10.1
   28 bytes from 192.168.10.1 to 192.168.10.197: icmp_seq=0 ttl=64 time=0 ms
   28 bytes from 192.168.10.1 to 192.168.10.197: icmp_seq=1 ttl=64 time=0 ms
   28 bytes from 192.168.10.1 to 192.168.10.197: icmp_seq=2 ttl=64 time=0 ms

   uart:~$ net arp

        Interface  Link              Address
   [ 0] 1          BC:EE:7B:32:E5:D0 192.168.10.1
   [ 1] 1          00:80:77:84:BF:81 192.168.10.82
