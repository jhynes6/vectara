---
source: "website"
content_type: "blogs_resources"
url: "https://gearboxgo.com/articles/filemaker/lets-encrypt-ssl-certificates-for-filemaker-server"
title: "Let's Encrypt SSL Certificates for FileMaker Server"
domain: "gearboxgo.com"
path: "/articles/filemaker/lets-encrypt-ssl-certificates-for-filemaker-server"
scraped_time: "2025-10-05T01:39:47.722463"
url_depth: 3
word_count: 121
client_name: "gearbox-solutions"
---

# Let's Encrypt SSL Certificates for FileMaker Server

[Let’s Encrypt](https://letsencrypt.org/) is a non-profit certificate authority with the mission of spreading the SSL love across the internet. We can use Let’s Encrypt to get free SSL certificates to use with FileMaker Server. We will use a PowerShell script and the Windows Task Scheduler on Windows Server to retrieve and automatically renew SSL certificates through Let’s Encrypt to make sure our connections to FileMaker Server are secure. With this, there’s no reason anyone should have an invalid SSL certificate on their FileMaker Server deployment!

This process also handles the intermediary certificates as required to make the connection secure.

Check our the documentation for [download links here](https://www.bluefeathergroup.com/docs/lets-encrypt-ssl-certificates/setup/downloads/) or download from the repository on [GitHub](https://github.com/gearbox-solutions/FileMaker-LetsEncrypt-Win).