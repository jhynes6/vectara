---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/understanding-osx-permissions/"
title: "/resources/blog/understanding-osx-permissions/"
domain: "www.byteworks.com"
path: "/resources/blog/understanding-osx-permissions/"
scraped_time: "2025-10-05T02:02:36.192950"
url_depth: 3
word_count: 1941
client_name: "byteworks"
---

Understanding OSX Permissions | Byteworks | IT Solutions, Services, and Consulting

[![](data:image/svg+xml;nitro-empty-id=MTAyODo0NTg=-1;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjQ1IDE3NiIgd2lkdGg9IjI0NSIgaGVpZ2h0PSIxNzYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PC9zdmc+)](/)

[

](#)

*   [Markets](https://www.byteworks.com/markets/)
*   [IT Solutions](https://www.byteworks.com/solutions/)
*   [Security](https://www.byteworks.com/solutions/security/)
*   [Infrastructure](https://www.byteworks.com/solutions/infrastructure/)
*   [Collaboration](https://www.byteworks.com/solutions/collaboration/)
*   [Cloud](https://www.byteworks.com/solutions/cloud/)
*   [Services](https://www.byteworks.com/services/)
*   [Managed Services](https://www.byteworks.com/services/managed-services/)
*   [Lifecycle Management](https://www.byteworks.com/services/lifecycle-management/)
*   [Technology Consulting](https://www.byteworks.com/technology-consulting/)
*   Resources
*   [Bits and Bytes by Byteworks](https://www.byteworks.com/bits-and-bytes-podcast/)
*   [Blog](https://www.byteworks.com/resources/blog/)
*   [Case Studies](https://www.byteworks.com/resources/case-studies/)
*   [eBooks](https://www.byteworks.com/resources/ebooks/)
*   [Events](https://www.byteworks.com/resources/events/)
*   [Cisco Technology Experience Portal](https://www.byteworks.com/cisco-technology-experience-portal/)
*   [About Us](https://www.byteworks.com/about-us/)
*   [Contact](https://www.byteworks.com/contact/)
*   [Remote Support](https://byteworks.screenconnect.com)
*   [Client Login](https://byteworks.myportallogin.com)

# Understanding OSX Permissions

[aharned](https://www.byteworks.com/resources/blog/author/aharned/)

May 6, 2014

The Macintosh OSX platform is based on Unix, and thus, the POSIX permissions model. With OSX, you can augment these permissions with Access Control Lists (ACLs), which allow for more granularity (very similar to Windows-based permissions), however troubleshooting them can sometimes be a pain.

## POSIX Permissions

Unix/Linux systems utilize a relatively basic structure for permissions. Each object, be it a file or folder, has 9 bits of metadata used in determining who or what has the ability to access it. This field is broken into three 3-bit sections; the first determines the permissions for the owner of the object, the second determines permissions for the group the object belongs to, and the third and final byte determines permissions for any user or service that does not fall into either of the two categories (some terms for this are “everyone”, “world”, or “other”).
`    **section :** owner | group | other   **type    :**  000  |  000  |  000    `

Each 3-bit section has a specific value for each individual bit. As in all binary, if that bit is a 1, access for that permission type is turned on; if it is a zero, the permission type is turned off. These three types of access are read (R), write (W), and execute (X). Read and write are fairly self-explanatory, and execute is used in different ways depending on the type of object. Files that need to run as scripts or applications require the execute permission, whereas directories require execute permissions in order to change directory into them or view their contents. These bits have a decimal value (see below).
`    **type    :** R | W | X   **value   :** 4 | 2 | 1    `

The decimal value of the permission section is calculated by adding the decimal value of each permission type. For example, read-only is a value of 4, where read-write is a value of 4+2 or 6.

Let’s say you want to set a file so that the file’s owner has full control, the file’s group can read and write to the file, but not execute it, and the “world” could only read, you would set the binary digits to match. By adding the values of each binary digit, you get the decimal value (which ranges from 0-7) for each section. In this case, the effective permissions end up as 764.
`    **section :** owner | group | other   **type    :** R W X | R W X | R W X   **binary  :** 1 1 1   1 1 0   1 0 0   **decimal :**   7       6       4    `

When you look at files in OSX via the terminal shell, you will be able to see the full POSIX permissions of the item that uses the permission type’s letter as a signifier of the value 1 (see below). If you are using the Finder’s “Get Info” window, or the OSX Server app, you will get a slightly simplified view (the GUI Apps do not display the “Execute” permission type; you can select from Read & Write, Read-only, and None).

JohnSmith@macserver:~$ ls -l
total 32
**drwxr-xr-x**   7 **JohnSmith staff**  238 Apr 10 09:36 Applications
**drwx-–-–-–+** 17 **JohnSmith staff**  578 Apr 15 17:27 Desktop
**drwx-–-–-–+** 25 **JohnSmith staff**  850 Apr 10 15:50 Documents
**drwxrwxrwx**  48 **JohnSmith staff** 1632 Apr 15 16:07 Downloads
**\-rwxr–-r-–@** 62 **JohnSmith staff** 4218 Apr 24 14:21 KittenPicture.jpeg
**\-rwx-–-–-–**  55 **JohnSmith staff** 2108 Apr 30 09:19 SuperSecretPassword.txt
…

You’ll notice some special characters in a few of these entries. In the first slot on all but the last object, there is the letter D, which means the object is a directory, not a file (see below for a more detailed explanation).

In the last slot, there are a few objects with a **+** sign, and one with an **@** sign. The + sign denotes that an ACL is also applied to this object, and the @ sign signifies that the object has extended attributes enabled (more on these later).

Another important note is that each one of these objects is owned by a user named JohnSmith, and the object itself is delegated to the “staff” group, which means that any users that are also in this group have the group’s effective permissions calculated in. On a quick note, the “staff” group in OSX is akin to the “All Users” group in Windows.

## POSIX Access Control Lists

As you may have noticed, the standard POSIX permission base isn’t very granular. You can either set owner, group, or world permissions, but that’s it. Granted, a user can belong to multiple groups, but what if you want two different groups to have two different effective permissions? That’s where Access Control Lists (ACLs) come into play. A POSIX ACL can either apply to the standard permissions (owner/group/world), or add entries, such as additional specific usernames, additional groups, and even a wildcard mask for user/group names.

The format for an ACL entry on an object is **<type>:\[<name>\]:<permission>**. The field is used to specify a specific user/group; if omitted, symbolizes the owner and default group from the standard POSIX permission base. A sample ACL-to-POSIX mapping table is listed below:

Access List Type

POSIX Permission Type

Format

Owner

Owner

`user::rwx`

Specific User

–

`user:johnsmith:rwx`

Default Group

Group

`group::rwx`

Additional Group

–

`group:employees:rwx`

Default Mask

–

`mask::rwx`

Other Users

Other

`other::rwx`

While the majority of these are self-explanatory, the addition of the “Default Mask” option may take some explaining. Basically, the value of the default mask is equal to the maximum value of effective permissions for specifically named items in the ACL. For example, if the ACL has an entry for user JohnSmith with configured permissions of `RWX`, and the default mask is set with `RW-`., then JohnSmith’s effective permissions are `RW-`. It is of note that this entry simply represents the maximum-allowed permission value for a specifically named user/group, it does not necessarily mean that level will be applied. Using the same example, if JohnSmith’s permissions are configured as `R--`, and the mask is at `RW-`, JohnSmith’s effective permissions are still `R--` because they did not exceed the mask value.

## Viewing and Setting Permissions

You can view the basic POSIX permissions on an object by performing an extended list of objects within a folder. To the left-hand side of each row is an 11-character code that includes an object type character, the aforementioned 9-character permission string, and a special character to denote certain flags on the object.

`    **section :** type | owner | group | other | special   **type    :**    T | R W X | R W X | R W X | S    `

The first character denotes the type of object for that row, and is symbolized by a single letter.

Character

Name

Description

–

File

Permissions applying to the file itself

d

Directory

Default permissions for the directory/folder

c

Character

Character special file

The last character denotes any special flags that are applied to the object.

Character

Name

Description

<blank>

None

No special flags are active for this object.

+

ACL

An Access Control List is applied to this object.

@

SELinux

A Special SELinux context is present.

Since there is an ACL entry for each corresponding POSIX permission type (owner, group, other), whenever the POSIX permissions of an item are changed (either via Finder, or the **chmod** command), the corresponding ACL entry is also changed. To view or modify the remaining ACL entries of a particular object, you can use the following commands.

JohnSmith@macserver:~$ ls -le
total 32
drwxr-xr-x   7 JohnSmith staff  238 Apr 10 09:36 Applications
drwx-–-–-–+ 17 JohnSmith staff  578 Apr 15 17:27 Desktop
0: group:everyone deny delete
drwx-–-–-–+ 25 JohnSmith staff  850 Apr 10 15:50 Documents
0: user:JohnSmith allow write
drwxrwxrwx  48 JohnSmith staff 1632 Apr 15 16:07 Downloads
\-rwxr–-r-–@ 62 JohnSmith staff 4218 Apr 24 14:21 KittenPicture.jpeg
\-rwx-–-–-–  62 JohnSmith staff 2108 Apr 30 09:19 SuperSecretPassword.txt
…JohnSmith@macserver:~$ chmod +a ‘FrankCustomer allow read,write,delete’ SuperSecretPassword.txt

JohnSmith@macserver:~$ ls -le
total 32
drwxr-xr-x   7 JohnSmith staff  238 Apr 10 09:36 Applications
drwx-–-–-–+ 17 JohnSmith staff  578 Apr 15 17:27 Desktop
0: group:everyone deny delete
drwx-–-–-–+ 25 JohnSmith staff  850 Apr 10 15:50 Documents
0: user:JohnSmith allow write
drwxrwxrwx  48 JohnSmith staff 1632 Apr 15 16:07 Downloads
\-rwxr–-r-–@ 62 JohnSmith staff 4218 Apr 24 14:21 KittenPicture.jpeg
\-rwx-–-–-–+ 62 JohnSmith staff 2108 Apr 30 09:19 SuperSecretPassword.txt
0: user: FrankCustomer allow read,write,delete
…

You can also add or edit permissions via the “Get Info” window for the object in the Finder App (see below).

## Determining Effective Permissions

When a user attempts to access a resource in a POSIX environment, the system must determine what the user’s effective permissions are in order to assess whether the user has access, and if so, what level of access to allow. In order to determine this, the system goes through the following process. If a line-item in this process is matched, then the process is complete. If not, then the next line-item is checked.

*   If the user is listed as the owner, apply the owner permissions.
*   If the user matches a specified user in an ACL entry, apply that specific user’s permissions.
*   If the user is a member of the owning group of the item, and the owning group allows for the requested permissions, apply the owning group permissions.
*   If the user is a member of a specified group in an ACL entry, and that entry contains the requested permissions, apply the specific group permissions.
*   If the user is a member of any group specified in the ACL, or a member of the owning group, and none of these groups allow for the requested permissions, deny the user access.
*   Apply the “other” permissions.

## Removable Storage Permissions

When a Removable Storage device, such as a USB Flashdrive, is formatted with the Macintosh File System, it can be configured with the same type of POSIX and ACL permissions as a fixed drive. This may present problems, however, if the volume is removed and mounted on a different system, which may not have the same users and groups. This would default to every user account matching the “other” section of the permissions for every object.

To counteract this, there is an option for removable media called “Ignore ownership on this volume”. This sets a volume-specific flag that tells the system that mounts the drive to match all users to the owner permissions, no matter what the permissions are set to, which usually means that any and every user would have ownership of all objects. This flag is turned on by default for removable media, but can be disabled via the “Get Info” window of the volume in the Finder.

It is of note that values for owner and group are still updated on newly-created files, they are simply ignored when checking access permissions.

[

Previous Post

The Best New Features of Cisco’s Unified Collaboration 10.X

](https://www.byteworks.com/resources/blog/bestofuc10x/ "The Best New Features of Cisco’s Unified Collaboration 10.X")[

Next Post

Install NVIDIA Drivers and CUDA Toolkit on Kali 1.0.6

](https://www.byteworks.com/resources/blog/install-nvidia-drivers-and-cuda-toolkit-on-kali-1-0-6/ "Install NVIDIA Drivers and CUDA Toolkit on Kali 1.0.6")

#### QUICK LINKS

[Case Studies](https://www.byteworks.com/resources/case-studies/)
[Privacy Policy](https://www.byteworks.com/privacy-policy/)

[](https://www.linkedin.com/company/byte-works-llc)

[](https://www.youtube.com/channel/UC0sglo13jgTeJvsoXqpyGCA)

[![](data:image/svg+xml;nitro-empty-id=MTIyNDoxODE3-1;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjQ1IDE3NiIgd2lkdGg9IjI0NSIgaGVpZ2h0PSIxNzYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PC9zdmc+)](https://www.byteworks.com/)

#### ADDRESS

[2675 Breckinri