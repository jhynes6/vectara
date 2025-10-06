---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/sudo/"
title: "Different flavors of Elevated Privileges"
domain: "www.byteworks.com"
path: "/resources/blog/sudo/"
scraped_time: "2025-10-05T02:01:50.812228"
url_depth: 3
word_count: 584
client_name: "byteworks"
---

# Different flavors of Elevated Privileges

Unix and Linux administrators have long been used to the concept of Elevated privileges, however the same concept doesn’t quite exist in the Windows Environment. The concept is simple: It is considered best practice that a user (even an administrator) of a computer system should use a user account that does not possess administrative privileges when logging into the machine. Instead, each task that requires administrative privileges should be authenticated and authorized at the time of the task.

To allow for these operations, each type of operating system has a built in command that can be executed from the command shell (command prompt or terminal). When these types of operations are attempted in a Windows environment, there is a GUI equivalent of each of these commands that prompt the user to authenticate properly, however the concept behind them is the same, so this write-up will focus on the terminal/shell versions.

## SUDO

To the Linux/Unix user, this concept is called **sudo** (pronounced “sou-due”). In the sudo model, each user account that requires the ability to run **su** (or super-user) commands has its’ username added to a list, called a “sudoers” file. When that user requests to run a su command, the system verifies whether their username is in this list, and if so, prompts them for their password. Once their password is authenticated, the task requested is executed with the privilege level of root (built-in administrator account).

```bash
sudo <command>
```

By default, sudo runs commands as the root user, but commands can be run as a specific user via command line options. This allows the user to execute commands as the other user without needing that target user’s password.

```bash
sudo -u <user> <command>
```

One advantage to the sudo command is that, once properly authenticated, it sets a timer for the current user, so that the user does not need to be prompted again for a period of time for additional sudo commands.

There are several other command line options available for sudo. Since Linux comes in many flavors, there are some variations, but the following article details some of the basic options available:

*   [https://gratisoft.us/](https://gratisoft.us/ "https://www.gratisoft.us/sudo/sudo.man.html")

## RUNAS

In contrast, there is a similar command for recent versions of Windows. The **runas** command is also used to execute tasks that require administrative privilege, however the execution of this command differs slightly. The runas command does not have a default administrative context like sudo does; the user must specify which user account the task is to be executed under. Because of this, the command takes more options than sudo in order to perform the task.

```bash
runas /user:<user> <command>
```

Another difference is that the runas command is available to all users in a Windows system, there is no list such as the “sudoers” file that a user needs to be listed in. Because of this, when running a program as another user (such as the local administrator account), the user must enter the password of that target user instead of their own. This is a major difference between runas and sudo.

Windows systems in the workplace are often members of a domain or Active Directory environment. The runas command is able to authenticate against both types of accounts.

```bash
runas /user:<localuser> <command>  
…  
runas /user:<domainuser@domain.com> <command>  
…  
runas /user:<domainname\domainuser> <command>
```

There are several other command line options for the runas command. Please check the following article from Microsoft for more information:

*   [https://technet.microsoft.com/en-us/library/cc771525.aspx](https://technet.microsoft.com/en-us/library/cc771525.aspx "https://technet.microsoft.com/en-us/library/cc771525.aspx")