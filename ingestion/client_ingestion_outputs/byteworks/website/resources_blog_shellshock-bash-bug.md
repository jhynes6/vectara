---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/shellshock-bash-bug/"
title: "Shellshock Bash Bug"
domain: "www.byteworks.com"
path: "/resources/blog/shellshock-bash-bug/"
scraped_time: "2025-10-05T02:00:34.675946"
url_depth: 3
word_count: 794
client_name: "byteworks"
---

# Shellshock Bash Bug

If you haven’t heard, a recent security flaw known as the Bash Bug has been discovered, and threatens to compromise quite a few internet-connected systems.  This vulnerability is relatively wide-spread and can affect devices from major web servers to small-scale connected devices such as cameras or sensors.

What’s worse?  That this is not a new vulnerability, just a newly-discovered one; According to sources, this flaw has existed for over 25 years.  Due to the sheer amount of -nix systems, including Apple’s OSX Operating System, that utilize some version of the Bash shell, this vulnerability is highly-regarded as one of the biggest security vulnerabilities in history.

## What exactly is a “Bash”?

For those that aren’t familiar, Bash (Bourne Again Shell) is one of the most popular shell systems for Unix- and Linux-based systems.  For those unfamiliar with -nix operating systems, it is somewhat similar to the Windows Command Processor (CMD.exe) in look and feel, however it is much more a central part of the operating system than CMD is for Windows.

As the Linux operating system can have a very small footprint, it tends to be the primary choice to use on smaller network-capable devices.  Because of this, the sheer number of potentially infected systems just skyrockets.

## How do I know if my system is vulnerable?

There are several ways to test vulnerability, as well as a few tools that some good samaritans have created.  Since these methods technically attempt to exploit a vulnerability, it is highly recommended to leave them to a professional, and if possible, to not perform on live customer-facing equipment.

It should also go without saying that you should **NOT** attempt these tests on equipment you do not own or have rightful access to administer.

### Option 1: Shell Access

The first two involve gaining access to the device’s shell and attempting to execute some “test” code, so these may or may not be viable choices depending on the type of device, security access, or comfort level.

If you are unable to access the device’s shell, or have any reluctance in executing shell commands, and the devices you are attempting to test are connected to the public internet, you may skip to the next section.

**Test 1**

To begin, connect to your device and open a Bash shell prompt, and type the following line and press \[ENTER\] or \[RETURN\].

John@mysystem:~$ **env x='() { :;}; echo vulnerable’ bash -c “echo this is a test”**

If your terminal prints the word “vulnerable”, then your version of bash is, well, vulnerable to this exploit.

```bash
John@mysystem:~$ env x='() { :;}; echo vulnerable’ bash -c “echo this is a test”
vulnerable
this is a test
JohnSmith@mysystem:~$
```

If you only see “this is a test” in the output, please proceed to the next step.

```bash
John@mysystem:~$ env x='() { :;}; echo vulnerable’ bash -c “echo this is a test”
this is a test
JohnSmith@mysystem:~$
```

**Test 2**

The next test checks a second portion of the vulnerability. At the bash prompt, type the following line and press \[ENTER\] or \[RETURN\].

```bash
John@mysystem:~$ env X='(){(a)=>\’ bash -c “echo date”; cat echo; rm -f echo
```

After the line that says “date”, you will either see the current date and time printed, or you will receive an error.

```bash
John@mysystem:~$ env X='(){(a)=>\’ bash -c “echo date”; cat echo; rm -f echo
date
cat: echo: No such file or directory
```

If you see the current date and time, your system is vulnerable.

```bash
John@mysystem:~$ env X='(){(a)=>\’ bash -c “echo date”; cat echo; rm -f echo
date
**[..the current date and time..]**
```

### Option 2: Public Internet Tools

The last two are web-based tools that work on web-based vulnerabilities. Since these tools are on the public internet themselves, they are only able to scan systems that are accessible from the internet themselves, such as web servers.

Before proceeding with either of these tools, please read all warnings associated with them. These sites are not owned nor operated by Byteworks, and Byteworks takes no responsibility for these sites or the actions they perform:

*   https://www.shellshocktest.com
*   https://shellshock.brandonpotter.com

## My system is vulnerable, what now?

If you fail any of the above tests, then it’s time to check the manufacturer of your -nix variant for any official patches. If your version of -nix doesn’t offer an official patch, then you may still have the option of compiling a patched version yourself.

Recently, Apple released a fix for OSX Mavericks

*   [https://support.apple.com/kb/HT6495](https://support.apple.com/kb/HT6495) For some instructions on downloading and compiling a patched version of Bash, check out the following link. It was written to address OSX Mavericks (prior to the official update), however it can apply to other variants of -nix as well.
*   [https://mac-how-to.wonderhowto.com/how-to/every-mac-is-vulnerable-shellshock-bash-exploit-heres-patch-os-x-0157606/](https://mac-how-to.wonderhowto.com/how-to/every-mac-is-vulnerable-shellshock-bash-exploit-heres-patch-os-x-0157606/)