---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/office-365-exchange-online-deprecating-basic-authentication-what-this-means-for-unified-messaging-with-unity-connection/"
title: "Office 365 Exchange Online Deprecating Basic Authentication"
domain: "www.byteworks.com"
path: "/resources/blog/office-365-exchange-online-deprecating-basic-authentication-what-this-means-for-unified-messaging-with-unity-connection/"
scraped_time: "2025-10-05T02:00:50.330677"
url_depth: 3
word_count: 916
client_name: "byteworks"
---

# Office 365 Exchange Online Deprecating Basic Authentication: What This Means for Unified Messaging with Unity Connection

_**Update:**  Microsoft postponed disabling of basic authentication for “tenants still actively using it until the second half of 2021” according to information published [here](https://techcommunity.microsoft.com/t5/exchange-team-blog/basic-authentication-and-exchange-online-april-2020-update/ba-p/1275508).  Be aware that beginning October 2020, if a tenant is not actively using basic authentication with Exchange Online then Microsoft will be disabling the option.

## Change is Coming…

A topic that hasn’t been top-of-mind for many recently is that last September Microsoft posted an article to inform they are deprecating Basic Authentication support for Exchange Online. It will no longer be available on October 13, 2020, per this Microsoft document [here](https://support.microsoft.com/en-us/help/4521831/exchange-online-deprecating-basic-auth).

Basic Authentication is the simple use of a username and password to obtain access. While this has been a reasonable solution in the past, the combination of saved passwords in email clients and more aggressive hacking tactics have pushed many to look to a more secure alternative. This is where OAuth 2.0 comes in as an ideal modern authentication solution.

## What is OAuth 2.0?

A detailed explanation of OAuth 2.0 can be a topic of significant length on its own, so we recommend reviewing other resources for a more in-depth explanation if interested to know more. While the reading can be a little dry, section 1 from [RFC 6749 – The OAuth 2.0 Authorization Framework](https://tools.ietf.org/html/rfc6749#section-1) does a good job covering the overall flow without getting too complex.

Ultimately the key thing to understand is that OAuth 2.0 adds an additional layer of security through the use of “access tokens” and “refresh tokens” with well-defined attributes pertaining to the access that the application (such as Unity Connection) is permitted and validity period. These tokens are issued by a separate authorization server with the permission of the resource server). A valid token for the requested access must be provided by the application when sending the request to the resource server in order to obtain access to the requested information.

## The Impact: What’s Going to Break?

At the beginning of February 2020, the published release of Cisco Unity Connection 12.5(1)SU2 introduced OAuth 2.0 support for Exchange authentication. All prior releases of the product lack this option, so unless you have upgraded Unity Connection within the past two months then it will certainly need an upgrade for Unified Messaging to continue to function. If this is not addressed prior to October 13, 2020 then Basic Authentication for Unified Messaging will simply start to fail and the synchronization between voicemail and email will no longer occur.

For those running Unity Connection 11.5 that aren’t yet ready to make the leap to 12.5 releases, 11.5(1)SU8 is stated to also be adding support for OAuth 2.0, although as of now it isn’t yet available for download.

It should also be known that this change only impacts access to email within the mailbox (such as via IMAP or POP used by most email applications). This has no impact on the ability to send email (via SMTP AUTH) due to the number of devices dependent on this functionality today, although Microsoft still plans to address these security concerns at some point later on.

## What is Unified Messaging?

For anyone less familiar with the term “Unified Messaging” as it pertains to Unity Connection and voicemail, you may have also seen it identified as “Single Inbox” or simply “voicemail-to-email sync.” Unified Messaging is the feature within Unity Connection that allows a two-way synchronization between your voicemail messages and your email inbox. With this implemented, you will notice that any voicemail messages received are also delivered to email, but with the additional advantage of any changes (such as deleting or marking read) on email will also be reflected to the voicemail accessible from your phone (and vice versa). This is different from regular voicemail-to-email delivery as in that case no changes to voicemail messages or emails would have any impact on the other and can ultimately lead to a large volume of “new” voicemail messages on the phone for someone that only checks the emails. While not a requirement, Unified Messaging is a very significant convenience.

## What About NTLM Authentication?

For anyone that has spent much time in Unity Connection, you may be asking “What about NTLM Authentication?” While Unity Connection does support NTLM Authentication as an alternative to Basic Authentication, this unfortunately is only available for on-premises Exchange servers and any attempt to use this with Exchange Online results in the server telling the application (such as Unity Connection) to use Basic Authentication instead.

## Solution: Upgrade!

To retain Unified Messaging for Exchange Online following October 13, 2020 it will be necessary to upgrade Unity Connection to at least 12.5(1)SU2 or 11.5(1)SU8. Even if you are already running a sufficient release, it’s important to ensure that the OAuth 2.0 configuration has been completed to avoid any disruption.

## Any Alternatives?

With Basic Authentication still being possible specifically for sending email, prior versions of Unity Connection can still send a copy of voicemail messages to an email address. This is different than Unified Messaging and involves a different configuration procedure to utilize.

Bear in mind, this is merely the delivery of a copy of the voicemail, and provides no synchronization between voicemail and email. This means that if someone only checks or deletes voicemail messages via email then those voicemails will still be unread when accessing voicemail via phone (and vice versa). The two-way synchronization is only possible with Unified Messaging.