.. _magpie_f777ni_usb_mass-sample:

USB Mass Storage
################

Overview
********

See :zephyr:code-sample:`usb-mass` for the original description.

.. _magpie_f777ni_usb_mass-sample-requirements:

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
      :build-dir: usb_mass-magpie_f777ni
      :board: magpie_f777ni
      :gen-args: -DEXTRA_DTC_OVERLAY_FILE="ramdisk.overlay"
      :west-args: -p
      :goals: flash
      :host-os: unix

Sample Output
-------------

The output to the console will look something like this:

   .. container:: highlight highlight-console notranslate no-copybutton

      .. parsed-literal::

         \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* \*\*\*
         [00:00:00.000,000] <inf> main: No file system selected
         [00:00:00.010,000] <inf> main: The device is put in **USB mass storage mode**
         [00:00:00.342,000] :byl:`<wrn> udc: Spurious resume event`
         [00:00:00.441,000] <inf> usbd_msc: Enable
         [00:00:00.441,000] <inf> usbd_msc: Bulk-Only Mass Storage Reset
         [00:00:03.587,000] :brd:`<err> usbd_msc: Unknown SCSI opcode 0xc5`
         [00:00:03.592,000] :brd:`<err> usbd_msc: Unknown SCSI opcode 0xc5`
         [00:00:03.596,000] :brd:`<err> usbd_msc: Unknown SCSI opcode 0xc5`
         [00:00:03.601,000] :brd:`<err> usbd_msc: Unknown SCSI opcode 0xc5`

FAT FS Example
==============

If more than 96KiB are available, FAT files system can be used with a RAM-disk.
Alternatively it is possible with the FLASH-based disk. In this example we will
build the sample with a RAM-based disk:

   .. zephyr-app-commands::
      :app: zephyr/samples/subsys/usb/mass
      :build-dir: usb_mass_fat-magpie_f777ni
      :board: magpie_f777ni
      :gen-args: -DEXTRA_DTC_OVERLAY_FILE="ramdisk.overlay" -DCONFIG_APP_MSC_STORAGE_RAM=y
      :west-args: -p
      :goals: flash
      :host-os: unix

Sample Output
-------------

After you have built and flashed the sample application image to your board,
plug the board into a host device, for example, a PC running Linux. The board
will be detected as shown by the Linux journalctl command:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         :bgn:`$` **journalctl -k -n 17**
         usb 1-6.3: new full-speed USB device number 19 using xhci_hcd
         usb 1-6.3: New USB device found, idVendor=\ |zephyr_VID|, idProduct=\ |zephyr_PID_MSC|, bcdDevice=\ |zephyr_BCD_MSC|
         usb 1-6.3: New USB device strings: Mfr=1, Product=2, SerialNumber=3
         usb 1-6.3: Product: |zephyr_PStr_MSC_usbd|
         usb 1-6.3: Manufacturer: |zephyr_VStr_usbd|
         usb 1-6.3: SerialNumber: 9E6B44AEA1E2B8980C4D32A6
         usb-storage 1-6.3:1.0: USB Mass Storage device detected
         scsi host7: usb-storage 1-6.3:1.0
         :b:`scsi 7:0:0:0: Direct-Access     Zephyr   RAMDisk          0.00 PQ: 0 ANSI: 4`
         :b:`sd 7:0:0:0: Attached scsi generic sg5 type 0`
         :b:`sd 7:0:0:0: [sdz] 192 512-byte logical blocks: (98.3 kB/96.0 KiB)`
         :b:`sd 7:0:0:0: [sdz] Write Protect is off`
         sd 7:0:0:0: [sdz] Mode Sense: 03 00 00 00
         :brd:`sd 7:0:0:0: [sdz] No Caching mode page found`
         :brd:`sd 7:0:0:0: [sdz] Assuming drive cache: write through`
          sdz:
         :b:`sd 7:0:0:0: [sdz] Attached SCSI removable disk`

The output to the console will look something like this
(file system contents will be different):

   .. container:: highlight highlight-console notranslate no-copybutton

      .. parsed-literal::

         \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* \*\*\*
         Mount /RAM:: 0
         /RAM:: bsize = 512 ; frsize = 512 ; blocks = 158 ; bfree = 158
         /RAM: opendir: 0
         End of files
         [00:00:00.061,000] <inf> main: The device is put in **USB mass storage mode**
         [00:00:00.404,000] :byl:`<wrn> udc: Spurious resume event`
         [00:00:00.502,000] <inf> usbd_msc: Enable
         [00:00:00.502,000] <inf> usbd_msc: Bulk-Only Mass Storage Reset
         [00:00:03.562,000] :brd:`<err> usbd_msc: Unknown SCSI opcode 0xc5`
         [00:00:03.566,000] :brd:`<err> usbd_msc: Unknown SCSI opcode 0xc5`
         [00:00:03.569,000] :brd:`<err> usbd_msc: Unknown SCSI opcode 0xc5`
         [00:00:03.572,000] :brd:`<err> usbd_msc: Unknown SCSI opcode 0xc5`

On most operating systems the drive will be automatically mounted.

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         :bgn:`$` **df -hlT -t vfat** | **tail -n1**
         /dev/sdz   vfat   79K     0   79K   0% /media/user/5A21-00C0
