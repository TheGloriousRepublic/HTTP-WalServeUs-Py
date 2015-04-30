WalServeUs for HTTP
===================

Formal Description
------------------
HTTP-WalServeUs is a professional, lightweight HTTP server designed for nontechnical humans. Its primary purpose is for those hosting small websites from home, whether hobbyist or small business or other. It is entirely free and open source, and will soon support useful and easy-to-install extensions. It contains well-detailed and easy-to-navigate documentation in HTML format in order to make the server as easy to use as possible regardless of technological experience.

What it can do
--------------
WalServeUs is an HTTP Server for the nontechnical. It is **not:**
* A website builder
* A way to have someone else host your websites (you need your own machine to run it)
* A way to purchase domain names (those must be purchased separately and have the DNS forwarded (explained in the help file))
* A program that you can simply run and immediately have your website open to the world. These probably don't even exist.

An HTTP server is a website hosting software. That is to say you connect your website files to WalServeUs, point a domain name to your IP, and run the software, and when the domain is entered it show the page.

Informal Introduction
---------------------
Hello, and welcome to the README!

I think I'm getting good at this...

So. I was browsing the internet when I came across an HTTP server in python. I downloaded it, played with it, and then got bored with it and it's ridiculously oversimplified structure. I erased the stuff in the file and rewrote it. And I made it good. Kind of. It now has rewriting, permissions, directories, et cetera. So, yeah.


Technical:
----------
**Version:** 0.5?

**Description:** An simple, lightweight HTTP server written in Python. ~Does not solve any problems. Basically you'll be better off with a different software.~ Solves the problem of servers like Apache being large, complicated, and being designed for technical people by being much more lightweight and containing simple documentation designed for the non-technical.

**Installing:** Download and unzip the file.

**Uninstalling:** Delete the folder.

**Config:** See below.

**Operating:** Run WalServeUs.py. It will handle things for you.

**Files:** The files necessary to run this are (arranged by folders) (this is the default arrangement. See config for how to change it.):

* config #Configuration files

 * rewriter #if you desire a URL rewriter
 
   * rewriter files #These can be divied up however you wish. Must be '.cfg's
  
 * settings
 
   * settings files #same as for rewriter files
  
* errors #Error code html documents. Default location

 * 404.html #404 documents
 
 * blocked.html #For when a forbidden URL is entered (e.g. a blocked file extension)
 
* logs

 * Files Recieved #All the files recieved via POST (that met the size limits)

   * [recieved files] #Named to the time which they were recieved by default

 * server.log #The log of what you see in the console

 * connected.log #a log of all the unique IPs that connect. Currently broken and I don't know why.

 * visitorcount.log #Basically just one number. Describes the total number of connections (ip independent.) Sloppy, I know, but I don't know where else to put it.

* pages #The html, css, js, etc. documents.

 * [documents]

* WalServeUs.py

**Credit/acknowledgements:** Jon Berg of turtlemeat.com. Off of his webserver this is based.

**Contact Information:** To Be Added

**Known Bugs:**
* No way to add universal file access.
* No way to add member classes.
* Two files recieved at exactly the same time (in milliseconds, I think) will result in the one processed second overwriting the first.
* Max recieved file size may not work on binaries (resulting in a crash upon recieval.)

Configuration
-------------
Configuration is currently divided into two folders. config/settings and config/rewrite. All files in each of those folders are read upon starting the server and saved to their respective settings. **Because of this, you MUST reboot the server upon any changes to config for them to take hold.** Config/settings handles the basic settings, such as directories and which filetypes users are permitted to open. The settings are as such (presently, all must be available in a file or else the application will crash upon startup.) (settings should be in `key=value` format.):

**Settings:**
* `pgdir`: The directory on your computer under which the pages are stored. Default: /pages.
* `erdir`: The directory containing the error files. Default: /errors.
* `lgdir`: The directory to which logs are saved. Default: /logs.
* `rcdir`: The directory under which files recieved via POST are recorded. Default: /logs/FilesRecieved
* `rcMax`: A security mechanism ensuring that files recieved are less than a certain length.
* `pgexr`: Which files the user has permission to access on the server that should be served raw (that is, openned in the default fashion)
* `pgexb`: Which files the user has permission to access on the server that should be served as-is (that is, openned as a binary.)

**Rewriter:**

The rewriter allows URLs to be rewritten. That is, when a path is recieved it will be matched to a file location that may not necessarily mirror the location of the file on the computer. This is done using the same `key=value` format as for settings, but `key` should be a regular expression and `value` should be the path to the file on the local computer. It should be noted that tail slashes are omited by default (that is, there is no need to write a file solely for the purpose of recognizing both `www.example.com/1` and `www.example.com/1/`.)
