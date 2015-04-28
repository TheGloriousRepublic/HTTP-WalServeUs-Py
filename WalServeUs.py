import Tkinter, BaseHTTPServer, cgi, socket, os, sys, datetime, atexit, re

settings = {}
rw = {}

def loadConfig(): #Open configuration files and save their options to settings
    for root, dirs, files in os.walk('config/settings/'): #Open all files in config directory
        for f in files:
            if f.endswith('.cfg'):
                for x in open('config/settings/'+f).read().split('\n'): #Separate lines in file and iterate
                    settings[x.split('=')[0]]=x.split('=')[1] #Set the option before the equal sign in the config file line to the value in the settings dict
                    
    for root, dirs, files in os.walk('config/rewriter/'):
        for f in files:
            if f.endswith('.cfg'):
                for x in open('config/rewriter/'+f).read().split('\n'):
                    rw[x.split('=')[0]]=x.split('=')[1]

def log(dat): #Print to console and save to log
    o='['+str(datetime.datetime.now())+'] '+str(dat)
    b=open(settings['lgdir']+'/server.log').read() #Retrieve current log
    open(settings['lgdir']+'/server.log', 'w').write(b+o+'\n') #Write a concatenation of old log and new log to log
    print(o)

class webServer(BaseHTTPServer.BaseHTTPRequestHandler): #Main handler class

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
        if p.endswith('.html'):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
        elif p.endswith('.css'):
            self.send_response(200)
            self.send_header('Content-type','text/css')
            self.end_headers()

    def do_GET(self):
        p=self.getPath()
        self.logCommand()
        if os.path.isfile(settings['pgdir']+'/'+p):
            if p.split('.')[-1] in settings['pgexr'].split('|'):
                self.sendHeader()
                self.wfile.write(open(settings['pgdir']+'/'+p).read())
            elif p.split('.')[-1] in settings['pgexb'].split('|'):
                self.sendHeader()
                self.wfile.write(open(settings['pgdir']+'/'+p,'rb').read())
            else:
                self.sendHeader()
                self.wfile.write(open(settings['erdir']+'/blocked.html').read())
        else:
            self.wfile.write(open(settings['erdir']+'/404.html').read())

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

def gracefulShutdown():
    log('Server stops')
    s.server_close
    c='\n'.join(connected)
    f=open(settings['lgdir']+'/connected.log', 'w')
    f.write(c)
    f=open(settings['lgdir']+'/visitorcount.log', 'w')
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

loadConfig() #load configuration files

connected=list(open(settings['lgdir']+'/connected.log').read().split('\n')) #Retrieve list of connected IPs
visitors=0#int(open(settings['lgdir']+'/visitorcount.log').read()) #Retrieve number of connectors
individualvisitors=len(connected) #Get number of unique connectors

atexit.register(gracefulShutdown) #Record logs at shutdown
if __name__ == '__main__':
    serve()
