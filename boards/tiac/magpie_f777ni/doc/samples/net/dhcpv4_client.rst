.. _magpie_f777ni_dhcpv4-client-sample:

DHCPv4 Client
#############

Overview
********

See :external+zephyr:zephyr:code-sample:`dhcpv4-client` for the
original description.

.. _magpie_f777ni_dhcpv4-client-sample-requirements:

Requirements
************

- This sample application negotiate IPv4 address from a DHCPv4 server
  running everywhere in your local network.
- The 10/100 Ethernet MAC already configured in RMII/MII mode with MDIO
  using the ``&mac`` :external+zephyr:ref:`devicetree <dt-guide>` label.

Building and Running
********************

Build and flash DHCPv4 Client as follows:

   .. zephyr-app-commands::
      :app: zephyr/samples/net/dhcpv4_client
      :build-dir: dhcpv4_client-magpie_f777ni
      :board: magpie_f777ni
      :west-args: -p
      :goals: flash
      :host-os: unix

Sample Output
=============

Once DHCPv4 client address negotiation completed with server, details
are shown on the console like this:

   .. container:: highlight highlight-console notranslate no-copybutton

      .. parsed-literal::

         [00:00:00.050,000] <inf> phy_mii: PHY (0) ID 221560
         \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* \*\*\*
         [00:00:00.057,000] <inf> net_dhcpv4_client_sample: Run dhcpv4 client
         [00:00:00.057,000] <inf> net_dhcpv4_client_sample: Start on **ethernet**: index=1
         [00:00:02.651,000] <inf> phy_mii: PHY (0) Link speed **100 Mb**, **full duplex**
         [00:00:05.658,000] <inf> net_dhcpv4_client_sample: DHCP Option 42: 192.168.10.1
         [00:00:05.658,000] :byl:`<wrn> net_dhcpv4: DHCP server provided more DNS servers than can be saved`
         [00:00:05.668,000] <inf> net_dhcpv4_client_sample: DHCP Option 42: 192.168.10.1
         [00:00:05.668,000] :byl:`<wrn> net_dhcpv4: DHCP server provided more DNS servers than can be saved`
         [00:00:05.669,000] <inf> net_dhcpv4: Received: **192.168.10.197**
         [00:00:05.669,000] <inf> net_dhcpv4_client_sample:    Address[1]: 192.168.10.197
         [00:00:05.669,000] <inf> net_dhcpv4_client_sample:     Subnet[1]: 255.255.255.0
         [00:00:05.669,000] <inf> net_dhcpv4_client_sample:     Router[1]: 192.168.10.1
         [00:00:05.669,000] <inf> net_dhcpv4_client_sample: Lease time[1]: 28800 seconds

To verify the Zephyr application client is running and has received
an IPv4 address by typing on Linux host:

   .. admonition:: Simple test execution on Linux host
      :class: note dropdown

      (text in bold is a command input)

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`$` **ping -c3 192.168.10.197**
            PING 192.168.10.197 (192.168.10.197) 56(84) bytes of data.
            64 bytes from 192.168.10.197: icmp_seq=1 ttl=64 time=0.746 ms
            64 bytes from 192.168.10.197: icmp_seq=2 ttl=64 time=0.420 ms
            64 bytes from 192.168.10.197: icmp_seq=3 ttl=64 time=0.421 ms

            --- 192.168.10.197 ping statistics ---
            3 packets transmitted, 3 received, 0% packet loss, time 2054ms
            rtt min/avg/max/mdev = 0.420/0.529/0.746/0.153 ms

On Zephyr, Shell command line:

   .. admonition:: Simple test execution on target
      :class: note dropdown

      (text in bold is a command input)

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **net iface show 1**
            Default interface: 1


            Interface eth0 (0x20020f08) (Ethernet) [1]
            ===================================
            Link addr : **02:80:E1:4F:98:16**
            MTU       : 1500
            Flags     : AUTO_START,IPv4
            Device    : **ethernet** (0x8020edc)
            Status    : oper=UP, admin=UP, carrier=ON
            Ethernet capabilities supported:
                    10 Mbits
                    100 Mbits
            Ethernet PHY device: **ethernet-phy@0** (0x8020eb8)
            Ethernet link speed: **100 Mbits full-duplex**
            IPv4 unicast addresses (max 1):
                    **192.168.10.197**/255.255.255.0 DHCP preferred
            IPv4 multicast addresses (max 2):
                    224.0.0.1
            IPv4 gateway : 192.168.10.1
            DHCPv4 lease time : 28800
            DHCPv4 renew time : 14400
            DHCPv4 server     : 192.168.10.10
            DHCPv4 requested  : 192.168.10.197
            DHCPv4 state      : bound
            DHCPv4 attempts   : 1
            DHCPv4 state      : bound

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **net ping -p 0 -c 1 192.168.10.1**
            PING 192.168.10.1
            28 bytes from 192.168.10.1 to **192.168.10.197**: icmp_seq=0 ttl=64 time=0 ms

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **net arp**
                 Interface  Link              Address
            [ 0] 1          BC:EE:7B:32:E5:D0 192.168.10.1
            [ 1] 1          00:80:77:84:BF:81 192.168.10.10
