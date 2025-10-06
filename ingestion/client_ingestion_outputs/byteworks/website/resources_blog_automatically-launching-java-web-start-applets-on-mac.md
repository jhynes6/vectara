---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/automatically-launching-java-web-start-applets-on-mac/"
title: "/resources/blog/automatically-launching-java-web-start-applets-on-mac/"
domain: "www.byteworks.com"
path: "/resources/blog/automatically-launching-java-web-start-applets-on-mac/"
scraped_time: "2025-10-05T02:02:19.107670"
url_depth: 3
word_count: 1160
client_name: "byteworks"
---

Automatically launching Java Web Start applets on Mac | Byteworks | IT Solutions, Services, and Consulting

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

# Automatically launching Java Web Start applets on Mac

[aharned](https://www.byteworks.com/resources/blog/author/aharned/)

February 12, 2015

It’s no secret that there have been some issues within the last few years between the folks at Apple, and the folks at Oracle, who now own the rights to the Java language and software engines. Due to several security concerns, Apple, along with several other developers, have adjusted their approach to running Java apps and applets in order to protect consumers from potentially-dangerous code being run on their machines. On paper, this sounds like a good strategy to ensure the safety of user information.

But what if you legitimately have a need to run a Java app? There are so many different versions of Java Runtime Engines (also known as JRE, or the environment in which Java code is executed on an operating system) that finding the right combination can be tricky. Once you \*do\* find the correct version (or versions), security concerns such as the ones previously mentioned may still keep these apps from performing properly.

One way Java apps are distributed is called Java Web Start (see [here](https://www.oracle.com/technetwork/java/javase/javawebstart/index.html "Oracle's website") for more information on this technology). These are small files that are downloaded and executed, as opposed to embedded code within a webpage. By default on several operating systems, including Apple’s OS X, these files are not executed automatically, which means they act as a regular download that must be double-clicked (or Command-O, for the keyboard fanatics out there like me) in order to run. While this isn’t a complete roadblock, it does diminish the convenience factor. Thankfully, there’s a way to get these programs to run automatically as they are downloaded, using Apples wonderful Automater tool. Here’s how:

**Note**: The screenshots in this document are tailored towards Apples most-recent version of OS X, Yosemite.  If you are on an older version of OS X, the pictures and steps may not match up perfec

*   From your Macintosh system, launch the Automater tool.  This can be done by selecting it from the [Launchpad](https://support.apple.com/en-us/HT202635 "Launchpad"), typing “Automater” into the [Spotlight](https://support.apple.com/en-us/HT204014 "Spotlight") search field, or simply locating the icon in your Applications Folder.

*   When Automater opens up, you  can click “New Document” to create a blank document.  This will open up the New Document wizard.

*   We will be creating what is called a Folder Action workflow, so click to highlight the “Folder Action” icon, and then click the **Choose** button.  A folder action workflow will perform a task any time the folder being monitored receives new files or folders within it.

*   First, we need to specify the folder we want to perform this action on.  Normally, this will be the “Downloads” folder, since this is where the downloaded Java Web Start files will be placed by default.  From the drop-down in the upper right, select “Other…” and browse to the Downloads folder.  Once that  folder is opened, click the **Choose** button, and the drop-down should now read “Downloads”.

*   Now we need to tell the workflow what action to perform.  In the left-hand column, listed under “Library” are all the categories of actions we can choose from.  Select “Utilities”, and all the utilities will come up in the next column.  From that middle column, drag-and-drop “Run Shell Script” to the workflow column on the right, and it will add it as a step.

*   Next, we need to configure the Shell Script action a little.  Next to the “Shell:” dropdown, make sure the value is set to “/bin/bash” so that the BASH shell is used to execute the script.  Then, on the right-hand side next to “Pass input:”, make sure it reads “as arguments”.
*   Lastly, we need to input the shell script in question, as the default value of “cat” will not do what we need to do.  Copy and paste the contents of the text box below into the shell script window.  This script will search for any Java Web Start files (\*.jnlp), and if it finds any, it will run the Java Web Start engine on them, and then delete them (so your downloads folder doesn’t get cluttered up).

for f in "$@"
do
if \[\[ $f =~ \\.jnlp$ \]\]
then
javaws "$f"
rm "$f"
fi
done

*   Once this is done, you can now save your Automater workflow from the **File** menu, or hit **Command-S**.  I have titled mine “Java WebStart Downloads.workflow” so that i can easily find it in the coming steps.

*   One last step is to activate the workflow for the downloads folder.   Open up a Finder window, and go to your home folder by either selecting it from the **Go** menu in the menu bar, or hitting **Command-Shift-H** on your keyboard.  This will allow you to see the Downloads folder in the Finder window itself, instead of just on the sidebar.

*   Perform a secondary click (also known as a right-click) on the Downloads folder and select “Services”, and then “Folder Action Setup”.  This brings up the Folder Actions Setup window.

*   From the list of available actions, select your workflow, “Java WebStart Downloads.workflow” in my case, and click **Attach**.  You will now see your Downloads folder in the lefthand column (with checkmark checked), and your workflow in the righthand column (also with checkmark checked).  That’s it.  Your Java Web Start documents will now automatically open, and then be removed.

Now, whenever a .jnlp file is downloaded or otherwise placed in your  Downloads folder, Automater will run (you will see a spinning gear in the top right of the menu bar).  Once the Jawa Web Start file is finished, the gear will go away.

**Note**: The script used in this example is specifically designed for opening .jnlp files, however it can be easily adjusted to perform roughly any task on any type of file.  This, however, is outside of the scope of this post.

While you’re at it, check out some of these sites for more Automator workflow ideas.

(Please note, the following sites are not affiliated with Byteworks)

*   Automated Workflows
*   Mac OSX Automation
*   Automator Actions

[

Previous Post

Allow or Block Anonymous Calls Into Cisco Communications Manager LUA Script Update

](https://www.byteworks.com/resources/blog/allow-or-block-anonymous-calls-into-cisco-communications-manager-lua-script-update/ "Allow or Block Anonymous Calls Into Cisco Communications Manager LUA Script Update")[

Next Post

The Best New Features of Cisco Unified Collaboration 11.0

](https://www.byteworks.com/resources/blog/the-best-new-features-of-cisco-unified-collaboration-11-0/ "The Best New Features of Cisco Unified Collaboration 11.0")

#### QUICK LINKS

[Case Studies](https://www.byteworks.com/resources/case-studies/)
[Privacy Policy](https://www.byteworks.com/privacy-policy/)

[](https://www.linkedin.com/company/byte-works-llc)

[](https://www.youtube.com/channel/UC0sglo13jgTeJvsoXqpyGCA)

[![](data:image/svg+xml;nitro-empty-id=MTEzMjoxODE3-1;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjQ1IDE3NiIgd2lkdGg9IjI0NSIgaGVpZ2h0PSIxNzYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PC9zdmc+)](https://www.byteworks.com/)

#### ADDRESS

[2675 Breckinridge Blvd Suite 200
Duluth, GA 30096](https://maps.app.goo.gl/CgnvPBK2ABG9MFnY6)

#