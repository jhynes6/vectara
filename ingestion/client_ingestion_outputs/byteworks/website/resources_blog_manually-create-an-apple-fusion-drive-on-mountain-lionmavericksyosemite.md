---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/manually-create-an-apple-fusion-drive-on-mountain-lionmavericksyosemite/"
title: "Manually Create an Apple Fusion Drive on Mountain Lion/Mavericks/Yosemite"
domain: "www.byteworks.com"
path: "/resources/blog/manually-create-an-apple-fusion-drive-on-mountain-lionmavericksyosemite/"
scraped_time: "2025-10-05T02:02:45.432835"
url_depth: 3
word_count: 984
client_name: "byteworks"
---

# Manually Create an Apple Fusion Drive on Mountain Lion/Mavericks/Yosemite

**UPDATE 12/26/14: As of 10.10.1 and above this process will not work. The workaround is to boot to a USB boot disk that has Mavericks on it and run the commands from there. If you try to use 10.10.1 and above, you will see a very generic error when trying to create a logical group with 2 or more drives.**

Apple has created their own form of a hybrid storage that works surprisingly well, its called the fusion drive. This can be done with non-retina macbook pro’s, Mac-Mini’s, old and new Mac Pro’s, and of course the iMac (where its officially supported).

To build the logical drive you need to be booted up in recovery or a startup disk that is either Mountain Lion (latest), Mavericks, or Yosemite. When inside of the startup you will start a terminal session to setup the drive. After that you are free to install the OS just like you would any other time. Its important though before performing this upgrade, you will need to do a complete backup because this process will ERASE ALL DATA on these drives. Use things like Time Machine or Super Duper in order to get your data off your device. Again, this process requires 10.8.2 or later to perform. Recovery mode is your best bet (Command + R upon boot).

Gather your drives, its important that one should be a platter drive, preferably a 7200rpm drive high performance drive and the other be a standard Solid State Drive. Device Sizes can vary on how you see fit but here are a few examples. Apple uses a 128GB Flash Storage and a 3TB Platter Drive to get a combined storage of around 3.1T. I have personally setup a 1T Platter with 512SSD and it works well. It all depends on what your budget will tolerate, but the way the Fusion drive works, it simply keeps all the “hot” blocks of data that are accessed frequently and keeps them on the SSD while keeping the “cold” blocks on the slower storage. This is evaluated frequently and happens behind the scenes which makes a very positive user experience. Keep in mind that Apple chooses the drives they select based off their own R&D and make it a point to let the world know that creating your own Fusion drive is not supported by Apple. So proceed at your own risk.

First things first, boot to [recovery mode](https://support.apple.com/kb/ht4718 "Recovery Mode"): Command-R when you first boot up and see the monotone Apple logo

Typically, the Disk Utility application (Application > Utilities > Disk Utility) would be enough to get partitions setup, but since Apple doesn’t support the management or creation of Fusion Drives in its graphical interface. Knowing Apple, it might not ever support it. To create the Fusion Drive, we’ll use Disk Utility, but the command line version that comes with every Mac. (Learn more about the Disk Utility command line.) You will need to open a terminal window manually within OSX recovery to get started. To get started, start terminal (Utilities->Terminal)

Once you have the Terminal open, you’re ready to get to creating the Fusion Drive.

List the drives you system can see. Use the following command to list the drives attached to your system:

```
diskutil list
```

This will list the drives like this:

The drive mount points are labeled /dev/disk#. Make a note of the mount points for the disks you want to make into a Fusion Drive. In the example, /dev/disk0 is the boot disk, while /dev/disk1 and /dev/disk2 are the SSD and hard drive (respectively) that you want to put together as a Fusion Drive. An easy way to tell drives apart is by their size and their name. Make sure you don’t confuse them, as the Terminal doesn’t give much warning before wiping your drive.

Next, create a CoreStorage logical volume group. The pool of data that will be made from the combined space of our physical drives. Use the following format of the diskutil command:

```
diskutil coreStorage create nameYourThing drive1 drive2
```

Going off the example using /dev/disk1 and /dev/disk2 as the drives to combine, type:

```
diskutil coreStorage create myLogicalVolGroup /dev/disk1 /dev/disk2
```

When the process is done, the logical volume group should be completed and the command will finish by presenting you with a unique identifier for the group, which you should copy to your clipboard. It should look similar to this:

The **UUID** is the unique identifier you want to copy.

Next, a logical volume. Now that we have a logical volume group, we can create the logical volume. This is what your Mac will recognize as a single, logical drive. Use the following format of the diskutil command:

```
diskutil coreStorage createVolume UUID type name size
```

**UUID:** This is the unique identifier that was copied from the previous step.  
**Type:** jhfs+ is Journaled HFS+ (Most common file system used by MacOS)  
**Name:** This can be whatever you would like it to be, typically is “Macintosh HD” but you can say “Fusion Drive” if you prefer.  
**Size:** This is how much of the “pool” that you want to make into a drive, using the following **Suffixes:** B(ytes), S(512-byte-blocks), K(ilobytes), M(egabytes), G(igabytes), T(erabytes), P(etabytes), or (%) a percentage of the current size of the logical volume group.

Using the previous example, the command would look like this:

```
diskutil coreStorage createVolume 50B457C3-ADC6-4EDC-9ABA-FD8C6EEDE69A jhfs+ "Macintosh HD" 100%
```

This finishes out the required steps to creating the fusion drive. Once this is complete you can exit out of Terminal and go back to OSX Setup and from there the Fusion Drive should be detected and selectable as a drive to install OSX on.

The final steps after OSX is installed would be to restore off of a TimeMachine backup and you are ready to go!. Enjoy.