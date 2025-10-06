---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/fixing-windows-services-that-are-hung-at-starting-or-stopping/"
title: "Fixing Windows Services that are Hung at Starting or Stopping"
domain: "www.byteworks.com"
path: "/resources/blog/fixing-windows-services-that-are-hung-at-starting-or-stopping/"
scraped_time: "2025-10-05T02:02:15.024978"
url_depth: 3
word_count: 258
client_name: "byteworks"
---

# Fixing Windows Services that are Hung at Starting or Stopping

Maintenance on Windows Devices sometimes requires the manual stopping/restarting of Services.  Sometimes these services play nice, and sometimes they do not.  Aside from restarting the system, there are some built-in commands that will allow you to stop and/or restart individual services.

First, locate the service that you are attempting to fix, and remember it’s Display Name (the name listed in the Service Management Snap-in, see above for an example).  Once you have the display name, open a Command Prompt Window (run as Administrator) and enter the following command:

```
sc queryex “<service_display_name>”
```

You should see an output similar to the following.  Take note the Process ID (PID) in this output (shown below in bold)

```
Microsoft Windows [Version 6.1.7601] Copyright (c) 2009 Microsoft Corporation. All rights reserved.C:\Users\Administrator>sc queryex “Windows Agent Service”  
SERVICE_NAME: Windows Agent Service  
TYPE : 10 WIN32_OWN_PROCESS  
STATE : 4 STOPPING  
(STOPPABLE, NOT_PAUSABLE, ACCEPTS_SHUTDOWN)  
WIN32_EXIT_CODE : 0 (0x0)  
SERVICE_EXIT_CODE : 0 (0x0)  
CHECKPOINT : 0x0  
WAIT_HINT : 0x0  
**PID : 4584**  
FLAGS :C:\Users\Administrator>
```

Now that you have the PID for the hung service, you can enter the following command to force it to terminate:

```
taskkill /f /pid <PID>
```

You can re-enter the “sc queryex” command to verify it is stopped, or refresh your view in the Services Management Snap-in in order to verify the service has actually stopped.  To restart the service, you can enter the following command, or start the service from the Snap-in.

```
sc queryex start “<service_display_name>”
```