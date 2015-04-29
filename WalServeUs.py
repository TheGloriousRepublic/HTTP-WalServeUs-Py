#This software is licensed under the Glorious Republic's Glorious Free Software License 1.0. Just in case you were wondering.
import Tkinter, BaseHTTPServer, cgi, socket, os, sys, datetime, atexit, re, mimetypes, socket

settings = {}
rw = {}
static = {}
serveAsPlaintext = ['text','application']

def loadConfig(): #Open configuration files and save their options to settings
    for root, dirs, files in os.walk('config/settings/'): #Open all files in config directory
        for f in files:
            if f.endswith('.cfg'):
                for x in open('config/settings/'+f).read().split('\n'): #Separate lines in file and iterate
                    if not x[0]=='#':
                        settings[x.split('=')[0]]=x.split('=')[1] #Set the option before the equal sign in the config file line to the value in the settings dict
                    
    for root, dirs, files in os.walk('config/rewriter/'):
        for f in files:
            if f.endswith('.cfg'):
                for x in open('config/rewriter/'+f).read().split('\n'):
                    if not x[0]=='#':
                        rw[x.split('=')[0]]=x.split('=')[1]

def log(dat): #Print to console and save to log
    o='['+str(datetime.datetime.now())+'] '+str(dat)+'\n'
    b=open(settings['lgdir']+'/server.log', 'r+').read() #Retrieve current log
    open(settings['lgdir']+'/server.log', 'w+').write(b+o+'\n\n') #Write a concatenation of old log and new log to log
    print(o)

class webServer(BaseHTTPServer.BaseHTTPRequestHandler): #Main handler class
    self.server_version='BaseHTTP/1.0'
    self.sys_version='Python/2.7.9'
    
    def log_message(*args):
        pass

    def logCommand(self):
        log(self.client_address[0]+' on port '+str(self.client_address[1])+': \''+self.command+' '+self.path+'\', interpreted as \''+self.command+' '+self.getPath()+'\'') #Log the time and client address/client port of a request, followed by the request submitted and what it was interpreted to.

    def logConnected(self):
        global connected, visitors, individualvisitors
        if not self.client_address[0] in connected:
            connected+=self.client_address[0]
            individualvisitors+=1
        visitors+=1

    def getPath(self):
        p=self.path
        if p.endswith('/'):
            p=self.path[:-1]
        for x in rw:
            if re.match(x, p):
                return(rw[x])
        return(p)

    def do_HEAD(self):
        self.logCommand()
        self.do_HEAD()
        
    def sendHeader(self):
        p=self.getPath()
        self.logConnected()
        self.send_response(200)
        self.send_header('Content-type',mimetypes.guess_type(p)[0])
        self.end_headers()


    def do_GET(self):
        p=self.getPath()
        self.logCommand()
        ext=p.split('.')[-1]
        self.sendHeader()
        if os.path.isfile(settings['pgdir']+'/'+p):
            if ext in settings['pgexr'].split('|') or ('*' in settings['pgexr'].split('|') and mimetypes.guess_type(p)[0].split('/')[0] in serveAsPlaintext):
                self.wfile.write(open(settings['pgdir']+'/'+p).read())
            elif ext in settings['pgexb'].split('|') or ('*' in settings['pgexb'].split('|') and not (mimetypes.guess_type(p)[0].split('/')[0] in serveAsPlaintext)):
                self.wfile.write(open(settings['pgdir']+'/'+p,'rb').read())
            elif os.path.isfile(settings['erdir']+'/403.html'):
                self.wfile.write(open(settings['erdir']+'/403.html').read())
            else:
                self.wfile.write('<center><h1>Error 403</h1><h2>You are forbidden to access this file on this server</h2>Furthermore, no 403.html file was found in the local server\'s error directory</center>')
        elif os.path.isfile(settings['erdir']+'/404.html'):
            self.wfile.write(open(settings['erdir']+'/404.html').read())
        else:
            self.wfile.write('<center><h1>Error 404</h1><h2>File not found</h2>Furthermore, no 404.html file was found in the local server\'s error directory</center>')

    def do_POST(self):
        p=self.getPath()
        self.logCommand()
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            query=cgi.parse_multipart(self.rfile, pdict)
        
        self.send_response(301, '')
        self.end_headers()
        self.fileContent=query.get('upfile')[0]
        if len(self.fileContent)<=8192: #Check maximum POSTed file size
            open(settings['rcdir']+'/'+str(datetime.datetime.now()).replace(':', '.')+'.txt', 'w+').write(self.fileContent) #record POSTed files
        else:
            log('File too large to record (>'+int(settings['rcmax'])+'b)')

    def do_KILL(self):        
        #sys.exit()
        pass

    def run(self):
        while True:
            handle_request()

def gracefulShutdown():
    log('Server stops')
    s.server_close
    c='\n'.join(connected)
    f=open(settings['lgdir']+'/connected.log', 'w+')
    f.write(c)
    f=open(settings['lgdir']+'/visitorcount.log', 'w+')
    f.write(str(individualvisitors))
    f.close()

def serve():
    global connected, s
    s = BaseHTTPServer.HTTPServer(('', 80), webServer)
    log('Server starts')
    try:
        s.serve_forever()
    except:
        pass

def interface(tkinter.Tk):
    pass

loadConfig() #load configuration files

connected=list(open(settings['lgdir']+'/connected.log', 'w+').read().split('\n')) #Retrieve list of connected IPs
visitors=0#int(open(settings['lgdir']+'/visitorcount.log').read()) #Retrieve number of connectors
individualvisitors=len(connected) #Get number of unique connectors

atexit.register(gracefulShutdown) #Record logs at shutdown
if __name__ == '__main__':
    serve()
