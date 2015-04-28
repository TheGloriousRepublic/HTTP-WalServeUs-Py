WalServeUs for HTTP
===================
Hello, and welcome to the README!

I think I'm getting good at this...

So. I was browsing the internet when I came across an HTTP server in python. I downloaded it, played with it, and then got bored with it and it's rediculously oversimplified structure. I erased the stuff in the file and rewrote it. And I made it good. Kind of. It now has rewriting, permissions, directories, et cetera. So, yeah.


Technical:
----------
**Version:** 0.5?

**Description:** An simple, lightweight HTTP server written in Python. Does not solve any problems. Basically you'll be better off with a different software.

**Installing:** Download the file.

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

   * [recieved files]

 * server.log #The log of what you see in the console

 * connected.log #a log of all the unique IPs that connect. Currently broken and I don't know why.

 * visitorcount.log #Basically just one number. Describes the total number of connections (ip independent.) Sloppy, I know, but I don't know where else to put it.

* pages #The html, css, js, etc. documents.

 * [documents]

**Credit/acknowledgements:** Jon Berg of turtlemeat.com. Off of his webserver this is based.

**Contact Information:** To Be Added

**Known Bugs:** No way to add universal file access. No way to add member classes.