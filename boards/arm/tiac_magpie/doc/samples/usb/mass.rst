.. _tiac_magpie_usb_mass-sample:

USB Mass Storage
################

Overview
********

See :ref:`usb_mass` for the original description.

.. _tiac_magpie_usb_mass-sample-requirements:

Requirements
************

On the TiaC Magpie board this sample application will use on-chip RAM.

Building and Running
********************

Build and flash USB Mass Storage as follows:

RAM-disk Example without any file system
========================================

The default configurations selects RAM-based disk without any file system.
This example only needs additional 32KiB RAM for the RAM-disk and is intended
for testing USB mass storage class implementation.

.. zephyr-app-commands::
   :app: zephyr/samples/subsys/usb/mass
   :build-dir: usb_mass-tiac_magpie
   :board: tiac_magpie
   :goals: build flash
   :host-os: unix

The output to the console will look something like this:

.. code-block:: none

   [00:00:00.003,000] <inf> main: No file system selected
   [00:00:00.059,000] <inf> main: The device is put in USB mass storage mode.

FAT FS Example
==============

If more than 96KiB are available, FAT files system can be used with a RAM-disk.
Alternatively it is possible with the FLASH-based disk. In this example we will
build the sample with a RAM-based disk:

.. zephyr-app-commands::
   :app: zephyr/samples/subsys/usb/mass
   :build-dir: usb_mass_fat-tiac_magpie
   :board: tiac_magpie
   :gen-args: -DCONFIG_APP_MSC_STORAGE_RAM=y
   :goals: build flash
   :host-os: unix

After you have built and flashed the sample application image to your board,
plug the board into a host device, for example, a PC running Linux. The board
will be detected as shown by the Linux journalctl command:

.. code-block:: console

   $ journalctl -k -n 17
   usb 1-6.3: new full-speed USB device number 16 using xhci_hcd
   usb 1-6.3: New USB device found, idVendor=2fe3, idProduct=0008, bcdDevice= 3.00
   usb 1-6.3: New USB device strings: Mfr=1, Product=2, SerialNumber=3
   usb 1-6.3: Product: Zephyr MSC sample
   usb 1-6.3: Manufacturer: ZEPHYR
   usb 1-6.3: SerialNumber: 3635393731375118
   usb-storage 1-6.3:1.0: USB Mass Storage device detected
   scsi host7: usb-storage 1-6.3:1.0
   scsi 7:0:0:0: Direct-Access     ZEPHYR   ZEPHYR USB DISK  0.01 PQ: 0 ANSI: 0 CCS
   sd 7:0:0:0: Attached scsi generic sg5 type 0
   sd 7:0:0:0: [sdz] 192 512-byte logical blocks: (98.3 kB/96.0 KiB)
   sd 7:0:0:0: [sdz] Write Protect is off
   sd 7:0:0:0: [sdz] Mode Sense: 03 00 00 00
   sd 7:0:0:0: [sdz] No Caching mode page found
   sd 7:0:0:0: [sdz] Assuming drive cache: write through
    sdz:
   sd 7:0:0:0: [sdz] Attached SCSI removable disk

The output to the console will look something like this
(file system contents will be different):

.. code-block:: none

   Mount /RAM:: 0
   /RAM:: bsize = 512 ; frsize = 512 ; blocks = 158 ; bfree = 158
   /RAM: opendir: 0
   End of files
   [00:00:00.115,000] <inf> main: The device is put in USB mass storage mode.

On most operating systems the drive will be automatically mounted.

.. code-block:: console

   $ df -hlT -t vfat | tail -n1
   /dev/sdz   vfat   79K     0   79K   0% /media/user/4821-0000
