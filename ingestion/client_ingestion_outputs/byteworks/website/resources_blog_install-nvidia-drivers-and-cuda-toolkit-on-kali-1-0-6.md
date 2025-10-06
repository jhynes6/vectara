---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/install-nvidia-drivers-and-cuda-toolkit-on-kali-1-0-6/"
title: "Install NVIDIA Drivers and CUDA Toolkit on Kali 1.0.6"
domain: "www.byteworks.com"
path: "/resources/blog/install-nvidia-drivers-and-cuda-toolkit-on-kali-1-0-6/"
scraped_time: "2025-10-05T02:03:36.554106"
url_depth: 3
word_count: 685
client_name: "byteworks"
---

# Install NVIDIA Drivers and CUDA Toolkit on Kali 1.0.6

The default Kali installation can be augmented with the ability to use its Graphics Processing Unit (GPU) to boost the performance of specific tools. Kali utilizes the open source nouveau driver to support graphics cards that does not support the usage of GPU based applications. So the first step is to install the NVIDIA Accelerated Linux Graphics Driver and then the CUDA toolkit. Once CUDA is installed the GPU based applications will then be able to utilize the GPU to perform tasks which will increase the effectiveness of the tools. This article will walk through the steps to install the NVIDIA graphics driver and CUDA toolkit 6. Once they are installed pyrit will be used to verify installation and check performance.

**First Step:** Update Kali  
Update the repositories to be able to access all sources during an update. Open /etc/apt/sources.list with either vi or nano and verify/update the following:  

Once all the repositories are configured, then run an update:

```
# apt-get update && apt-get upgrade -y && apt-get dist-upgrade -y
```

**Second Step:** Install Linux Headers  
The following command installs the Linux Headers which is required to build the NVIDIA kernel module:

```
# apt-get install linux-headers-$(uname -r)
```

At this point we are ready to start the actual install of the NVIDIA Accelerated Linux Drivers.

**Third Step:** Install NVIDIA Dynamic Kernel Module Support

```
# apt-get install nvidia-kernel-dkms
```

**Fourth Step:** Install NVIDIA XConfig  
Installs a utility called nvidia-xconfig, which is designed to make editing the X configuration file

```
# apt-get install nvidia-xconfig
```

**Fifth Step:** Run the NVIDIA XConfig Utility  
nvidia-xconfig will find the X configuration file and modify it to use the NVIDIA X driver instead of the nouveau driver

```
# nvidia-xconfig
```

**Sixth Step:** Reboot Kali  
If during the boot up process a blank screen with a blinking cursor then do the following:

Hit Atl-Ctrl-F1 and login  
```
# rm /etc/X11/xorg.conf  
# nvidia-xconfig  
Reboot the system
```

**Seventh Step:** Verify that NVIDIA Driver Installed correctly  
Checking the glxinfo to see if direct rendering is set to “Yes”

```
# glxinfo | grep -i “direct rendering
```

**Eighth Step:** Install NVIDIA CUDA 6 Toolkit

```
# apt-get install nvidia-cuda-toolkit
```

**Ninth Step:** Install NVIDIA OpenCL

```
# apt-get install nvidia-opencl-icd
```

At this point NVIDIA drivers are installed and ready to be tested. Pyrit will be the GPU application that we will utilize to verify our installation.

**Installation of Pyrit**  
Kali comes with an older version of pyrit which we will uninstall:

```
# apt-get remove pyrit
```

Once it has been removed there are dependencies that need to be installed:

```
# apt-get install python2.7-dev python2.7-libpcap libpcap-dev
```

Download the latest pyrit, cpyrit-cuda, and cpyrit-opencl at [https://code.google.com/p/pyrit/downloads/list](https://code.google.com/p/pyrit/downloads/list "Pyrit Download")

Extract the files into the /home directory:

```
# tar xvzf pyrit-0.4.0.tar.gz  
# tar xvzf cpyrit-cuda-0.4.0.tar.gz  
# tar xvzf cpyrit-opencl-0.4.0.tar.gz
```

Compile pyrit:

```
# cd pyrit-0.4.0  
# python setup.py build
```

If no errors during the compile then:

```
# python setup.py install
```

After Pyrit is installed the CUDA modules will be next.

```
# cd ..  
# cd cpyrit-cuda-0.4.0  
# python setup.py build
```

If no errors during the compile then:

```
# python setup.py install
```

Installing OpenCL is optional:

```
# cd ..  
# cd cpyrit-opencl-0.4.0  
# python setup.py build
```

If no errors during the compile then:

```
# python setup.py install
```

Pyrit is now installed and we can check to see if it sees the correct cores:

```
# pyrit list_cores
```

If no CUDA or OpenCL device is displayed then either the drivers were installed incorrectly or the Graphics card does not support CUDA or OpenCL.

Pyrit also has a benchmark command that can be utilized to check for performance and verify functionality:

```
# pyrit benchmark
```

Kali is now utilizing the NVIDIA Accelerated Linux Drivers, CUDA Toolkit, and OpenCL. This will allow for better performance for applications that support CUDA or OpenCL. If you have any comments or questions please do not hesitate to leave a reply below.