---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/customhtmlformacmail/"
title: "Getting your Custom HTML to work in Mac Mail for Yosemite"
domain: "www.byteworks.com"
path: "/resources/blog/customhtmlformacmail/"
scraped_time: "2025-10-05T02:01:09.982450"
url_depth: 3
word_count: 472
client_name: "byteworks"
---

# Getting your Custom HTML to work in Mac Mail for Yosemite

Say that you are working in Outlook for Mac 2011 and you want to leverage the new features within the new Mail app that comes with OS X Yosemite and say that one of the things that needs to happen is getting your custom, rich, HTML signature to move over with it. Well let me be the one to tell you its not impossible! It does however take about 5 minutes to make it work.

1.  First and foremost, rich text signatures only apply to rich text emails. To create and attach html to your outgoing mail, switch your default mail format in Mail > Preferences > Composing > Message Format. In the drop down menu select **Rich Text**.
2.  Now switch to Signatures and create a basic one. Put something like the word “temporary” in there that way when you go to modify the file you will know you are working on the right one. Whatever you do put in will not really matter as it is going to be replaced by your custom signature. This will only create the necessary file if you followed step 1.
3.  Quit Apple Mail! This is important as Mail would **overwrite** the custom signature file otherwise.
4.  Again, the Mail app will attempt to overwrite the file as soon as its launched. Make sure you have closed out the mail app.
5.  Locate the file on you hard disk. It can be found at **_~/Library/Mail/V2/MailData/Signatures/_**  and is usually a file named something like **_BE34FA81-E35F-4AED-ADA0-DB29A8F9802D.mailsignature_**. This file is only created in step 1.  If you can not find the file go back to step 1.
6.  Open the signature file from your favorite text editor.
7.  Inside you will see something like this:_Content-Transfer-Encoding: 7bit_  
    _Content-Type: text/html;_  
    _charset=us-ascii_  
    _Message-Id: <0A91E146-D8BE-435E-85DB-D459EDA6EA81@byteworks.com_  
    _Mime-Version: 1.0 (Mac OS X Mail 8.0 \(1990.1\))__<body style=”color: rgb(0, 0, 0); letter-spacing: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-stroke-width: 0px; word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space;”><font size=”3″>temporary</font></body>_
8.  Once inside, remove the HTML code starting with “**_<body_**” and replace it with your own custom HTML code.
9.  Save the file and close your favorite text editor
10.  Lock the file to write protect it so apple mail does not overwrite when you start the Mail app. You can do this by right clicking on the file within Finder, selecting “**_Get Info_**” and then selecting the “_**Locked**_” checkbox.
11.  Restart the Mail app and check signature settings. If the signature shows “_**temporary**_” and not your custom code, then you either left the Mail app running, didn’t lock the file, or edited the wrong file. Once its verified, the HTML signature will work as expected and work just like it does within Outlook for Mac 2011.