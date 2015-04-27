import Tkinter, BaseHTTPServer, socket, os, sys, datetime, atexit

settings = {}

def loadConfig(): #Open configuration files and save their options to settings
    for root, dirs, files in os.walk('config/settings/'): #Open all files in config directory
        for f in files:
            if f.endswith('.cfg'):
                for x in open('config/'+f).read().split('\n'): #Separate lines in file and iterate
                    settings[x.split('=')[0]]=x.split('=')[1] #Set the option before the equal sign in the config file line to the value in the settings dict
    for root, dirs, files in os.walk('config/settings/'): #Open all files in config directory
        for f in files:
            if f.endswith('.cfg'):
                for x in open('config/'+f).read().split('\n'): #Separate lines in file and iterate
                    settings[x.split('=')[0]]=x.split('=')[1] #Set the option before the equal sign in the config file line to the value in the settings dict

def log(dat): #Print to console and save to log
    o='['+str(datetime.datetime.now())+'] '+str(dat)
    b=open(settings['lgdir']+'/server.log').read() #Retrieve current log
    open(settings['lgdir']+'/server.log', 'w').write(b+o+'\n') #Write a concatenation of old log and new log to log
    print(o)

class webServer(BaseHTTPServer.BaseHTTPRequestHandler): #Main handler class

    def log_message(*args):
        pass

    def logCommand(self):
        log(self.client_address[0]+' on port '+str(self.client_address[1])+': \''+self.command+' '+self.path+'\'')

    def logConnected(self):
        global connected, visitors, individualvisitors
        if not self.client_address[0] in connected:
            connected+=self.client_address[0]
            individualvisitors+=1
        visitors+=1

    def do_HEAD(self):
        self.logCommand()
        self.logConnected()
        if self.path.endswith('.html'):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
        elif self.path.endswith('.css'):
            self.send_response(200)
            self.send_header('Content-type','text/css')
            self.end_headers()

    def do_GET(self):
        if self.path.endswith('/'):
            self.path=self.path[:-1]
        if os.path.isfile(settings['pgdir']+'/'+self.path):
            if self.path.endswith('.html') or self.path.endswith('.css'):
                self.do_HEAD()
                self.wfile.write(open(settings['pgdir']+'/'+self.path).read())
            else:
                self.do_HEAD()
                self.wfile.write(open(settings['erdir']+'/blocked.html').read())
        else:
            self.wfile.write(open(settings['erdir']+'/404.html').read())
    def do_KILL(self):
        sys.exit()

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
loadConfig()

connected=list(open(settings['lgdir']+'/connected.log').read().split('\n')) #Retrieve list of connected IPs
visitors=int(open(settings['lgdir']+'/visitorcount.log').read()) #Retrieve number of connectors
individualvisitors=len(connected) #Get number of unique connectors

atexit.register(gracefulShutdown) #Record logs at shutdown
if __name__ == '__main__':
    serve()
