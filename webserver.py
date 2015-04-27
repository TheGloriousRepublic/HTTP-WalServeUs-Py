import Tkinter, BaseHTTPServer, socket, os, sys, datetime

settings = {}

def loadConfig():
    for root, dirs, files in os.walk('config/'):
        for f in files:
            if f.endswith(".cfg"):
                for x in open('config/'+f).read().split('\n'):
                    settings[x.split('=')[0]]=x.split('=')[1]

def log(dat):
    o='['+str(datetime.datetime.now())+'] '+str(dat)
    b=open(settings['lgdir']+'/server.log').read()
    open(settings['lgdir']+'/server.log', 'w').write(b+o+'\n')
    print(o)

class webServer(BaseHTTPServer.BaseHTTPRequestHandler):

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

    def do_GET(self):
        if self.path.endswith('/'):
            self.path=self.path[:-1]
        self.do_HEAD()
        if os.path.isfile(os.curdir+os.sep+self.path):
            if self.path.endswith('.html'):
                self.wfile.write(open(os.curdir+os.sep+self.path).read())
        else:
            self.wfile.write(open(os.curdir+os.sep+'errors/404.html').read())
    def do_KILL(self):
        sys.exit()


def serve():
    global connected
    s = BaseHTTPServer.HTTPServer(('', 80), webServer)
    log('Server starts')
    try:
        s.serve_forever()
    except KeyboardInterrupt:
        s.server_close
        c='\n'.join(connected)
        open('logs/connected.log', 'w').write(c)
            
        log('Server stops')

loadConfig()

connected=open(settings['lgdir']+os.sep+'connected.log').read().split('\n')
visitors=int(open(settings['lgdir']+os.sep+'/visitorcount.log').read())
individualvisitors=len(connected)

serve()
