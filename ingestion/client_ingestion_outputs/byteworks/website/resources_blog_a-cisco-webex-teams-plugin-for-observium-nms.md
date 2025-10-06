---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/a-cisco-webex-teams-plugin-for-observium-nms/"
title: "A Cisco Webex Teams plugin for Observium NMS"
domain: "www.byteworks.com"
path: "/resources/blog/a-cisco-webex-teams-plugin-for-observium-nms/"
scraped_time: "2025-10-05T02:02:01.825381"
url_depth: 3
word_count: 134
client_name: "byteworks"
---

# A Cisco Webex Teams plugin for Observium NMS

This script written in PHP by the Byteworks team can run on-box with an Observium Network Monitoring Server somewhere in the web path (Ex. ../html/…) and Observium can call the script as a Webhook contact for alerting. When Observium posts a JSON alert notification, the script will decode the payload and post the alert details to a designated Cisco Webex Teams Space.

You will need a valid Cisco Webex Teams AccessToken (Ex. Webex Teams Bot) and the “roomId” of the space you wish to post the alerts to. Whomever the AccessToken belongs to (a user or bot), that account must be a member in the space that you wish to post alerts to.

The Observium Webex plugin: [https://github.com/ryanthuff/Observium_Webex_Notifier](https://github.com/ryanthuff/Observium_Webex_Notifier)

The Observium Network Monitoring Server (NMS): [https://observium.org](https://observium.org)