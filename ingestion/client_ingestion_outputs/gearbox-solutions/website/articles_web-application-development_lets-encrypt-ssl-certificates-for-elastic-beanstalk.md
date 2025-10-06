---
source: "website"
content_type: "blogs_resources"
url: "https://gearboxgo.com/articles/web-application-development/lets-encrypt-ssl-certificates-for-elastic-beanstalk"
title: "Let's Encrypt SSL Certificates for Elastic Beanstalk"
domain: "gearboxgo.com"
path: "/articles/web-application-development/lets-encrypt-ssl-certificates-for-elastic-beanstalk"
scraped_time: "2025-10-05T01:39:31.808059"
url_depth: 3
word_count: 281
client_name: "gearbox-solutions"
---

# Let's Encrypt SSL Certificates for Elastic Beanstalk

## Introduction

Let's Encrypt SSL certificates are a great way to secure your website for free, and the automated renewal process is very convenient. However, the process of scripting their deployment and renewal can be challenging for single-instance Elastic Beanstalk deployments.

This script helps you automate the process of generating and renewing Let's Encrypt SSL certificates for your Elastic Beanstalk environment. The script uses Certbot to generate the certificates and stores them in an S3 bucket. When a new instance is deployed, the script will retrieve the certificates from S3 and configure the instance to use them.

We've published the script we use to help with the deployment and configuration of CertBot and Let's Encrypt SSL certificates on Elastic Beanstalk.

## Why use this?

Elastic Beanstalk regularly destroys and recreates EC2 instances as part of the instance security maintenance and app deployment processes. This means that the certificates stored on the instance will be lost when the instance is destroyed. If you force-fetch a new cert from LE you run the risk of hitting your certificate limit and being stuck without a valid certificate. This script automates the process of renewing and storing the certificates in S3 for use in Elastic Beanstalk when new instances are deployed.

You should not use this script if you are using a load balancer with SSL termination. In that case, AWS will provide your SSL certificate and manage the renewal process for you.

## Download the Script

[This script for Let's Encrypt on Elastic Beanstalk is available for download from GitHub.](https://github.com/gearbox-solutions/elastic-beanstalk-lets-encrypt-script) The instructions for installing, configuring, and deployment can be found in the readme in the repository.